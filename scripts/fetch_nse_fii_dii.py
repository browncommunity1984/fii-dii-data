import requests
import csv

CSV_PATH = "data/fii_dii.csv"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://www.nseindia.com/"
}

URL = "https://www.nseindia.com/api/fiidiiTradeInfo"

def fetch_data():
    try:
        r = requests.get(URL, headers=HEADERS, timeout=15)
        r.raise_for_status()
        data = r.json()

        if "data" not in data or len(data["data"]) == 0:
            print("No data returned.")
            return None

        return data["data"]

    except Exception as e:
        print("Error:", e)
        return None


def save_csv(records):
    headers = [
        "date",
        "fii_buy", "fii_sell", "fii_net",
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

    print("Saved:", len(records), "rows")


def main():
    print("Fetching FII/DII data…")
    records = fetch_data()

    if records:
        save_csv(records)
    else:
        print("Failed to fetch data.")


if __name__ == "__main__":
    main()
