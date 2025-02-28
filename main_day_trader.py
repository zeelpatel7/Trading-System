import os

from src.alpaca_utils.market_data_manager import MarketDataManager
from src.alpaca_utils.account_manager import AccountManager
from src.alpaca_utils.trade_manager import TradeManager
from src.alpaca_utils.trading_strategy import TradingStrategy
from src.alpaca_utils.risk_manager import RiskManager

# Initialize modules
account_manager = AccountManager(paper=True)
market_data_manager = MarketDataManager()
trading_strategy = TradingStrategy()
trade_manager = TradeManager()
risk_manager = RiskManager(risk_per_trade=0.01, atr_period=14, atr_multiplier=1, risk_reward_ratio=2)

# Fetch account details
account_info = account_manager.get_account_details()
print(f"📈 Equity: ${account_info['equity']}")
print(f"💰 Account Balance: ${account_info['cash']}")
print(f"💵 Buying Power: ${account_info['buying_power']}")
print(f"🔄 Profit/Loss Today: ${account_info['realized_pnl']}")
print(f"🛠️ Maintenance Margin: ${account_info['maintenance_margin']}")
print(f"📊 Margin Available: ${account_info['margin_available']}")

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

# 📡 **Fetch historical data ONCE for all securities** (reducing API calls)
historical_data = market_data_manager.fetch_historical_data()

if historical_data is None or historical_data.empty:
    print("❌ No historical data available. Exiting test.")
else:
    # Fetch account details **once per batch**
    account_info = account_manager.get_account_details()
    current_equity = account_info["equity"]
    cash = account_info["cash"]
    buying_power = account_info["buying_power"]

    # 📌 **Loop through all securities**
    for symbol in market_data_manager.stock_tickers + market_data_manager.etfs:
        symbol_data = historical_data[historical_data["symbol"] == symbol]

        if symbol_data.empty:
            print(f"⚠️ No data found for {symbol}, skipping...")
            continue  # Skip this security if no data is available

        # Update strategy buffer with fetched data
        for _, row in symbol_data.iterrows():
            trading_strategy.update_buffer(symbol, row)

        # Generate trade signal for the symbol
        trade_signal = trading_strategy.generate_trade_signal(symbol)
        print(f"\n📈 Trade Signal for {symbol}: {trade_signal}")

        # If we have a BUY or SELL signal, calculate risk parameters and place an order
        if trade_signal in ["BUY", "SELL"]:
            # Use the latest close price as the entry price
            entry_price = symbol_data.iloc[-1]['close']
            print(f"Entry Price for {symbol}: {entry_price}")

            # Pass the historical data, entry price, and account details to the risk manager
            risk_params = risk_manager.calculate_trade_parameters(
                df=symbol_data,
                entry_price=entry_price,
                equity=current_equity,
                side=trade_signal,
                buying_power=buying_power,
                cash=cash
            )

            print("Calculated Risk Parameters:", risk_params)
            print(f"Trade Signal: {trade_signal}, Entry Price: {entry_price}, Quantity: {risk_params['quantity']}, Total Value: {entry_price * risk_params['quantity']}")

            # TODO: Implement Portfolio level risk management