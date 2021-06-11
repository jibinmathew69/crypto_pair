from os import read
import requests
from datetime import datetime, timedelta
from fetch_tokens import symbol_to_id
from feather_io import read_file, append_file
from df_processor import get_prices, get_start_end_date, date_intersection, price_ratios, clean_json

URL = "https://api.coincap.io/v2/assets/{token_id}/history?interval=d1"
LIVE_URL = "https://api.coincap.io/v2/assets/{token_id}"


def fetch_token_price(token_id, url=None):
    if not url:
        url = URL.format(token_id = token_id)
    
    response = requests.get(url)

    if response.status_code != 200:
        return False
    
    response = response.json()

    return response['data']

def format_response(df):
    df_dates = get_start_end_date(df)
    prices = get_prices(df)
    return {
        "start_date": df_dates[0],
        "end_date": df_dates[1],
        "prices": prices
    }

def fetch_pair_history(df1, df2):
        
    df = date_intersection(df1, df2)

    if df.shape[0] < 1:
        return False

    df = price_ratios(df)

    return format_response(df)

def fetch_live_price(token_id):
    url = LIVE_URL.format(token_id = token_id)

    response = requests.get(url)

    if response.status_code != 200:
        return False
    
    response = response.json()

    return response['data']['priceUsd']


def update_price(token_id):
    token_name = symbol_to_id(token_id)
    if token_name == False:
        return False

    token_file = "{}.dat".format(token_id)

    df = read_file(token_file)
    df = df.tail(1)
    if df.shape[0] < 1:
        return False

    last_time = df["time"]
    start_time = datetime.fromtimestamp(last_time) + timedelta(days=1)
    start_time = int(start_time.timestamp()*1000)
    yesterday = datetime.utcnow().date() - timedelta(days=1)
    end_time = int(datetime(yesterday.year, yesterday.month, yesterday.day, 0, 0, 0, 0).timestamp()*1000)

    url = URL.format(token_id = token_id)+"&start={}&end={}".format(start_time, end_time)
    price_dict = fetch_token_price(token_id, url)
    if not price_dict:
        return False

    df = clean_json(price_dict, ['priceUsd', 'time', 'date'])
    return append_file(df, token_file)
    