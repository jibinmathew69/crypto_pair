import requests
from fetch_tokens import symbol_to_id

MCAP_URL = "https://api.coincap.io/v2/assets/{asset}"

def get_supply(token_id):
    token_id = token_id.upper()
    token_name = symbol_to_id(token_id)
    
    if type(token_name) == bool:
        return False

    mcap_url = MCAP_URL.format(asset=token_name)
    response = requests.get(mcap_url)

    if response.status_code != 200:
        return False
    
    response = response.json()
    result = {
        "error": None,
        "payload": {
            "price": response['data']['priceUsd'],
            "supply": {
                "total": response['data']["maxSupply"],
                "issued": response['data']["supply"],
            },
            "symbol": token_id,
            "name": token_name,
        }
    }
    return result

