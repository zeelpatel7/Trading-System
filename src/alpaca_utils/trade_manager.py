import os
from dotenv import load_dotenv
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest, LimitOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce, OrderType

class TradeManager:
    """
    Handles trade execution using Alpaca API.
    Can place, modify, and cancel orders.
    """

    def __init__(self, paper=True):
        """Initialize the Alpaca Trading Client for executing trades."""
        load_dotenv()

        self.api_key = os.getenv("ALPACA_API_KEY")
        self.secret_key = os.getenv("ALPACA_SECRET_KEY")

        if not self.api_key or not self.secret_key:
            raise ValueError("Missing API credentials. Ensure they are set in the .env file.")

        self.client = TradingClient(self.api_key, self.secret_key, paper=paper)

    def place_market_order(self, symbol, qty, side):
        """
        Places a market order (buy/sell).
        :param symbol: Stock ticker
        :param qty: Quantity to buy/sell
        :param side: 'buy' or 'sell'
        """
        try:
            order = MarketOrderRequest(
                symbol=symbol,
                qty=qty,
                side=OrderSide.BUY if side.lower() == "buy" else OrderSide.SELL,
                time_in_force=TimeInForce.GTC  # Good 'til canceled
            )

            response = self.client.submit_order(order)
            print(f"✅ Market order placed: {side.upper()} {qty} shares of {symbol}")
            return response

        except Exception as e:
            print(f"❌ Error placing market order for {symbol}: {e}")
            return None

    def place_limit_order(self, symbol, qty, side, limit_price):
        """
        Places a limit order (buy/sell).
        :param symbol: Stock ticker
        :param qty: Quantity to buy/sell
        :param side: 'buy' or 'sell'
        :param limit_price: Price at which to execute the trade
        """
        try:
            order = LimitOrderRequest(
                symbol=symbol,
                qty=qty,
                side=OrderSide.BUY if side.lower() == "buy" else OrderSide.SELL,
                time_in_force=TimeInForce.GTC,
                limit_price=limit_price
            )

            response = self.client.submit_order(order)
            print(f"✅ Limit order placed: {side.upper()} {qty} shares of {symbol} at ${limit_price}")
            return response

        except Exception as e:
            print(f"❌ Error placing limit order for {symbol}: {e}")
            return None

    def cancel_order(self, order_id):
        """
        Cancels an order given its ID.
        :param order_id: The ID of the order to cancel
        """
        try:
            self.client.cancel_order_by_id(order_id)
            print(f"✅ Order {order_id} canceled successfully.")
        except Exception as e:
            print(f"❌ Error canceling order {order_id}: {e}")

    def cancel_all_orders(self):
        """
        Cancels all open orders.
        """
        try:
            self.client.cancel_orders()
            print("✅ All open orders have been canceled.")
        except Exception as e:
            print(f"❌ Error canceling all orders: {e}")