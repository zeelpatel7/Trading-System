import os

from src.alpaca_utils.market_data_manager import MarketDataManager
from src.alpaca_utils.account_manager import AccountManager
from src.alpaca_utils.trade_manager import TradeManager
from src.alpaca_utils.trading_strategy import TradingStrategy
from src.alpaca_utils.risk_manager import RiskManager

# -------------------
# Initialize modules
# -------------------
account_manager = AccountManager(paper=True)
market_data_manager = MarketDataManager()
trading_strategy = TradingStrategy()
trade_manager = TradeManager()
risk_manager = RiskManager(
    risk_per_trade=0.01, 
    atr_period=14, 
    atr_multiplier=1, 
    risk_reward_ratio=2, 
    max_position_fraction=0.01, 
    max_open_positions=10, 
    max_notional_ratio=0.50
)

# -------------------
# Fetch account details
# -------------------
account_info = account_manager.get_account_details()
print(f"📈 Equity: ${account_info['equity']}")
print(f"💰 Account Balance: ${account_info['cash']}")
print(f"💵 Buying Power: ${account_info['buying_power']}")
print(f"🔄 Profit/Loss Today: ${account_info['realized_pnl']}")
print(f"🛠️ Maintenance Margin: ${account_info['maintenance_margin']}")
print(f"📊 Margin Available: ${account_info['margin_available']}")

# -------------------
# Fetch open positions
# -------------------
positions = account_manager.get_positions()
if positions:
    print("\n📌 Open Positions:")
    for pos in positions:
        print(f" - {pos['symbol']}: {pos['qty']} shares, Market Value: ${pos['market_value']}, "
              f"Unrealized P/L: ${pos['unrealized_pl']} ({pos['unrealized_plpc']:.2f}%)")
else:
    print("\n❌ No open positions.")

# -------------------
# Fetch closed positions
# -------------------
closed_positions = account_manager.get_closed_positions()
if closed_positions:
    print("\n📉 Closed Positions:")
    for pos in closed_positions:
        print(f" - {pos['symbol']}: Market Value: ${pos['market_value']}, "
              f"Cost Basis: ${pos['cost_basis']}, Realized P/L: ${pos['realized_pnl']}")
else:
    print("\n🛑 No closed positions yet.")

# -------------------
# Fetch historical data once for all securities (reduces API calls)
# -------------------
# historical_data = market_data_manager.fetch_historical_data()

# if historical_data is None or historical_data.empty:
#     print("❌ No historical data available. Exiting test.")
# else:
#     # Fetch updated account details before processing trades
#     account_info = account_manager.get_account_details()

#     # -------------------
#     # Loop through all securities
#     # -------------------
#     for symbol in market_data_manager.stock_tickers + market_data_manager.etfs:
#         symbol_data = historical_data[historical_data["symbol"] == symbol]

#         if symbol_data.empty:
#             print(f"⚠️ No data found for {symbol}, skipping...")
#             continue

#         # Update strategy buffer
#         for _, row in symbol_data.iterrows():
#             trading_strategy.update_buffer(symbol, row)

#         # Generate trade signal
#         trade_signal = trading_strategy.generate_trade_signal(symbol)
#         print(f"\n📈 Trade Signal for {symbol}: {trade_signal}")

#         if trade_signal in ["BUY", "SELL"]:
#             # Re-fetch latest account details
#             account_info = account_manager.get_account_details()
#             open_positions = account_manager.get_positions()

#             entry_price = symbol_data.iloc[-1]['close']
#             print(f"Entry Price for {symbol}: {entry_price}")

#             # Calculate trade parameters (includes portfolio-level risk checks)
#             risk_params = risk_manager.calculate_trade_parameters(
#                 df=symbol_data,
#                 entry_price=entry_price,
#                 account_info=account_info,
#                 open_positions=open_positions,
#                 side=trade_signal
#             )

#             print("Calculated Risk Parameters:", risk_params)

#             if risk_params["quantity"] <= 0:
#                 print(f"🚫 Skipping {symbol}. Quantity is zero or invalid.")
#                 continue  # Skip trade if no valid quantity

#             print(f"Trade Signal: {trade_signal}, Entry Price: {entry_price}, "
#                   f"Quantity: {risk_params['quantity']}, Total Value: {entry_price * risk_params['quantity']}")

#             # 3) If all checks pass, place the order
#             if account_manager.check_market_open():
#                 print(f"Placing {trade_signal} order for {symbol}...")
#                 order_response = trade_manager.place_market_order(
#                     symbol=symbol,
#                     qty=risk_params["quantity"],
#                     side=trade_signal.lower(),
#                     stop_loss_price=risk_params["stop_loss"],
#                     take_profit_price=risk_params["take_profit"]
#                 )

#                 print(f"Order Response for {symbol}:", order_response)
#             else:
#                 print("❌ Market is closed. Cannot place orders.")

# Close all positions
# account_manager.close_all_positions()