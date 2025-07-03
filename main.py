import requests
import time

def get_live_price(base="EUR", quote="USD"):
    url = f"https://api.frankfurter.app/latest?from={base}&to={quote}"
    try:
        response = requests.get(url)
        print("🔍 Raw JSON:", response.text)  # Debug print
        data = response.json()
        rate = data["rates"][quote]
        return round(rate, 5)
    except Exception as e:
        print("❌ Error fetching price:", e)
        return None

if __name__ == "__main__":
    while True:
        price = get_live_price("EUR", "USD")
        if price:
            print(f"✅ EUR/USD: {price}")
        else:
            print("⚠️ Could not fetch live price.")
        time.sleep(5)