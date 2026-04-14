---
name: strategy-validation-checklist
description: Validate quantitative trading strategies before deployment using a 6-step checklist. Use when evaluating a new strategy, reviewing backtesting results, conducting peer review, performing strategy health checks, or assessing robustness after market regime changes. Covers Indian market specifics (STT, GST, brokerage).
---

# Strategy Validation Checklist

Rigorous, standardized framework for validating quantitative trading strategies before deployment. Ensures consistent methodological scrutiny to prevent overfitting, identify hidden risks, and verify real-world viability.

## When to Use

- Evaluating a new trading strategy for deployment
- Reviewing backtesting results for statistical validity
- Conducting peer review of another researcher's strategy
- Performing quarterly strategy health checks on live strategies
- Assessing strategy robustness after market regime changes

## Validation Workflow

Copy this checklist to track progress:

```
Strategy Validation Progress:
- [ ] Step 1: Data Integrity Check
- [ ] Step 2: Backtest Configuration Review
- [ ] Step 3: Statistical Validity Assessment
- [ ] Step 4: Overfitting Detection
- [ ] Step 5: Market Microstructure Reality Check
- [ ] Step 6: Risk Assessment
```

---

### Step 1: Data Integrity Check

Verify data quality before any analysis.

| Check | Requirement | Red Flag |
|-------|-------------|----------|
| Data source | Documented, reputable provider | Unknown or unverified source |
| Missing values | <1% missing, documented handling | >5% missing or undocumented |
| Corporate actions | Adjusted for splits, dividends, bonuses | Raw unadjusted prices |
| Data frequency | Matches strategy timeframe | Mismatch (e.g., daily data for intraday) |
| Look-ahead bias | No future information in features | Features using future prices |

**Indian Market Specifics:**
- Verify NSE/BSE data consistency
- Check for T+1 settlement effects in position calculations
- Confirm muhurat trading sessions handled correctly

---

### Step 2: Backtest Configuration Review

Validate realistic simulation assumptions.

| Parameter | Minimum Standard | Indian Market Adjustment |
|-----------|------------------|--------------------------|
| Train/Test/OOS split | 60/20/20 | Same |
| Transaction costs | Explicit modeling | See Indian cost table below |
| Slippage | Modeled for liquidity | +50% for mid/small caps |
| Position sizing | Max 10% per position | Same |
| Rebalance frequency | Matches strategy intent | Consider T+1 settlement |

**Indian Market Transaction Costs:**

| Cost Component | Typical Rate | Notes |
|----------------|--------------|-------|
| Brokerage (delivery) | 0.03-0.50% | Varies by broker (Zerodha, Upstox, 5paisa) |
| Brokerage (intraday) | 0.01-0.03% | Often flat fee (₹20/order) |
| STT (Securities Transaction Tax) | 0.1% (buy+sell) | Delivery; 0.025% sell-side for intraday |
| Exchange charges | 0.00325% | NSE/BSE |
| GST | 18% of (brokerage + exchange) | On service charges |
| SEBI turnover fee | 0.0001% | Negligible but include |
| Stamp duty | 0.015% (buy-side) | State-dependent |

**Total estimated round-trip cost (delivery):** ~0.5-1.2% depending on broker

---

### Step 3: Statistical Validity Assessment

Quantify strategy performance with proper statistics.

**Required Metrics:**

| Metric | Acceptable | Good | Excellent |
|--------|------------|------|-----------|
| Sharpe Ratio (annualized) | >0.5 | >1.0 | >1.5 |
| Sortino Ratio | >0.7 | >1.2 | >2.0 |
| Max Drawdown | <30% | <20% | <15% |
| Win Rate | >40% | >50% | >55% |
| Profit Factor | >1.2 | >1.5 | >2.0 |
| Calmar Ratio | >0.5 | >1.0 | >1.5 |

**Additional Analysis Required:**

1. **Monte Carlo Simulation** (minimum 1000 runs)
   - 95% CI for terminal wealth
   - Drawdown distribution

2. **Parameter Sensitivity** (±20% on each key parameter)
   - Sharpe should not degrade >30%
   - No sign flips in expected return

3. **Regime Analysis**
   - Bull market performance (Nifty +15%+ years)
   - Bear market performance (Nifty -10%+ years)
   - Sideways market performance (Nifty ±10%)

---

### Step 4: Overfitting Detection

**Critical threshold: Out-of-sample Sharpe / In-sample Sharpe > 0.5**

| Test | Pass Condition | Fail Action |
|------|----------------|-------------|
| OOS/IS Sharpe ratio | >0.5 | Reduce parameters or extend OOS |
| Degrees of freedom | Parameters < sqrt(data points) | Simplify model |
| Walk-forward efficiency | >0.6 | Re-examine signal decay |
| Performance decay | <20% drop across time splits | Check for data snooping |

