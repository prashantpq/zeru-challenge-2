import requests
import pandas as pd
import time

COMPOUND_SUBGRAPH_URL = "https://api.thegraph.com/subgraphs/name/graphprotocol/compound-v2"

QUERY_TEMPLATE = """
{
  account(id: "%s") {
    id
    tokens {
      symbol
      supplyBalanceUnderlying
      borrowBalanceUnderlying
    }
  }
}
"""

def fetch_wallet_data(wallet_ids):
    all_data = []
    for wallet in wallet_ids:
        query = QUERY_TEMPLATE % wallet.lower()
        response = requests.post(COMPOUND_SUBGRAPH_URL, json={'query': query})
        if response.status_code == 200:
            data = response.json()
            account = data.get("data", {}).get("account")
            if account:
                for token in account["tokens"]:
                    all_data.append({
                        "wallet": wallet,
                        "token_symbol": token["symbol"],
                        "supply_balance": float(token["supplyBalanceUnderlying"]),
                        "borrow_balance": float(token["borrowBalanceUnderlying"])
                    })
        else:
            print(f"Failed to fetch for {wallet}")
        time.sleep(0.2)  # rate limit handling

    return pd.DataFrame(all_data)

if __name__ == "__main__":
    # Load wallet IDs
    with open("data/wallet_ids.txt") as f:
        wallet_ids = [line.strip() for line in f.readlines()]

    # Fetch data
    df = fetch_wallet_data(wallet_ids)
    df.to_csv("data/compound_wallets_data.csv", index=False)
    print("Compound data saved to data/compound_wallets_data.csv")
