import os

from src.alpaca_utils.market_data_manager import MarketDataManager
from src.alpaca_utils.account_manager import AccountManager
from src.alpaca_utils.trade_manager import TradeManager
from src.alpaca_utils.trading_strategy import TradingStrategy

account_manager = AccountManager(paper=True)
manager = MarketDataManager()
strategy = TradingStrategy()

# Fetch account details
account_info = account_manager.get_account_details()
print(f"📈 Equity: ${account_info['equity']}")
print(f"💰 Account Balance: ${account_info['cash']}")
print(f"💵 Buying Power: ${account_info['buying_power']}")
print(f"🔄 Profit/Loss Today: ${account_info['realized_pnl']}")

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

# Test strategy with historical data
# Fetch historical data for all securities
historical_data = manager.fetch_historical_data()

if historical_data is None or historical_data.empty:
    print("❌ No historical data available. Exiting test.")
else:
    # Process each symbol
    for symbol in manager.stock_tickers + manager.etfs:  # Loop through all symbols
        symbol_data = historical_data[historical_data["symbol"] == symbol]

        if symbol_data.empty:
            print(f"⚠️ No data found for {symbol}, skipping...")
            continue  # Skip this security if no data is available

        # Update strategy buffer with fetched data
        for _, row in symbol_data.iterrows():
            strategy.update_buffer(symbol, row)

        # Generate trade signal for the symbol
        trade_signal = strategy.generate_trade_signal(symbol)
        print(f"📈 Trade Signal for {symbol}: {trade_signal}")

