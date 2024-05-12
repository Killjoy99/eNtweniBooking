import requests

def connect(base_url: str = "http://127.0.0.1:8000", endpoint: str = None, data=None):
    url = f"{base_url}{endpoint}" if endpoint else base_url
    
    headers = {"Accept": "application/json"}
    
    response = requests.get(url, headers=headers) if not data else requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None
