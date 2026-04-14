# Strategy Validation Reference

Detailed checklists and expanded criteria for each validation step.

## Step 1: Data Integrity - Expanded Checklist

### Source Verification
- [ ] Data provider is documented (NSE, BSE, vendor name)
- [ ] Data license permits intended use
- [ ] Historical depth matches strategy requirements
- [ ] Real-time vs EOD distinction is clear

### Quality Checks
- [ ] Count missing values per column
- [ ] Identify and document handling method (forward-fill, interpolate, exclude)
- [ ] Verify OHLCV consistency (High >= Low, Open/Close within High-Low)
- [ ] Check for duplicate timestamps
- [ ] Validate volume is non-negative

### Corporate Actions (Indian Markets)
- [ ] Stock splits adjusted (e.g., 1:5 splits common in India)
- [ ] Bonus issues adjusted
- [ ] Rights issues handled
- [ ] Dividend adjustments (if using adjusted close)
- [ ] Demergers and mergers handled
- [ ] Name changes mapped correctly

### Look-Ahead Bias Checks
- [ ] Features use only past data relative to signal date
- [ ] No future earnings/announcements in features
- [ ] Index composition uses point-in-time membership
- [ ] Survivorship bias addressed (include delisted stocks)

### Indian Market Data Sources

| Source | Type | Notes |
|--------|------|-------|
| NSE India | Official | Bhavcopy, indices |
| BSE India | Official | EOD data |
| Yahoo Finance | Free | Adjusted data, gaps possible |
| Google Finance | Free | Limited historical depth |
| Quandl/Nasdaq | Paid | Corporate actions included |
| Tickertape/Screener | Paid | Fundamentals included |
| Broker APIs | Free with account | Real-time, limited history |

---

## Step 2: Backtest Configuration - Expanded Checklist

### Data Split Protocol
- [ ] Total data >= 5 years (for daily strategies)
- [ ] Train set: 60% minimum
- [ ] Validation set: 20% for hyperparameter tuning
- [ ] Out-of-sample: 20% minimum, never touched until final test
- [ ] No information leakage between splits

### Transaction Cost Modeling

**Zerodha (Market Leader)**
| Trade Type | Brokerage | STT | Total (approx) |
|------------|-----------|-----|----------------|
| Equity Delivery Buy | 0 | 0.1% | 0.16% |
| Equity Delivery Sell | 0 | 0.1% | 0.16% |
| Equity Intraday | ₹20/order or 0.03% | 0.025% (sell) | 0.05-0.08% |
| F&O Futures | ₹20/order | 0.0125% (sell) | 0.02-0.05% |
| F&O Options | ₹20/order | 0.0625% (sell) | 0.03-0.10% |

**Other Brokers Comparison**
| Broker | Delivery | Intraday | Notes |
|--------|----------|----------|-------|
| Upstox | ₹20/order | ₹20/order | Similar to Zerodha |
| 5paisa | ₹20/order | ₹20/order | Power Investor plan |
| Angel One | ₹20/order | ₹20/order | Additional research tools |
| ICICI Direct | 0.55% | 0.05% | Full-service, higher cost |
| HDFC Securities | 0.50% | 0.05% | Full-service |

### Slippage Model

```python
def estimate_slippage(order_value, avg_daily_volume, market_cap_category):
    """
    Estimate slippage based on order size and liquidity.
    
    Args:
        order_value: Order size in INR
        avg_daily_volume: 20-day ADV in INR
        market_cap_category: 'large', 'mid', 'small'
    
    Returns:
        Estimated slippage as decimal (e.g., 0.001 for 0.1%)
    """
    participation_rate = order_value / avg_daily_volume
    
    base_slippage = {
        'large': 0.0005,   # 0.05% base for Nifty 50
        'mid': 0.001,      # 0.10% base for mid caps
        'small': 0.002     # 0.20% base for small caps
    }
    
    # Impact increases with participation
    impact_multiplier = 1 + (participation_rate * 10)
    
    return base_slippage[market_cap_category] * impact_multiplier
```

### Position Sizing Constraints
- [ ] Max single position: 10% of portfolio
- [ ] Max sector concentration: 30%
- [ ] Max correlated positions: 40%
- [ ] Cash buffer: 5-10% for rebalancing

---

## Step 3: Statistical Validity - Expanded Checklist

### Core Metrics Calculation

