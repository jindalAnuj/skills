---
name: avoid-high-cardinality-hash-cache
description: >-
  Detects and prevents the anti-pattern of using Redis hash cache (@Cache with
  hash field pattern) for high-cardinality data like geo-coordinates, IPs, or
  per-user values. Use when reviewing or writing @Cache decorators, caching
  strategies, or when lat/long/coordinates appear in cached methods.
---

# Avoid High-Cardinality Hash Cache

## The Anti-Pattern

Using `@Cache('HASH_KEY', '{$query}', ttl)` (hash cache mode) when the query
contains high-cardinality fields like `lat`, `long`, IP addresses, or
user-specific values.

### Why It Is Dangerous

In this codebase, `CacheService.hSet` works as follows:

```typescript
await this.client.hSet(hKey, key, data);   // add field to hash
await this.client.expire(hKey, ttl);       // reset TTL on ENTIRE hash
```

This causes three compounding problems:

1. **TTL resets on every write** -- `EXPIRE` is called on the hash key after
   every `HSET`, resetting the TTL for ALL existing fields, not just the new one.
2. **Unbounded memory growth** -- each unique coordinate pair creates a new
   hash field. Since coordinates are floating-point and vary per user, the hash
   grows indefinitely and never expires.
3. **Stale data** -- old fields persist forever, serving outdated results long
   past the intended TTL.

### How to Detect

Flag any `@Cache` usage where:

- The **second argument** (hash field pattern) is non-empty (`'{$query}'`,
  `'{$params}'`, etc.)
- AND the serialized object includes **any** of: `lat`, `long`, `latitude`,
  `longitude`, `ip`, `coordinates`, timestamps, or other per-request unique
  floating-point/string values.

**Bad examples found in this codebase:**

```typescript
// Hash field = JSON.stringify(query) which includes lat/long floats
@Cache('PATHSHALA_CENTERS_NEAR_BY_BY_SORTING_TYPE', '{$query}', CACHE_TTL.HOUR)
async getNearbyCentresByVerticalSortingType(query: NearbyCentresBySortingTypeDto, ...)

@Cache('PATHSHALA_CENTERS_NEAR_BY_V3', '{$query}', CACHE_TTL.HOUR)
async searchNearByCenterV3({ lat, long, organizationId, ... })

@Cache('PATHSHALA_CENTERS_WITHIN_RANGE', '{$query}', CACHE_TTL.HOUR)
async getPathshalaCentersWithinSpecificRange({ long, lat, organizationId })
```

---

## Invalidation Constraint

In this codebase, cache invalidation uses `CacheService.del()` with exact key
names (see `PathshalaCentersCache.flushPathshalaCentreCache`). There is no
efficient pattern-based deletion -- `deleteKeysByRegex` exists but is
deprecated because Redis `KEYS` is O(N) and blocks the server.

This means the **hash key name must remain a single, known constant** so that
`DEL hashKey` can wipe all cached variants in one call. Switching to string
keys (`@Cache('KEY_{$query}', '', ttl)`) would scatter data across many keys
that cannot be enumerated for deletion without the caller knowing every
possible lat/long combination.

**Rule:** When the cache has a corresponding flush/invalidation path, always
use hash cache mode so the key name stays fixed and predictable.

---

## Recommended Alternatives

### Alternative 1: Hash Cache + Coordinate Quantization (Preferred)

Keep hash cache mode but **quantize lat/long before calling the cached method**
so the hash field set becomes bounded. The `@Cache` decorator and all
invalidation code remain unchanged.

**Step 1** -- Add a quantization utility:

```typescript
function quantizeCoord(value: number, decimals = 2): number {
  const factor = Math.pow(10, decimals);
  return Math.round(value * factor) / factor;
}
```

Precision guide:

| Decimals | Grid size | Use case |
|----------|-----------|----------|
| 1        | ~11 km    | Coarse city-level |
| 2        | ~1.1 km   | Neighborhood-level (recommended) |
| 3        | ~110 m    | Block-level |

**Step 2** -- Quantize coordinates in the caller before invoking the cached
method. Build a deterministic query object with rounded values:

