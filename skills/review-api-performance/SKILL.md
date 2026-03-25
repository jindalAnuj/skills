---
name: review-api-performance
description: Use when reviewing API performance, detecting N+1 queries, missing projections, lean opportunities, cacheable queries, or repeated DB access patterns. Triggers include "review API performance", "slow API", "optimize queries", "caching opportunities", "db call audit", or investigating high latency endpoints.
---

# Review API Performance (Database & Caching Audit)

A comprehensive performance review skill that traces every database call from controller to repository—auditing queries, caching opportunities, and optimization potential.

---

## Overview

**Core principle:** Trace every database interaction end-to-end. Every query should justify its existence, use optimal patterns, and consider caching.

**Complementary skill:** Use `review-database` for MongoDB-level optimization (schema design, aggregation pipelines).

---

## Supporting Resources

This skill includes reference files for implementation:

| Resource | Description |
|----------|-------------|
| [caching-standards.md](./caching-standards.md) | Comprehensive caching guide: method vs DB cache, TTL grading, invalidation patterns |
| [cache.constants.ts](./cache.constants.ts) | TTL constant values (`CacheTTL.VERY_HIGH`, `HIGH`, `MEDIUM`, `LOW`) |

**Index Review:** For index suggestions, always check `*.entity.ts` files for `@Index()` decorators.

---

## When to Use

**Triggers:**
- ✅ Investigating slow API endpoints
- ✅ Before production deployment (performance audit)
- ✅ Module with high DB load
- ✅ Refactoring data access patterns
- ✅ Adding caching layer to existing code
- ✅ Auditing N+1 patterns in orchestrators

**Don't Use When:**
- ❌ Schema design → Use `review-database`
- ❌ Index optimization → Use `review-database`
- ❌ Simple CRUD audit (overkill)

---

## Output Strategy: Artifact-First Approach

> [!IMPORTANT]
> **Always create artifacts FIRST** in the brain folder, then copy to codebase after user approval.

### Step 1: Create Artifact (Always)

```
<appDataDir>/brain/<conversation-id>/db-calls-review.md
```

Use `IsArtifact: true` when writing to ensure visibility in Antigravity IDE.

### Step 2: Copy to Codebase (After Approval)

```
{module}/code-review/{api-name}-db-review.md
```

Only copy after user reviews and approves the artifact.

---

## Artifact-First Workflow

### Artifact Directory Structure

```
<appDataDir>/brain/<conversation-id>/
├── task.md                          # Track review progress
├── implementation_plan.md           # Document review scope & approach
├── db-calls-review.md               # Main review artifact
└── walkthrough.md                   # Final summary with findings
```

### Workflow with task_boundary

**1. PLANNING Mode:**
- Create `implementation_plan.md` with:
  - API entry point and route
  - Repository calls to trace
  - Review criteria to apply
- Use `notify_user` for approval before execution

**2. EXECUTION Mode:**
- Create `db-calls-review.md` as structured artifact
- Update `task.md` checkboxes as review progresses:
  - `[/]` Tracing DB calls
  - `[x]` N+1 Query analysis
  - `[ ]` Projection review
  - `[ ]` Lean usage check
  - `[ ]` Caching opportunities
  - `[ ]` Batch operation review

**3. VERIFICATION Mode:**
- Create `walkthrough.md` with:
  - Summary metrics (Critical/Warning/Suggestion counts)
  - Prioritized optimization targets
  - Estimated performance impact
  - Links to generated review file

### Artifact Metadata

```markdown
---
ArtifactType: other
Summary: DB calls review for {API Name} with X critical, Y warnings, Z caching opportunities
---
```

### User Review Points

Use `notify_user` with `PathsToReview` at:
1. **After planning** - Confirm review scope
2. **After execution** - Review findings and recommendations
3. **Final review** - Request approval before copying to codebase

---

## Review Artifact Structure

