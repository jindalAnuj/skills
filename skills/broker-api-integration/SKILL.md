---
name: broker-api-integration
description: >
  Standardize integration of Indian broker APIs (Zerodha KiteConnect, Upstox, 5paisa, AngelOne)
  for market data fetching and paper trading execution. Provides templates and patterns for
  authentication, API clients, data loading, and broker adapters.
---

# Broker API Integration Skill

Use this skill when integrating a new Indian broker API into the quant framework.

## Trigger Conditions

Use this skill when:
- Adding a new broker API integration (Zerodha, 5paisa, AngelOne, or any new broker)
- Implementing OAuth2 authentication for Indian broker APIs
- Building market data loaders that need rate limiting and caching
- Creating paper trading adapters that simulate broker execution
- Debugging authentication or API errors with broker endpoints

## Prerequisites

Before starting, ensure you have:
1. Broker API credentials (API key, secret, redirect URI)
2. Access to broker's API documentation
3. Understanding of the broker's OAuth2 flow
4. Test symbols for validation (e.g., RELIANCE, INFY, TCS)

## 4-Phase Workflow

### Phase 1: Authentication Setup

**Goal:** Implement OAuth2 authentication following the established pattern.

**Steps:**
1. Create `{broker}_auth.py` using `templates/auth_template.py`
2. Configure environment variables:
   - `{BROKER}_API_KEY`
   - `{BROKER}_API_SECRET`
   - `{BROKER}_REDIRECT_URI`
   - `{BROKER}_ACCESS_TOKEN` (optional, for pre-authenticated tokens)
3. Implement authorization URL generation
4. Implement code-to-token exchange
5. Handle token expiry (typically 24h for Indian brokers)

**Key Patterns:**
```python
class BrokerAuthError(Exception):
    """Custom exception for auth failures."""
    pass

class BrokerAuth:
    def __init__(self, api_key=None, api_secret=None, ...):
        self.api_key = api_key or os.environ.get("{BROKER}_API_KEY", "")
        # Support both env vars and explicit params
    
    @property
    def has_valid_token(self) -> bool:
        # Check token exists and not expired
    
    def get_authorization_url(self, state: str) -> str:
        # Generate OAuth2 authorization URL
    
    def exchange_code_for_token(self, code: str) -> str:
        # Exchange auth code for access token
    
    def get_headers(self) -> dict[str, str]:
        # Return headers with Bearer token
```

**Validation:**
- Test authorization URL generation
- Test token exchange with valid code
- Verify headers are correctly formatted

### Phase 2: API Client Implementation

**Goal:** Create a robust HTTP client with retry logic and error handling.

**Steps:**
1. Implement `_make_request()` method with retry logic
2. Handle rate limits (HTTP 429) with exponential backoff
3. Handle auth errors (HTTP 401) by raising custom exception
4. Set appropriate timeouts (30s recommended)
5. Add logging for debugging

**Key Patterns:**
```python
def _make_request(self, method: str, endpoint: str, params=None, data=None) -> dict:
    for attempt in range(self.max_retries):
        try:
            response = requests.request(method, url, headers=self.auth.get_headers(), ...)
            
            if response.status_code == 429:  # Rate limited
                wait_time = self.retry_delay * (2 ** attempt)
                time.sleep(wait_time)
                continue
            
            if response.status_code == 401:  # Auth error
                raise BrokerAuthError("Token expired or invalid")
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException:
            if attempt < self.max_retries - 1:
                time.sleep(self.retry_delay * (attempt + 1))
                continue
            raise
```

**Validation:**
- Test successful request handling
- Test retry behavior on transient errors
- Verify rate limit handling

### Phase 3: Data Loading

**Goal:** Implement `MarketDataLoader` interface for OHLCV and live quotes.

**Steps:**
1. Create `{broker}_loader.py` using `templates/loader_template.py`
2. Implement live quote fetching with caching (5s TTL)
3. Implement historical OHLCV data loading
4. Add batch quote support (if API supports it)
5. Handle Indian market hours (9:15 AM - 3:30 PM IST)
6. Normalize data to standard pandas DataFrame format

