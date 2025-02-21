# Trading System

This is an automated trading system that interacts with Alpaca's API for paper trading. The system retrieves market data and executes trades based on predefined strategies.

## Getting Started

### 1️⃣ Clone the Repository
#### Using SSH (Recommended):
```bash
git clone git@github.com:sohammandal/trading-system.git
cd trading-system
```

### 2️⃣ Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Configure API Keys
Create a `.env` file in the project root and ensure it is included in `.gitignore`:
```bash
ALPACA_API_KEY=your_api_key
ALPACA_SECRET_KEY=your_secret_key
```

### 5️⃣ Verify Setup by Checking Account Balance
Run the following command to confirm your API keys are working correctly:

```bash
python check_balance.py
```

## Running the TCP Client

The **TCP client** connects to the server to receive real-time market data and execute trades based on a predefined strategy. The market data is **mocked** to be real-time by streaming historical prices from a CSV file at a controlled interval.

### 1️⃣ Start the Server (in a dedicated terminal)
Before running the client, ensure the **TCP server** is running and streaming data. The server reads from the historical CSV file and sends price updates to connected clients in a simulated real-time manner.

```bash
python tcp_server.py -p 9999 -f data/historical_stock_data_daily_5_yrs.csv -t 1
```

### 2️⃣ Run the TCP Client
Once the server is running, start the client to receive market data and execute trades:

```bash
python tcp_client.py
```
You should see market updates, trade signals, and portfolio status being printed in real time.

### 3️⃣ How it Works
- The server mimics real-time trading by sending historical stock data from the CSV file at regular intervals.
- The client processes the data and applies a simple trading strategy: Buy if the closing price is lower than the opening price, sell otherwise.
- All balances and profit/loss calculations are logged in `data/trading_session_report.csv` for review.

### 4️⃣ Stopping the Client
To stop the client, use `Ctrl + C` in the terminal.