# AI-Powered Dispute Assistant (Modular)

This package provides a modular, end-to-end skeleton implementation for the
"AI-Powered Dispute Assistant" described in your assignment. It focuses on:

- Data ingestion (disputes + transactions)
- Preprocessing & feature engineering
- Rule-based high-precision classifier
- Fuzzy duplicate detection (RapidFuzz optional)
- Resolution suggestion engine
- Modular code structure and a CLI `main.py`

NOTE: This is a robust, production-oriented skeleton. The ML model component
is included as a placeholder (train/predict) and assumes you will provide
labeled training data if you want to train a supervised classifier.

## How to run (example)

1. Place your `disputes.csv` and `transactions.csv` in `/mnt/data/` (the notebook/user already uploaded them).
2. From a Python environment, run:
   ```
   python /mnt/data/ai_dispute_assistant/main.py --disputes /mnt/data/disputes\ (4)\ (1).csv --transactions /mnt/data/transactions\ (3)\ (1)\ (1).csv
   ```
   (Adjust paths to match uploaded filenames.)

3. Outputs:
   - `/mnt/data/classified_disputes.csv`
   - `/mnt/data/resolutions.csv`

## Requirements
- Python 3.8+
- Optional: `rapidfuzz` for better fuzzy string matching
- Optional for ML: `lightgbm`, `scikit-learn`, `shap`

The code will fall back to a simple string similarity implementation if `rapidfuzz` is not available.