**Walk-Forward Optimization Protocol:**

1. Divide data into 5+ periods
2. Train on period N, test on period N+1
3. Roll forward and repeat
4. Average OOS performance should match or exceed IS estimate

**Warning Signs of Overfitting:**
- Sharpe >3.0 (suspiciously high)
- Perfect win rate in backtests
- Strategy only works on specific date ranges
- Many parameters for simple logic

---

### Step 5: Market Microstructure Reality Check

Verify strategy is executable in real markets.

| Check | Requirement | Indian Market Note |
|-------|-------------|-------------------|
| Liquidity | Avg daily volume > 10x position size | Check both NSE and BSE |
| Impact cost | <0.1% for typical trade | Higher for Nifty Next 50 |
| Order book depth | Sufficient at limit price | Review L2 data if available |
| Circuit limits | Strategy handles 5/10/20% limits | Common in mid/small caps |
| Trading hours | Logic respects 9:15-15:30 IST | Pre-open auction handling |

**Position Size vs Liquidity:**

| Category | Min Avg Daily Volume | Max Position % of ADV |
|----------|---------------------|----------------------|
| Nifty 50 | ₹500 Cr | 1% |
| Nifty Next 50 | ₹100 Cr | 0.5% |
| Mid Cap | ₹20 Cr | 0.25% |
| Small Cap | ₹5 Cr | 0.1% |

**Broker API Considerations:**
- Zerodha Kite: 200 orders/minute limit
- Upstox: 10 orders/second
- 5paisa: Check current limits
- All: Handle API downtime gracefully

---

### Step 6: Risk Assessment

Comprehensive risk profiling before deployment.

**Required Risk Metrics:**

| Metric | Calculation | Threshold |
|--------|-------------|-----------|
| VaR (95% daily) | Historical or parametric | <3% of capital |
| VaR (99% daily) | Historical or parametric | <5% of capital |
| CVaR (95% daily) | Expected shortfall | <4% of capital |
| Max consecutive losses | From backtest | <10 trades |
| Recovery time | From max DD | <180 trading days |

**Stress Test Scenarios (Required):**

| Scenario | Apply to | Expected |
|----------|----------|----------|
| 2008 GFC | Full period | Document DD and recovery |
| COVID crash (Mar 2020) | 20-day window | Max 1-day loss |
| Demonetization (Nov 2016) | 30-day window | Volatility spike handling |
| Budget day moves | Historical budget days | Gap handling |

**Correlation Analysis:**
- Correlation with Nifty 50: Document (ideally <0.5)
- Correlation with existing strategies: <0.7 preferred
- Factor exposure: Document momentum, value, size tilts

---

## Output Format

Generate a **Strategy Validation Report** with this structure:

```markdown
# Strategy Validation Report

**Strategy Name:** [Name]
**Validation Date:** [Date]
**Validator:** [Agent/Researcher]

## Executive Summary

| Overall Assessment | [APPROVED / CONDITIONAL / REJECTED] |
|-------------------|--------------------------------------|
| Data Integrity | ✅ Pass / ⚠️ Warning / ❌ Fail |
| Backtest Config | ✅ Pass / ⚠️ Warning / ❌ Fail |
| Statistical Validity | ✅ Pass / ⚠️ Warning / ❌ Fail |
| Overfitting Check | ✅ Pass / ⚠️ Warning / ❌ Fail |
| Microstructure | ✅ Pass / ⚠️ Warning / ❌ Fail |
| Risk Assessment | ✅ Pass / ⚠️ Warning / ❌ Fail |

## Key Metrics

| Metric | Value | Status |
|--------|-------|--------|
| Sharpe (OOS) | [X.XX] | [Status] |
| Max Drawdown | [X.X%] | [Status] |
| OOS/IS Ratio | [X.XX] | [Status] |
| VaR 95% | [X.X%] | [Status] |

## Detailed Findings

[Step-by-step findings with specific issues or confirmations]

## Recommendations

1. [Specific actionable item]
2. [Specific actionable item]

## Risk Flags

- 🔴 **Critical:** [Must address before deployment]
- 🟡 **Moderate:** [Address within 30 days]
- 🟢 **Minor:** [Nice to have]
```

---

## Approval Criteria

| Decision | Criteria |
|----------|----------|
| **APPROVED** | All steps pass, no critical flags |
| **CONDITIONAL** | Minor issues, approved with monitoring plan |
| **REJECTED** | Any critical failure, requires rework |

**Automatic Rejection Triggers:**
- OOS/IS Sharpe ratio < 0.3
- Max drawdown > 40%
- Insufficient liquidity for position sizes
- Unaddressed look-ahead bias
- Transaction costs not modeled

---

## Additional Resources

For detailed checklists with expanded criteria, see [reference.md](reference.md).
