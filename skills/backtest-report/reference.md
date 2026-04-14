# Backtest Report Reference

Detailed metric definitions, formulas, and Indian market-specific considerations.

## Performance Metrics

### Total Return

```
Total Return = (Final Portfolio Value - Initial Portfolio Value) / Initial Portfolio Value × 100
```

Include realized P&L from closed trades and unrealized P&L from open positions at period end.

### CAGR (Compound Annual Growth Rate)

```
CAGR = ((Final Value / Initial Value)^(1/Years) - 1) × 100
```

Where Years = Number of trading days / 252 (NSE trading days per year)

**Indian context:** Compare against:
- Bank FD rates: ~7%
- Nifty 50 historical CAGR: ~12%
- Target for active strategy: > 15%

### Sharpe Ratio

```
Sharpe = (Rp - Rf) / σp

Where:
- Rp = Portfolio annualized return
- Rf = Risk-free rate (RBI 91-day T-bill rate)
- σp = Portfolio annualized standard deviation
```

**Risk-free rate sources:**
- RBI website: https://www.rbi.org.in/
- Current rate (2024): ~6.5-7%
- Use 91-day or 364-day T-bill rate depending on strategy horizon

**Interpretation:**
| Sharpe | Quality |
|--------|---------|
| < 1.0 | Poor |
| 1.0-1.5 | Acceptable |
| 1.5-2.0 | Good |
| 2.0-3.0 | Very Good |
| > 3.0 | Excellent (verify for overfitting) |

### Sortino Ratio

```
Sortino = (Rp - Rf) / σd

Where:
- σd = Downside deviation (std dev of negative returns only)
```

More appropriate for strategies with asymmetric return distributions.

### Maximum Drawdown

```
Drawdown(t) = (Peak(t) - Value(t)) / Peak(t) × 100
Max Drawdown = max(Drawdown(t)) for all t
```

**Recovery analysis:**
- Recovery time = Days from trough to new peak
- Underwater period = Days below previous peak

**Indian market context:**
| Event | Typical Nifty Drawdown |
|-------|------------------------|
| Normal correction | 5-10% |
| Moderate bear | 15-25% |
| Major crash (2008, 2020) | 40-60% |

### Win Rate

```
Win Rate = Number of Winning Trades / Total Trades × 100
```

**Note:** Win rate alone is insufficient. A 30% win rate can be profitable with high profit factor.

### Profit Factor

```
Profit Factor = Gross Profit / Gross Loss
```

| Profit Factor | Interpretation |
|---------------|----------------|
| < 1.0 | Losing strategy |
| 1.0-1.5 | Marginal |
| 1.5-2.0 | Good |
| > 2.0 | Excellent |

### Average Holding Period

```
Avg Holding = Σ(Exit Date - Entry Date) / Number of Trades
```

**Company mandate:** 1-45 days (short to medium term)
Flag trades exceeding 45 days for review.

---

## Risk Metrics

### Value at Risk (VaR)

**Parametric VaR (assuming normal distribution):**
```
VaR(α) = μ - z(α) × σ

Where:
- μ = Mean daily return
- z(α) = Z-score for confidence level (1.645 for 95%, 2.326 for 99%)
- σ = Daily standard deviation
```

**Historical VaR:**
Sort daily returns, take the αth percentile.

**Express as:**
- Daily VaR (for overnight risk)
- Annualized VaR = Daily VaR × √252

### Expected Shortfall (CVaR)

```
CVaR(α) = E[Loss | Loss > VaR(α)]
```

Average of all losses exceeding VaR. More informative for tail risk.

### Beta

```
Beta = Cov(Rp, Rm) / Var(Rm)

Where:
- Rp = Portfolio returns
- Rm = Market (Nifty 50) returns
```

| Beta | Interpretation |
|------|----------------|
| < 0 | Inverse correlation |
| 0-0.5 | Low market sensitivity |
| 0.5-1.0 | Moderate sensitivity |
| 1.0 | Market-like |
| > 1.0 | Amplified market moves |

### Correlation

```
Correlation = Cov(Rp, Rm) / (σp × σm)
```

Range: -1 to +1. Low correlation indicates diversification benefit.

---

## Statistical Validity

### t-Statistic for Sharpe Ratio

```
t = Sharpe × √(N)

Where N = Number of return observations
```

**Interpretation:**
| t-stat | Significance |
|--------|--------------|
| < 1.96 | Not significant at 95% |
| 1.96-2.58 | Significant at 95% |
| > 2.58 | Significant at 99% |

**Required history for significance:**
- For Sharpe = 1.0, need ~4 years (1000+ daily returns)
- For Sharpe = 2.0, need ~1 year

### Out-of-Sample Degradation

```
OOS Degradation = (In-Sample Sharpe - Out-of-Sample Sharpe) / In-Sample Sharpe × 100
```

**Thresholds:**
- < 20%: Good generalization
- 20-30%: Acceptable
- > 30%: Likely overfitting

**Recommended split:**
- 70% in-sample (training)
- 30% out-of-sample (validation)
- Or use walk-forward with 12-month windows

### Parameter Sensitivity

