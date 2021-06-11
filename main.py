from fastapi import FastAPI
from get_price import fetch_price, fetch_live_pairprice, fetch_yearly, update_history
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
    