**Key Patterns:**
```python
class BrokerLoader(MarketDataLoader):
    def __init__(self, auth=None, cache_enabled=True, max_retries=3):
        self.auth = auth or BrokerAuth()
        self._cache: dict[str, pd.DataFrame] = {}
        self._quote_cache: dict[str, tuple[datetime, dict]] = {}
    
    def get_live_quote(self, symbol: str, exchange: Exchange) -> dict:
        # Check cache first (5s TTL)
        # Make API request
        # Cache and return result
    
    def load_ohlcv(self, symbol: str, exchange: Exchange, 
                   start_date: date, end_date: date) -> pd.DataFrame:
        # Return DataFrame with columns: date, open, high, low, close, volume
        # Indexed by date, sorted ascending
```

**DataFrame Format:**
- Index: `date` (datetime.date)
- Columns: `open`, `high`, `low`, `close` (float), `volume` (int)
- Sorted by date ascending

**Validation:**
- Test quote fetching returns expected fields
- Test historical data returns correct DataFrame format
- Verify caching behavior

### Phase 4: Broker Adapter (Paper Trading)

**Goal:** Extend `BrokerAdapter` for paper trading simulation.

**Steps:**
1. Create `{broker}_adapter.py` using `templates/adapter_template.py`
2. Extend `BrokerAdapter` abstract base class
3. Implement paper trading mode (NEVER execute real trades)
4. Handle NSE/BSE exchanges and product types (CNC, MIS, NRML)
5. Track orders and positions locally
6. Simulate slippage and fills

**Key Patterns:**
```python
class BrokerPaperAdapter(BrokerAdapter):
    def __init__(self, auth=None, loader=None, slippage_pct=0.001):
        self.auth = auth or BrokerAuth()
        self.loader = loader or BrokerLoader(auth=self.auth)
        self._orders: dict[str, Order] = {}
        self._positions: dict[str, Position] = {}
    
    def place_order(self, order: Order) -> str:
        # PAPER MODE: Simulate order, never execute real trade
        # Get live quote for realistic fill price
        # Apply slippage
        # Update positions
    
    def get_positions(self) -> list[Position]:
        return list(self._positions.values())
```

**Critical Safety Rule:**
```python
# ALWAYS include this check
if not self._paper_mode:
    raise RuntimeError("PAPER MODE ONLY - Real trading disabled")
```

**Validation:**
- Test order placement returns valid order ID
- Test position tracking after fills
- Verify no real API calls for order execution

## Expected Outputs

After completing all phases, you should have:

```
src/quant_framework/
├── data/
│   └── {broker}_loader.py      # MarketDataLoader implementation
└── broker/
    ├── {broker}_auth.py        # OAuth2 authentication
    └── {broker}_adapter.py     # BrokerAdapter implementation (paper mode)
```

Plus test file:
```
tests/
└── test_{broker}_integration.py  # Tests with mock API responses
```

## Integration with Framework

Register your new loader and adapter:

```python
from quant_framework.data.loaders import DataLoaderRegistry
from quant_framework.broker.{broker}_loader import BrokerLoader
from quant_framework.broker.{broker}_adapter import BrokerPaperAdapter

# Data loading
registry = DataLoaderRegistry()
registry.register_market_loader("{broker}", BrokerLoader())

# Paper trading
adapter = BrokerPaperAdapter()
adapter.connect({})  # Paper mode - no real credentials needed
```

## Reference Material

See `reference.md` for:
- API documentation links for each broker
- Environment variable reference
- Rate limits and quotas
- Common error codes

See `templates/` for:
- `auth_template.py` - OAuth2 authentication boilerplate
- `loader_template.py` - MarketDataLoader implementation template
- `adapter_template.py` - BrokerAdapter implementation template

## Existing Implementations

Reference these for patterns:
- `src/quant_framework/data/upstox_loader.py` - Complete Upstox loader
- `src/quant_framework/broker/base.py` - Abstract broker interface
- `src/quant_framework/broker/paper.py` - Paper trading reference

## Troubleshooting

**Token Expired (401)**
- Indian broker tokens expire daily (typically at EOD)
- Re-authenticate via OAuth2 flow or update `{BROKER}_ACCESS_TOKEN`

**Rate Limited (429)**
- Exponential backoff is implemented in templates
- Reduce request frequency if persistent
- Check broker-specific rate limits in `reference.md`

**Market Closed**
- Live quotes unavailable outside 9:15 AM - 3:30 PM IST
- Use `is_market_open()` helper before fetching live data
- Historical data available anytime

**Invalid Instrument Key**
- Each broker has different symbol formats
- Check `_get_instrument_key()` mapping for your broker
