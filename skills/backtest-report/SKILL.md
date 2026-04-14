---
name: backtest-report
description: Generate standardized backtesting analysis reports for Indian equity trading strategies (NSE/BSE). Use when backtest results are available, comparing strategy variants, preparing performance reports for review, validating before deployment, or conducting post-mortem analysis.
---

# Backtest Report Skill

Generate consistent, comprehensive backtesting analysis reports for trading strategies targeting Indian equity markets.

## When to Use

- Backtest results need formal documentation
- Comparing multiple strategy variants or parameter sets
- Preparing strategy performance for manager/board review
- Validating strategy before live deployment
- Post-mortem analysis on strategy performance

## Workflow

### Step 1: Input Validation

Verify before generating report:

```
Input Validation Checklist:
- [ ] Backtest data source confirmed (broker API / historical provider)
- [ ] Date range covers 3+ years (sufficient market cycles)
- [ ] Stock universe checked for survivorship bias
- [ ] Corporate actions handled (splits, bonuses, dividends)
```

**Required inputs:**
- Trade log with entry/exit timestamps, prices, quantities
- Benchmark data (Nifty 50 or relevant sector index)
- Risk-free rate (current RBI T-bill rate, typically 6-7%)

### Step 2: Calculate Core Metrics

Calculate and populate these metrics (see [reference.md](reference.md) for formulas):

| Metric | Description | Threshold |
|--------|-------------|-----------|
| Total Return | Cumulative P&L | - |
| CAGR | Annualized return | > 15% (beat FD) |
| Sharpe Ratio | Risk-adjusted return | > 1.5 |
| Sortino Ratio | Downside risk-adjusted | > 2.0 |
| Max Drawdown | Largest peak-to-trough | < 20% |
| Win Rate | % profitable trades | > 50% |
| Profit Factor | Gross profit / Gross loss | > 1.5 |
| Avg Holding Period | Mean days per trade | 1-45 days |

### Step 3: Risk Analysis

Calculate risk metrics:

| Metric | Confidence Level |
|--------|-----------------|
| Value at Risk (VaR) | 95% and 99% |
| Expected Shortfall (CVaR) | 95% |
| Beta vs Nifty 50 | - |
| Daily Volatility | Annualized |
| Benchmark Correlation | - |

### Step 4: Indian Market-Specific Analysis

**Must include:**

1. **Budget Session Performance** (February)
   - Returns during Union Budget week
   - Volatility spike handling

2. **Expiry Behavior**
   - Monthly expiry (last Thursday) performance
   - Weekly expiry impact (if F&O strategies)

3. **Circuit Breaker Analysis**
   - Trades affected by 5%/10%/20% limits
   - Position stuck scenarios

4. **Cost Impact**
   - STT: 0.1% on delivery sell, 0.025% on intraday
   - Brokerage: 0.03% or ₹20 (Zerodha model)
   - GST: 18% on brokerage
   - Stamp duty: 0.015% (varies by state)

5. **Settlement Considerations**
   - T+1 settlement impact
   - Pre-open session (9:00-9:15) handling

### Step 5: Statistical Robustness

Include at least:

- t-statistic for Sharpe ratio (> 2.0 for significance)
- Bootstrap confidence intervals (95% CI)
- Out-of-sample vs in-sample comparison
- Parameter sensitivity (±10% change impact)

### Step 6: Generate Report

Use the template below to generate the final report.

## Report Template

