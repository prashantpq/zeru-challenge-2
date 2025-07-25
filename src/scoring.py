# src/scoring.py

from sklearn.preprocessing import MinMaxScaler

def generate_scores(df):
    scaler = MinMaxScaler(feature_range=(0,1000))
    features = ["total_supplied", "total_borrowed", "unique_assets", "net_position"]
    df[features] = scaler.fit_transform(df[features])

    # Final score as mean of scaled features
    df["score"] = df[features].mean(axis=1).round(0)
    return df[["wallet", "score"]]