Test strategy with ±10% parameter changes:

```
Sensitivity = (Max Sharpe - Min Sharpe) / Base Sharpe × 100
```

High sensitivity (> 30%) indicates fragile parameters.

---

## Indian Market Specifics

### Transaction Costs

| Component | Rate | Applied To |
|-----------|------|------------|
| STT (Delivery) | 0.1% | Sell value |
| STT (Intraday) | 0.025% | Sell value |
| STT (F&O) | 0.05% | Premium on sell |
| Brokerage (Zerodha) | 0.03% or ₹20 | Per executed order |
| Brokerage (Traditional) | 0.1-0.5% | Trade value |
| GST | 18% | On brokerage + STT |
| Stamp Duty | 0.015% | Buy value (varies by state) |
| Exchange Fees | 0.00325% | Turnover |
| SEBI Charges | 0.0001% | Turnover |

**Total cost estimation:**
- Delivery trades: ~0.15-0.20% per round trip
- Intraday trades: ~0.05-0.10% per round trip
- F&O trades: ~0.05-0.08% per round trip

### Circuit Breaker Limits

**Index circuits (Nifty/Sensex):**
| Trigger | Duration |
|---------|----------|
| 10% | 45 min halt |
| 15% | 1h45m halt |
| 20% | Trading suspended |

**Stock circuits:**
- 2%, 5%, 10%, 20% bands based on stock category
- Price band reset daily

**Impact on backtesting:**
- Flag trades where entry/exit price hit circuit
- Model potential slippage when limit-up/down

### Settlement Cycle

- **T+1:** Standard settlement for equities (since 2023)
- **T+0:** Same-day settlement (pilot phase)

**Implications:**
- Funds available next day after sell
- Short selling limited to intraday (for non-F&O)

### Trading Hours (IST)

| Session | Time |
|---------|------|
| Pre-open | 9:00-9:08 (order entry) |
| Pre-open match | 9:08-9:15 |
| Normal trading | 9:15-15:30 |
| Closing session | 15:40-16:00 |

**Considerations:**
- Pre-open can have significant gaps
- Last 15 minutes often volatile (unwinding)

### Expiry Dates

| Contract | Expiry |
|----------|--------|
| Monthly F&O | Last Thursday |
| Weekly Nifty/BankNifty | Every Thursday |
| Stock F&O | Last Thursday |

**Expiry week effects:**
- Higher volatility Thu-Thu
- Rollover activity mid-week
- Max pain theory considerations

### Key Market Events

| Event | Typical Impact | When |
|-------|---------------|------|
| Union Budget | High volatility | Feb 1 |
| RBI Policy | Rate-sensitive moves | Bi-monthly |
| GST Council | Sector-specific | Quarterly |
| Elections | Sustained volatility | 5-year cycle |
| FII/DII flows | Daily sentiment | Daily |

---

## SEBI Margin Requirements

### Upfront Margin (since 2020)

- VaR + ELM (Extreme Loss Margin) upfront
- Peak margin reporting

### Margin Categories

| Segment | Margin Type |
|---------|-------------|
| Equity Delivery | 100% (no leverage) |
| Equity Intraday | ~15-20% (broker dependent) |
| F&O | SPAN + Exposure (varies) |

**Impact on backtest:**
- Capital efficiency calculations
- Leveraged return adjustments

---

## Benchmark Data Sources

### Free Sources

- NSE India: https://www.nseindia.com/
- BSE India: https://www.bseindia.com/
- Yahoo Finance: ^NSEI (Nifty), ^BSESN (Sensex)

### Paid Sources

- Bloomberg
- Reuters
- NSE archives (historical)

### Sector Indices

| Index | Sector |
|-------|--------|
| Nifty Bank | Banking |
| Nifty IT | Technology |
| Nifty Pharma | Healthcare |
| Nifty Auto | Automotive |
| Nifty FMCG | Consumer |
| Nifty Metal | Metals |

Use sector-appropriate benchmark for sector strategies.

---

## Risk Flag Decision Matrix

### Returns Flag

```
if cagr >= 20% and sharpe >= 2.0:
    return GREEN
elif cagr >= 10% and sharpe >= 1.5:
    return YELLOW
else:
    return RED
```

### Drawdown Flag

```
if max_drawdown <= 15%:
    return GREEN
elif max_drawdown <= 25%:
    return YELLOW
else:
    return RED
```

### Consistency Flag

```
if win_rate >= 55% and profit_factor >= 1.5:
    return GREEN
elif win_rate >= 45% and profit_factor >= 1.2:
    return YELLOW
else:
    return RED
```

### Statistical Validity Flag

```
if sharpe_tstat >= 2.5 and oos_decay <= 20%:
    return GREEN
elif sharpe_tstat >= 2.0 and oos_decay <= 30%:
    return YELLOW
else:
    return RED
```

### Overall Rating

```
flags = [returns, drawdown, consistency, statistical]
red_count = flags.count(RED)
yellow_count = flags.count(YELLOW)

if red_count >= 2:
    return NEEDS_WORK
elif red_count >= 1 or yellow_count >= 2:
    return CONDITIONAL
else:
    return APPROVED
```
