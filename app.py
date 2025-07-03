import streamlit as st
import requests
import json
from datetime import datetime
import uuid
import pandas as pd

# --- Config ---
ACCOUNTS_FILE = "accounts.json"
API_KEY = st.secrets["API_KEY"]

# --- Load Data ---
def load_accounts():
    with open(ACCOUNTS_FILE, "r") as file:
        return json.load(file)

def save_accounts(data):
    with open(ACCOUNTS_FILE, "w") as file:
        json.dump(data, file, indent=2)

import ast
USERS = json.loads(st.secrets["USERS"])


def get_live_price(base="EUR", quote="USD"):
    url = f"https://api.twelvedata.com/price?symbol={base}/{quote}&apikey={API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()
        return float(data["price"])
    except Exception as e:
        st.error(f"Error fetching live price: {e}")
        return "N/A"

def place_trade(direction, amount=100):
    data = load_accounts()
    price = get_live_price("EUR", "USD")
    trade_id = str(uuid.uuid4())[:8]

    trade = {
        "id": trade_id,
        "pair": "EUR/USD",
        "direction": direction,
        "amount": amount,
        "price": price,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "open"
    }

    if direction.lower() == "buy":
        data["master"]["balance"] -= amount
        for client_data in data["clients"].values():
            client_data["balance"] -= amount

    for client_data in data["clients"].values():
        copied_trade = trade.copy()
        copied_trade["copied_from"] = "master"
        client_data["trades"].append(copied_trade)

    data["master"]["trades"].append(trade)
    save_accounts(data)

def calculate_pnl(trade, current_price):
    try:
        entry_price = trade["price"]
        amount = trade["amount"]
        direction = trade["direction"]

        if direction.lower() == "buy":
            pnl = (current_price - entry_price) * amount
        elif direction.lower() == "sell":
            pnl = (entry_price - current_price) * amount
        else:
            pnl = 0
        return round(pnl, 2)
    except:
        return 0

def show_client_trades(cid, cdata, price):
    trades = cdata["trades"]
    enriched_trades = []
    total_pnl = 0

    for t in trades:
        pnl = calculate_pnl(t, price)
        total_pnl += pnl
        enriched_trades.append({
            "ID": t["id"],
            "Direction": t["direction"],
            "Amount": t["amount"],
            "Entry Price": t["price"],
            "Current Price": price,
            "P&L": pnl,
            "Time": t["timestamp"]
        })

    color = "green" if total_pnl > 0 else "red" if total_pnl < 0 else "black"
    st.markdown(f"<h5>💼 Portfolio P&L: <span style='color:{color}'>{round(total_pnl, 2)}</span></h5>", unsafe_allow_html=True)

    df = pd.DataFrame(enriched_trades)

    def color_pnl(val):
        return f"color: {'green' if val > 0 else 'red' if val < 0 else 'black'}; font-weight: bold"

    styled_df = df.style.applymap(color_pnl, subset=["P&L"])
    st.dataframe(styled_df, use_container_width=True)

# --- Streamlit App ---
st.set_page_config(page_title="Forex Copy Trading Simulator", layout="wide")

# --- Login Section ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None

if not st.session_state.logged_in:
    st.title("🔐 Login to Copy Trading App")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in USERS and USERS[username]["password"] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"✅ Logged in as {username}")
            st.rerun()
        else:
            st.error("❌ Invalid credentials")
    st.stop()

# --- Main App ---
data = load_accounts()
username = st.session_state.username
st.sidebar.success(f"Logged in as: {username}")

price = get_live_price("EUR", "USD")
st.title("📈 Forex Copy Trading Simulator (Demo)")
st.metric("💱 EUR/USD Price", value=price)

# --- Master Controls ---
if username == "master":
    st.write("### Place Trade (Master)")
    if st.button("🟢 Buy EUR/USD"):
        place_trade("buy")
        st.rerun()
    if st.button("🔴 Sell EUR/USD"):
        place_trade("sell")
        st.rerun()
# --- Account Balances ---
st.write("## 🧾 Account Balance")
if username == "master":
    cols = st.columns(len(data["clients"]) + 1)
    cols[0].metric("Master", f"${data['master']['balance']:.2f}")
    for i, (cid, cdata) in enumerate(data["clients"].items(), start=1):
        cols[i].metric(cid.capitalize(), f"${cdata['balance']:.2f}")
else:
    st.metric(username.capitalize(), f"${data['clients'][username]['balance']:.2f}")

# --- Trade Logs ---
if username == "master":
    st.write("### Master Trades")
    st.table(data["master"]["trades"])

    st.write("### Client Trades")
    for cid, cdata in data["clients"].items():
        show_client_trades(cid, cdata, price)
else:
    st.write(f"### 👥 {username.capitalize()} Trades")
    show_client_trades(username, data["clients"][username], price)
    
    
# --- Logout ---
if st.sidebar.button("🚪 Logout"):
    st.session_state.logged_in = False
    st.session_state.username = None
    st.rerun()