# Caching Standards & Best Practices

> **The definitive guide for implementing, invalidating, and grading cache operations in this codebase.**

---

## Table of Contents

1. [Why Cache](#1-why-cache)
2. [Method Cache vs DB Call Cache](#2-method-cache-vs-db-call-cache)
3. [When to Implement Cache](#3-when-to-implement-cache)
4. [Cache Preference Grading](#4-cache-preference-grading)
5. [How to Implement Cache](#5-how-to-implement-cache)
6. [When to Invalidate Cache](#6-when-to-invalidate-cache)
7. [Secondary Key Invalidation](#7-secondary-key-invalidation)
8. [Cross-Module Cache Invalidation](#8-cross-module-cache-invalidation)
9. [Quick Reference Cheatsheet](#9-quick-reference-cheatsheet)

---

## 1. Why Cache

### Benefits

| Benefit | Description |
|---------|-------------|
| **Reduced DB Load** | Fewer database queries = lower costs and better performance |
| **Faster Response Times** | Redis reads are ~10-100x faster than MongoDB queries |
| **Scalability** | Offload repetitive reads to cache layer |
| **Consistency** | Centralized data access patterns |

### When NOT to Cache

> [!CAUTION]
> Avoid caching in these scenarios:
> - **Highly volatile data** that changes every few seconds
> - **Security-sensitive data** that must always be fresh (auth tokens, permissions)
> - **Large payloads** (>1MB) that could bloat Redis memory
> - **One-time queries** that are rarely repeated

---

## 2. Method Cache vs DB Call Cache

### Overview

| Type | What It Caches | When to Use |
|------|----------------|-------------|
| **Method Cache** | Entire method result (transformed/computed data) | Business logic, transformations, aggregations |
| **DB Call Cache** | Raw database result (entity/document) | Direct entity lookups, frequently accessed records |

### Method Cache

**Definition**: Caches the final output of a method, including any transformations, filtering, or business logic applied.

```
┌─────────────────────────────────────────────────────────────┐
│  Request → [Method Cache Check] → HIT → Return cached result │
│                    ↓ MISS                                    │
│            DB Query → Transform → Compute → Cache → Return   │
└─────────────────────────────────────────────────────────────┘
```

**Use When:**
- ✅ Method applies business logic or transformations
- ✅ Method aggregates data from multiple sources
- ✅ Output is different from raw DB data
- ✅ Expensive computations involved
- ✅ Same method called with same params repeatedly

**Example:**

```typescript
// ✅ METHOD CACHE - Caches transformed/computed result
@Cache('user_notify_status_{userId}', '', 86400)  // 24 hours
async getNotifyStatusList(userId: Types.ObjectId): Promise<BatchNotifyStatus[]> {
  const list = await this.baseRepo.list({ userId });  // Raw DB data
  
  // Business logic applied - this is what gets cached
  return list.map(item => ({
    batchId: item.batchId,
    status: this.computeStatus(item),
    displayName: this.formatName(item),
  }));
}
```

### DB Call Cache

**Definition**: Caches raw database entities/documents without transformation.

```
┌─────────────────────────────────────────────────────────────┐
│  Request → Method → [DB Cache Check] → HIT → Return entity   │
│                           ↓ MISS                             │
│                     DB Query → Cache → Return                │
└─────────────────────────────────────────────────────────────┘
```

**Use When:**
- ✅ Fetching entities by ID (findById, fetchOne)
- ✅ Same entity accessed from multiple services/methods
- ✅ Entity rarely changes but frequently read
- ✅ Raw data needed in multiple contexts

**Example:**

```typescript
// ✅ DB CALL CACHE - Caches raw entity in dedicated cache service
async getBatchById(batchId: Types.ObjectId): Promise<Batch> {
  // Check cache first
  let batch = await this.cache.get(`batch_id:${batchId}`);
  
  if (!batch) {
    batch = await this.baseRepo.fetchOne({ _id: batchId });
    if (batch) await this.cache.set(`batch_id:${batchId}`, batch);
  }
  
  return batch;  // Raw entity, no transformation
}
```

### Decision Guide

```
┌─────────────────────────────────────────────────────────────┐
│  Does the method transform/compute data?                     │
│      ↓ YES                        ↓ NO                       │
│  Use METHOD CACHE          Is it a direct entity lookup?     │
│  (@Cache decorator)             ↓ YES           ↓ NO         │
│                          Use DB CALL CACHE   Consider if     │
│                          (dedicated service) caching needed  │
└─────────────────────────────────────────────────────────────┘
```

### Why Separate Them?

| Concern | Method Cache | DB Call Cache |
|---------|--------------|---------------|
| **Invalidation** | Invalidate when logic changes OR data changes | Only invalidate when data changes |
| **Reusability** | Cache specific to one method | Cache reusable across methods |
| **Key Design** | Based on method params | Based on entity identifiers |
| **Granularity** | Coarse (whole result) | Fine (individual entities) |

> [!IMPORTANT]
> **Avoid double-caching!** If using DB call cache, don't also use method cache on the same method unless the transformation adds significant value.

---

## 3. When to Implement Cache

### Decision Matrix

| Scenario | Cache? | Grade | Reasoning |
|----------|--------|-------|-----------|
| Fetching user profile by ID | ✅ Yes | 🟢 Low | Stable data, frequent access |
| Listing items with pagination | ⚠️ Depends | 🟡 Medium | Cache if sort/filter is consistent |
| Getting counts/aggregations | ✅ Yes | 🔵 High | Expensive queries, stable results |
| Real-time notifications | ❌ No | - | Must be fresh |
| Configuration/lookup data | ✅ Yes | 🟢 Low | Changes infrequently |
| Search results | ⚠️ Depends | 🔴 Very High | Only if queries are repetitive |
| User session data | ✅ Yes | 🔴 Very High | Must be near real-time |

### Signs You Need Caching

1. **Same query executed multiple times** per request or across requests
2. **Database metrics show slow queries** (>100ms for simple reads)
3. **High read-to-write ratio** (reads >> writes)
4. **Computed/aggregated data** that's expensive to calculate
5. **External API responses** that have rate limits

---

## 4. Cache Preference Grading

Use this grading system to determine cache strategy and consistency requirements.

### TTL Constants

> [!TIP]
> **Always use `CacheTTL` constants** instead of raw seconds. Developers don't need to memorize values!

```typescript
import { CacheTTL } from 'src/common/constants/cache.constants';

// Just pick the grade - no need to know the seconds!
@Cache('user_session_{userId}', '', CacheTTL.VERY_HIGH)
@Cache('user_bookings_{userId}', '', CacheTTL.HIGH)
@Cache('batch_details_{batchId}', '', CacheTTL.MEDIUM)
@Cache('config_data_{key}', '', CacheTTL.LOW)
```

### Preference Levels

| Level | Constant | TTL | Consistency | Use Case |
|-------|----------|-----|-------------|----------|
| 🔴 **Very High** | `CacheTTL.VERY_HIGH` | 20 min | Near real-time | User sessions, live counts, active status |
| 🟡 **High** | `CacheTTL.HIGH` | 2 hours | Eventual | User preferences, notifications, bookings |
| 🔵 **Medium** | `CacheTTL.MEDIUM` | 6 hours | Relaxed | Batch details, course info, entity lookups |
| 🟢 **Low** | `CacheTTL.LOW` | 24 hours | Lazy | Config data, lookup tables, static content |

> [!NOTE]
> **Higher priority = Shorter TTL** because data freshness is more critical.
> **Lower priority = Longer TTL** because data can be stale without issues.

### Grading Criteria

```
GRADE = f(data_freshness_need, read_frequency, write_frequency, business_impact)
```

| Factor | Very High (short TTL) | Low (long TTL) |
|--------|----------------------|----------------|
| **Data Freshness** | Must be fresh (<20 min) | Can be stale (24+ hours) |
| **Read Frequency** | >1000/min | <10/min |
| **Write Frequency** | >10/min | <1/day |
| **Business Impact** | Affects user actions | Display-only, informational |

### Examples

```typescript
import { CacheTTL } from 'src/common/constants/cache.constants';

// 🔴 VERY HIGH - Near real-time (20 min)
// User's active session or live counts
@Cache('user_active_session_{userId}', '', CacheTTL.VERY_HIGH)
async getActiveSession(userId: Types.ObjectId)

// 🟡 HIGH - Eventual consistency (2 hours)
// User preferences, notification settings
@Cache('user_notify_bookings:{userId}', '', CacheTTL.HIGH)
async getBatchUserNotifyList(userId: Types.ObjectId)

// 🔵 MEDIUM - Relaxed consistency (6 hours)
// Entity details, batch info
@Cache('batch_details_{batchId}', '', CacheTTL.MEDIUM)
async getBatchDetails(batchId: Types.ObjectId)

// 🟢 LOW - Lazy consistency (24 hours)
// Config, lookup tables, static content
@Cache('lookup_categories_{orgId}', '', CacheTTL.LOW)
async getCategoryList(orgId: Types.ObjectId)
```

---

## 5. How to Implement Cache

### Approach Selection Guide

```
┌─────────────────────────────────────────────────────────────┐
│                    START HERE                                │
│              ↓                                               │
│    Is caching simple (single key, auto get/set)?            │
│              ↓                                               │
│    YES ──────────────→ Use @Cache Decorator                  │
│              ↓                                               │
│    Do you need custom key generation?                        │
│              ↓                                               │
│    YES ──────────────→ Create Dedicated Cache Service        │
│              ↓                                               │
│    Do you need bulk operations (getMultiple)?                │
│              ↓                                               │
│    YES ──────────────→ Create Dedicated Cache Service        │
│              ↓                                               │
│    Do you need manual cache control in business logic?       │
│              ↓                                               │
│    YES ──────────────→ Create Dedicated Cache Service        │
│              ↓                                               │
│    Do you need secondary key invalidation (id + slug)?       │
│              ↓                                               │
│    YES ──────────────→ Create Dedicated Cache Service        │
│              ↓                                               │
│    Otherwise ────────→ Use @Cache Decorator                  │
└─────────────────────────────────────────────────────────────┘
```

---

### Approach 1: `@Cache` Decorator (Method Cache)

**Best for**: Simple method-level caching with automatic get/set behavior.

#### Basic Usage

```typescript
import Cache from 'src/bootstrap/decorators/cache.decorator';

// Pattern: {module}_{entity}_{identifier}:{paramName}
@Cache('batch_user_notify_batchId:{batchId}')
async getNotifyCount(batchId: Types.ObjectId) {
  return await this.baseRepo.count({ batchId });
}
```

#### With TTL Constants (Recommended)

```typescript
import { CacheTTL } from 'src/common/constants/cache.constants';

// 🔴 Very High - 20 minutes
@Cache('user_session_{userId}', '', CacheTTL.VERY_HIGH)

// 🟡 High - 2 hours
@Cache('user_bookings_{userId}', '', CacheTTL.HIGH)

// 🔵 Medium - 6 hours (default for most cases)
@Cache('batch_details_{batchId}', '', CacheTTL.MEDIUM)

// 🟢 Low - 24 hours
@Cache('config_data_{key}', '', CacheTTL.LOW)
```

#### With Hash Key (for grouped data)

```typescript
// Key: user_data_orgId:123, HKey: userId:456
@Cache('user_data_orgId:{$sp.orgId}', 'userId:{$sp.userId}')
async getUserData(params: Params<User>) {
  return await this.baseRepo.fetchOne(params);
}
```

#### Key Pattern Syntax

| Pattern | Description | Example |
|---------|-------------|---------|
| `{paramName}` | Direct parameter | `{batchId}` → value of batchId arg |
| `{$sp.field}` | From searchParams | `{$sp.userId}` → params.searchParams.userId |
| `{$_id}` | From first arg's _id | `{$_id}` → user._id |

---

### Approach 2: Dedicated Cache Service (DB Call Cache)

**Best for**: Entity caching, custom key generation, bulk operations, secondary key invalidation.

#### File Structure

```
src/services/your_module/
├── your_module.cache.ts        # Cache service
├── your_module.cache.spec.ts   # Cache tests
├── your_module.service.ts      # Main service (uses cache)
├── your_module.module.ts       # Registers both services
└── ...
```

#### Template: Cache Service

```typescript
// your_module.cache.ts
import { Injectable } from '@nestjs/common';
import { Types } from 'mongoose';
import { CacheService } from '../../bootstrap/cache/cache.service';
import { CacheTTL } from 'src/common/constants/cache.constants';

@Injectable()
export class YourModuleCacheService {
  // ✅ Use descriptive base key with module name
  private BASE_KEY = 'your_module_';
  
  // ✅ Use TTL constant - no need to know seconds!
  private TTL = CacheTTL.MEDIUM;  // 🔵 6 hours

  constructor(private readonly cache: CacheService) {}

  // ✅ Key generation methods - single source of truth
  private getKeyById(id: Types.ObjectId): string {
    return `${this.BASE_KEY}id:${id}`;
  }

  private getKeyBySlug(slug: string): string {
    return `${this.BASE_KEY}slug:${slug}`;
  }

  // ✅ Get by primary key
  async getById(id: Types.ObjectId) {
    return await this.cache.get(this.getKeyById(id));
  }

  // ✅ Get by secondary key (slug)
  async getBySlug(slug: string) {
    return await this.cache.get(this.getKeyBySlug(slug));
  }

  // ✅ Set with both keys
  async set(entity: { _id: Types.ObjectId; slug: string }, data: any) {
    await Promise.all([
      this.cache.set(this.getKeyById(entity._id), data, this.TTL),
      this.cache.set(this.getKeyBySlug(entity.slug), data, this.TTL),
    ]);
  }

  // ✅ Invalidate both keys
  async invalidate(entity: { _id: Types.ObjectId; slug: string }) {
    await Promise.all([
      this.cache.del(this.getKeyById(entity._id)),
      this.cache.del(this.getKeyBySlug(entity.slug)),
    ]);
  }

  // ✅ Bulk get
  async getBulk(ids: Types.ObjectId[]): Promise<Map<string, any>> {
    const keys = ids.map(id => this.getKeyById(id));
    const keysMap = await this.cache.getMultipleKeys(keys);
    
    const result = new Map();
    Object.entries(keysMap).forEach(([key, value]) => {
      const id = key.replace(`${this.BASE_KEY}id:`, '');
      if (value) result.set(id, value);
    });
    return result;
  }
}
```

#### Template: Module Registration

```typescript
// your_module.module.ts
import { Module } from '@nestjs/common';
import { CacheModule } from 'src/bootstrap/cache/cache.module';
import { YourModuleService } from './your_module.service';
import { YourModuleCacheService } from './your_module.cache';

@Module({
  imports: [
    CacheModule,  // ✅ Required for cache injection
    // ... other imports
  ],
  providers: [
    YourModuleService,
    YourModuleCacheService,  // ✅ Register cache service
  ],
  exports: [
    YourModuleService,
    YourModuleCacheService,  // ✅ Export if other modules need it
  ],
})
export class YourModuleModule {}
```

#### Template: Using Cache in Service

```typescript
// your_module.service.ts
@Injectable()
export class YourModuleService {
  constructor(
    @Inject(YourEntity.name)
    private readonly baseRepo: BaseRepository<YourEntity>,
    private readonly cache: YourModuleCacheService,
  ) {}

  // ✅ Get by ID with caching
  async getById(id: Types.ObjectId) {
    let data = await this.cache.getById(id);
    
    if (!data) {
      data = await this.baseRepo.fetchOne({ _id: id });
      if (data) await this.cache.set(data, data);
    }
    
    return data;
  }

  // ✅ Get by slug with caching
  async getBySlug(slug: string) {
    let data = await this.cache.getBySlug(slug);
    
    if (!data) {
      data = await this.baseRepo.fetchOne({ slug });
      if (data) await this.cache.set(data, data);
    }
    
    return data;
  }

  // ✅ Update with cache invalidation
  async update(id: Types.ObjectId, updateData: Partial<YourEntity>) {
    // Get current entity for slug (needed for invalidation)
    const current = await this.getById(id);
    
    const updated = await this.baseRepo.updateOne({ _id: id }, updateData);
    
    // Invalidate both old and new caches
    if (current) await this.cache.invalidate(current);
    if (updated) await this.cache.set(updated, updated);
    
    return updated;
  }
}
```

---

## 6. When to Invalidate Cache

### Invalidation Triggers

| Event | Action | Example |
|-------|--------|---------|
| **Create** | Clear list caches | New batch → clear `user_batches_list` |
| **Update** | Clear specific + list caches | Update batch → clear `batch_123` + `user_batches_list` |
| **Delete** | Clear specific + list caches | Delete batch → clear `batch_123` + `user_batches_list` |
| **Bulk Update** | Clear all related caches | Batch status change → clear all affected user caches |

### Using `@ClearCache` Decorator

```typescript
import ClearCache from 'src/bootstrap/decorators/clearCache.decorator';

// Clear single key
@ClearCache('user_notify_bookings:{userId}')
async updateUserNotifyDetails(userId: Types.ObjectId, ...) { }

// Clear multiple keys (stack decorators)
@ClearCache('user_notify_bookings:{$_id}')
@ClearCache('user_notify_{$_id}')
async createUserNotify(user: UserDetailsInterface, data: CreateUserNotifyDto) { }
```

### Manual Invalidation in Cache Service

```typescript
// In your cache service
async invalidateUserCaches(userId: Types.ObjectId) {
  await Promise.all([
    this.cache.del(`user_notify_${userId}`),
    this.cache.del(`user_notify_bookings:${userId}`),
    this.cache.del(`user_profile_${userId}`),
  ]);
}
```

---

## 7. Secondary Key Invalidation

> [!IMPORTANT]
> When you cache by `_id` but also need to invalidate by `slug`, `code`, or other identifiers.

### The Problem

```
Cache keys:
  • batch_id:507f1f77bcf86cd799439011 → { _id, slug: "my-batch", ... }
  • batch_slug:my-batch → { _id, slug: "my-batch", ... }

On update by ID → Need to clear BOTH keys
On update by slug → Need to clear BOTH keys
```

### Solution: DB Lookup Before Invalidation

```typescript
// your_module.cache.ts
@Injectable()
export class YourModuleCacheService {
  private BASE_KEY = 'entity_';

  constructor(
    private readonly cache: CacheService,
    @Inject(YourEntity.name)
    private readonly baseRepo: BaseRepository<YourEntity>,  // ✅ Inject repo
  ) {}

  // ✅ Invalidate by ID (fetches slug for secondary invalidation)
  async invalidateById(id: Types.ObjectId) {
    // First, try to get from cache (to get slug)
    let entity = await this.cache.get(`${this.BASE_KEY}id:${id}`);
    
    // If not in cache, fetch from DB
    if (!entity) {
      entity = await this.baseRepo.fetchOne(
        { searchParams: { _id: id } },
        { projection: { slug: 1 } }  // ✅ Only fetch needed field
      );
    }

    // Invalidate both keys
    await Promise.all([
      this.cache.del(`${this.BASE_KEY}id:${id}`),
      entity?.slug && this.cache.del(`${this.BASE_KEY}slug:${entity.slug}`),
    ]);
  }

  // ✅ Invalidate by slug (fetches _id for primary invalidation)
  async invalidateBySlug(slug: string) {
    let entity = await this.cache.get(`${this.BASE_KEY}slug:${slug}`);
    
    if (!entity) {
      entity = await this.baseRepo.fetchOne(
        { searchParams: { slug } },
        { projection: { _id: 1 } }
      );
    }

    await Promise.all([
      this.cache.del(`${this.BASE_KEY}slug:${slug}`),
      entity?._id && this.cache.del(`${this.BASE_KEY}id:${entity._id}`),
    ]);
  }

  // ✅ Invalidate with known entity (no DB call needed)
  async invalidateEntity(entity: { _id: Types.ObjectId; slug: string }) {
    await Promise.all([
      this.cache.del(`${this.BASE_KEY}id:${entity._id}`),
      this.cache.del(`${this.BASE_KEY}slug:${entity.slug}`),
    ]);
  }
}
```

### Usage in Service

```typescript
// When you have the full entity (preferred - no extra DB call)
async updateBatch(id: Types.ObjectId, data: UpdateDto) {
  const existing = await this.getById(id);  // Already fetched
  const updated = await this.baseRepo.updateOne({ _id: id }, data);
  
  await this.cache.invalidateEntity(existing);  // ✅ Use entity
  return updated;
}

// When you only have ID
async deleteBatch(id: Types.ObjectId) {
  await this.cache.invalidateById(id);  // ✅ Will lookup slug
  await this.baseRepo.delete({ _id: id });
}

// When you only have slug
async archiveBatchBySlug(slug: string) {
  await this.cache.invalidateBySlug(slug);  // ✅ Will lookup _id
  await this.baseRepo.updateOne({ slug }, { archived: true });
}
```

### Reference Key Pattern (Alternative)

Store a reference from secondary key to primary key:

```typescript
// When setting cache
async set(entity: YourEntity) {
  const idKey = `${this.BASE_KEY}id:${entity._id}`;
  const slugRefKey = `${this.BASE_KEY}slug_ref:${entity.slug}`;
  
  await Promise.all([
    this.cache.set(idKey, entity, this.TTL),
    this.cache.set(slugRefKey, entity._id.toString(), this.TTL),  // ✅ Reference only
  ]);
}

// When invalidating by slug
async invalidateBySlug(slug: string) {
  const slugRefKey = `${this.BASE_KEY}slug_ref:${slug}`;
  const id = await this.cache.get(slugRefKey);  // ✅ Get ID from reference
  
  await Promise.all([
    this.cache.del(slugRefKey),
    id && this.cache.del(`${this.BASE_KEY}id:${id}`),
  ]);
}
```

---

## 8. Cross-Module Cache Invalidation

> [!IMPORTANT]
> When Module A's data changes, it may affect Module B's cached data. Plan for this!

### Dependency Map Template

Document which modules affect which caches:

```
┌─────────────────────────────────────────────────────────────────┐
│  MODULE: batch_user_notify                                       │
├─────────────────────────────────────────────────────────────────┤
│  OWNS CACHES:                                                    │
│  • batch_user_notify_userId:{id}_batchId:{id}                   │
│  • batch_user_notify_batchId:{id}                               │
│  • user_notify_{userId}                                          │
│  • user_notify_bookings:{userId}                                 │
├─────────────────────────────────────────────────────────────────┤
│  AFFECTED BY:                                                    │
│  • batches module (batch deletion → clear all notify caches)    │
│  • users module (user deletion → clear user's notify caches)    │
│  • schedules module (schedule update → clear schedule caches)   │
├─────────────────────────────────────────────────────────────────┤
│  AFFECTS:                                                        │
│  • (none - leaf module)                                          │
└─────────────────────────────────────────────────────────────────┘
```

### Cross-Module Invalidation Strategies

#### Strategy 1: Event-Based (Recommended)

```typescript
// In batches.service.ts
async deleteBatch(batchId: Types.ObjectId) {
  await this.baseRepo.delete({ _id: batchId });
  
  // Emit event for other modules to react
  this.eventEmitter.emit('batch.deleted', { batchId });
}

// In batch_user_notify.service.ts
@OnEvent('batch.deleted')
async handleBatchDeleted(payload: { batchId: Types.ObjectId }) {
  await this.cache.invalidateBatchCaches(payload.batchId);
}
```

#### Strategy 2: Direct Injection

```typescript
// In batches.service.ts
constructor(
  private readonly batchUserNotifyCache: BatchUserNotifyCacheService,
) {}

async deleteBatch(batchId: Types.ObjectId) {
  await this.baseRepo.delete({ _id: batchId });
  await this.batchUserNotifyCache.invalidateBatchCaches(batchId);
}
```

---

## 9. Quick Reference Cheatsheet

### Key Naming Convention

```
{module}_{identifier}:{value}[_{identifier2}:{value2}]

Examples:
• batch_id:507f1f77bcf86cd799439011
• batch_slug:my-batch-2024
• user_notify_userId:abc_batchId:xyz
```

### TTL Quick Reference (Grade-Based)

| Grade | Constant | TTL | Use Case |
|-------|----------|-----|----------|
| 🔴 Very High | `CacheTTL.VERY_HIGH` | 20 min | Sessions, live data |
| 🟡 High | `CacheTTL.HIGH` | 2 hours | Preferences, bookings |
| 🔵 Medium | `CacheTTL.MEDIUM` | 6 hours | Entity details |
| 🟢 Low | `CacheTTL.LOW` | 24 hours | Config, lookups |

### Decorator Quick Reference

```typescript
import { CacheTTL } from 'src/common/constants/cache.constants';

// 🔴 Very High (20 min)
@Cache('key:{param}', '', CacheTTL.VERY_HIGH)

// 🟡 High (2 hours)
@Cache('key:{param}', '', CacheTTL.HIGH)

// 🔵 Medium (6 hours) - DEFAULT
@Cache('key:{param}', '', CacheTTL.MEDIUM)

// 🟢 Low (24 hours)
@Cache('key:{param}', '', CacheTTL.LOW)

// With hash key
@Cache('key:{param}', 'hkey:{param2}', CacheTTL.HIGH)

// Clear cache
@ClearCache('key:{param}')
```

### CacheService Methods

| Method | Use Case |
|--------|----------|
| `get(key)` | Get single value |
| `set(key, data, ttl?)` | Set single value |
| `del(key)` | Delete single key |
| `getMultipleKeys(keys)` | Bulk get |
| `setMultipleKeys(data, ttl?)` | Bulk set |
| `hGet(hKey, key)` | Get from hash |
| `hSet(hKey, key, data, ttl?)` | Set in hash |
| `hDel(hKey, key)` | Delete from hash |

---

## Appendix: Decision Checklist

Use this before implementing cache:

- [ ] **TYPE**: Method cache or DB call cache?
- [ ] **GRADE**: What priority level? (Very High/High/Medium/Low)
- [ ] **APPROACH**: Decorator or dedicated service?
- [ ] **KEYS**: What identifiers are used? (id, slug, code, etc.)
- [ ] **SECONDARY**: Need secondary key invalidation?
- [ ] **INVALIDATION**: What mutations clear this cache?
- [ ] **CROSS-MODULE**: Which other modules affect/are affected?
- [ ] **TESTING**: Are cache operations covered in tests?

---

*Last updated: 2026-01-29*
