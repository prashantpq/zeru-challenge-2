# risk_scoring_pipeline.py

import pandas as pd
from src.feature_engineering import engineer_features
from src.scoring import generate_scores

def main():
    # Load fetched data
    df = pd.read_csv("data/compound_wallets_data.csv")

    # Feature engineering
    features_df = engineer_features(df)

    # Generate scores
    scores_df = generate_scores(features_df)

    # Save output
    scores_df.to_csv("outputs/wallet_risk_scores.csv", index=False)
    print("Risk scores saved to outputs/wallet_risk_scores.csv")

if __name__ == "__main__":
    main()
