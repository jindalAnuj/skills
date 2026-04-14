# Broker API Integration Reference

Quick reference for API documentation, environment variables, and broker-specific details.

## Broker API Documentation

### Upstox (Implemented)
- **Docs:** https://upstox.com/developer/api-documentation/
- **Base URL:** `https://api.upstox.com`
- **Auth:** OAuth2 with daily token refresh
- **Rate Limits:** 25 requests/second, 250,000 requests/day
- **Instrument Format:** `{EXCHANGE}_EQ|{SYMBOL}` (e.g., `NSE_EQ|RELIANCE`)

### Zerodha KiteConnect
- **Docs:** https://kite.trade/docs/connect/v3/
- **Base URL:** `https://api.kite.trade`
- **Auth:** OAuth2 with session token (daily refresh)
- **Rate Limits:** 3 requests/second per user
- **Instrument Format:** `{EXCHANGE}:{SYMBOL}` (e.g., `NSE:RELIANCE`)
- **SDK:** `pip install kiteconnect`

### Upstox v2
- **Docs:** https://upstox.com/developer/api-documentation/
- **Base URL:** `https://api.upstox.com/v2`
- **Auth:** OAuth2
- **Rate Limits:** 25 req/s, 250k/day
- **SDK:** `pip install upstox-python-sdk`

### 5paisa
- **Docs:** https://www.5paisa.com/developerapi/overview
- **Base URL:** `https://openapi.5paisa.com`
- **Auth:** OAuth2 + TOTP for 2FA
- **Rate Limits:** 10 requests/second
- **Instrument Format:** Exchange code + ScripCode
- **SDK:** `pip install py5paisa`

### AngelOne SmartAPI
- **Docs:** https://smartapi.angelbroking.com/docs
- **Base URL:** `https://apiconnect.angelbroking.com`
- **Auth:** API key + TOTP
- **Rate Limits:** 10 requests/second
- **Instrument Format:** Symbol token based
- **SDK:** `pip install smartapi-python`

### Dhan
- **Docs:** https://dhanhq.co/docs/v2/
- **Base URL:** `https://api.dhan.co`
- **Auth:** Access token
- **Rate Limits:** 25 requests/second
- **SDK:** `pip install dhanhq`

## Environment Variables

### Template
```bash
# Authentication
{BROKER}_API_KEY=your_api_key
{BROKER}_API_SECRET=your_api_secret
{BROKER}_REDIRECT_URI=http://localhost:8000/callback
{BROKER}_ACCESS_TOKEN=pre_authenticated_token  # Optional

# Optional overrides
{BROKER}_BASE_URL=https://api.broker.com  # For sandbox/testing
{BROKER}_TIMEOUT=30  # Request timeout in seconds
```

### Upstox
```bash
UPSTOX_API_KEY=
UPSTOX_API_SECRET=
UPSTOX_REDIRECT_URI=http://localhost:8000/callback
UPSTOX_ACCESS_TOKEN=
```

### Zerodha KiteConnect
```bash
KITE_API_KEY=
KITE_API_SECRET=
KITE_REDIRECT_URI=http://localhost:8000/callback
KITE_ACCESS_TOKEN=
```

### 5paisa
```bash
FIVEPAISA_APP_NAME=
FIVEPAISA_APP_SOURCE=
FIVEPAISA_USER_ID=
FIVEPAISA_PASSWORD=
FIVEPAISA_USER_KEY=
FIVEPAISA_ENCRYPTION_KEY=
FIVEPAISA_ACCESS_TOKEN=
```

### AngelOne SmartAPI
```bash
ANGELONE_API_KEY=
ANGELONE_CLIENT_ID=
ANGELONE_PASSWORD=
ANGELONE_TOTP_SECRET=  # For 2FA
ANGELONE_ACCESS_TOKEN=
```

## Indian Market Hours

