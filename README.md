# AI-Powered Dispute Assistant — v2 (Optimized & Production-ready)

What's new in v2:
- Vectorized data processing and minimized Python-level loops.
- Parallelized fuzzy duplicate detection (RapidFuzz + joblib) with efficient pruning.
- Config-driven pipeline via `config.yaml`.
- Structured logging, benchmarking utilities and runtime reports.
- Optional SHAP explainability hooks (if LightGBM and shap installed).
- SQLite export for quick querying.
- Type hints, docstrings, and unit-test stubs.

How to run:
1. Place `disputes.csv` and `transactions.csv` in `/mnt/data/`.
2. Optional: edit `/mnt/data/ai_dispute_assistant_v2/config.yaml`.
3. Run:
   ```
   python /mnt/data/ai_dispute_assistant_v2/cli.py --disputes "/mnt/data/disputes (4) (1).csv" --transactions "/mnt/data/transactions (3) (1) (1).csv"
   ```
Outputs:
- `/mnt/data/classified_disputes_v2.csv`
- `/mnt/data/resolutions_v2.csv`
- `/mnt/data/disputes_v2.sqlite` (optional)

Requirements (recommended):
- Python 3.8+
- pandas, numpy
- rapidfuzz (optional but recommended)
- joblib
- pyyaml
- lightgbm, shap (optional for ML + explainability)