```typescript
const quantizedQuery = {
  ...query,
  lat: quantizeCoord(query.lat),
  long: quantizeCoord(query.long),
};
const result = await this.getNearbyCentresByVerticalSortingType(
  quantizedQuery,
  userHeaders,
);
```

The `@Cache` decorator remains exactly as-is:

```typescript
@Cache('PATHSHALA_CENTERS_NEAR_BY_BY_SORTING_TYPE', '{$query}', CACHE_TTL.HOUR)
async getNearbyCentresByVerticalSortingType(query, userHeaders) { ... }
```

**Why this works:**

- Hash key stays fixed (`PATHSHALA_CENTERS_NEAR_BY_BY_SORTING_TYPE`) --
  `DEL` invalidation works unchanged.
- Hash field cardinality is bounded: ~grid cells x sorting types x slugs x
  pagination combos. The hash size plateaus instead of growing unboundedly.
- TTL reset becomes beneficial: keeps frequently accessed, bounded data alive.
- `flushPathshalaCentreCache` needs zero changes.

### Alternative 2: String Key Cache (When Invalidation Is Not Needed)

Use string keys only when the cache has **no flush/invalidation path** or when
a pattern-based delete mechanism is available.

```typescript
// Only if no invalidation is needed for this cache:
@Cache('SOME_KEY_{$query}', '', CACHE_TTL.HOUR)
async method(query) { ... }
```

Each key gets an independent TTL via `SET ... EX`, so no TTL-reset problem.
Still quantize coordinates to bound total key count.

### Alternative 3: Geohash Bucketing

Convert lat/long to a geohash string of fixed precision. Use as the hash field
or as part of the key. Produces a bounded, predictable set of buckets.

```typescript
import Geohash from 'ngeohash';

const geoHash = Geohash.encode(lat, long, 5); // ~4.9km x 4.9km cell
```

Use with `useCache` (non-decorator) for full control over key composition, or
quantize via geohash before calling the cached method (same pattern as Alt 1).

### Alternative 4: Remove Cache Entirely

If cache hit rate is inherently low (every user has unique coordinates and
quantization is unacceptable for the use case), caching wastes memory without
benefit. Profile hit rates first; remove cache if < 5% hit rate.

```typescript
// Simply remove the @Cache decorator
async getNearbyCentres(query, userHeaders) { ... }
```

---

## When Hash Cache IS Appropriate

Hash cache (`@Cache('KEY', '{$field}', ttl)`) is correct when:

- The field set is **bounded** (e.g., enum values, known IDs, quantized
  coordinates, finite slugs)
- Invalidation requires wiping all variants at once via `DEL hashKey`
- TTL reset from continuous writes is acceptable (bounded data stays warm)

Examples of valid hash cache usage:

```typescript
// Good: cityId is a bounded set of known MongoDB ObjectIds
@Cache('CENTERS_BY_CITY_{$cityId}', '{$params}', CACHE_TTL.HOUR)

// Good: centerId is a specific document ID, no hash field
@Cache('CENTER_DETAIL_{$centerId}', '', CACHE_TTL.HOUR)

// Good: coordinates are quantized before reaching the cache
@Cache('CENTERS_NEARBY', '{$query}', CACHE_TTL.HOUR)
async method(quantizedQuery) { ... } // lat/long already rounded
```

---

## Review Checklist

When reviewing or writing `@Cache` decorators:

- [ ] Does the hash field contain geo-coordinates, IPs, or timestamps?
      If yes, **quantize or remove them** before they reach the cache layer.
- [ ] Is the set of possible hash field values bounded and predictable?
      If no, **quantize the high-cardinality fields** to make it bounded.
- [ ] Does this cache have a flush/invalidation path (e.g., in a `*Cache`
      service)? If yes, **keep hash cache mode** -- do not switch to string keys.
- [ ] Are floating-point numbers in the cache key or field? If yes,
      **quantize them** (round to fixed decimal places).
- [ ] Does the method receive pagination params (`page`, `limit`)? Decide
      whether paginated results should be cached separately or excluded.
- [ ] After fixing, estimate the max number of unique hash fields and verify
      it is acceptable for your Redis memory budget.
