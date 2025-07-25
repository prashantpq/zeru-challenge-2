import requests
import pandas as pd
from tqdm import tqdm
import time
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')
CHAIN_ID = "1"  # Ethereum Mainnet

def fetch_wallet_transactions(wallet_address):
    """
    Fetch transactions for a single wallet from Covalent API.
    """
    url = f"https://api.covalenthq.com/v1/{CHAIN_ID}/address/{wallet_address}/transactions_v2/?key={API_KEY}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error fetching wallet {wallet_address}: {response.status_code}")
        return []
    
    data = response.json()
    return data.get("data", {}).get("items", [])

def fetch_all_wallets(wallet_list_path, output_path):
    """
    Fetch transactions for all wallets listed in the CSV file.
    Saves consolidated data as a CSV for feature engineering.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    wallets_df = pd.read_csv(wallet_list_path)
    all_data = []

    for _, row in tqdm(wallets_df.iterrows(), total=wallets_df.shape[0], desc="Fetching wallets"):
        wallet = row['wallet_id']
        transactions = fetch_wallet_transactions(wallet)
        for tx in transactions:
            tx['wallet_id'] = wallet
            all_data.append(tx)
        time.sleep(0.2)  # to respect API rate limits

    df = pd.json_normalize(all_data)
    df.to_csv(output_path, index=False)
    print(f"Transactions data saved to {output_path}")

if __name__ == "__main__":
    fetch_all_wallets("data/wallets.csv", "outputs/wallet_transactions_raw.csv")
