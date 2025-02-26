from src.alpaca_utils.market_data_manager import MarketDataManager
from src.alpaca_utils.account_manager import AccountManager
from src.alpaca_utils.trade_manager import TradeManager

account_manager = AccountManager(paper=True)

# Fetch account details
account_info = account_manager.get_account_details()
print(f"📈 Equity: ${account_info['equity']}")
print(f"💰 Account Balance: ${account_info['cash']}")
print(f"💵 Buying Power: ${account_info['buying_power']}")
print(f"🔄 Profit/Loss Today: ${account_info['profit_loss_today']}")

# Fetch open positions
positions = account_manager.get_positions()
if positions:
    print("\n📌 Open Positions:")
    for pos in positions:
        print(f" - {pos['symbol']}: {pos['qty']} shares, Market Value: ${pos['market_value']}, Unrealized P/L: ${pos['unrealized_pl']} ({pos['unrealized_plpc']:.2f}%)")
else:
    print("\n❌ No open positions.")

# Fetch closed positions
closed_positions = account_manager.get_closed_positions()
if closed_positions:
    print("\n📉 Closed Positions:")
    for pos in closed_positions:
        print(f" - {pos['symbol']}: Market Value: ${pos['market_value']}, Cost Basis: ${pos['cost_basis']}, Realized P/L: ${pos['realized_pl']}")
else:
    print("\n🛑 No closed positions yet.")

manager = MarketDataManager()
historical_data = manager.fetch_historical_data()
print(historical_data.tail(5))