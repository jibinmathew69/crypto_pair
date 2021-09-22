import datetime
import pandas as pd
from pandas.io import json

def clean_json(json_data, columns: list):
    df = pd.DataFrame(json_data)
    if "priceUsd" in df.columns:
        df["priceUsd"] = df["priceUsd"].astype(float)
        df["priceUsd"] = df["priceUsd"].round(5)
    return df[columns]

def get_start_end_date(df):
    try:
        return (df.iloc[0]["date"], df.iloc[-1]["date"])
    except:
        return False

def get_prices(df):
    return df['priceUsd'].to_list()

def get_extremes(df):
    if df.shape < 1:
        return False
    return (df['priceUsd'].min(), df['priceUsd'].max())

def get_date_and_price(df):
    def get_date(date_string):
        date_parts = datetime.datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%fZ').date()
        return "Date({}, {}, {})".format(date_parts.year, date_parts.month-1, date_parts.day) 

    return df.apply(lambda tdf: [get_date(tdf["date"]), tdf["priceUsd"]], axis=1).to_list()

def date_intersection(df1, df2):
    df = pd.merge(df1, df2, how='inner', on=["time"], suffixes=['_df1', '_df2'])
    return df

def price_ratios(df):
    df["priceUsd"] = df["priceUsd_df1"] / df["priceUsd_df2"]
    df["priceUsd"] = df["priceUsd"].round(5)
    df.drop(['priceUsd_df1', 'priceUsd_df2', 'date_df1'], axis = 1, inplace=True)
    df.rename(columns={"date_df2": "date"}, inplace=True)

    return df