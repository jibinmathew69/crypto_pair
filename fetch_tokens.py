from fetch_price import fetch_token_price
import requests
from df_processor import clean_json
from feather_io import write_file

TOKEN_URL = "https://api.coincap.io/v2/assets"

def fetch_symbols():
    response = requests.get(TOKEN_URL)

    if response.status_code != 200:
        return False
    
    response = response.json()
    return response["data"]

def update_symbols():
    json_data = fetch_symbols()

    if not json_data:
        return False

    df = clean_json(json_data, ["id", "symbol"])
    return write_file(df, "symbols")
    