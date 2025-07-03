import json
import uuid
import time
from datetime import datetime

ACCOUNTS_FILE = "accounts.json"

def load_accounts():
    with open(ACCOUNTS_FILE, "r") as file:
        return json.load(file)

def save_accounts(data):
    with open(ACCOUNTS_FILE, "w") as file:
        json.dump(data, file, indent=2)

def place_trade(pair, direction, amount):
    accounts = load_accounts()

    # Simulate master trade
    trade_id = str(uuid.uuid4())[:8]
    price = 1.1782  # use live price later

    trade = {
        "id": trade_id,
        "pair": pair,
        "direction": direction,
        "amount": amount,
        "price": price,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    print(f"📌 Master {direction.upper()} {amount} of {pair} at {price}")
    accounts["master"]["trades"].append(trade)
    accounts["master"]["balance"] -= amount  # simplified

    # Copy to clients
    for client_id, client_data in accounts["clients"].items():
        copied_trade = trade.copy()
        copied_trade["copied_from"] = "master"
        print(f"↪️  Copied to {client_id}")
        client_data["trades"].append(copied_trade)
        client_data["balance"] -= amount  # simplified

    save_accounts(accounts)

# Example usage
if __name__ == "__main__":
    place_trade("EUR/USD", "buy", 100)