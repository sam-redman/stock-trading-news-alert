# ---------------------------------- MODULES ---------------------------------- #

import os
from dotenv import load_dotenv
from twilio.rest import Client
from bs4 import BeautifulSoup
import time
import schedule

from data.api import stock_data
from data.api import news_data
from data.stocks import STOCK_NAME

# -------------------------- MISC -------------------------- #

# Load the .env file.
load_dotenv()

# ---------------------------------- MAIN ---------------------------------- #


def stock_alert():
    """Takes stock information from the previous day and the day before yesterday and calculates the price difference.
    If it meets a pre-defined threshold it sends a text with news information relating to the stocks."""

    # Turn the stock data into a list.
    stock_data_list = [value for (key, value) in stock_data.items()]

    # Tap into the data from the previous day.
    yesterday_stock_data = stock_data_list[0]
    # Tap into the closing price key.
    yesterday_closing_price = yesterday_stock_data["4. close"]

    # Tap into the data from the day before yesterday.
    day_before_yesterday_stock_data = stock_data_list[1]
    # Tap into the closing price key.
    day_before_yesterday_closing_price = day_before_yesterday_stock_data["4. close"]

    # Find the positive difference.
    difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
    # Checking to see if the stock price went up or down and capturing an emoji to represent it.
    up_down = None
    if difference > 0:
        up_down = "🔺"
    else:
        up_down = "🔻"

    # Percentage difference between the two days.
    difference_percentage = round((difference / float(yesterday_closing_price)) * 100)

    # If the difference is greater than 2% then print news about the stock.
    if abs(difference_percentage) > 2:
        # Pick out the top articles with Python slice operator.
        top_articles = news_data[:1]

    # Format articles with just the Headline and the Description.
    formatted_articles = [f"{STOCK_NAME}: {up_down}{difference_percentage}%\n\nHeadline: {article['title']}, \n\nBrief: {article ['description']}" for article in top_articles]

# ---------------------------------- MESSAGING ---------------------------------- #

    # Twilio client.
    client = Client(os.environ['TWILIO_SID'], os.environ['TWILIO_AUTH_TOKEN'])

    # Send a message for each article.
    for article in formatted_articles:
        # Text message to be sent.
        message = client.messages.create(
            # BeautifulSoup cleans up any gross HTML tags in the text.
            body=BeautifulSoup(article).text,
            from_=os.environ['TWILIO_PHONE_NUMBER'],
            to=os.environ['PERSONAL_PHONE_NUMBER']
        )

    # Check that the SMS sent successfully.
    print(message.status)

# ---------------------------------- TIME/SCHEDULING ---------------------------------- #


# Run the stock alert check at US stock market open (converted to UK time).
schedule.every().monday.at("14:30").do(stock_alert)
schedule.every().tuesday.at("14:30").do(stock_alert)
schedule.every().wednesday.at("14:30").do(stock_alert)
schedule.every().thursday.at("14:30").do(stock_alert)
schedule.every().friday.at("14:30").do(stock_alert)

# Keeps looping every second to check the time.
while True:
    schedule.run_pending()
    time.sleep(1)
