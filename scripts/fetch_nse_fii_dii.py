import requests
import csv
import os
from datetime import datetime

CSV_PATH = "data/fii_dii.csv"

NSE_URL = "https://www.nseindia.com/api/fiidiiTradeReact"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.nseindia.com/",
    "Connection": "keep-alive"
}

def fetch_data():
    try:
        session = requests.Session()
        session.get("https://www.nseindia.com/", headers=HEADERS)  # required
        response = session.get(NSE_URL, headers=HEADERS)

        if response.status_code != 200:
            print("Error: NSE returned status", response.status_code)
            return None

        data = response.json()

        if "data" not in data or len(data["data"]) == 0:
            print("Error: No data received")
            return None

        latest = data["data"][0]

        result = {
            "date": latest["date"],
            "fii_buy": latest.get("FII_BUY", 0),
            "fii_sell": latest.get("FII_SELL", 0),
            "dii_buy": latest.get("DII_BUY", 0),
            "dii_sell": latest.get("DII_SELL", 0)
        }

        print("Fetched:", result)
        return result

    except Exception as e:
        print("Error fetching data:", e)
        return None


def save_to_csv(row):
    file_exists = os.path.isfile(CSV_PATH)

    with open(CSV_PATH, mode="a", newline="") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["date", "fii_buy", "fii_sell", "dii_buy", "dii_sell"])

        writer.writerow([
            row["date"], row["fii_buy"], row["fii_sell"], row["dii_buy"], row["dii_sell"]
        ])

        print("Saved row:", row)


def main():
    row = fetch_data()
    if row:
        save_to_csv(row)
    else:
        print("No data saved.")

if __name__ == "__main__":
    main()