```markdown
# DB Calls Review: {API Name}

## Summary
- **API Path:** {route}
- **Entry Point:** {controller method}
- **Total DB Calls Traced:** {count}
- **Critical Issues:** {count}
- **Warnings:** {count}
- **Caching Opportunities:** {count}

## Review Criteria Checklist
- [x] N+1 Query Detection
- [x] Missing Projections
- [x] Missing `.lean()` Usage
- [x] Repeated Queries (Same Request)
- [x] Batch Operation Opportunities
- [x] Caching Candidates
- [x] Query Complexity Analysis
- [x] Index Review & Optimization

## DB Call Trace
[Complete call graph with every repository method]

## Findings

### 🔴 Critical (Must Fix)
### 🟡 Warning (Should Fix)
### 💾 Caching Opportunities
### 🟢 Suggestion (Nice to Have)

## Optimization Summary
[Prioritized list with estimated impact]
```

---

## Review Criteria

### 1. N+1 Query Detection

| Pattern | Indicator | Severity |
|---------|-----------|----------|
| **Loop with await query** | `for...await findById` | 🔴 Critical |
| **forEach with query** | `forEach...await repository` | 🔴 Critical |
| **map with await** | `.map(async x => await find...)` | 🔴 Critical |
| **$lookup missing** | Related data fetched separately | 🟡 Warning |

**Detection Pattern:**
```typescript
// ❌ N+1: Hits DB N times
for (const orderId of orderIds) {
  const order = await this.orderRepo.findById(orderId);
}

// ✅ Batch: Hits DB once
const orders = await this.orderRepo.findByIds(orderIds);
```

### 2. Missing Projections

| Pattern | Indicator | Severity |
|---------|-----------|----------|
| **Full doc fetch** | `findById(id)` returns all fields | 🟡 Warning |
| **Query without select** | `.find({})` no projection | 🟡 Warning |
| **DTO needs few fields** | Method uses <50% of fetched fields | 🟡 Warning |

**Detection:** If response DTO uses fewer than half the entity fields, add projection.

### 3. Missing `.lean()` Usage

| Pattern | Indicator | Severity |
|---------|-----------|----------|
| **Read-only query** | No `.save()` on result | 🟡 Warning |
| **List queries** | `.find()` returns array for display | 🟡 Warning |
| **DTO transformation** | Entity → DTO mapping only | 🟡 Warning |

**Rule:** Use `.lean()` when:
- Not calling `.save()` on document
- Not using Mongoose virtuals or methods
- Only reading/transforming data

**Implementation:**
```typescript
// Pass isLean: true to repository methods
return this.repo.fetchOne({
  searchParams: { ... },
  isLean: true // ✅ Explicitly request POJO
});
```

### 4. Repeated Queries (Same Request)

| Pattern | Indicator | Severity |
|---------|-----------|----------|
| **Same ID queried twice** | Different functions fetch same entity | 🟡 Warning |
| **Master data refetched** | Categories/configs fetched per item | 🔴 Critical |
| **User context refetched** | User loaded in multiple services | 🟡 Warning |

**Detection:** Trace call graph, find same `findById` with same ID parameter across functions.

### 5. Missing Batch Operations

| Pattern | Indicator | Severity |
|---------|-----------|----------|
| **Loop inserts** | `for...await create(item)` | 🔴 Critical |
| **Loop updates** | `for...await updateOne()` | 🔴 Critical |
| **Sequential deletes** | `for...await deleteOne()` | 🟡 Warning |

**Fix:** Replace with `insertMany`, `updateMany`, `bulkWrite`.

### 6. Caching Candidates

**Output Format:** When identifying caching opportunities, add TODO comments in the review:

```typescript
// TODO-cache: Cache master data (categories change infrequently, high read volume)
// TODO-cache: Cache user profile lookup (same user fetched multiple times per request)
// TODO-cache: Cache aggregation result (expensive computation, 5-min staleness acceptable)
```

**Cache Decision Criteria:**
- ✅ Called frequently (hot path)
- ✅ Data changes infrequently
- ✅ Same query repeated across requests
- ✅ Expensive aggregation/computation

### 7. Query Complexity Analysis

