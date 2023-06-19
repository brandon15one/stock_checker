import os
import requests
from twilio.rest import Client

# ___________________________________________________CONSTANTS____________________________________________#
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "###"
NEWS_API_KEY = "###"

TWILIO_SID = "###"
TWILIO_AUTH_TOKEN = "####"

stock_params = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY
}
# ___________________________________________________REQUESTS____________________________________________#
response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
data_lst = [value for (key, value) in data.items()]
yesterday_data = data_lst[0]
yesterday_closing_price = yesterday_data["4. close"]

day_before_yesterday_data = data_lst[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]

difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
up_down = None
if difference > 0:
    up_down = "📈"
else:
    up_down = "📉"
diff_percentage = round(difference / float(yesterday_closing_price)) * 100

if abs(diff_percentage) > 1:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME
    }
    newz_response = requests.get(NEWS_ENDPOINT, params=news_params)
    article = newz_response.json()["articles"]

    three_articles = article[:3]

    formatted_articles = [f'''{STOCK_NAME}: {up_down}{diff_percentage}% \nHeadline: {article['title']}. 
                        \nBrief: {article['description']}''' for article in three_articles]

    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_="+14067197991",
            to="+918595118498"
        )
