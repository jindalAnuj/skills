# Code Review Quant Reference

Detailed criteria and examples for each code review check. Use this reference when evaluating quantitative trading strategy implementations.

---

## Code Quality Checks

### Type Hints

**Requirement:** All functions must have type hints for parameters and return values.

**Good example:**
```python
def calculate_signal(prices: pd.Series, lookback: int = 20) -> pd.Series:
    """Calculate momentum signal from price series."""
    return prices.pct_change(lookback)
```

**Bad example:**
```python
def calculate_signal(prices, lookback=20):
    return prices.pct_change(lookback)
```

**Why it matters:** Type hints enable static analysis, improve IDE support, and make code self-documenting.

### Docstrings

**Requirement:** All public functions must have docstrings with:
- Brief description
- Parameter descriptions with types
- Return value description
- Raises section (if applicable)

**Good example:**
```python
def calculate_rsi(prices: pd.Series, period: int = 14) -> pd.Series:
    """
    Calculate Relative Strength Index.
    
    Args:
        prices: Close price series indexed by date
        period: Lookback period for RSI calculation
        
    Returns:
        RSI values between 0 and 100
        
    Raises:
        ValueError: If period exceeds price series length
    """
```

### Magic Numbers

**Requirement:** No hardcoded numeric literals in logic. Use named constants.

**Bad example:**
```python
if rsi < 30:
    signal = 1
elif rsi > 70:
    signal = -1
```

**Good example:**
```python
RSI_OVERSOLD = 30
RSI_OVERBOUGHT = 70

if rsi < RSI_OVERSOLD:
    signal = Signal.LONG
elif rsi > RSI_OVERBOUGHT:
    signal = Signal.SHORT
```

### Error Handling

**Required edge cases to handle:**
- Empty dataframes
- Missing data (NaN handling)
- Division by zero
- Date range issues
- Invalid parameters

**Example:**
```python
def safe_divide(numerator: float, denominator: float) -> float:
    if denominator == 0:
        logger.warning("Division by zero, returning 0")
        return 0.0
    return numerator / denominator
```

---

## Backtest Integrity Checks

### Look-Ahead Bias

**Definition:** Using information that would not have been available at the time of the trade decision.

**Common sources:**
1. **Future price in calculation:**
   ```python
   # BAD: Tomorrow's close used today
   df['signal'] = df['close'].shift(-1) > df['close']
   ```

2. **Survivorship bias in universe:**
   ```python
   # BAD: Using current Nifty 50 constituents for 2015 backtest
   universe = get_current_nifty50()
   
   # GOOD: Point-in-time constituents
   universe = get_nifty50_constituents(as_of_date=trade_date)
   ```

3. **Using final adjusted prices:**
   ```python
   # BAD: Backward-adjusted prices
   prices = get_adjusted_prices(symbol)
   
   # GOOD: Forward-adjusted or raw prices with explicit adjustment
   prices = get_pit_prices(symbol, adjustment='forward')
   ```

### Point-in-Time Data

**Requirement:** All data must reflect what was known at the time of the decision.

**Check points:**
- Earnings data: Use report date, not period end date
- Index constituents: Use historical membership
- Corporate actions: Apply at ex-date, not announcement date
- Fundamental data: Lag by reporting delay (typically 30-45 days)

### Slippage and Commission Modeling

**Required transaction cost model:**

```python
TRANSACTION_COSTS = {
    'stt_delivery': 0.001,      # 0.1% on sell
    'stt_intraday': 0.00025,    # 0.025% on sell
    'brokerage': 0.0003,         # 0.03% or ₹20 cap
    'gst': 0.18,                 # 18% on brokerage
    'stamp_duty': 0.00015,       # 0.015% on buy
    'exchange_fees': 0.0000325,  # 0.00325%
    'slippage': 0.001,           # 0.1% default assumption
}

def apply_costs(trade_value: float, is_sell: bool, is_intraday: bool) -> float:
    """Calculate net trade value after costs."""
    # Implementation should apply all relevant costs
```

**Slippage considerations:**
- Higher for low-liquidity stocks
- Higher during market open/close
- Higher during high-volatility events
- Model as percentage of trade value (0.05-0.2%)

