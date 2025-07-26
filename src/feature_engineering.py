import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def engineer_features(df):
    """
    Performs feature engineering to compute:
    - Number of transactions
    - Total transaction value in ETH
    - Average and max gas price
    - Scaled risk score between 0 - 1000
    """

    grouped = df.groupby('wallet_id').agg(
        num_transactions=('tx_hash', 'count'),
        total_value_eth=('value', 'sum'),
        avg_gas_price=('gas_price', 'mean'),
        max_gas_price=('gas_price', 'max')
    ).reset_index()

    grouped['total_value_eth'] = pd.to_numeric(grouped['total_value_eth'], errors='coerce') / 1e18

    grouped.fillna(0, inplace=True)

    scaler = MinMaxScaler()

    scaled_features = scaler.fit_transform(grouped[['num_transactions', 'total_value_eth', 'avg_gas_price', 'max_gas_price']])

    grouped[['num_transactions_scaled', 'total_value_scaled', 'avg_gas_scaled', 'max_gas_scaled']] = scaled_features

    grouped['risk_score'] = (
        grouped['num_transactions_scaled'] * 0.4 +
        grouped['total_value_scaled'] * 0.3 +
        grouped['avg_gas_scaled'] * 0.2 +
        grouped['max_gas_scaled'] * 0.1
    ) * 1000

    grouped['risk_score'] = grouped['risk_score'].clip(0, 1000)

    return grouped[['wallet_id', 'risk_score']]


if __name__ == "__main__":
    df = pd.read_csv("outputs/wallet_transactions_raw.csv")
    features_df = engineer_features(df)
    
    features_df.to_csv("output/wallet_features.csv", index=False)

    print("Feature engineering complete. Output saved to output/wallet_features.csv")
