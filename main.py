from fastapi import FastAPI
from get_price import fetch_price, fetch_live_price

app = FastAPI()

@app.get("/history/{token_id1}/{token_id2}")
def get_history(token_id1: str, token_id2: str):
    return fetch_price(token_id1, token_id2)

@app.get("/live/{token_id1}/{token_id2}")
def live(token_id1: str, token_id2: str):
    return fetch_live_price(token_id1, token_id2)