```python
from zoneinfo import ZoneInfo

IST = ZoneInfo("Asia/Kolkata")

MARKET_OPEN_HOUR = 9
MARKET_OPEN_MINUTE = 15
MARKET_CLOSE_HOUR = 15
MARKET_CLOSE_MINUTE = 30

# Pre-market: 9:00 AM - 9:15 AM
# Trading: 9:15 AM - 3:30 PM
# Post-market: 3:30 PM - 4:00 PM
```

## Exchange Codes

| Exchange | Upstox | Zerodha | 5paisa | AngelOne |
|----------|--------|---------|--------|----------|
| NSE Equity | `NSE_EQ` | `NSE` | `N` | `NSE` |
| BSE Equity | `BSE_EQ` | `BSE` | `B` | `BSE` |
| NSE F&O | `NSE_FO` | `NFO` | `N` | `NFO` |
| BSE F&O | `BSE_FO` | `BFO` | `B` | `BFO` |
| NSE Currency | `CDS` | `CDS` | `N` | `CDS` |
| MCX Commodity | `MCX_FO` | `MCX` | `M` | `MCX` |

## Product Types

| Type | Description | Use Case |
|------|-------------|----------|
| CNC | Cash and Carry | Delivery trades, no intraday margin |
| MIS | Margin Intraday Square-off | Intraday with leverage, auto-squared at EOD |
| NRML | Normal | F&O overnight positions |

## Common Error Codes

| HTTP Code | Meaning | Action |
|-----------|---------|--------|
| 400 | Bad Request | Check request parameters |
| 401 | Unauthorized | Token expired, re-authenticate |
| 403 | Forbidden | Check API permissions/subscription |
| 404 | Not Found | Invalid endpoint or symbol |
| 429 | Rate Limited | Back off, retry with exponential delay |
| 500 | Server Error | Retry after delay |
| 503 | Service Unavailable | Broker maintenance, retry later |

## Instrument Key Mapping

### Upstox
```python
def get_instrument_key(symbol: str, exchange: str) -> str:
    prefix_map = {
        "NSE": "NSE_EQ",
        "BSE": "BSE_EQ",
        "NFO": "NSE_FO",
        "BFO": "BSE_FO",
    }
    return f"{prefix_map.get(exchange, 'NSE_EQ')}|{symbol}"
```

### Zerodha
```python
def get_instrument_key(symbol: str, exchange: str) -> str:
    return f"{exchange}:{symbol}"
```

### Index Symbols

| Index | Upstox | Zerodha |
|-------|--------|---------|
| Nifty 50 | `NSE_INDEX\|Nifty 50` | `NSE:NIFTY 50` |
| Nifty Bank | `NSE_INDEX\|Nifty Bank` | `NSE:NIFTY BANK` |
| Sensex | `BSE_INDEX\|SENSEX` | `BSE:SENSEX` |

## Testing Symbols

Use these liquid stocks for integration testing:
- `RELIANCE` - Reliance Industries
- `TCS` - Tata Consultancy Services
- `INFY` - Infosys
- `HDFCBANK` - HDFC Bank
- `ICICIBANK` - ICICI Bank

## OAuth2 Flow Summary

```
1. Generate Authorization URL
   GET /login/authorization/dialog
   ?client_id={api_key}
   &redirect_uri={redirect_uri}
   &response_type=code
   &state={state}

2. User authenticates at broker website

3. Broker redirects to redirect_uri with code
   {redirect_uri}?code={authorization_code}&state={state}

4. Exchange code for token
   POST /login/authorization/token
   {code, client_id, client_secret, redirect_uri, grant_type=authorization_code}

5. Use token in requests
   Authorization: Bearer {access_token}
```

## Rate Limit Handling

```python
import time

def exponential_backoff(attempt: int, base_delay: float = 1.0) -> float:
    """Calculate delay with exponential backoff."""
    return base_delay * (2 ** attempt)

def handle_rate_limit(response, attempt: int) -> bool:
    """Returns True if should retry."""
    if response.status_code == 429:
        retry_after = response.headers.get("Retry-After")
        wait_time = int(retry_after) if retry_after else exponential_backoff(attempt)
        time.sleep(wait_time)
        return True
    return False
```