| Issue | Indicator | Severity |
|-------|-----------|----------|
| **Unbounded query** | `.find({})` without limit | 🔴 Critical |
| **Deep nested conditions** | 4+ levels of $or/$and | 🟡 Warning |
| **Large $in array** | `$in` with 1000+ items | 🟡 Warning |
| **Regex without anchor** | `/pattern/` not `/^pattern/` | 🟡 Warning |
| **Sort without index** | Large result set sorted in memory | 🔴 Critical |

### 8. Index Review & Optimization

#### 8.1 Index Suggestion Based on Query Patterns

For each query identified, check if supporting index exists in entity file:

| Query Pattern | Suggested Index | Priority |
|---------------|-----------------|----------|
| `find({ userId })` | `{ userId: 1 }` | 🔴 High (frequent) |
| `find({ status, createdAt }).sort({ createdAt: -1 })` | `{ status: 1, createdAt: -1 }` | 🔴 High |
| `find({ $in: [ids] })` | `{ _id: 1 }` (default) | ✅ Exists |
| `find({ categoryId, isActive })` | `{ categoryId: 1, isActive: 1 }` | 🟡 Medium |
| `aggregate([{ $match: { programId } }])` | `{ programId: 1 }` | 🔴 High |

**Index Suggestion Workflow:**
1. Extract query filters from repository methods
2. Locate entity file: `src/**/entities/{collection-name}.entity.ts` or `src/**/{module}/*.entity.ts`
3. Check for `@Index()` decorators in entity class
4. Suggest missing indexes with compound field order (equality → sort → range)

**Entity File Patterns:**
```bash
# Find entity files for a collection
find src -name "*.entity.ts" | xargs grep -l "collection.*{collection_name}"
```

#### 8.2 Redundant Index Detection

Review existing indexes for redundancy:

| Redundancy Type | Example | Action |
|-----------------|---------|--------|
| **Prefix Covered** | `{ a: 1 }` when `{ a: 1, b: 1 }` exists | 🔴 Remove `{ a: 1 }` |
| **Duplicate** | Same index defined twice | 🔴 Remove duplicate |
| **Low Selectivity** | Index on boolean field alone | 🟡 Consider compound |
| **Unused Index** | Index not matching any query | 🟡 Candidate for removal |

**Detection Pattern (from entity file):**

Two ways indexes are defined in this codebase:

**1. Using `@Prop({ index: true })` (single field):**
```typescript
@Prop({
  type: SchemaTypes.ObjectId,
  required: true,
  ref: 'phase_data',
  index: true,  // ✅ Single field index
})
phaseId: Types.ObjectId;
```

**2. Using `Schema.index()` (compound/complex indexes):**
```typescript
// ========== Indexes for Performance Optimization ==========

// Primary lookup index
TestCategoryV2Schema.index({ phaseId: 1 });

// Composite index for cohort-based lookups
TestCategoryV2Schema.index({ phaseId: 1, 'testDetails.cohortId': 1 });

// Index for nested field lookups
TestCategoryV2Schema.index({ 'testDetails.satTestDetails._id': 1 });

// Index for foreign key lookups
TestCategoryV2Schema.index({ 'testDetails.scholarshipConfigId': 1 });
```

**Redundancy Example:**
```typescript
// ⚠️ REDUNDANT: { phaseId: 1 } already covered by compound index
@Prop({ index: true }) phaseId;
Schema.index({ phaseId: 1, 'testDetails.cohortId': 1 });  // This covers phaseId-only queries
```

#### 8.3 Unnecessary Index Check

| Issue | Indicator | Severity |
|-------|-----------|----------|
| **Write-heavy collection** | > 5 indexes on frequently updated docs | 🟡 Warning |
| **Never queried field** | Index on field not in any query | 🟡 Warning |
| **Text index unused** | `{ field: 'text' }` but no `$text` queries | 🟡 Warning |
| **Sparse on required field** | `{ sparse: true }` on non-nullable field | 🟢 Suggestion |

**Max Index Guidelines:**
- ✅ 3-4 indexes per collection (ideal)
- ⚠️ 5-6 indexes (acceptable for read-heavy)
- 🔴 7+ indexes (review for necessity)

