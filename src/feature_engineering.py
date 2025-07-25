import pandas as pd

def engineer_features(df):
    """
    Engineer relevant features from raw transaction data for risk scoring.
    """
    df['value'] = pd.to_numeric(df['value'], errors='coerce')

    grouped = df.groupby('wallet_id').agg(
        total_txn_count = ('hash', 'count'),
        total_value = ('value', 'sum'),
        avg_txn_value = ('value', 'mean'),
        max_txn_value = ('value', 'max'),
        unique_to_addresses = ('to_address', pd.Series.nunique),
    ).reset_index()

    grouped.fillna(0, inplace=True)
    return grouped

if __name__ == "__main__":
    df = pd.read_csv("outputs/wallet_transactions_raw.csv")
    features_df = engineer_features(df)
    features_df.to_csv("outputs/features.csv", index=False)
    print("✅ Features saved to outputs/features.csv")
