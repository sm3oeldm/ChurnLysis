import pandas as pd
import joblib

# Load saved model, scaler, threshold
rf = joblib.load("churn_rf_model.pkl")
scaler = joblib.load("scaler.pkl")
threshold = joblib.load("threshold.pkl")

# Load new user data
new_users = pd.read_csv("data/new_users.csv")
X_new = new_users[['session_length_sec', 'matches_played', 'rage_quits', 'max_inactivity_gap_sec']]

# Scale features
X_new_s = scaler.transform(X_new)

# Predict probabilities
probs = rf.predict_proba(X_new_s)[:, 1]

# Apply threshold
preds = (probs >= threshold).astype(int)

# Add predictions to dataframe
new_users['predicted_churn'] = preds
print(new_users)
