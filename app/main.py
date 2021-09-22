from datetime import date
from fastapi import FastAPI
from get_price import fetch_price, fetch_live_pairprice, fetch_yearly, update_history, fetch_by_date
from fetch_tokens import update_symbols

app = FastAPI()

@app.get("/history/")
def get_history(_from: str, _to: str):
    return fetch_price(_from, _to)

@app.get("/live/")
def live(_from: str, _to: str):
    return fetch_live_pairprice(_from, _to)

@app.get("/update_tokens/")
def update_tokens():
    return update_symbols()

@app.get("/update_history/")
def update_all_prices():
    return update_history()

@app.get("/ytd/")
def fetch_ytd(_from: str, _to: str):
    today = date.today()
    previous_year = date(today.year-1, today.month, today.day)
    return fetch_by_date(_from, _to, previous_year.strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d"))

@app.get("/mtd/{month}")
def fetch_mtd(month: int, _from: str, _to: str):
    today = date.today()
    previous_months = date(today.year, today.month-month, today.day)
    return fetch_by_date(_from, _to, previous_months.strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d"))

@app.get("/{year}/")
def get_yearly(year: int, _from: str, _to: str):
    return fetch_yearly(_from, _to, year)

@app.get("/")
def fetch(_from: str, _to: str, start: str, end: str):
    return fetch_by_date(_from, _to, start, end)

