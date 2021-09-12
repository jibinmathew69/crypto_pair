import pandas as pd
import glob
from df_processor import clean_json
from fetch_tokens import symbol_to_id
from feather_io import write_file, read_file
from fetch_price import fetch_token_price, fetch_pair_history, format_response, \
    fetch_live_price, update_price, format_response_js

def resolve_new_token(token_id):
    token_name = symbol_to_id(token_id)
    if token_name == False:
        return False

    price_dict = fetch_token_price(token_name)
    df = clean_json(price_dict, ['priceUsd', 'time', 'date'])
    return write_file(df, "{}.dat".format(token_id))


def validate_df(df, token_id):
    if isinstance(df, pd.DataFrame) and df.shape[0] < 1:
        return None
    elif type(df) == bool:
        if not resolve_new_token(token_id):
            return False
        else:
            df = read_file("{}.dat".format(token_id))
    return df

def fetch_price(token_id1, token_id2):
    token_id1 = token_id1.upper()
    token_id2 = token_id2.upper()

    df1 = read_file("{}.dat".format(token_id1))
    df1 = validate_df(df1, token_id1)

    if type(df1) == bool:
        return False

    if token_id2 == "USD":
        return format_response_js(df1, (token_id1, token_id2))

    df2 = read_file("{}.dat".format(token_id2))
    df2 = validate_df(df2, token_id2)

    if type(df2) == bool:
        return False

    return fetch_pair_history(df1, df2, (token_id1, token_id2))

def fetch_live_pairprice(token_id1, token_id2):
    token_id1 = token_id1.upper()
    token_id2 = token_id2.upper()

    token_id1 = symbol_to_id(token_id1)
    if type(token_id1) == bool:
        return False

    token1_price = fetch_live_price(token_id1)
    if type(token1_price) == bool:
        return False

    if token_id2 == 'USD':
        return token1_price

    token_id2 = symbol_to_id(token_id2)
    if type(token_id2) == bool:
        return False

    token2_price = fetch_live_price(token_id2)
    if type(token2_price) == bool:
        return False

    return round(float(token1_price)/float(token2_price), 5)
    
def fetch_yearly(token_id1, token_id2, year):
    
    start_date = "{}-01-01".format(year)
    end_date = "{}-12-31".format(year)

    return fetch_by_date(token_id1, token_id2, start_date, end_date)


def fetch_by_date(token_id1, token_id2, start, end):
    token_id1 = token_id1.upper()
    token_id2 = token_id2.upper()

    df1 = read_file("{}.dat".format(token_id1))
    df1 = validate_df(df1, token_id1)

    if type(df1) == bool:
        return False

    start_date = "{}T00:00:00.000Z".format(start)
    end_date = "{}T00:00:00.000Z".format(end)

    df1 = df1[(df1["date"]>=start_date) & (df1["date"]<=end_date)]

    if token_id2 == "USD":
        return format_response_js(df1, (token_id1, token_id2))

    df2 = read_file("{}.dat".format(token_id2))
    df2 = validate_df(df2, token_id2)

    if type(df2) == bool:
        return False

    df2 = df2[(df2["date"]>=start_date) & (df2["date"]<=end_date)]

    return fetch_pair_history(df1, df2, (token_id1, token_id2))


def update_history():
    symbols = glob.glob("*.dat")
    symbols = [symbol.split(".")[0] for symbol in symbols]
    symbols.remove("symbols")

    return all([update_price(symbol) for symbol in symbols])
