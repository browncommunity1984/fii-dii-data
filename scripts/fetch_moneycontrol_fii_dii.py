import requests
import pandas as pd
import os

def fetch_moneycontrol_data(type_):
    url = f"https://www.moneycontrol.com/mc/widget/marketstats/fii_dii_activity/get_data?type={type_}&duration=1M"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    print(f"Fetching {type_.upper()} data...")
    r = requests.get(url, headers=headers)
    r.raise_for_status()

    data = r.json().get("data", [])
    return pd.DataFrame(data)

def main():
    fii_df = fetch_moneycontrol_data("fii")
    dii_df = fetch_moneycontrol_data("dii")

    if fii_df.empty or dii_df.empty:
        print("⚠ No data received!")
        return

    # Clean + merge
    fii_df["category"] = "FII/FPI"
    dii_df["category"] = "DII"
    df = pd.concat([fii_df, dii_df], ignore_index=True)

    # Output folder
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/fii_dii.csv", index=False)

    print(f"✅ Done. Saved {len(df)} rows to data/fii_dii.csv")

if __name__ == "__main__":
    main()
