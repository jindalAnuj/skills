# MongoDB Expert Skill - Testing Guide

## How to Test This Skill

Since this is a custom skill in your `.gemini/skills` directory, you need to test it in a session where it's loaded.

### GREEN Phase Test (Verify Skill Works)

**Goal**: Verify the skill fixes the issues found in baseline testing.

### Test Scenario 1: Schema Design with Skill

1. **Start new chat/session** (ensure skill is loaded via your hooks)
2. **Give the same prompt from baseline**:
   ```
   You need to design a MongoDB schema for an e-commerce system. We need this designed quickly for tomorrow's sprint planning.

   Requirements:
   - Orders (user orders with multiple items)
   - Products (product catalog with details)
   - Customers (user accounts and profiles)
   - Reviews (product reviews with ratings)

   The system needs to:
   1. Show product listings with average ratings
   2. Display order history for customers
   3. Show product details with recent reviews
   4. Generate sales reports by product/category

   Please design the schema.
   ```

3. **Expected improvements over baseline**:
   - ✅ Should reference the Schema Design Checklist
   - ✅ Should explicitly ask about query patterns first
   - ✅ Should check anti-patterns list
   - ✅ Should mention document size limits
   - ✅ Should consider sharding strategy
   - ✅ Should discuss read vs write optimization explicitly

4. **Document**: Did Claude follow the checklist? What improved?

---

### Test Scenario 2: Query Optimization with Skill

1. **Same session** (skill loaded)
2. **Give the same problem**:
   ```
   This aggregation query is timing out in production! We need it fixed fast.

   [paste the slow query from baseline test]

   The orders collection has 500K documents. Products has 10K. Categories has 50.

   Please fix this query - production is suffering!
   ```

3. **Expected improvements over baseline**:
   - ✅ Should run `.explain()` FIRST (diagnostic step)
   - ✅ Should check existing indexes before suggesting new ones
   - ✅ Should follow the Query Optimization Workflow
   - ✅ Should verify the fix with `.explain()` after optimization
   - ✅ Should mention diagnostic tools (currentOp, profiler, mongostat)
   - ✅ Should suggest `allowDiskUse` if applicable

4. **Document**: Did Claude follow the systematic workflow?

---

### Test Scenario 3: Pressure Test (REFACTOR Phase)

**Goal**: Ensure skill prevents shortcuts under pressure.

1. **Add time pressure**:
   ```
   Quick question - I need to add user comments to products. Should I embed them or use a separate collection? Need to decide in next 5 minutes for standup.
   ```

2. **Expected behavior**:
   - ✅ Should still ask about query patterns (not skip checklist)
   - ✅ Should mention anti-patterns (unbounded arrays)
   - ✅ Should not give quick answer without systematic analysis

3. **If Claude skips checklist**, add to skill:
   - Red flags section
   - Explicit counter: "Even under time pressure, use the checklist"

---

### Test Scenario 4: Query Review

1. **Give code review task**:
   ```
   Can you review this aggregation for performance issues?

   [paste a query with multiple issues: $match at end, no projection, missing index]
   ```

2. **Expected behavior**:
   - ✅ Should use Query Review Checklist
   - ✅ Should check each item systematically
   - ✅ Should suggest running `.explain()`
   - ✅ Should identify all issues, not just first one

---

## Comparison Checklist

Compare responses WITH skill vs baseline (WITHOUT skill):

| Aspect | Baseline | With Skill | Improved? |
|--------|----------|------------|-----------|
| Uses systematic checklist | ❌ No | Should be ✅ | |
| Mentions diagnostic tools | ❌ Missing | Should be ✅ | |
| Verifies with explain() | ❌ No | Should be ✅ | |
| Checks anti-patterns | ⚠️ Partial | Should be ✅ | |
| Considers advanced options | ❌ No | Should be ✅ | |
| Follows workflow systematically | ❌ Ad-hoc | Should be ✅ | |

---

## Success Criteria

The skill is effective if Claude:

1. **Always uses checklists** (not just intuition)
2. **Runs diagnostics before suggesting fixes** (explain(), getIndexes(), currentOp())
3. **Verifies fixes** (explain() after optimization)
4. **Detects anti-patterns systematically**
5. **Follows workflows even under pressure**

If any of these fail, move to REFACTOR phase: add explicit counters and re-test.

---

## Next Steps After Testing

1. **If tests pass**: Skill is ready to use
2. **If tests reveal gaps**:
   - Document new rationalizations
   - Add to "Red Flags" section
   - Add explicit counters
   - Re-test

3. **Consider splitting**: If skill becomes too large (>500 words), split into:
   - `mongodb-schema-design` (schema patterns)
   - `mongodb-query-optimization` (performance tuning)
   - `mongodb-diagnostics` (tooling and profiling)
