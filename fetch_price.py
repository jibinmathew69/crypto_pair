import requests


URL = "https://api.coincap.io/v2/assets/{token_id}/history?interval=d1"

def fetch_token_price(token_id):
    url = URL.format(token_id = token_id)

    response = requests.get(url)

    if response.status_code != 200:
        return False
    
    response = response.json()

    return response

