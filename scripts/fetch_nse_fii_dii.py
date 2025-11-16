import requests
import csv
from datetime import datetime, timedelta

CSV_PATH = "data/fii_dii.csv"

# NSE headers (important)
HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://www.nseindia.com/"
}

def fetch_data_for_date(date_str):
    """Fetch FII/DII cash market data for a specific date."""
    url = f"https://www.nseindia.com/api/market-data-pre-open?key=fiiDiiCash&date={date_str}"

    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        if "data" not in data or not data["data"]:
            return None

        return data["data"][0]

    except Exception:
        return None


def save_to_csv(rows):
    headers = [
        "date", "fii_buy", "fii_sell", "fii_net",
        "dii_buy", "dii_sell", "dii_net"
    ]

    with open(CSV_PATH, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)


def main():
    today = datetime.now()
    start_day = today - timedelta(days=365)

    all_rows = []

    print("Fetching last 365 days FII/DII data...")

    for i in range(366):
        day = start_day + timedelta(days=i)
        date_str = day.strftime("%d-%m-%Y")

        print("Checking:", date_str)

        data = fetch_data_for_date(date_str)
        if data:
            row = [
                date_str,
                data.get("fiiBuyValue", 0),
                data.get("fiiSellValue", 0),
                data.get("fiiNetValue", 0),
                data.get("diiBuyValue", 0),
                data.get("diiSellValue", 0),
                data.get("diiNetValue", 0),
            ]
            all_rows.append(row)

    if all_rows:
        save_to_csv(all_rows)
        print("Saved", len(all_rows), "days of data to CSV.")
    else:
        print("No data fetched.")


if __name__ == "__main__":
    main()
