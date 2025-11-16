import requests
import csv
import datetime
import time

CSV_PATH = "data/fii_dii.csv"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.nseindia.com/"
}

HOME_URL = "https://www.nseindia.com"
DATA_URL = "https://www.nseindia.com/api/historical/fiidii?from={}&to={}"


def fetch_historical():
    """Fetch 365 days of FII/DII historical data from NSE."""
    try:
        session = requests.Session()

        # Step 1: Visit homepage for mandatory cookies
        session.get(HOME_URL, headers=HEADERS, timeout=15)
        time.sleep(1)  # NSE rate-limit bypass

        # Date range
        to_date = datetime.date.today()
        from_date = to_date - datetime.timedelta(days=365)

        url = DATA_URL.format(from_date.strftime("%d-%m-%Y"), to_date.strftime("%d-%m-%Y"))
        print("Fetching:", url)

        response = session.get(url, headers=HEADERS, timeout=15)
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
    with open(CSV_PATH, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "fii_buy", "fii_sell", "fii_net", "dii_buy", "dii_sell", "dii_net"])

        for row in records:
            writer.writerow([
                row.get("date", ""),
                row.get("fiiBuyValue", 0),
                row.get("fiiSellValue", 0),
                row.get("fiiNetValue", 0),
                row.get("diiBuyValue", 0),
                row.get("diiSellValue", 0),
                row.get("diiNetValue", 0),
            ])

    print(f"Saved {len(records)} rows.")


def main():
    print("Fetching historical FII/DII data…")
    data = fetch_historical()

    if data:
        save_csv(data)
    else:
        print("Failed to fetch history.")


if __name__ == "__main__":
    main()