```python
import numpy as np

def sharpe_ratio(returns, risk_free_rate=0.06, periods_per_year=252):
    """
    Calculate annualized Sharpe ratio.
    Indian risk-free rate: ~6% (10-year G-Sec yield)
    """
    excess_returns = returns - risk_free_rate / periods_per_year
    return np.sqrt(periods_per_year) * excess_returns.mean() / excess_returns.std()

def sortino_ratio(returns, risk_free_rate=0.06, periods_per_year=252):
    """
    Sortino ratio uses only downside deviation.
    """
    excess_returns = returns - risk_free_rate / periods_per_year
    downside_returns = excess_returns[excess_returns < 0]
    downside_std = np.sqrt((downside_returns ** 2).mean())
    return np.sqrt(periods_per_year) * excess_returns.mean() / downside_std

def max_drawdown(cumulative_returns):
    """
    Calculate maximum drawdown from cumulative returns series.
    """
    running_max = cumulative_returns.cummax()
    drawdown = (cumulative_returns - running_max) / running_max
    return drawdown.min()

def calmar_ratio(returns, periods_per_year=252):
    """
    Calmar = Annualized return / Max drawdown
    """
    cumulative = (1 + returns).cumprod()
    ann_return = cumulative.iloc[-1] ** (periods_per_year / len(returns)) - 1
    mdd = abs(max_drawdown(cumulative))
    return ann_return / mdd if mdd > 0 else np.inf
```

### Monte Carlo Protocol

1. **Bootstrap Method:**
   - Resample daily returns with replacement
   - Generate 1000+ equity curves
   - Calculate metrics distribution

2. **Report:**
   - Median final wealth
   - 5th and 95th percentile outcomes
   - Probability of >20% drawdown
   - Probability of negative total return

### Regime Classification (Indian Market)

| Regime | Nifty 50 Return | Historical Frequency |
|--------|-----------------|---------------------|
| Strong Bull | >25% annual | ~15% of years |
| Bull | 10-25% annual | ~35% of years |
| Sideways | -10% to +10% | ~25% of years |
| Bear | -10% to -25% | ~15% of years |
| Crash | <-25% annual | ~10% of years |

---

## Step 4: Overfitting Detection - Expanded Checklist

### Degrees of Freedom Rule

```
Maximum safe parameters = sqrt(number of data points)

Example:
- 5 years daily data = ~1250 points
- Max parameters = sqrt(1250) ≈ 35

If strategy has >35 parameters, risk of overfitting is HIGH
```

### Walk-Forward Protocol (Detailed)

```python
def walk_forward_validation(data, strategy, n_splits=5, train_ratio=0.8):
    """
    Implement anchored walk-forward validation.
    
    Returns IS and OOS performance for each fold.
    """
    results = []
    fold_size = len(data) // n_splits
    
    for i in range(n_splits - 1):
        # Expanding window: train on all data up to fold i
        train_end = (i + 1) * fold_size
        train_data = data[:int(train_end * train_ratio)]
        test_data = data[int(train_end * train_ratio):train_end]
        
        # Train strategy
        strategy.fit(train_data)
        
        # Evaluate
        is_sharpe = strategy.evaluate(train_data)
        oos_sharpe = strategy.evaluate(test_data)
        
        results.append({
            'fold': i,
            'is_sharpe': is_sharpe,
            'oos_sharpe': oos_sharpe,
            'ratio': oos_sharpe / is_sharpe if is_sharpe > 0 else 0
        })
    
    return results
```

### Overfitting Red Flags Checklist
- [ ] No strategy component depends on specific dates
- [ ] No hardcoded price levels or thresholds from backtest
- [ ] Parameters are rounded/simplified, not precise decimals
- [ ] Strategy logic is explainable in plain terms
- [ ] Similar strategies exist in academic literature
- [ ] Performance doesn't collapse with small parameter changes

---

## Step 5: Market Microstructure - Expanded Checklist

### Liquidity Assessment

```python
def check_liquidity(symbol, position_value, lookback_days=20):
    """
    Verify sufficient liquidity for position size.
    
    Returns:
        dict with liquidity metrics and pass/fail
    """
    avg_volume = get_avg_volume(symbol, lookback_days)
    avg_value = get_avg_value_traded(symbol, lookback_days)
    
    participation = position_value / avg_value
    
    return {
        'avg_daily_volume': avg_volume,
        'avg_daily_value': avg_value,
        'participation_rate': participation,
        'pass': participation < 0.01,  # <1% of daily volume
        'warning': participation < 0.05  # <5% is manageable
    }
```

### Circuit Limit Handling (India-Specific)

| Index/Stock | Circuit Limit | Notes |
|-------------|---------------|-------|
| Nifty 50/Sensex | 10%, 15%, 20% | Market-wide, rare |
| F&O stocks | 10% (dynamic) | Based on volatility |
| Non-F&O stocks | 5%, 10%, 20% | Daily price bands |
| SME/New listings | 5% | Tight initial bands |

**Strategy must handle:**
- [ ] Position sizing accounts for potential locked positions
- [ ] Exit logic has circuit limit contingency
- [ ] No assumptions about executing at limit price

### Order Execution Assumptions

| Order Type | Realistic Fill Rate | Typical Slippage |
|------------|---------------------|------------------|
| Market (Nifty 50) | 100% | 0.02-0.05% |
| Market (Mid cap) | 100% | 0.10-0.30% |
| Limit at best bid/ask | 60-80% | 0% |
| Limit 0.5% away | 95%+ | -0.5% (favorable) |

