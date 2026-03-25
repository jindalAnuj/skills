# MongoDB Expert Skill - Test Scenarios

## Purpose
Test what Claude does WRONG without the skill, then verify skill fixes those issues.

## Scenario 1: Schema Design with Pressure
**Setup:** Complex e-commerce system needs schema for orders, products, customers, reviews.
**Pressure:** "We need this designed quickly for tomorrow's sprint planning"
**Test:** Does Claude:
- ❌ Default to SQL-style normalization without considering MongoDB patterns?
- ❌ Miss opportunities for embedding vs referencing?
- ❌ Forget to consider query patterns before designing schema?
- ❌ Skip index planning?

## Scenario 2: Query Optimization
**Setup:** Given a slow aggregation pipeline with 5+ stages
**Pressure:** "This query is timing out in production, fix it fast"
**Test:** Does Claude:
- ❌ Suggest changes without explaining WHY it's slow?
- ❌ Miss obvious issues like missing indexes?
- ❌ Fail to check if $lookup can be avoided?
- ❌ Not consider adding compound indexes?

## Scenario 3: Query Review
**Setup:** Review 3 queries for a new feature
**Pressure:** "Code review this PR before merge"
**Test:** Does Claude:
- ❌ Only check syntax, not performance?
- ❌ Miss N+1 query patterns?
- ❌ Not verify indexes exist?
- ❌ Skip checking projection usage?

## Scenario 4: Complex Aggregation
**Setup:** Build aggregation for: "Get top 10 products by revenue, grouped by category, with avg rating"
**Pressure:** "Business needs this report for meeting in 2 hours"
**Test:** Does Claude:
- ❌ Create inefficient pipeline ordering?
- ❌ Not use $match early to reduce documents?
- ❌ Miss opportunities for $project to reduce payload?
- ❌ Forget to consider index usage in aggregation?

## Running Tests

### Baseline (WITHOUT skill):
1. Spawn subagent without skill loaded
2. Give scenario + pressure
3. Document exact behavior and mistakes
4. Save transcript

### With Skill (GREEN phase):
1. Write minimal skill addressing documented failures
2. Spawn subagent WITH skill loaded
3. Run same scenarios
4. Verify skill fixes the issues

### Refactor (Close loopholes):
1. Find new rationalizations
2. Add explicit counters
3. Re-test until bulletproof
