# 🧠 Ethereum Wallet Risk Scoring System

## 📌 Overview

This project implements a **feature engineering pipeline** to compute a **risk score** for Ethereum wallets based on their transaction history. The goal is to **quantitatively assess** the risk associated with each wallet, using interpretable on-chain features such as transaction count, value transacted, and gas price behavior.

---

## 🚨 Problem Statement

In blockchain ecosystems, particularly Ethereum, it's crucial to assess the **risk profile** of a wallet before interacting with it — especially in the context of:

- Anti-money laundering (AML)
- Fraud detection
- Compliance analysis
- Whitelisting/blacklisting

However, manual analysis is impractical due to:
- Large volumes of data
- Complex behavioral patterns

**Hence**, this project develops a data-driven risk scoring mechanism to assist in automated risk profiling of Ethereum wallets.

---

## ⚙️ Features Engineered

The pipeline groups transaction data by `wallet_id` and calculates the following:

| Feature                | Description                                |
|------------------------|--------------------------------------------|
| `num_transactions`     | Total number of transactions               |
| `total_value_eth`      | Total transaction value (in ETH)           |
| `avg_gas_price`        | Average gas price used                     |
| `max_gas_price`        | Maximum gas price used                     |

These features are then scaled and weighted to generate the final `risk_score`.

---

## 🧮 Risk Score Calculation Logic

1. **Normalization**:  
   All features are scaled using **MinMaxScaler** to bring them to a common [0,1] range.

2. **Weight Assignment**:  
   Features contribute to the score using the following weights:

   - 🧾 `num_transactions` → 40%
   - 💸 `total_value_eth` → 30%
   - ⛽ `avg_gas_price` → 20%
   - 🚀 `max_gas_price` → 10%

3. **Final Score**:  
   \[
   \text{Risk Score} = (F_1 \times 0.4 + F_2 \times 0.3 + F_3 \times 0.2 + F_4 \times 0.1) \times 1000
   \]

4. **Range**:  
   The final score is clipped between **0 and 1000** for interpretability.

---

## 🧠 Interpretation

| Risk Score Range | Risk Level | Description                                                                 |
|------------------|------------|-----------------------------------------------------------------------------|
| 0 - 300          | Low        | Very limited or dormant wallet activity. Safe to interact.                 |
| 301 - 600        | Medium     | Average transaction activity. Proceed with standard caution.               |
| 601 - 800        | High       | Aggressive transaction behavior or large values. Review before trusting.   |
| 801 - 1000       | Critical   | Suspiciously high activity, gas usage. Potentially risky or malicious.     |

---

## 📂 Output

After execution, a new file is saved: wallet_features.csv