#### 8.4 MongoDB Index Best Practices (Long-Term Impact)

> [!WARNING]
> **Too many indexes can severely impact write performance and storage costs over time.**

**Index Overhead Costs:**

| Impact | Description | Symptom |
|--------|-------------|---------|
| **Write Amplification** | Every insert/update must update ALL indexes | Slow writes, high disk I/O |
| **Memory Pressure** | Indexes must fit in RAM for optimal perf | Swapping, slow queries |
| **Storage Bloat** | Each index = ~10-30% of collection size | Increased storage costs |
| **Replication Lag** | More indexes = more work for secondaries | Replica delays |
| **Index Build Time** | Large indexes take hours to create | Deployment delays |

**Best Practices:**

| Practice | Rationale |
|----------|-----------|
| **Compound > Multiple Single** | `{ a: 1, b: 1 }` covers `{ a: 1 }` queries too |
| **ESR Rule** | Order: Equality → Sort → Range for compound indexes |
| **Partial Indexes** | Only index active docs: `{ partialFilterExpression: { status: 'active' } }` |
| **Sparse Indexes** | Skip nulls: `{ sparse: true }` for optional fields |
| **TTL for Expiring Data** | Auto-delete old docs instead of manual cleanup |
| **Covered Queries** | Include all queried fields in index projection |

**Index Review Triggers:**

| Trigger | Action |
|---------|--------|
| Collection has 7+ indexes | Audit for redundancy |
| Write-heavy collection (>1000 writes/min) | Minimize indexes, use compound |
| Index size > 20% of collection size | Review necessity |
| Queries using COLLSCAN | Add missing index OR accept if rare query |
| Index never used (check `$indexStats`) | Remove after validation |

**MongoDB Commands for Index Health:**

```javascript
// Check index usage statistics
db.collection.aggregate([{ $indexStats: {} }])

// Find unused indexes (totalScan = 0)
// Result shows accesses.ops - if 0, index is unused

// Check index size
db.collection.stats().indexSizes

// Check total index memory
db.collection.totalIndexSize()
```

#### 8.5 Index Audit Checklist

- [ ] All query patterns have supporting indexes
- [ ] Compound indexes ordered by: equality → sort → range
- [ ] No redundant single-field indexes when compound exists
- [ ] Write-heavy collections have minimal indexes
- [ ] Unused indexes identified for removal
- [ ] Index names are meaningful (not auto-generated)
- [ ] Total index count per collection < 7

#### 8.6 Index Finding Template

```markdown
### Finding: {Index Issue Title}

| Attribute | Value |
|-----------|-------|
| **Type** | Missing / Redundant / Unnecessary |
| **Collection** | `{collection_name}` |
| **Entity File** | `{file.entity.ts}:{line}` |
| **Query Pattern** | `find({ field1, field2 })` |
| **Current Indexes** | `{ field1: 1 }`, `{ field2: 1 }` |
| **Recommendation** | Add `{ field1: 1, field2: 1 }` / Remove `{ field1: 1 }` |
| **Impact** | Query time: ~100ms → ~5ms |
```

---

## Review Workflow

### Function Trace Format

```
1. ENTRY POINT → TRACE ALL DB CALLS

   ┌─ getOrders (Controller) ──────────────────────────────┐
   │  Route: GET /orders                                   │
   │  DB Calls: None (delegates only)                      │
   └───────────────────────────────────────────────────────┘
           │
           ▼
   ┌─ getOrdersByUser (Orchestrator) ──────────────────────┐
   │  File: order.orchestrator.ts:45                       │
   │  DB Calls:                                            │
   │    🔴 Line 52: N+1 in loop (getProductsByOrder)       │
   │    🟡 Line 58: Missing projection (user only needs 3) │
   └───────────────────────────────────────────────────────┘
           │
           ├──────────────────┬──────────────────┐
           ▼                  ▼                  ▼
   ┌─ orderRepo.find │ productRepo.find │ userRepo.findById ─┐
   │  Issues:        │  Issues:          │  Issues:           │
   │  💾 Cacheable   │  🔴 N+1 pattern   │  ✅ OK             │
```

