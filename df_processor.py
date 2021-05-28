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

def date_intersection(df1, df2):
    df = pd.merge(df1, df2, how='inner', on=["time"], suffixes=['_df1', '_df2'])
    df["priceUsd"] = df["priceUsd_df1"] / df["priceUsd_df2"]
    df["priceUsd"].round(2, inplace=True)
    del df[['priceUsd_df1', 'priceUsd_df2']]

    return df
