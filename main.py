import requests
from datetime import datetime
import os
import csv


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
    
def log_rates(data):
    date = data["date"]
    rates = data["rates"]
    
    file_exists = os.path.exists("rates.csv")
    
    with open("rates.csv", "a", newline="") as f:
        fieldnames = ["date", "CAD_to_JPY", "CAD_to_EUR", "CAD_to_USD", "CAD_to_BSD"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()
            
        writer.writerow({
            "date": date,
            "CAD_to_JPY": rates["JPY"],
            "CAD_to_EUR": rates["EUR"],
            "CAD_to_USD": rates["USD"],
            "CAD_to_BSD": rates["USD"]
        })
        
        print(f"Rates logged to rates.csv")
    
def check_alerts(data):
    rates = data["rates"]
    
    alerts = {
        "JPY": {"threshold" : 115, "direction": "above"},
        "EUR": {"threshold" : 0.60, "direction": "below"},
        "USD": {"threshold" : 0.70, "direction": "below"}
    }
    
    print("Checking alerts...")
    triggered = False
    
    for currency, config in alerts.items():
        rate = rates.get(currency)
        if rate is None:
            continue
        
        if config["direction"] == "above" and rate > config["threshold"]:
            print(f"⚠️  ALERT: CAD → {currency} is {rate} (above {config['threshold']})")
            triggered = True
        elif config["direction"] == "below" and rate < config["threshold"]:
            print(f"  ⚠️  ALERT: CAD → {currency} is {rate} (below {config['threshold']})")
            triggered = True
    
    if not triggered:
        print("No alerts triggered.")
        
    print()

if __name__ == "__main__":
    print(f"Fetching rates at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    data = get_exchange_rate()
    display_rates(data)
    log_rates(data)
    check_alerts(data)
