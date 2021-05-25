from fastapi import FastAPI, Response, HTTPException

app = FastAPI()

@app.post("/get_history/{token_symbol}")
def get_history(token_symbol: str):
    pass
