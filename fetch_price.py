import requests
from feather_io import read_file
from df_processor import get_prices, get_start_end_date, date_intersection, price_ratios

URL = "https://api.coincap.io/v2/assets/{token_id}/history?interval=d1"

def fetch_token_price(token_id):
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
