import requests
import pandas as pd
from datetime import datetime

# Output file
CSV_PATH = "data/fii_dii.csv"

# NSE API endpoint for FII/DII cash market activity
URL = "https://www.nseindia.com/api/fiidiiTradeInfo"

# NSE requires headers
HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

def fetch_data():
    session = requests.Session()
    session.headers.update(HEADERS)

    try:
        response = session.get(URL, timeout=10)
        data = response.json()
    except Exception as e:
        print("Error fetching data:", e)
        return None

    # Extract cash market data
    cash = data.get("data", [])

    if not cash:
        print("No data received")
        return None

    latest = cash[0]  # Latest day

    # Extract values
    date_str = latest["date"]
    fii_net = latest["fii_net"]
    dii_net = latest["dii_net"]

    # Format date to YYYY-MM-DD
    try:
        date_fmt = datetime.strptime(date_str, "%d-%b-%Y").strftime("%Y-%m-%d")
    except:
        date_fmt = date_str

    return {
        "date": date_fmt,
        "fii_net": fii_net,
        "dii_net": dii_net
    }

def update_csv():
    new = fetch_data()
    if new is None:
        return

    print("Fetched:", new)

    try:
        df = pd.read_csv(CSV_PATH)
    except:
        df = pd.DataFrame(columns=["date", "fii_net", "dii_net"])

    # Avoid duplicates
    if new["date"] in df["date"].values:
        print("Already updated for today")
        return

    df = pd.concat([df, pd.DataFrame([new])], ignore_index=True)
    df.to_csv(CSV_PATH, index=False)
    print("CSV updated.")

if __name__ == "__main__":
    update_csv()
