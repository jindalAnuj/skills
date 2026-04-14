"""
{BROKER} OAuth2 Authentication Handler

Template for implementing broker authentication.
Replace {BROKER} and {Broker} with actual broker name.

Environment Variables Required:
- {BROKER}_API_KEY: Your API key
- {BROKER}_API_SECRET: Your API secret
- {BROKER}_REDIRECT_URI: OAuth redirect URI
- {BROKER}_ACCESS_TOKEN: (Optional) Pre-authenticated access token
"""

import os
import logging
from datetime import datetime, timedelta
from typing import Optional
from zoneinfo import ZoneInfo

import requests

logger = logging.getLogger(__name__)

IST = ZoneInfo("Asia/Kolkata")

# TODO: Replace with actual broker base URL
{BROKER}_BASE_URL = "https://api.broker.com"


class {Broker}AuthError(Exception):
    """Authentication failed with {Broker} API."""
    pass


class {Broker}RateLimitError(Exception):
    """Rate limit exceeded on {Broker} API."""
    pass


class {Broker}Auth:
    """
    OAuth2 authentication handler for {Broker} API.
    
    Supports two modes:
    1. Pre-authenticated token via {BROKER}_ACCESS_TOKEN env var
    2. Manual OAuth2 flow (generate auth URL -> user login -> callback with code)
    
    For paper trading/backtesting, a pre-authenticated token is recommended.
    Tokens typically expire daily and need manual refresh.
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        redirect_uri: Optional[str] = None,
        access_token: Optional[str] = None,
    ):
        self.api_key = api_key or os.environ.get("{BROKER}_API_KEY", "")
        self.api_secret = api_secret or os.environ.get("{BROKER}_API_SECRET", "")
        self.redirect_uri = redirect_uri or os.environ.get(
            "{BROKER}_REDIRECT_URI", "http://localhost:8000/callback"
        )
        self._access_token = access_token or os.environ.get("{BROKER}_ACCESS_TOKEN", "")
        self._token_expiry: Optional[datetime] = None
    
    @property
    def access_token(self) -> str:
        """Get current access token, raising if unavailable."""
        if not self._access_token:
            raise {Broker}AuthError(
                "No access token available. Set {BROKER}_ACCESS_TOKEN env var "
                "or complete OAuth2 flow with exchange_code_for_token()."
            )
        return self._access_token
    
    @property
    def is_configured(self) -> bool:
        """Check if API credentials are configured."""
        return bool(self.api_key and self.api_secret)
    
    @property
    def has_valid_token(self) -> bool:
        """Check if we have a non-expired token."""
        if not self._access_token:
            return False
        if self._token_expiry and datetime.now(IST) >= self._token_expiry:
            return False
        return True
    
    def get_authorization_url(self, state: str = "paperclip") -> str:
        """
        Generate OAuth2 authorization URL.
        
        User must visit this URL to login and authorize the app.
        After login, broker redirects to redirect_uri with auth code.
        
        Args:
            state: State parameter for CSRF protection
            
        Returns:
            Authorization URL string
        """
        if not self.api_key:
            raise {Broker}AuthError("{BROKER}_API_KEY not configured")
        
        # TODO: Update path to match broker's OAuth endpoint
        return (
            f"{{BROKER}_BASE_URL}/v2/login/authorization/dialog"
            f"?response_type=code"
            f"&client_id={self.api_key}"
            f"&redirect_uri={self.redirect_uri}"
            f"&state={state}"
        )
    
    def exchange_code_for_token(self, authorization_code: str) -> str:
        """
        Exchange authorization code for access token.
        
        Args:
            authorization_code: Code received from OAuth2 callback
            
        Returns:
            Access token string
            
        Raises:
            {Broker}AuthError: If token exchange fails
        """
        if not self.api_key or not self.api_secret:
            raise {Broker}AuthError("{BROKER}_API_KEY and {BROKER}_API_SECRET required")
        
        # TODO: Update path to match broker's token endpoint
        url = f"{{BROKER}_BASE_URL}/v2/login/authorization/token"
        
        payload = {
            "code": authorization_code,
            "client_id": self.api_key,
            "client_secret": self.api_secret,
            "redirect_uri": self.redirect_uri,
            "grant_type": "authorization_code",
        }
        
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }
        
        try:
            response = requests.post(url, data=payload, headers=headers, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            self._access_token = data.get("access_token", "")
            
            if not self._access_token:
                raise {Broker}AuthError(f"No access token in response: {data}")
            
            # Most Indian broker tokens expire at end of day
            # Set expiry to 23 hours to be safe
            self._token_expiry = datetime.now(IST) + timedelta(hours=23)
            
            logger.info("Successfully obtained {Broker} access token")
            return self._access_token
            
        except requests.exceptions.RequestException as e:
            raise {Broker}AuthError(f"Token exchange failed: {e}") from e
    
    def get_headers(self) -> dict[str, str]:
        """
        Get HTTP headers with authorization token.
        
        Returns:
            Dict of headers including Bearer token
        """
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Accept": "application/json",
        }
    
    def refresh_token(self) -> str:
        """
        Refresh access token if supported by broker.
        
        Note: Most Indian brokers don't support refresh tokens.
        User must re-authenticate daily.
        
        Returns:
            New access token if refresh supported
            
        Raises:
            {Broker}AuthError: If refresh not supported or fails
        """
        # TODO: Implement if broker supports token refresh
        raise {Broker}AuthError(
            "{Broker} does not support token refresh. "
            "Re-authenticate via OAuth2 flow."
        )
