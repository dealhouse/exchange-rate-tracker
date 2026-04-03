import requests
from datetime import datetime

BASE_URL = "https://api.frankfurter.app"
BASE_CURRENCY = "CAD"
TARGET_CURRENCIES = ["JPY", "EUR", "USD"]

def get_exchange_rate():
    currencies = ",".join(TARGET_CURRENCIES)
    url = f"{BASE_URL}/latest?from={BASE_CURRENCY}&to={currencies}"
    
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data

def display_rates(data):
    date = data["date"]
    base = data["base"]
    rates = data["rates"]
    
    print(f"\nExchange Rates - {date}")
    print(f"Base Currency: {base}")
    print("-" * 30)
    
    for currency, rate in rates.items():
        print(f"{base} -> {currency}: {rate}")
        
    print(f"{base} -> BSD: {rates['USD']}  (BSD pegged 1:1 to USD)")

        
    print()
    

if __name__ == "__main__":
    print(f"Fetching rates at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    data = get_exchange_rate()
    display_rates(data)
