import requests
from feather_io import read_file
from df_processor import get_start_end_date, date_intersection

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

def fetch_history(token_id1, token_id2="usd"):
    token_id1 = token_id1.lower()
    token_id2 = token_id2.lower()

    df1 = read_file(token_id1)

    if type(df1) == bool:
        return False
    
    if df1.shape[0] < 1:
        return False

    if token_id2 == "usd":
        return format_response(df1)

    df2 = read_file(token_id2)

    if type(df2) == bool:
        return False
    
    if df2.shape[0] < 1:
        return False

    df = date_intersection(df1, df2)

    return format_response(df)
    