### Broker API Rate Limits

```python
# Rate limit handling example
BROKER_LIMITS = {
    'zerodha': {'orders_per_minute': 200, 'orders_per_second': 10},
    'upstox': {'orders_per_second': 10},
    'fivepaisa': {'orders_per_minute': 120},
    'angel': {'orders_per_second': 10}
}

def check_execution_feasibility(num_orders, execution_window_seconds, broker):
    """
    Check if order batch is executable within API limits.
    """
    limits = BROKER_LIMITS[broker]
    orders_per_second = limits.get('orders_per_second', 
                                    limits.get('orders_per_minute', 60) / 60)
    
    required_time = num_orders / orders_per_second
    
    return {
        'feasible': required_time <= execution_window_seconds,
        'required_seconds': required_time,
        'available_seconds': execution_window_seconds
    }
```

---

## Step 6: Risk Assessment - Expanded Checklist

### VaR Calculation Methods

```python
def historical_var(returns, confidence=0.95):
    """
    Historical VaR using empirical distribution.
    """
    return np.percentile(returns, (1 - confidence) * 100)

def parametric_var(returns, confidence=0.95):
    """
    Parametric VaR assuming normal distribution.
    """
    from scipy import stats
    mu = returns.mean()
    sigma = returns.std()
    return stats.norm.ppf(1 - confidence, mu, sigma)

def expected_shortfall(returns, confidence=0.95):
    """
    CVaR / Expected Shortfall - average of losses beyond VaR.
    """
    var = historical_var(returns, confidence)
    return returns[returns <= var].mean()
```

### Stress Test Dates (Indian Market)

| Event | Date Range | Impact |
|-------|------------|--------|
| GFC 2008 | Oct 2008 - Mar 2009 | Nifty -60% |
| Eurozone Crisis | Aug 2011 - Dec 2011 | Nifty -25% |
| Taper Tantrum | May 2013 - Aug 2013 | Nifty -15%, INR -20% |
| China Deval | Aug 2015 | Nifty -10% in weeks |
| Demonetization | Nov 2016 | Volatility spike, 3-day impact |
| IL&FS Crisis | Sep 2018 - Oct 2018 | NBFC stocks -40% |
| COVID Crash | Feb 2020 - Mar 2020 | Nifty -40% |
| COVID Recovery | Apr 2020 - Dec 2020 | Nifty +80% |

### Factor Exposure Analysis

```python
def factor_exposure(strategy_returns, factor_returns):
    """
    Regress strategy returns against common factors.
    
    Indian factors to consider:
    - Market (Nifty 50)
    - Size (small vs large)
    - Value (P/B, P/E)
    - Momentum (12-1 month)
    - Quality (ROE, debt)
    """
    import statsmodels.api as sm
    
    X = sm.add_constant(factor_returns)
    model = sm.OLS(strategy_returns, X).fit()
    
    return {
        'alpha': model.params[0],
        'betas': model.params[1:],
        'r_squared': model.rsquared,
        't_stats': model.tvalues
    }
```

### Correlation Thresholds

| Correlation With | Preferred | Acceptable | Concerning |
|------------------|-----------|------------|------------|
| Nifty 50 | <0.3 | <0.5 | >0.7 |
| Existing strategies | <0.5 | <0.7 | >0.85 |
| Momentum factor | <0.5 | <0.7 | >0.8 |

---

## Common Rejection Reasons

1. **Data Issues**
   - Survivorship bias not addressed
   - Look-ahead bias in features
   - Corporate actions not adjusted

2. **Backtest Issues**
   - Zero transaction costs
   - Unrealistic slippage
   - Ignoring T+1 settlement

3. **Statistical Issues**
   - In-sample only testing
   - Too many parameters
   - Cherry-picked time periods

4. **Execution Issues**
   - Positions exceed liquidity
   - Ignoring circuit limits
   - API rate limits not considered

5. **Risk Issues**
   - No stress testing
   - High correlation with market
   - Concentrated sector exposure

---

## Validation Report Template (Extended)

For comprehensive reports, include:

1. **Strategy Overview** (1 page)
   - Logic summary
   - Key parameters
   - Expected holding period

2. **Data Summary** (1 page)
   - Source and period
   - Universe definition
   - Quality metrics

3. **Performance Summary** (2 pages)
   - Key metrics table
   - Equity curve
   - Drawdown chart
   - Monthly returns heatmap

4. **Robustness Analysis** (2 pages)
   - Walk-forward results
   - Parameter sensitivity
   - Regime breakdown

5. **Risk Profile** (1 page)
   - VaR/CVaR
   - Stress test results
   - Factor exposures

6. **Execution Plan** (1 page)
   - Order types
   - Broker selection
   - Monitoring requirements

7. **Recommendations** (1 page)
   - Approval decision
   - Conditions if any
   - Review schedule
