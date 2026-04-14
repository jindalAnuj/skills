"""
{BROKER} Paper Trading Broker Adapter

Template for implementing BrokerAdapter interface for paper trading.
Replace {BROKER}, {Broker}, and {broker} with actual broker name.

PAPER TRADING ONLY - This adapter simulates trades, never executes real ones.
"""

import uuid
import logging
from datetime import datetime
from typing import Optional
from zoneinfo import ZoneInfo

# TODO: Import from your auth and loader modules
# from .{broker}_auth import {Broker}Auth
# from ..data.{broker}_loader import {Broker}Loader
from .base import (
    BrokerAdapter,
    Order,
    OrderSide,
    OrderStatus,
    OrderType,
    Position,
    ProductType,
)

logger = logging.getLogger(__name__)

IST = ZoneInfo("Asia/Kolkata")


class {Broker}PaperAdapter(BrokerAdapter):
    """
    Paper trading adapter for {Broker}.
    
    CRITICAL: This adapter operates in PAPER MODE ONLY.
    All orders are simulated locally - no real trades are ever executed.
    
    Features:
    - Simulates order execution with configurable fill behavior
    - Tracks positions and P&L locally
    - Uses live quotes from {Broker} API for realistic fills
    - Applies configurable slippage
    
    Usage:
        adapter = {Broker}PaperAdapter()
        adapter.connect({})  # Paper mode - no real credentials needed
        
        order = Order(
            symbol="RELIANCE",
            exchange="NSE",
            side=OrderSide.BUY,
            order_type=OrderType.MARKET,
            quantity=10,
        )
        order_id = adapter.place_order(order)
    """
    
    def __init__(
        self,
        auth: Optional["{Broker}Auth"] = None,
        loader: Optional["{Broker}Loader"] = None,
        initial_capital: float = 1_000_000.0,
        slippage_pct: float = 0.001,  # 0.1% slippage
    ):
        # TODO: Import and use actual auth/loader classes
        # self.auth = auth or {Broker}Auth()
        # self.loader = loader or {Broker}Loader(auth=self.auth)
        self.auth = auth
        self.loader = loader
        
        self._initial_capital = initial_capital
        self._capital = initial_capital
        self._slippage_pct = slippage_pct
        
        # Local order and position tracking
        self._orders: dict[str, Order] = {}
        self._positions: dict[str, Position] = {}
        self._connected = False
        
        # CRITICAL: Paper mode flag
        self._paper_mode = True
    
    @property
    def name(self) -> str:
        return "{broker}_paper"
    
    @property
    def is_connected(self) -> bool:
        return self._connected
    
    @property
    def capital(self) -> float:
        """Current available capital."""
        return self._capital
    
    @property
    def total_value(self) -> float:
        """Total portfolio value (capital + positions)."""
        position_value = sum(
            pos.quantity * pos.last_price for pos in self._positions.values()
        )
        return self._capital + position_value
    
    def connect(self, credentials: dict = None) -> bool:
        """
        Connect to {Broker} API.
        
        PAPER MODE: Validates credentials format but simulates connection.
        In paper mode, we may still use the loader for live quotes.
        
        Args:
            credentials: Optional credentials dict (ignored in paper mode)
            
        Returns:
            True if connection successful
        """
        if not self._paper_mode:
            raise RuntimeError("PAPER MODE ONLY - Real trading disabled")
        
        # In paper mode, we always connect successfully
        # Optionally validate loader is available for quotes
        if self.loader:
            try:
                self.loader.is_available()
            except Exception as e:
                logger.warning(f"Loader not available, using simulated quotes: {e}")
        
        self._connected = True
        logger.info("{Broker} paper trading adapter connected")
        return True
    
    def disconnect(self) -> None:
        """Disconnect from broker API."""
        self._connected = False
        logger.info("{Broker} paper trading adapter disconnected")
    
    def place_order(self, order: Order) -> str:
        """
        Place an order.
        
        PAPER MODE: Simulates order placement and execution locally.
        Never sends orders to {Broker} API.
        
        Args:
            order: Order to place
            
        Returns:
            Order ID string
        """
        if not self._connected:
            raise RuntimeError("Not connected to broker")
        
        if not self._paper_mode:
            raise RuntimeError("PAPER MODE ONLY - Real trading disabled")
        
        # Generate paper order ID
        order_id = f"{BROKER}_PAPER_{uuid.uuid4().hex[:12].upper()}"
        order.order_id = order_id
        order.placed_at = datetime.now(IST)
        order.status = OrderStatus.OPEN
        
        # Get fill price
        fill_price = self._get_fill_price(order)
        
        # Check capital for buy orders
        if order.side == OrderSide.BUY:
            order_value = fill_price * order.quantity
            if order_value > self._capital:
                order.status = OrderStatus.REJECTED
                self._orders[order_id] = order
                logger.warning(f"Order rejected: Insufficient capital ({order_value} > {self._capital})")
                return order_id
        
        # Execute order (instant fill for market orders)
        if order.order_type == OrderType.MARKET:
            self._fill_order(order, fill_price)
        else:
            # For limit orders, check if price condition met
            if self._should_fill_limit_order(order, fill_price):
                self._fill_order(order, fill_price)
        
        self._orders[order_id] = order
        
        logger.info(
            f"Paper order placed: {order.side.value} {order.quantity} {order.symbol} "
            f"@ {fill_price:.2f} (ID: {order_id})"
        )
        
        return order_id
    
    def _get_fill_price(self, order: Order) -> float:
        """
        Get realistic fill price for order.
        
        Uses live quote if loader available, otherwise uses order price.
        Applies slippage based on order side.
        """
        base_price = None
        
        # Try to get live quote
        if self.loader:
            try:
                from ..data.models import Exchange
                exchange = Exchange.NSE if order.exchange == "NSE" else Exchange.BSE
                quote = self.loader.get_live_quote(order.symbol, exchange)
                if quote:
                    base_price = quote.get("last_price") or quote.get("close")
            except Exception as e:
                logger.debug(f"Could not get live quote: {e}")
        
        # Fallback to order price or default
        if not base_price:
            base_price = order.price or 100.0
        
        # Apply slippage
        if order.side == OrderSide.BUY:
            fill_price = base_price * (1 + self._slippage_pct)
        else:
            fill_price = base_price * (1 - self._slippage_pct)
        
        return round(fill_price, 2)
    
    def _should_fill_limit_order(self, order: Order, current_price: float) -> bool:
        """Check if limit order conditions are met."""
        if order.order_type == OrderType.LIMIT and order.price:
            if order.side == OrderSide.BUY:
                return current_price <= order.price
            else:
                return current_price >= order.price
        return False
    
    def _fill_order(self, order: Order, fill_price: float) -> None:
        """Execute order fill."""
        order.filled_quantity = order.quantity
        order.average_price = fill_price
        order.status = OrderStatus.COMPLETE
        order.filled_at = datetime.now(IST)
        
        # Update position
        self._update_position(order)
        
        # Update capital
        trade_value = fill_price * order.quantity
        if order.side == OrderSide.BUY:
            self._capital -= trade_value
        else:
            self._capital += trade_value
    
    def _update_position(self, order: Order) -> None:
        """Update positions after order fill."""
        symbol = order.symbol
        quantity = order.filled_quantity if order.side == OrderSide.BUY else -order.filled_quantity
        price = order.average_price
        
        if symbol in self._positions:
            pos = self._positions[symbol]
            new_quantity = pos.quantity + quantity
            
            if new_quantity == 0:
                # Position closed
                del self._positions[symbol]
            else:
                # Update average price for additions
                if quantity > 0:
                    total_cost = pos.quantity * pos.average_price + quantity * price
                    pos.average_price = total_cost / new_quantity
                pos.quantity = new_quantity
                pos.last_price = price
                pos.pnl = (pos.last_price - pos.average_price) * pos.quantity
        else:
            if quantity != 0:
                self._positions[symbol] = Position(
                    symbol=symbol,
                    exchange=order.exchange,
                    quantity=quantity,
                    average_price=price,
                    last_price=price,
                    product=order.product,
                )
    
    def cancel_order(self, order_id: str) -> bool:
        """
        Cancel an open order.
        
        Args:
            order_id: Order ID to cancel
            
        Returns:
            True if order was cancelled
        """
        if order_id not in self._orders:
            return False
        
        order = self._orders[order_id]
        if order.status in (OrderStatus.PENDING, OrderStatus.OPEN):
            order.status = OrderStatus.CANCELLED
            logger.info(f"Paper order cancelled: {order_id}")
            return True
        return False
    
    def get_order_status(self, order_id: str) -> Optional[Order]:
        """Get current status of an order."""
        return self._orders.get(order_id)
    
    def get_orders(self, status: Optional[OrderStatus] = None) -> list[Order]:
        """
        Get all orders, optionally filtered by status.
        
        Args:
            status: Optional status filter
            
        Returns:
            List of orders
        """
        orders = list(self._orders.values())
        if status:
            orders = [o for o in orders if o.status == status]
        return orders
    
    def get_positions(self) -> list[Position]:
        """Get current positions."""
        return list(self._positions.values())
    
    def get_position(self, symbol: str) -> Optional[Position]:
        """Get position for a specific symbol."""
        return self._positions.get(symbol)
    
    def get_quote(self, symbol: str, exchange: str = "NSE") -> Optional[dict]:
        """
        Get current quote for a symbol.
        
        Uses loader for live quotes if available, otherwise returns simulated data.
        """
        if self.loader:
            try:
                from ..data.models import Exchange
                ex = Exchange.NSE if exchange == "NSE" else Exchange.BSE
                return self.loader.get_live_quote(symbol, ex)
            except Exception as e:
                logger.debug(f"Could not get live quote: {e}")
        
        # Return simulated quote
        return {
            "symbol": symbol,
            "exchange": exchange,
            "last_price": 100.0,
            "bid": 99.95,
            "ask": 100.05,
            "volume": 1000000,
            "timestamp": datetime.now(IST).isoformat(),
            "is_simulated": True,
        }
    
    def reset(self, initial_capital: Optional[float] = None) -> None:
        """
        Reset broker state for new simulation.
        
        Args:
            initial_capital: Optional new starting capital
        """
        if initial_capital:
            self._initial_capital = initial_capital
        self._capital = self._initial_capital
        self._orders.clear()
        self._positions.clear()
        logger.info(f"{Broker} paper adapter reset with capital: {self._capital}")
    
    def get_summary(self) -> dict:
        """
        Get account summary.
        
        Returns:
            Dict with capital, positions, total value, P&L
        """
        position_value = sum(
            pos.quantity * pos.last_price for pos in self._positions.values()
        )
        total_pnl = sum(pos.pnl for pos in self._positions.values())
        
        return {
            "initial_capital": self._initial_capital,
            "available_capital": self._capital,
            "position_value": position_value,
            "total_value": self._capital + position_value,
            "unrealized_pnl": total_pnl,
            "realized_pnl": (self._capital + position_value) - self._initial_capital - total_pnl,
            "total_pnl": (self._capital + position_value) - self._initial_capital,
            "return_pct": ((self._capital + position_value) / self._initial_capital - 1) * 100,
            "num_positions": len(self._positions),
            "num_orders": len(self._orders),
        }
