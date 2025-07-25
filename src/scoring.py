import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def generate_scores(df):
    """
    Generate risk scores for wallets based on engineered features.
    """
    scaler = MinMaxScaler(feature_range=(0, 1000))
    score_cols = ['total_txn_count', 'total_value', 'avg_txn_value', 'max_txn_value', 'unique_to_addresses']
    df[score_cols] = scaler.fit_transform(df[score_cols])
    df['score'] = df[score_cols].mean(axis=1) * 1000
    df['score'] = df['score'].round(0)
    return df[['wallet_id', 'score']]

if __name__ == "__main__":
    df = pd.read_csv("outputs/features.csv")
    scores_df = generate_scores(df)
    scores_df.to_csv("outputs/wallet_scores.csv", index=False)
    print("✅ Wallet scores saved to outputs/wallet_scores.csv")
