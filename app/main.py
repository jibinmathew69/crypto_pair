from datetime import date
from fastapi import FastAPI
from get_price import fetch_price, fetch_live_pairprice, fetch_yearly, update_history, fetch_by_date
from fetch_tokens import update_symbols

app = FastAPI()

@app.get("/history/{token_id1}/{token_id2}")
def get_history(token_id1: str, token_id2: str):
    return fetch_price(token_id1, token_id2)

@app.get("/live/{token_id1}/{token_id2}")
def live(token_id1: str, token_id2: str):
    return fetch_live_pairprice(token_id1, token_id2)

@app.get("/update_tokens")
def update_tokens():
    return update_symbols()
    
@app.get("/{year}/{token_id1}/{token_id2}")
def get_yearly(year: int, token_id1: str, token_id2: str):
    return fetch_yearly(token_id1, token_id2, year)

@app.get("/update_history")
def update_all_prices():
    return update_history()

@app.get("/{token_id1}/{token_id2}/")
def fetch(token_id1: str, token_id2: str, start: str, end: str):
    return fetch_by_date(token_id1, token_id2, start, end)

@app.get("/ytd")
def fetch_ytd(token_id1: str, token_id2: str):
    today = date.today()
    previous_year = date(today.year-1, today.month, today.day)
    return fetch_by_date(token_id1, token_id2, previous_year.strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d"))
