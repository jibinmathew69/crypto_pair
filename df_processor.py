import re
import pandas as pd
from pandas.io import json

def clean_json(json_data, columns: list):
    df = pd.DataFrame(json_data)

    return df[columns]

def get_start_end_date(df):
    return (df.iloc[0]["date"], df.iloc[-1]["date"])

def get_prices(df):
    return df['priceUsd'].to_list()

