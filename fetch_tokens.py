import requests

TOKEN_URL = "https://api.coincap.io/v2/assets"

def fetch_token_symbol():
    response = requests.get(TOKEN_URL)

    if response.status_code != 200:
        return False
    
    response = response.json()
    return response["data"]
    