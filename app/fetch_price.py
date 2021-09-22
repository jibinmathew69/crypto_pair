from os import read
import requests
from datetime import datetime, timedelta
from fetch_tokens import symbol_to_id
from feather_io import read_file, append_file
from df_processor import get_prices, get_start_end_date, date_intersection, \
    price_ratios, clean_json, get_date_and_price, get_extremes

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
    if type(df_dates) == bool:
        return df_dates

    prices = get_prices(df)
    return {
        "start_date": df_dates[0],
        "end_date": df_dates[1],
        "prices": prices
    }

def format_response_js(df, pair):
    df_dates = get_start_end_date(df)
    if type(df_dates) == bool:
        return df_dates
        
    df_extremes = get_extremes(df)
    print(df_extremes)
    return {
        "meta": {
            "start_date": df_dates[0],
            "end_date": df_dates[1],
            "range": {"low": df_extremes[0], "high": df_extremes[1]},
            "pair": {"from": pair[0], "to": pair[1]}
        },
        "payload": {
            "ratios": [
                [{"label": "Date", "type": "date"}, "Ratio"],
                *get_date_and_price(df)
            ] 
        }
    }

def fetch_pair_history(df1, df2, pair):
        
    df = date_intersection(df1, df2)

    if df.shape[0] < 1:
        return False

    df = price_ratios(df)

    return format_response_js(df, pair)

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
    start_time = datetime.fromtimestamp(last_time/1000) + timedelta(days=1)
    start_time = int(start_time.timestamp()*1000)
    end_time = int(datetime.utcnow().timestamp()*1000)

    url = URL.format(token_id=token_name)+"&start={}&end={}".format(start_time, end_time)
    price_dict = fetch_token_price(token_id, url)
    if type(price_dict) == bool:
        return False
    elif price_dict == []:
        return True

    df = clean_json(price_dict, ['priceUsd', 'time', 'date'])
    return append_file(df, token_file)