### DB Call Inventory Table

For each repository method called, document:

| # | Method | File:Line | Query Pattern | Issues | Caching |
|---|--------|-----------|---------------|--------|---------|
| 1 | `orderRepo.findByUserId` | order.repo.ts:34 | `find({userId})` | Missing lean | ❌ Per-user |
| 2 | `productRepo.findById` | product.repo.ts:20 | `findById(id)` | 🔴 In loop (N+1) | ❌ |
| 3 | `categoryRepo.getAll` | category.repo.ts:15 | `find({active:true})` | None | ✅ 15min TTL |

---

## Finding Template

```markdown
### Finding: {Short Title}

| Attribute | Value |
|-----------|-------|
| **Severity** | 🔴 Critical / 🟡 Warning / 💾 Caching / 🟢 Suggestion |
| **Category** | {N+1 / Projection / Lean / Caching / Batch / Complexity} |
| **Location** | `{file}:{line}` |
| **Query** | `{repository method and filter}` |
| **Current Pattern** | ```typescript\n{current code}\n``` |
| **Issue** | {What's inefficient} |
| **Impact** | {Performance consequence} |
| **Fix** | ```typescript\n{optimized code}\n``` |
| **Estimated Improvement** | {e.g., "N DB calls → 1 call"} |
```

---

## Quick Reference: Detection Patterns

| Grep Pattern | Likely Issue |
|--------------|--------------|
| `for.*await.*find` | N+1 Query |
| `forEach.*await.*repo` | N+1 Query |
| `.find({})` without limit | Unbounded Query |
| `findById(` without 2nd param | Missing Projection |
| `.find(` without `.lean()` | Missing Lean |
| `for.*await.*create\|save` | Missing Batch |
| Same `findById` called twice | Repeated Query |

---

## Caching Annotation Examples

When reviewing code, annotate caching opportunities with `TODO-cache:` comments:

```typescript
// TODO-cache: Cache getActiveCategories (master data, 15-min TTL, invalidate on category CRUD)
async getActiveCategories(): Promise<Category[]> {
  return this.categoryRepo.findActive().lean();
}

// TODO-cache: Cache getConfigById (config rarely changes, 30-min TTL, key: config:{id})
async getConfigById(id: string): Promise<Config> {
  return this.configRepo.findById(id).lean();
}

// TODO-cache: Method-level cache for getUserProfile (same user queried multiple times in request)
async getUserProfile(userId: string): Promise<User> {
  return this.userRepo.findById(userId).lean();
}
```

---

## Checklist Before Completion

- [ ] All repository calls traced from controller
- [ ] Every query checked for N+1 pattern
- [ ] All queries reviewed for projection needs
- [ ] Read-only queries checked for `.lean()`
- [ ] Same entity fetched multiple times detected
- [ ] Batch operation opportunities identified
- [ ] Caching candidates marked with TTL suggestions
- [ ] Unbounded queries flagged
- [ ] Findings prioritized by impact
- [ ] Artifact created in brain folder first
- [ ] User approval obtained before codebase copy

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Writing directly to codebase | Always create artifact in brain folder FIRST |
| Reviewing only orchestrator layer | Trace ALL service → repository calls recursively |
| Missing query inside helper functions | Grep for all `await.*repo\|Model\|find` patterns |
| Not checking mapper transformations | Large entity → small DTO = projection candidate |
| Ignoring nested async calls | `Promise.all` can hide N+1 in parallel |
| Generic caching recommendations | Specify exact TTL and cache key strategy |

---

## Example Usage

**Prompt:** "Review DB calls for the getScholarshipCategories API"

**Output (Artifact-First):**
1. `<appDataDir>/brain/<conversation-id>/db-calls-review.md` - Artifact created first
2. User reviews findings: 2 N+1 patterns, 3 missing projections, 2 caching opportunities
3. `scholarship-categories/code-review/get-categories-db-review.md` - Copied to codebase after approval
