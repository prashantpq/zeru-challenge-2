# main.py

import os

# Fetch transactions
os.system("python src/fetch_transactions.py")

# Engineer features & calculate risk score
os.system("python src/feature_engineering.py")
