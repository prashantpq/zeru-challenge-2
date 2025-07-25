# src/feature_engineering.py

import pandas as pd

def engineer_features(df):
    grouped = df.groupby('wallet').agg(
        total_supplied = pd.NamedAgg(column='supply_balance', aggfunc='sum'),
        total_borrowed = pd.NamedAgg(column='borrow_balance', aggfunc='sum'),
        unique_assets = pd.NamedAgg(column='token_symbol', aggfunc=pd.Series.nunique)
    ).reset_index()

    grouped["net_position"] = grouped["total_supplied"] - grouped["total_borrowed"]
    grouped.fillna(0, inplace=True)
    return grouped
