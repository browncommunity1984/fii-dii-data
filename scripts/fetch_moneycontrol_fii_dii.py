import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def fetch_table(url, category):
    print(f"Fetching {category} data...")

    response = requests.get(url, headers=HEADERS, timeout=15)
    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find("table", {"class": "mctable1"})

    if table is None:
        print(f"❌ Table not found for {category}")
        return pd.DataFrame()

    rows = []
    for tr in table.find_all("tr")[1:]:
        tds = [td.text.strip() for td in tr.find_all("td")]
        if len(tds) < 4:
            continue

        date_raw = tds[0]
        buy = tds[1].replace(",", "")
        sell = tds[2].replace(",", "")
        net = tds[3].replace(",", "")

        try:
            date_obj = datetime.strptime(date_raw, "%d-%b-%Y").date()
        except:
            continue

        rows.append([category, date_obj, float(buy), float(sell), float(net)])

    df = pd.DataFrame(rows, columns=["CATEGORY", "DATE", "BUY", "SELL", "NET"])
    return df


url_fii = "https://www.moneycontrol.com/stocks/marketstats/fii-dii-activity/institutional/cash/institutionType/FII"
url_dii = "https://www.moneycontrol.com/stocks/marketstats/fii-dii-activity/institutional/cash/institutionType/DII"

df_fii = fetch_table(url_fii, "FII/FPI")
df_dii = fetch_table(url_dii, "DII")

df = pd.concat([df_fii, df_dii], ignore_index=True)
df = df.sort_values("DATE")

output_path = "data/fii_dii.csv"
df.to_csv(output_path, index=False)

print(f"✅ Done. Saved {len(df)} rows to {output_path}")
