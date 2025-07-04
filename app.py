# import streamlit as st
# import requests
# import json
# from datetime import datetime
# import uuid
# import pandas as pd
# from pdf_report import generate_pdf_report
# from send_email import send_pdf_email

# # --- Config ---
# ACCOUNTS_FILE = "accounts.json"
# API_KEY = st.secrets["API_KEY"]

# # --- Load Data ---
# def load_accounts():
#     with open(ACCOUNTS_FILE, "r") as file:
#         return json.load(file)

# def save_accounts(data):
#     with open(ACCOUNTS_FILE, "w") as file:
#         json.dump(data, file, indent=2)

# import ast
# USERS = json.loads(st.secrets["USERS"])


# def get_live_price(base="EUR", quote="USD"):
#     url = f"https://api.twelvedata.com/price?symbol={base}/{quote}&apikey={API_KEY}"
#     try:
#         response = requests.get(url)
#         data = response.json()
#         return float(data["price"])
#     except Exception as e:
#         st.error(f"Error fetching live price: {e}")
#         return "N/A"

# def place_trade(direction, amount=100):
#     data = load_accounts()
#     price = get_live_price("EUR", "USD")
#     trade_id = str(uuid.uuid4())[:8]

#     trade = {
#         "id": trade_id,
#         "pair": "EUR/USD",
#         "direction": direction,
#         "amount": amount,
#         "price": price,
#         "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#         "status": "open"
#     }

#     if direction.lower() == "buy":
#         data["master"]["balance"] -= amount
#         for client_data in data["clients"].values():
#             client_data["balance"] -= amount

#     for client_data in data["clients"].values():
#         copied_trade = trade.copy()
#         copied_trade["copied_from"] = "master"
#         client_data["trades"].append(copied_trade)

#     data["master"]["trades"].append(trade)
#     save_accounts(data)

# def calculate_pnl(trade, current_price):
#     try:
#         entry_price = trade["price"]
#         amount = trade["amount"]
#         direction = trade["direction"]

#         if direction.lower() == "buy":
#             pnl = (current_price - entry_price) * amount
#         elif direction.lower() == "sell":
#             pnl = (entry_price - current_price) * amount
#         else:
#             pnl = 0
#         return round(pnl, 2)
#     except:
#         return 0

# def show_client_trades(cid, cdata, price):
#     trades = cdata["trades"]
#     enriched_trades = []
#     total_pnl = 0

#     for t in trades:
#         pnl = calculate_pnl(t, price)
#         total_pnl += pnl
#         enriched_trades.append({
#             "ID": t["id"],
#             "Direction": t["direction"],
#             "Amount": t["amount"],
#             "Entry Price": t["price"],
#             "Current Price": price,
#             "P&L": pnl,
#             "Time": t["timestamp"]
#         })

#     color = "green" if total_pnl > 0 else "red" if total_pnl < 0 else "black"
#     st.markdown(f"<h5>💼 Portfolio P&L: <span style='color:{color}'>{round(total_pnl, 2)}</span></h5>", unsafe_allow_html=True)

#     df = pd.DataFrame(enriched_trades)

#     def color_pnl(val):
#         return f"color: {'green' if val > 0 else 'red' if val < 0 else 'black'}; font-weight: bold"

#     styled_df = df.style.applymap(color_pnl, subset=["P&L"])
#     st.dataframe(styled_df, use_container_width=True)

# # --- Streamlit App ---
# st.set_page_config(page_title="Forex Copy Trading Simulator", layout="wide")

# # --- Login Section ---
# if "logged_in" not in st.session_state:
#     st.session_state.logged_in = False
#     st.session_state.username = None

# if not st.session_state.logged_in:
#     st.title("🔐 Login to Copy Trading App")
#     username = st.text_input("Username")
#     password = st.text_input("Password", type="password")
#     if st.button("Login"):
#         if username in USERS and USERS[username]["password"] == password:
#             st.session_state.logged_in = True
#             st.session_state.username = username
#             st.success(f"✅ Logged in as {username}")
#             st.rerun()
#         else:
#             st.error("❌ Invalid credentials")
#     st.stop()

# # --- Main App ---
# data = load_accounts()
# username = st.session_state.username
# st.sidebar.success(f"Logged in as: {username}")

# price = get_live_price("EUR", "USD")
# st.title("📈 Forex Copy Trading Simulator (Demo)")
# st.metric("💱 EUR/USD Price", value=price)

# # --- Master Controls ---
# if username == "master":
#     st.write("### Place Trade (Master)")

#     trade_amount = st.number_input("Enter Trade Amount ($)", min_value=10, max_value=10000, value=100, step=50)

