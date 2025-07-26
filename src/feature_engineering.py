# src/feature_engineering.py

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
    # Aggregate features by wallet
    grouped = df.groupby('wallet_id').agg(
        num_transactions=('tx_hash', 'count'),
        total_value_eth=('value', 'sum'),
        avg_gas_price=('gas_price', 'mean'),
        max_gas_price=('gas_price', 'max')
    ).reset_index()

    # Convert value from wei to ETH
    grouped['total_value_eth'] = pd.to_numeric(grouped['total_value_eth'], errors='coerce') / 1e18

    # Replace NaN with 0 for safe calculations
    grouped.fillna(0, inplace=True)

    # Initialize scaler
    scaler = MinMaxScaler()

    # Scale selected features to [0,1]
    scaled_features = scaler.fit_transform(grouped[['num_transactions', 'total_value_eth', 'avg_gas_price', 'max_gas_price']])

    grouped[['num_transactions_scaled', 'total_value_scaled', 'avg_gas_scaled', 'max_gas_scaled']] = scaled_features

    # Calculate risk score as weighted sum (adjust weights as needed)
    grouped['risk_score'] = (
        grouped['num_transactions_scaled'] * 0.4 +
        grouped['total_value_scaled'] * 0.3 +
        grouped['avg_gas_scaled'] * 0.2 +
        grouped['max_gas_scaled'] * 0.1
    ) * 1000

    # Clip risk score to [0, 1000]
    grouped['risk_score'] = grouped['risk_score'].clip(0, 1000)

    return grouped


if __name__ == "__main__":
    # Load input data
    df = pd.read_csv("outputs/wallet_transactions_raw.csv")

    # Engineer features
    features_df = engineer_features(df)

    # Save features with risk score
    features_df.to_csv("output/wallet_features.csv", index=False)

    print("Feature engineering complete. Output saved to outputs/wallet_features.csv")
