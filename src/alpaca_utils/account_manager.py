import os
from dotenv import load_dotenv
from alpaca.trading.client import TradingClient

class AccountManager:
    """
    Manages account and portfolio tasks (excluding order placement).
    """

    def __init__(self, paper=True):
        """Initialize the Alpaca Trading Client for account management."""
        # Load environment variables
        load_dotenv()

        self.API_KEY = os.getenv("ALPACA_API_KEY")
        self.SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")

        if not self.API_KEY or not self.SECRET_KEY:
            raise ValueError("Missing API credentials. Ensure they are set in the .env file.")

        # Initialize Alpaca Trading Client (paper trading mode enabled by default)
        self.client = TradingClient(self.API_KEY, self.SECRET_KEY, paper=paper)

    def get_account_details(self):
        """Fetch and return account details like balance, equity, and buying power."""
        account = self.client.get_account()
        return {
            "equity": float(account.equity),
            "cash": float(account.cash),
            "buying_power": float(account.buying_power),
            "profit_loss_today": float(account.equity) - float(account.last_equity)
        }

    def get_positions(self):
        """Fetch all open positions and return them as a list of dictionaries."""
        positions = self.client.get_all_positions()
        position_data = []
        
        for pos in positions:
            position_data.append({
                "symbol": pos.symbol,
                "qty": float(pos.qty),
                "market_value": float(pos.market_value),
                "cost_basis": float(pos.cost_basis),
                "unrealized_pl": float(pos.unrealized_pl),
                "unrealized_plpc": float(pos.unrealized_plpc) * 100,  # Convert to percentage
            })

        return position_data

    def get_closed_positions(self):
        """Alternative approach: Fetch closed positions from trade history."""
        closed_positions = []
        positions = self.client.get_all_positions()

        for pos in positions:
            if float(pos.qty) == 0:  # If quantity is zero, it's a closed position
                closed_positions.append({
                    "symbol": pos.symbol,
                    "market_value": float(pos.market_value),
                    "cost_basis": float(pos.cost_basis),
                    "realized_pl": float(pos.unrealized_pl)
                })

        return closed_positions