#     col1, col2 = st.columns(2)
#     with col1:
#         if st.button("🟢 Buy EUR/USD"):
#             place_trade("buy", amount=trade_amount)
#             st.rerun()
#     with col2:
#         if st.button("🔴 Sell EUR/USD"):
#             place_trade("sell", amount=trade_amount)
#             st.rerun()
# # --- Account Balances ---
# st.write("## 🧾 Account Balance")
# if username == "master":
#     cols = st.columns(len(data["clients"]) + 1)
#     cols[0].metric("Master", f"${data['master']['balance']:.2f}")
#     for i, (cid, cdata) in enumerate(data["clients"].items(), start=1):
#         cols[i].metric(cid.capitalize(), f"${cdata['balance']:.2f}")
# else:
#     st.metric(username.capitalize(), f"${data['clients'][username]['balance']:.2f}")

# # --- Trade Logs ---
# # 📄 PDF Generation for Clients
# if username != "master":
#     st.write(f"### 👥 {username.capitalize()} Trades")

#     trades = data["clients"][username]["trades"]
#     enriched_trades = []
#     total_pnl = 0

#     for t in trades:
#         pnl = calculate_pnl(t, price)
#         total_pnl += pnl
#         enriched_trades.append({
#             "ID": t["id"],
#             "Direction": t["direction"],
#             "Amount": t["amount"],
#             "Entry Price": t["price"],
#             "Current Price": price,
#             "P&L": pnl,
#             "Time": t["timestamp"]
#         })

#     color = "green" if total_pnl > 0 else "red" if total_pnl < 0 else "black"
#     st.markdown(f"<h5>💼 Portfolio P&L: <span style='color:{color}'>{round(total_pnl, 2)}</span></h5>", unsafe_allow_html=True)

#     df = pd.DataFrame(enriched_trades)

#     def color_pnl(val):
#         return f"color: {'green' if val > 0 else 'red' if val < 0 else 'black'}; font-weight: bold"

#     st.dataframe(df.style.applymap(color_pnl, subset=["P&L"]), use_container_width=True)

#     # 📥 PDF Download
#     if st.button("📄 Download PDF Report"):
#         filename = f"{username}_report.pdf"
#         generate_pdf_report(username, enriched_trades, data["clients"][username]["balance"], total_pnl, filename)
#         with open(filename, "rb") as f:
#             st.download_button(label="⬇️ Click to Download PDF", data=f, file_name=filename, mime="application/pdf")
#         # Email form
#     with st.expander("📧 Send PDF Report via Email"):
#         recipient = st.text_input("Recipient Email", placeholder="someone@example.com")
#         if st.button("📤 Send Email"):
#             if recipient:
#                 success = send_pdf_email(
#                     recipient=recipient,
#                     subject="📈 Your Forex Trading Report",
#                     body="Hello,\n\nPlease find your attached trading report.\n\n- Forex Trading App",
#                     attachment_path=filename
#                 )
#                 if success:
#                     st.success("✅ Email sent successfully!")
#                 else:
#                     st.error("❌ Failed to send email. Check logs.")
#             else:
#                 st.warning("⚠️ Please enter a valid email address.")

# # 📄 PDF Generation for Master
# if username == "master":
#     st.write("### Master Trades")

#     trades = data["master"]["trades"]
#     enriched_trades = []
#     total_pnl = 0

#     for t in trades:
#         pnl = calculate_pnl(t, price)
#         total_pnl += pnl
#         enriched_trades.append({
#             "ID": t["id"],
#             "Direction": t["direction"],
#             "Amount": t["amount"],
#             "Entry Price": t["price"],
#             "Current Price": price,
#             "P&L": pnl,
#             "Time": t["timestamp"]
#         })

#     df = pd.DataFrame(enriched_trades)
#     st.dataframe(df, use_container_width=True)

#     if st.button("📄 Download PDF Report"):
#         filename = f"{username}_report.pdf"
#         generate_pdf_report(username, enriched_trades, data["master"]["balance"], total_pnl, filename)
    
#         with open(filename, "rb") as f:
#             st.download_button(label="⬇️ Click to Download PDF", data=f, file_name=filename, mime="application/pdf")

#         with st.expander("📧 Send PDF Report via Email"):
#             recipient = st.text_input("Recipient Email", placeholder="example@gmail.com")
#             send_clicked = st.button("📤 Send Email")
        
#             if send_clicked:
#                 if recipient:
#                     success = send_pdf_email(
#                     recipient=recipient,
#                     subject="📈 Your Forex Copy Trading Report",
#                     body="Hi,\n\nPlease find attached your trading report.\n\nRegards,\nForex Trading App",
#                     attachment_path=filename
#                 )
#                     if success:
#                         st.success("✅ Email sent successfully!")
#                     else:
#                         st.error("❌ Failed to send email.")
#                 else:
#                     st.warning("⚠️ Please enter a recipient email.")

#     st.write("### Client Trades")
#     for cid, cdata in data["clients"].items():
#         show_client_trades(cid, cdata, price)
    
# # --- Logout ---
# if st.sidebar.button("🚪 Logout"):
#     st.session_state.logged_in = False
#     st.session_state.username = None
#     st.rerun()
# ✅ FINAL CLEAN CODE WITH PDF DOWNLOAD + EMAIL FUNCTIONALITY

