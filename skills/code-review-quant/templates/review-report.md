# Code Review Report: [Strategy Name]

**Review Date:** [YYYY-MM-DD]
**Reviewer:** [Agent Name]
**Strategy:** [Strategy Name/ID]
**Implementation:** [File paths or PR reference]
**Related Task:** [Issue identifier]

---

## Executive Summary

[1-2 sentence summary of review outcome and key finding]

**Recommendation:** [GO / CONDITIONAL GO / NO-GO]

---

## Review Status

| Category | Status | Pass Rate | Notes |
|----------|--------|-----------|-------|
| Code Quality | 🟢/🟡/🔴 | X/8 | |
| Backtest Integrity | 🟢/🟡/🔴 | X/8 | |
| Strategy Logic | 🟢/🟡/🔴 | X/8 | |
| Risk Controls | 🟢/🟡/🔴 | X/7 | |
| Test Coverage | 🟢/🟡/🔴 | X/7 | |

**Overall:** [X/38 checks passed]

---

## Code Quality Checks

| # | Check | Status | Notes |
|---|-------|--------|-------|
| 1 | Type hints on all functions | ✅/❌ | |
| 2 | Docstrings with parameter descriptions | ✅/❌ | |
| 3 | No hardcoded magic numbers | ✅/❌ | |
| 4 | Constants defined at module level | ✅/❌ | |
| 5 | Error handling for edge cases | ✅/❌ | |
| 6 | Logging for key operations | ✅/❌ | |
| 7 | No commented-out code | ✅/❌ | |
| 8 | Consistent naming conventions | ✅/❌ | |

**Code Quality Summary:** [Brief assessment]

---

## Backtest Integrity Checks

| # | Check | Status | Notes |
|---|-------|--------|-------|
| 1 | No look-ahead bias | ✅/❌ | |
| 2 | Point-in-time data handling | ✅/❌ | |
| 3 | Slippage/commission modeled | ✅/❌ | |
| 4 | Universe survivorship bias addressed | ✅/❌ | |
| 5 | Corporate actions handled | ✅/❌ | |
| 6 | T+1 settlement respected | ✅/❌ | |
| 7 | Pre-open session handling | ✅/❌ | |
| 8 | Circuit breaker scenarios | ✅/❌ | |

**Backtest Integrity Summary:** [Brief assessment]

---

## Strategy Logic Checks

| # | Check | Status | Notes |
|---|-------|--------|-------|
| 1 | Entry signals match specification | ✅/❌ | |
| 2 | Exit signals match specification | ✅/❌ | |
| 3 | Position sizing follows risk limits | ✅/❌ | |
| 4 | Stop-loss mechanisms implemented | ✅/❌ | |
| 5 | Take-profit logic (if specified) | ✅/❌/N/A | |
| 6 | Rebalance logic matches spec | ✅/❌ | |
| 7 | Holding period enforced (1-45 days) | ✅/❌ | |
| 8 | Order type appropriate | ✅/❌ | |

**Strategy Logic Summary:** [Brief assessment]

---

## Risk Controls Checks

| # | Check | Status | Notes |
|---|-------|--------|-------|
| 1 | Max drawdown limits enforced | ✅/❌ | |
| 2 | Position concentration limits | ✅/❌ | |
| 3 | Daily loss circuit breakers | ✅/❌ | |
| 4 | Capital allocation boundaries | ✅/❌ | |
| 5 | Max positions per sector | ✅/❌ | |
| 6 | Leverage limits (if applicable) | ✅/❌/N/A | |
| 7 | Overnight exposure limits | ✅/❌ | |

**Risk Controls Summary:** [Brief assessment]

---

## Test Coverage Checks

| # | Check | Status | Notes |
|---|-------|--------|-------|
| 1 | Unit tests for core functions | ✅/❌ | |
| 2 | Integration test for full pipeline | ✅/❌ | |
| 3 | Edge case tests present | ✅/❌ | |
| 4 | Gap handling tested | ✅/❌ | |
| 5 | Corporate action tests | ✅/❌ | |
| 6 | Circuit breaker scenarios tested | ✅/❌ | |
| 7 | Test coverage > 80% | ✅/❌ | Actual: X% |

**Test Coverage Summary:** [Brief assessment]

---

## Issues Found

### Critical Issues

| # | Location | Description | Impact |
|---|----------|-------------|--------|
| 1 | [file:line] | [Description] | [Impact] |

### High Priority Issues

| # | Location | Description | Impact |
|---|----------|-------------|--------|
| 1 | [file:line] | [Description] | [Impact] |

### Medium Priority Issues

| # | Location | Description | Impact |
|---|----------|-------------|--------|
| 1 | [file:line] | [Description] | [Impact] |

### Low Priority Issues

| # | Location | Description | Suggestion |
|---|----------|-------------|------------|
| 1 | [file:line] | [Description] | [Suggestion] |

---

## Issue Summary

| Severity | Count | Must Fix |
|----------|-------|----------|
| Critical | X | Yes |
| High | X | Yes |
| Medium | X | Recommended |
| Low | X | Optional |

---

## Recommendations

### Required Before Deployment

1. [Specific action item]
2. [Specific action item]

### Suggested Improvements

1. [Improvement suggestion]
2. [Improvement suggestion]

---

## Decision

**Recommendation:** [GO / CONDITIONAL GO / NO-GO]

**Rationale:**
[Explanation of decision based on findings]

**Conditions (if CONDITIONAL GO):**
1. [Condition that must be met]
2. [Condition that must be met]

**Next Steps:**
1. [Action item for implementer]
2. [Action item for reviewer]
3. [Timeline/milestone reference]

---

## Appendix

### Files Reviewed

| File | Lines | Coverage |
|------|-------|----------|
| [path/file.py] | X | Y% |

### Test Results

```
[Paste test output summary]
```

### Metric Verification

| Metric | Specification | Implementation | Match |
|--------|---------------|----------------|-------|
| [Metric] | [Spec value] | [Impl value] | ✅/❌ |

---

**Review completed by:** [Agent Name]
**Review task:** [Issue identifier with link]
