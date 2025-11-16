import requests
import csv
import time

CSV_PATH = "data/fii_dii.csv"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.nseindia.com/"
}

HOME_URL = "https://www.nseindia.com"
DATA_URL = "https://www.nseindia.com/api/fiidiiTradeInfo"


def fetch_data():
    try:
        session = requests.Session()

        # Step 1: Get NSE homepage to get cookies
        home = session.get(HOME_URL, headers=HEADERS, timeout=10)
        time.sleep(1)

        # Step 2: Request FII/DII API
        response = session.get(DATA_URL, headers=HEADERS, timeout=10)
        response.raise_for_status()

        data = response.json()

        if "data" not in data or not data["data"]:
            print("No data returned.")
            return None

        return data["data"]

    except Exception as e:
        print("Error:", e)
        return None


def save_csv(records):
    headers = [
        "date", "fii_buy", "fii_sell", "fii_net",
        "dii_buy", "dii_sell", "dii_net"
    ]

    with open(CSV_PATH, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)

        for item in records:
            writer.writerow([
                item.get("date", ""),
                item.get("fiiBuyValue", 0),
                item.get("fiiSellValue", 0),
                item.get("fiiNetValue", 0),
                item.get("diiBuyValue", 0),
                item.get("diiSellValue", 0),
                item.get("diiNetValue", 0),
            ])

    print(f"Saved {len(records)} rows.")


def main():
    print("Fetching FII/DII data…")
    records = fetch_data()

    if records:
        save_csv(records)
    else:
        print("Failed to fetch data.")


if __name__ == "__main__":
    main()
