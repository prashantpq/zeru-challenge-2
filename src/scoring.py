def calculate_wallet_score(row):
    """
    Calculate risk score for a wallet based on features.
    The score is normalized to be between 0 and 1000.
    """
    score = 0

    # Example heuristic scaled proportionally:
    if row['num_transactions'] > 10:
        score += 200
    if row['total_value_eth'] > 1:
        score += 300
    if row['avg_gas_price'] > 50e9:  # 50 Gwei
        score += 200
    if row['max_value_eth'] > 0.5:
        score += 200
    if row['min_value_eth'] < 0.01:
        score += 100

    # Clip between 0 and 1000
    return max(0, min(score, 1000))
