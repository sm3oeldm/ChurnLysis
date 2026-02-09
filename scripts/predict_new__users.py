import pandas as pd
import joblib

rf = joblib.load("churn_rf_model.pkl")
scaler = joblib.load("scaler.pkl")
threshold = joblib.load("threshold.pkl")

new_users = pd.read_csv("data/new_users.csv")
X_new = new_users[['session_length_sec', 'matches_played', 'rage_quits', 'max_inactivity_gap_sec']]

X_new_s = scaler.transform(X_new)

probs = rf.predict_proba(X_new_s)[:, 1]

preds = (probs >= threshold).astype(int)

new_users['predicted_churn'] = preds
print(new_users)
