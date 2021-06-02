import pandas as pd
from fetch_price import fetch_token_price, fetch_pair_history, format_response, fetch_live_price
from fetch_tokens import symbol_to_id
from df_processor import clean_json
from feather_io import write_file, read_file

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

    df1 = read_file(token_id1)
    df1 = validate_df(df1, token_id1)

    if type(df1) == bool:
        return False

    if token_id2 == "USD":
        return format_response(df1)

    df2 = read_file(token_id2)
    df2 = validate_df(df2, token_id2)

    if type(df2) == bool:
        return False

    return fetch_pair_history(df1, df2)

def fetch_live_price(token_id1, token_id2):
    token_id1 = token_id1.upper()
    token_id2 = token_id2.upper()

    token_id1 = symbol_to_id(token_id1)
    if type(token_id1) == bool:
        return False

    token1_price = fetch_live_price(token_id1)

    if token_id2 == 'USD':
        return token1_price

    token_id2 = symbol_to_id(token_id2)
    if type(token_id2) == bool:
        return False

    token2_price = fetch_live_price(token_id2)

    return round(token1_price/token2_price, 5)
    