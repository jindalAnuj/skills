---
name: code-review-quant
description: Standardize code reviews for quantitative trading strategy implementations. Use when reviewing strategy code from QuantResearcher or DataEngineer, validating backtest implementations, preparing code for paper trading, or conducting pre-deployment reviews.
---

# Code Review Quant Skill

Standardized code review process for quantitative trading strategies targeting Indian equity markets (NSE/BSE). Ensures consistent quality checks for backtesting code, strategy logic, and risk management.

## When to Use

- Review task assigned with pattern `*Review*` or `*code review*`
- Strategy implementation completed by QuantResearcher or DataEngineer
- New strategy ready for validation before paper trading
- Backtest results need code verification
- Pre-deployment validation checkpoint

## Workflow

### Step 1: Gather Context

Before reviewing, collect:

```
Context Checklist:
- [ ] Strategy specification document
- [ ] Related backtest report (if available)
- [ ] Previous review feedback (if iteration)
- [ ] Target deployment phase
```

**Required information:**
- Strategy name and variant
- Implementation files/modules
- Expected behavior from specification
- Any known constraints or edge cases

### Step 2: Code Quality Checks

Run through the code quality checklist:

| Check | Status | Notes |
|-------|--------|-------|
| Type hints on all functions | ⬜ | |
| Docstrings with parameter descriptions | ⬜ | |
| No hardcoded magic numbers | ⬜ | |
| Constants defined at module level | ⬜ | |
| Error handling for edge cases | ⬜ | |
| Logging for key operations | ⬜ | |
| No commented-out code | ⬜ | |
| Consistent naming conventions | ⬜ | |

See [reference.md](reference.md) for detailed criteria.

### Step 3: Backtest Integrity Checks

Critical checks for backtesting accuracy:

| Check | Status | Notes |
|-------|--------|-------|
| No look-ahead bias | ⬜ | |
| Point-in-time data handling | ⬜ | |
| Slippage/commission modeled | ⬜ | |
| Universe survivorship bias addressed | ⬜ | |
| Corporate actions handled | ⬜ | |
| T+1 settlement respected | ⬜ | |
| Pre-open session handling | ⬜ | |
| Circuit breaker scenarios | ⬜ | |

**Look-ahead bias red flags:**
- Using `df.shift(-1)` without clear justification
- Future dates in any calculation
- Accessing data beyond current bar timestamp

### Step 4: Strategy Logic Checks

Verify trading logic implementation:

| Check | Status | Notes |
|-------|--------|-------|
| Entry signals match specification | ⬜ | |
| Exit signals match specification | ⬜ | |
| Position sizing follows risk limits | ⬜ | |
| Stop-loss mechanisms implemented | ⬜ | |
| Take-profit logic (if specified) | ⬜ | |
| Rebalance logic matches spec | ⬜ | |
| Holding period enforced (1-45 days) | ⬜ | |
| Order type appropriate (market/limit) | ⬜ | |

### Step 5: Risk Controls Checks

Verify risk management implementation:

| Check | Status | Notes |
|-------|--------|-------|
| Max drawdown limits enforced | ⬜ | |
| Position concentration limits | ⬜ | |
| Daily loss circuit breakers | ⬜ | |
| Capital allocation boundaries | ⬜ | |
| Max positions per sector | ⬜ | |
| Leverage limits (if applicable) | ⬜ | |
| Overnight exposure limits | ⬜ | |

### Step 6: Test Coverage Checks

Verify testing adequacy:

| Check | Status | Notes |
|-------|--------|-------|
| Unit tests for core functions | ⬜ | |
| Integration test for full pipeline | ⬜ | |
| Edge case tests present | ⬜ | |
| Gap handling tested | ⬜ | |
| Corporate action tests | ⬜ | |
| Circuit breaker scenarios tested | ⬜ | |
| Test coverage > 80% | ⬜ | |

### Step 7: Generate Review Report

Use the [review report template](templates/review-report.md) to document findings.

**Output requirements:**
1. Complete checklist with pass/fail status
2. Issues list with severity classification
3. Go/No-go recommendation
4. Suggested improvements

## Severity Classification

| Severity | Definition | Action |
|----------|------------|--------|
| Critical | Data integrity or calculation errors | Block deployment |
| High | Risk control gaps or logic errors | Must fix before next phase |
| Medium | Code quality issues affecting maintainability | Fix within sprint |
| Low | Style or minor improvements | Nice to have |

## Go/No-Go Decision Matrix

```
Critical issues: 0     → Eligible for GO
High issues: 0-1       → Conditional GO (with remediation plan)
High issues: 2+        → NO-GO
Any look-ahead bias    → Automatic NO-GO
Missing risk controls  → Automatic NO-GO
```

## Indian Market Considerations

During review, verify handling of:

- **STT impact:** 0.1% delivery, 0.025% intraday
- **Circuit breakers:** Stock-level 2/5/10/20% bands
- **Settlement:** T+1 (funds available next day)
- **Trading hours:** 9:15-15:30 IST
- **Expiry effects:** Weekly/monthly Thursday expiry volatility
- **Pre-open session:** 9:00-9:15 gap potential

## Additional Resources

- Detailed check criteria: [reference.md](reference.md)
- Report template: [templates/review-report.md](templates/review-report.md)
- Related skill: [backtest-report](../backtest-report/SKILL.md)
