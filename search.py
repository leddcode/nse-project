from datetime import date, timedelta
import os

from dotenv import load_dotenv
import requests


load_dotenv()
API_KEY = os.getenv('API_KEY')


def process_search(search_query, search_period):
    today = date.today()
    period = (today - timedelta(days=int(search_period))).strftime("%Y-%m-%d")
    url = ('http://newsapi.org/v2/everything?'
           f'q={search_query}&'
           f'from={period}&'
           'sortBy=popularity&'
           f'apiKey={API_KEY}')

    r = requests.get(url)
    return r.json()['articles']
    