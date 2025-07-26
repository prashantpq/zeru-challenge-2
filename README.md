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
- Used external APIs Covalent to fetch historical on-chain transactions.

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

## Features Engineered

The pipeline groups transaction data by `wallet_id` and calculates the following:

| Feature                | Description                                |
|------------------------|--------------------------------------------|
| `num_transactions`     | Total number of transactions               |
| `total_value_eth`      | Total transaction value (in ETH)           |
| `avg_gas_price`        | Average gas price used                     |
| `max_gas_price`        | Maximum gas price used                     |

These features are then scaled and weighted to generate the final `risk_score`.

---

## Risk Score Calculation Logic

1. **Normalization**:  
   All features are scaled using **MinMaxScaler** to bring them to a common [0,1] range.

2. **Weight Assignment**:  
   Features contribute to the score using the following weights:

   - `num_transactions` → 40%
   - `total_value_eth` → 30%
   - `avg_gas_price` → 20%
   - `max_gas_price` → 10%

3. **Final Score**:  
   \[
   \text{Risk Score} = (F_1 \times 0.4 + F_2 \times 0.3 + F_3 \times 0.2 + F_4 \times 0.1) \times 1000
   \]

4. **Range**:  
   The final score is clipped between **0 and 1000** for interpretability.

---

## Scoring Method

```python
score = (
    0.4 * num_transactions_scaled +
    0.3 * total_value_scaled +
    0.2 * avg_gas_scaled +
    0.1 * max_gas_scaled
) * 1000
```

---

## 📂 Output

After execution, a new file is saved: wallet_features.csv to output

---

##  Interpretation

| Risk Score Range | Risk Level | Description                                                                 |
|------------------|------------|-----------------------------------------------------------------------------|
| 0 - 300          | Low        | Very limited or dormant wallet activity. Safe to interact.                 |
| 301 - 600        | Medium     | Average transaction activity. Proceed with standard caution.               |
| 601 - 800        | High       | Aggressive transaction behavior or large values. Review before trusting.   |
| 801 - 1000       | Critical   | Suspiciously high activity, gas usage. Potentially risky or malicious.     |

---

## 📂 Project Structure

```bash

zeru-challenge-2/
├── data/
│   └── wallets.csv                
├── output/
│   └── wallet_features.csv     
├── outputs/
│   └── wallet_transactions_raw.csv 
├── notebooks/
│   └── analysis.ipynb         
├── src/
│   ├── fetch_transactions.py       
│   ├── feature_engineering.py    
│   └── __init__.py
├── .gitignore
├── requirements.txt
├── README.md
└── LICENSE

```
---
