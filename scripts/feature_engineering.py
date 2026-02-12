import os
import json
import pandas as pd
from datetime import datetime
import numpy as np

RAW_DIR = rawDataDIR # A place where you stored data from phaser
OUTPUT_PATH = "data/processed/features_dataset.csv" # Put your's here

rows = []

for filename in os.listdir(RAW_DIR):
    if not filename.endswith(".json"):
        continue

    with open(os.path.join(RAW_DIR, filename), "r") as f:
        event = json.load(f)

    rows.append(event)

df = pd.DataFrame(rows)

df["timestamp"] = pd.to_datetime(df["timestamp"])

df = df.sort_values(by=["user_id", "session_id", "timestamp"])

features = []

for (user_id, session_id), group in df.groupby(["user_id", "session_id"]):
    timestamps = group["timestamp"].sort_values()

    session_length_sec = (timestamps.max() - timestamps.min()).total_seconds()

    matches_played = (group["event_name"] == "match_played").sum()
    rage_quits = (group["event_name"] == "disconnect").sum()

    inactivity_gaps = timestamps.diff().dt.total_seconds().dropna()
    max_inactivity_gap_sec = inactivity_gaps.max() if not inactivity_gaps.empty else 0

    features.append({
        "user_id": user_id,
        "session_id": session_id,
        "session_length_sec": session_length_sec,
        "matches_played": matches_played,
        "rage_quits": rage_quits,
        "max_inactivity_gap_sec": max_inactivity_gap_sec,
        "last_event_time": timestamps.max()
    })

features_df = pd.DataFrame(features)


now = datetime.utcnow()

churn_labels = []

for _, row in features_df.iterrows():
    churn_prob = 0.15

    if row["rage_quits"] >= 2:
        churn_prob += 0.35

    if row["max_inactivity_gap_sec"] > 600:
        churn_prob += 0.25

    if row["session_length_sec"] < 300:
        churn_prob += 0.20

    if row["matches_played"] <= 1:
        churn_prob += 0.10

    churn_prob = min(churn_prob, 0.95)

    churn = 1 if np.random.rand() < churn_prob else 0
    churn_labels.append(churn)

features_df["churn"] = churn_labels

features_df = features_df.drop(columns=["last_event_time"])

os.makedirs("data/processed", exist_ok=True)
features_df.to_csv(OUTPUT_PATH, index=False)

print(f"Feature dataset saved to {OUTPUT_PATH}")
print(features_df["churn"].value_counts())
