# Wallet Risk Scoring From Scratch

## Overview

This project was developed as part of a technical assignment focused on **on-chain risk profiling** using data from DeFi lending protocols like **Compound V2/V3** or **Aave V2**.

Our goal:  
 - To retrieve on-chain transaction data for a set of wallets  
 - Engineer meaningful features  
 - Assign a **risk score between 0 and 1000** to each wallet  
 - Make the approach explainable, reproducible, and scalable

---

## Assignment Requirements

### 1. **Fetch Transaction History**
- Retrieved transaction data using wallet addresses.
- Used external APIs like Covalent or custom scrapers to fetch historical on-chain transactions.

### 2. **Data Preparation**
- Cleaned, deduplicated, and standardized transaction records.
- Extracted wallet-specific summaries:
  - Total transaction count
  - Total amount transacted
  - Average transaction value
  - Gas fee consumption
  - Interaction types (e.g., deposits, borrows, swaps)

### 3. **Risk Scoring**
- Developed a scoring model that outputs a risk score ∈ [0, 1000].
- Risk score reflects the probability of unusual or suspicious activity based on wallet behavior.

---

## ⚙️ Features Considered

| Feature Name              | Description                                           | Risk Signal            |
|---------------------------|-------------------------------------------------------|-------------------------|
| `transaction_count`       | Total number of transactions                         | ↑ Higher = riskier      |
| `total_transacted_value`  | Total ETH or token volume moved                      | ↑ Higher = riskier      |
| `average_txn_value`       | Mean transaction size                                | ↓ Lower = riskier       |
| `gas_fees_spent`          | Total gas paid in Gwei                               | Neutral/signal activity |
| `night_activity_ratio`    | Ratio of txns between 12am–6am UTC                   | ↑ Higher = suspicious   |
| `country_risk_factor`     | Country mapped from IP/geo/metadata (if available)   | ↑ High-risk = riskier   |
| `protocols_interacted`    | Number of DeFi protocols interacted with             | ↓ Diverse = less risky  |

All features were **normalized using MinMax scaling**, and final scores were **weighted and summed** to produce a single value per wallet.

---

## Scoring Method

```python
score = (
    w1 * normalized_txn_count +
    w2 * normalized_value +
    w3 * (1 - normalized_avg_txn_value) +
    w4 * normalized_gas +
    w5 * night_activity +
    ...
) * 1000
