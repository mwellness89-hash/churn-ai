# src/data/prepare_data.py
# Download and prepare Telco churn dataset

import os
import pandas as pd
from urllib.error import HTTPError, URLError


def download_training_data():
    """Download Telco customer churn dataset and save to data/raw."""
    # Create folders
    os.makedirs("data/raw", exist_ok=True)

    print("📥 Downloading Telco churn dataset...")

    # Working Telco churn CSV URL
    url = "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv"

    try:
        df = pd.read_csv(url)

        # Save locally
        output_path = "data/raw/telco_churn.csv"
        df.to_csv(output_path, index=False)

        print(f"✅ Downloaded {len(df)} customers")
        churn_rate = (df["Churn"].eq("Yes").sum() / len(df)) * 100
        print(f"📊 Churn rate: {churn_rate:.1f}%")
        print(f"💾 Saved to: {output_path}")

        return df

    except (HTTPError, URLError) as e:
        print(f"❌ Network/HTTP error while downloading data: {e}")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


if __name__ == "__main__":
    download_training_data()