import streamlit as st
import requests
import json
from datetime import datetime
import uuid
import pandas as pd
from pdf_report import generate_pdf_report
from send_email import send_pdf_email

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

USERS = json.loads(st.secrets["USERS"])

# --- Price Fetch ---
def get_live_price(base="EUR", quote="USD"):
    url = f"https://api.twelvedata.com/price?symbol={base}/{quote}&apikey={API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()
        return float(data["price"])
    except Exception as e:
        st.error(f"Error fetching live price: {e}")
        return "N/A"

# --- Place Trade ---
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

# --- Calculate P&L ---
def calculate_pnl(trade, current_price):
    try:
        entry_price = trade["price"]
        amount = trade["amount"]
        direction = trade["direction"]
        pnl = (current_price - entry_price) * amount if direction == "buy" else (entry_price - current_price) * amount
        return round(pnl, 2)
    except:
        return 0

# --- Show Trades with P&L ---
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
    st.dataframe(df.style.applymap(lambda val: f"color: {'green' if val > 0 else 'red' if val < 0 else 'black'}; font-weight: bold" if isinstance(val, (int, float)) else None, subset=["P&L"]), use_container_width=True)

    return enriched_trades, total_pnl

# --- App Setup ---
st.set_page_config(page_title="Forex Copy Trading Simulator", layout="wide")

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
            st.rerun()
        else:
            st.error("❌ Invalid credentials")
    st.stop()

# --- Main Dashboard ---
data = load_accounts()
username = st.session_state.username
st.sidebar.success(f"Logged in as: {username}")
price = get_live_price("EUR", "USD")
st.title("📈 Forex Copy Trading Simulator (Demo)")
st.metric("💱 EUR/USD Price", value=price)

# --- Master ---
if username == "master":
    st.write("### 📊 Master Controls")
    amt = st.number_input("Trade Amount ($)", min_value=10, value=100, step=10)
    col1, col2 = st.columns(2)
    if col1.button("🟢 Buy EUR/USD"):
        place_trade("buy", amt)
        st.rerun()
    if col2.button("🔴 Sell EUR/USD"):
        place_trade("sell", amt)
        st.rerun()

# --- Balances ---
st.subheader("🧾 Account Balances")
if username == "master":
    cols = st.columns(len(data["clients"]) + 1)
    cols[0].metric("Master", f"${data['master']['balance']:.2f}")
    for i, (cid, cdata) in enumerate(data["clients"].items(), 1):
        cols[i].metric(cid.capitalize(), f"${cdata['balance']:.2f}")
else:
    st.metric(username.capitalize(), f"${data['clients'][username]['balance']:.2f}")

# --- Trades ---
st.subheader("📄 Trade Logs")

if username == "master":
    st.write("### Master Trades")
    enriched, pnl = show_client_trades("master", data["master"], price)

    if st.button("📄 Generate PDF Report"):
        filename = f"{username}_report.pdf"
        generate_pdf_report(username, enriched, data["master"]["balance"], pnl, filename)
        st.session_state.generated_pdf = filename
        st.success("✅ PDF created!")

    if "generated_pdf" in st.session_state:
        with open(st.session_state.generated_pdf, "rb") as f:
            st.download_button("⬇️ Download PDF", f, file_name=st.session_state.generated_pdf, mime="application/pdf")

        st.markdown("---")
        recipient = st.text_input("📧 Email Recipient", key="master_email")
        if st.button("📤 Send Email"):
            if recipient:
                result = send_pdf_email(
                    recipient,
                    "📈 Your Forex Master Report",
                    "Hi,\n\nAttached is your Master trading report.\n\nRegards,\nForex App",
                    st.session_state.generated_pdf
                )
                if result:
                    st.success("✅ Email sent!")
                else:
                    st.error("❌ Email failed.")
else:
    enriched, pnl = show_client_trades(username, data["clients"][username], price)
    if st.button("📄 Generate PDF Report"):
        filename = f"{username}_report.pdf"
        generate_pdf_report(username, enriched, data["clients"][username]["balance"], pnl, filename)
        st.session_state.generated_pdf = filename
        st.success("✅ PDF created!")

    if "generated_pdf" in st.session_state:
        with open(st.session_state.generated_pdf, "rb") as f:
            st.download_button("⬇️ Download PDF", f, file_name=st.session_state.generated_pdf, mime="application/pdf")

        st.markdown("---")
        recipient = st.text_input("📧 Email Recipient", key="client_email")
        if st.button("📤 Send Email"):
            if recipient:
                result = send_pdf_email(
                    recipient,
                    "📈 Your Forex Client Report",
                    "Hi,\n\nAttached is your trading report.\n\nRegards,\nForex App",
                    st.session_state.generated_pdf
                )
                if result:
                    st.success("✅ Email sent!")
                else:
                    st.error("❌ Email failed.")

# --- Logout ---
if st.sidebar.button("🚪 Logout"):
    st.session_state.logged_in = False
    st.session_state.username = None
    st.rerun()