```markdown
# Backtest Report: [Strategy Name]

**Generated:** [Date]
**Period:** [Start Date] to [End Date]
**Benchmark:** [Nifty 50 / Sector Index]

## Executive Summary

[1 paragraph: Strategy type, key finding, recommendation]

## Risk Flag Summary

| Category | Status | Notes |
|----------|--------|-------|
| Returns | 🟢/🟡/🔴 | [Brief note] |
| Drawdown | 🟢/🟡/🔴 | [Brief note] |
| Consistency | 🟢/🟡/🔴 | [Brief note] |
| Statistical Validity | 🟢/🟡/🔴 | [Brief note] |

**Overall:** [APPROVED / CONDITIONAL / NEEDS WORK]

## Performance Metrics

| Metric | Value | Benchmark | Status |
|--------|-------|-----------|--------|
| Total Return | X% | Y% | 🟢/🟡/🔴 |
| CAGR | X% | Y% | 🟢/🟡/🔴 |
| Sharpe Ratio | X | Y | 🟢/🟡/🔴 |
| Sortino Ratio | X | - | 🟢/🟡/🔴 |
| Max Drawdown | X% | Y% | 🟢/🟡/🔴 |
| Win Rate | X% | - | 🟢/🟡/🔴 |
| Profit Factor | X | - | 🟢/🟡/🔴 |
| Avg Holding | X days | - | 🟢/🟡/🔴 |

## Risk Metrics

| Metric | Value |
|--------|-------|
| VaR (95%) | X% |
| VaR (99%) | X% |
| CVaR (95%) | X% |
| Beta | X |
| Correlation | X |
| Annualized Vol | X% |

## Indian Market Analysis

### Expiry Week Performance
[Table of monthly expiry week returns]

### Budget Session Impact
[Returns during Feb budget period]

### Transaction Costs
| Component | Annual Impact |
|-----------|---------------|
| STT | ₹X (Y%) |
| Brokerage | ₹X (Y%) |
| GST | ₹X (Y%) |
| Slippage | ₹X (Y%) |
| **Total** | ₹X (Y%) |

## Statistical Validity

| Test | Result | Threshold | Pass |
|------|--------|-----------|------|
| Sharpe t-stat | X | > 2.0 | ✅/❌ |
| OOS Sharpe Decay | X% | < 30% | ✅/❌ |
| Parameter Stability | X% | < 20% | ✅/❌ |

## Monthly Returns Heatmap

[Year x Month matrix of returns]

## Equity Curve

[Describe or embed equity curve chart]

## Drawdown Analysis

| Drawdown | Start | End | Recovery | Days |
|----------|-------|-----|----------|------|
| -X% | Date | Date | Date | N |

## Recommendations

1. [Specific recommendation]
2. [Specific recommendation]
3. [Specific recommendation]

## Appendix: Trade Statistics

- Total trades: N
- Avg trade P&L: ₹X
- Largest winner: ₹X (Y%)
- Largest loser: ₹X (Y%)
- Longest winning streak: N
- Longest losing streak: N
```

## JSON Output Format

Also output structured data for DataEngineer integration:

```json
{
  "meta": {
    "strategyName": "string",
    "generatedAt": "ISO8601",
    "periodStart": "YYYY-MM-DD",
    "periodEnd": "YYYY-MM-DD",
    "benchmark": "string"
  },
  "riskFlags": {
    "overall": "APPROVED|CONDITIONAL|NEEDS_WORK",
    "returns": "GREEN|YELLOW|RED",
    "drawdown": "GREEN|YELLOW|RED",
    "consistency": "GREEN|YELLOW|RED",
    "statisticalValidity": "GREEN|YELLOW|RED"
  },
  "performance": {
    "totalReturn": 0.0,
    "cagr": 0.0,
    "sharpeRatio": 0.0,
    "sortinoRatio": 0.0,
    "maxDrawdown": 0.0,
    "winRate": 0.0,
    "profitFactor": 0.0,
    "avgHoldingDays": 0
  },
  "risk": {
    "var95": 0.0,
    "var99": 0.0,
    "cvar95": 0.0,
    "beta": 0.0,
    "correlation": 0.0,
    "annualizedVol": 0.0
  },
  "indianMarket": {
    "sttImpact": 0.0,
    "brokerageImpact": 0.0,
    "totalCostImpact": 0.0,
    "expiryWeekReturn": 0.0,
    "budgetPeriodReturn": 0.0
  },
  "statistics": {
    "sharpeTStat": 0.0,
    "oosSharpDecay": 0.0,
    "parameterStability": 0.0
  },
  "trades": {
    "total": 0,
    "avgPnl": 0.0,
    "largestWinner": 0.0,
    "largestLoser": 0.0
  }
}
```

## Risk Flag Thresholds

| Flag | GREEN | YELLOW | RED |
|------|-------|--------|-----|
| Returns | CAGR > 20% | CAGR 10-20% | CAGR < 10% |
| Drawdown | < 15% | 15-25% | > 25% |
| Consistency | Win rate > 55% | 45-55% | < 45% |
| Statistical | t-stat > 2.5 | 2.0-2.5 | < 2.0 |

## Additional Resources

- For detailed metric formulas and calculations, see [reference.md](reference.md)
