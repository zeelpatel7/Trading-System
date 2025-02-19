from alpaca.data.historical.news import NewsClient
from alpaca.data.requests import NewsRequest
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

load_dotenv()

# Retrieve API credentials
API_KEY = os.getenv("ALPACA_API_KEY")
SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")

if not API_KEY or not SECRET_KEY:
    raise ValueError("Missing API credentials. Ensure they are set as environment variables or in a .env file.")

# no keys required for news data
client = NewsClient(API_KEY, SECRET_KEY)

request_params = NewsRequest(
    symbols="PLTR",
    start=datetime.now() - timedelta(days=7)
)

news = client.get_news(request_params)

# convert to dataframe
print(news.df.headline.values)
