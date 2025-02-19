# Trading System

This is an automated trading system that interacts with Alpaca's API for paper trading. The system retrieves market data and executes trades based on predefined strategies.

## Getting Started

### 1️⃣ Clone the Repository
#### Using SSH (Recommended):
```bash
git clone git@github.com:sohammandal/trading-system.git
cd trading-system
```

### 2️⃣ Create a Virtual Environment (Using `virtualenv`)
```bash
pip install virtualenv  # Install virtualenv if not installed
virtualenv venv
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

