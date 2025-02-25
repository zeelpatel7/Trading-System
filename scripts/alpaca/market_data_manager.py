import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import pandas as pd
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
from alpaca.data.enums import Adjustment
from alpaca.data.historical.stock import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest

class MarketDataManager:
    """
    Manages market data retrieval from Alpaca API.
    Fetches historical stock and ETF data, retrieving 5-minute bars for the past 5 days by default.
    """

    def __init__(self, timeframe=TimeFrame(5, TimeFrameUnit.Minute), days=5):
        """Initialize Alpaca API client and set query parameters."""
        load_dotenv()

        self.api_key = os.getenv("ALPACA_API_KEY")
        self.secret_key = os.getenv("ALPACA_SECRET_KEY")

        if not self.api_key or not self.secret_key:
            raise ValueError("Missing API credentials. Ensure they are set in the .env file.")

        self.client = StockHistoricalDataClient(self.api_key, self.secret_key)

        self.stock_tickers = [
            "AAPL", "MSFT", "AMZN", "GOOGL", "META", "BRK.B", "NVDA", "JPM", "TSLA", "JNJ",
            "V", "PG", "UNH", "HD", "MA", "BAC", "DIS", "PYPL", "CRM", "PFE",
            "VZ", "INTC", "CMCSA", "NFLX", "XOM", "KO", "ABT", "T", "NKE", "MRK",
            "WMT", "ADP", "CVX", "TMO", "ORCL", "IBM", "ACN", "MCD", "MDLZ", "UPS",
            "COST", "HON", "DHR", "QCOM", "MDT", "TXN", "AVGO", "SPGI", "ADBE", "LLY"
        ]

        self.etfs = ["SPY", "DIA", "QQQ", "IWM", "VTI", "IYT", "IDU", "VXX"]

        self.timeframe = timeframe
        self.days = days

    def fetch_historical_data(self):
        """Fetches historical 5-minute bars for all securities for the last `self.days` days."""
        now = datetime.now(ZoneInfo("America/New_York"))

        request = StockBarsRequest(
            symbol_or_symbols=self.stock_tickers + self.etfs,
            timeframe=self.timeframe,
            start=now - timedelta(days=self.days),
            adjustment=Adjustment.ALL,
        )

        print(f"📡 Fetching {self.timeframe} bars for the last {self.days} days...")

        try:
            df = self.client.get_stock_bars(request).df

            if df.empty:
                print("❌ No data received. Check your API or market hours.")
                return None

            df = df.reset_index()
            df = df.sort_values(by=["timestamp", "symbol"])

            print(f"✅ Successfully fetched {len(df)} rows of historical data.")
            return df

        except Exception as e:
            print(f"❌ Error fetching data: {e}")
            return None

# manager = MarketDataManager()
# historical_data = manager.fetch_historical_data()
# print(historical_data.tail(5))