### Corporate Actions

**Must handle:**

| Action | Handling |
|--------|----------|
| Stock split | Adjust historical prices and quantities |
| Bonus issue | Adjust like split (e.g., 1:1 bonus = 2:1 split) |
| Dividend | Adjust for ex-date (optional for total return) |
| Rights issue | Complex - may need manual handling |
| Merger/Demerger | Update universe, handle delisting |

**Example check:**
```python
def check_corporate_actions(df: pd.DataFrame) -> List[str]:
    """Flag suspicious price movements that may indicate unhandled corporate actions."""
    issues = []
    daily_returns = df['close'].pct_change()
    
    # Flag returns > 20% (potential split/bonus)
    large_moves = daily_returns.abs() > 0.20
    for date in df[large_moves].index:
        issues.append(f"Large move on {date}: {daily_returns[date]:.1%} - verify corporate action")
    
    return issues
```

---

## Strategy Logic Checks

### Signal Generation

**Verify:**
1. Signal calculated only from available data
2. Signal aligns with specification exactly
3. Signal handling for edge cases (first N bars, gaps)

**Common issues:**
- Off-by-one errors in lookback
- Incorrect handling of NaN in indicator calculation
- Signal generated on close but execution assumes open

### Position Sizing

**Acceptable methods:**
1. Fixed fractional (e.g., 2% of capital per position)
2. Volatility-adjusted (e.g., target 1% daily risk)
3. Equal weight across universe
4. Kelly criterion (capped)

**Required constraints:**
```python
MAX_POSITION_SIZE = 0.10      # 10% max per position
MAX_SECTOR_EXPOSURE = 0.30    # 30% max per sector
MAX_POSITIONS = 20            # Portfolio limit
MIN_POSITION_SIZE = 0.02      # 2% minimum (avoid micro positions)
```

### Stop-Loss Implementation

**Required types:**
1. **Hard stop:** Exit at fixed loss threshold
2. **Trailing stop:** Follow price, exit on reversal
3. **Time stop:** Exit if holding period exceeded

**Verification:**
```python
def verify_stop_loss(trades: pd.DataFrame) -> bool:
    """Verify no trade exceeded max loss threshold."""
    MAX_LOSS_PCT = 0.10  # 10% max loss
    
    for _, trade in trades.iterrows():
        if trade['pnl_pct'] < -MAX_LOSS_PCT:
            logger.error(f"Trade {trade['id']} exceeded max loss: {trade['pnl_pct']:.1%}")
            return False
    return True
```

---

## Risk Controls Checks

### Drawdown Limits

**Implementation pattern:**
```python
class RiskManager:
    MAX_DRAWDOWN = 0.15  # 15% max drawdown
    
    def check_drawdown(self, equity_curve: pd.Series) -> bool:
        peak = equity_curve.expanding().max()
        drawdown = (equity_curve - peak) / peak
        
        if drawdown.min() < -self.MAX_DRAWDOWN:
            self.trigger_risk_off()
            return False
        return True
```

### Daily Loss Circuit Breaker

**Pattern:**
```python
DAILY_LOSS_LIMIT = 0.03  # 3% max daily loss

def check_daily_loss(self, current_pnl: float, portfolio_value: float) -> bool:
    daily_loss_pct = current_pnl / portfolio_value
    
    if daily_loss_pct < -DAILY_LOSS_LIMIT:
        logger.warning(f"Daily loss limit breached: {daily_loss_pct:.1%}")
        self.close_all_positions()
        return False
    return True
```

### Position Concentration

**Verify enforcement of:**
- Single position limit (typically 5-10%)
- Sector concentration (typically 20-30%)
- Correlation-based limits (if applicable)

---

## Test Coverage Checks

### Required Test Categories

1. **Unit tests:**
   - Signal calculation functions
   - Position sizing logic
   - Risk check functions
   - Utility functions

2. **Integration tests:**
   - Full backtest pipeline
   - Data loading and preprocessing
   - Order generation flow

3. **Edge case tests:**
   - Empty universe
   - Single-day backtest
   - All signals same direction
   - Circuit breaker scenarios
   - Corporate action dates

### Test Coverage Threshold

