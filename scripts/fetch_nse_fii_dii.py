import requests
import csv
import os
from datetime import datetime

CSV_PATH = "data/fii_dii.csv"

URL = "https://www.nseindia.com/api/fiidiiDashboard"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Referer": "https://www.nseindia.com/"
}

def fetch_data():
    try:
        session = requests.Session()
        session.get("https://www.nseindia.com/", headers=HEADERS)

        response = session.get(URL, headers=HEADERS)

        if response.status_code != 200:
            print("Error: NSE returned", response.status_code)
            return None

        data = response.json()

        # Cash Market data
        cash = data["data"]["cash"]

        if len(cash) == 0:
            print("Error: Cash list empty")
            return None

        latest = cash[0]  # today's data

        result = {
            "date": latest["date"],
            "fii_buy": latest["FII_BUY"],
            "fii_sell": latest["FII_SELL"],
            "dii_buy": latest["DII_BUY"],
            "dii_sell": latest["DII_SELL"]
        }

        print("Fetched:", result)
        return result

    except Exception as e:
        print("Error fetching data:", e)
        return None


def save_to_csv(row):
    file_exists = os.path.isfile(CSV_PATH)

    with open(CSV_PATH, mode="a", newline="") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(["date", "fii_buy", "fii_sell", "dii_buy", "dii_sell"])

        writer.writerow([
            row["date"],
            row["fii_buy"],
            row["fii_sell"],
            row["dii_buy"],
            row["dii_sell"]
        ])

        print("Saved:", row)


def main():
    row = fetch_data()
    if row:
        save_to_csv(row)
    else:
        print("No data saved.")


if __name__ == "__main__":
    main()
