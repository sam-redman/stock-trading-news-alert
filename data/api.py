# ---------------------------------- MODULES ---------------------------------- #

import requests
import os
from dotenv import load_dotenv

from data.stocks import STOCK_NAME
from data.stocks import COMPANY_NAME

# -------------------------- MISC -------------------------- #

# Load the .env file.
load_dotenv()

# ---------------------------------- API ---------------------------------- #

# API endpoints.
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

# Parameters to manipulate the API request.
stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": os.environ['ALPHA_VANTAGE']
}

# Contact Vantage API.
stock_response = requests.get(STOCK_ENDPOINT, params=stock_parameters)
# Check for API errors.
stock_response.raise_for_status()
# Capture response as .json - narrowed down to the daily data.
stock_data = stock_response.json()["Time Series (Daily)"]

# Parameters to manipulate the API request.
news_parameters = {
    "qInTitle": COMPANY_NAME,
    "apiKey": os.environ['NEWS_API']
}

# Contact News API.
news_response = requests.get(NEWS_ENDPOINT, params=news_parameters)
# Check for API errors.
news_response.raise_for_status()
# Capture response as .json - narrowed down to articles data.
news_data = news_response.json()["articles"]