**Minimum:** 80% line coverage for core modules

**Verify with:**
```bash
pytest --cov=src/strategies --cov-report=term-missing
```

### Example Test Cases

```python
class TestMomentumStrategy:
    def test_signal_calculation_basic(self):
        """Signal correctly identifies uptrend."""
        prices = pd.Series([100, 105, 110, 115, 120])
        signal = calculate_momentum_signal(prices, lookback=3)
        assert signal.iloc[-1] == Signal.LONG
    
    def test_signal_handles_nan(self):
        """NaN in prices produces NaN signal, not error."""
        prices = pd.Series([100, np.nan, 110, 115, 120])
        signal = calculate_momentum_signal(prices, lookback=3)
        assert pd.isna(signal.iloc[1])
    
    def test_no_look_ahead(self):
        """Signal at time T uses only data up to T."""
        prices = pd.Series([100, 105, 110, 115, 120], 
                          index=pd.date_range('2024-01-01', periods=5))
        
        # Signal on day 3 should be same whether we have day 4-5 or not
        signal_full = calculate_momentum_signal(prices, lookback=2)
        signal_partial = calculate_momentum_signal(prices.iloc[:4], lookback=2)
        
        assert signal_full.iloc[3] == signal_partial.iloc[3]
```

---

## Indian Market-Specific Checks

### Trading Hours Validation

```python
MARKET_OPEN = dt.time(9, 15)
MARKET_CLOSE = dt.time(15, 30)
PRE_OPEN_START = dt.time(9, 0)
PRE_OPEN_END = dt.time(9, 15)

def validate_trade_time(trade_time: dt.datetime) -> bool:
    """Verify trade occurred during valid market hours."""
    t = trade_time.time()
    return MARKET_OPEN <= t <= MARKET_CLOSE
```

### Circuit Breaker Handling

```python
CIRCUIT_BANDS = {
    'category_a': [0.02, 0.05, 0.10, 0.20],  # Large caps
    'category_b': [0.05, 0.10, 0.20],         # Mid caps
    'category_c': [0.10, 0.20],               # Small caps
}

def check_circuit_risk(price_change: float, stock_category: str) -> str:
    """Assess circuit breaker risk for trade."""
    bands = CIRCUIT_BANDS.get(stock_category, CIRCUIT_BANDS['category_c'])
    
    for band in bands:
        if abs(price_change) >= band:
            return f"WARNING: Price near {band:.0%} circuit band"
    return "OK"
```

### Expiry Week Handling

```python
def is_expiry_week(date: dt.date) -> bool:
    """Check if date falls in monthly F&O expiry week."""
    # Last Thursday of month
    last_day = calendar.monthrange(date.year, date.month)[1]
    last_date = dt.date(date.year, date.month, last_day)
    
    # Find last Thursday
    days_to_thu = (last_date.weekday() - 3) % 7
    expiry_date = last_date - dt.timedelta(days=days_to_thu)
    
    # Expiry week is Mon-Thu of that week
    week_start = expiry_date - dt.timedelta(days=expiry_date.weekday())
    return week_start <= date <= expiry_date

def get_volatility_multiplier(date: dt.date) -> float:
    """Adjust slippage for expiry week volatility."""
    if is_expiry_week(date):
        return 1.5  # 50% higher slippage during expiry
    return 1.0
```

---

## Review Checklist Summary

Use this condensed checklist during reviews:

```
CODE QUALITY
[ ] Type hints present
[ ] Docstrings complete
[ ] No magic numbers
[ ] Error handling adequate
[ ] Logging present

BACKTEST INTEGRITY
[ ] No look-ahead bias
[ ] Point-in-time data
[ ] Transaction costs modeled
[ ] Corporate actions handled
[ ] Settlement rules respected

STRATEGY LOGIC
[ ] Signals match spec
[ ] Position sizing correct
[ ] Stop-loss implemented
[ ] Holding period enforced

RISK CONTROLS
[ ] Drawdown limits
[ ] Concentration limits
[ ] Daily loss limits
[ ] Capital boundaries

TESTING
[ ] Unit tests present
[ ] Integration tests pass
[ ] Edge cases covered
[ ] Coverage > 80%
```
