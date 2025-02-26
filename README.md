# Trading System

This is an **automated trading system** that interacts with **[Alpaca](https://alpaca.markets/)'s API** for paper trading and a **TCP-based simulated trading** environment for testing strategies locally. The system retrieves market data, calculates indicators, generates trade signals and executes orders based on predefined strategies.

## 📂 Project Structure

```plaintext
📂 trading-system/
│── 📜 README.md             # Project documentation & setup instructions
│── 📜 requirements.txt      # Python dependencies
│── 📜 main_day_trader.py    # 🚀 Entry point for Alpaca paper trading (Alpaca API)

├── 📂 data/                 # 📊 Historical market data and trade logs

├── 📂 models/               # 🧠 Trained ML models and feature scalers  

├── 📂 notebooks/            # 📓 Strategy research, backtesting and model training  

├── 📂 src/                  # 🏗️ Core trading system  
│   ├── 📂 alpaca_utils/     # 📡 Alpaca API modules
│   ├── 📂 local_trading/    # 🔌 Simulated trading & backtesting (TCP-based)
│   └── 📂 scripts/          # 🛠️ Utility scripts (data fetching, API checks)
```

## Getting Started

### 1️⃣ Clone the Repository

#### Using SSH (Recommended):
```bash
git clone git@github.com:sohammandal/trading-system.git
cd trading-system
```

#### Using HTTPS:
```bash
git clone https://github.com/sohammandal/trading-system.git
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
python src/scripts/check_balance.py
```

## Running TCP-based Simulated Trading Locally (No API Keys Required)
The **TCP-based system** mimics real-time trading by streaming historical data from CSV files. The TCP client connects to the TCP server to receive market data and execute trades based on a predefined strategy. Unlike the Alpaca-based system, the TCP-based system does not require API keys.

### 1️⃣ Start the Server (in a dedicated terminal)
Before running the client, ensure the **TCP server** is running and streaming data. The server reads from the historical CSV file and sends price updates to connected clients in a simulated real-time manner.

```bash
python src/local_trading/tcp_server.py -p 9999 -f data/historical_stock_data_5min_6months.csv -t 0.1
```

### 2️⃣ Run the TCP Client
Once the server is running, start the client to receive market data and execute trades:

```bash
python src/local_trading/four_factor_day_trader.py
```
You should see market updates, trade signals, and portfolio status being printed in real time.

### 3️⃣ How it Works
- The TCP server streams data from a historical CSV file, simulating real-time price updates.
- The trading client processes this data and applies a strategy.
- All trades & performance logs are stored in the `data/` directory.

### 4️⃣ Stopping the Client
To stop the client, use `Ctrl + C` in the terminal.