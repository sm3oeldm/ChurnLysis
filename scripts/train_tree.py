import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import joblib  # for saving the model

# ---------------------------
# Load dataset
# ---------------------------
df = pd.read_csv("data/processed/features_dataset.csv")

# Features + target
X = df.drop(columns=["user_id", "session_id", "churn"])
y = df["churn"]

# ---------------------------
# Train / Validation / Test split
# ---------------------------
x_train, x_temp, y_train, y_temp = train_test_split(
    X, y, test_size=0.3, random_state=2006, stratify=y
)

x_val, x_test, y_val, y_test = train_test_split(
    x_temp, y_temp, test_size=0.5, random_state=2006, stratify=y_temp
)

# ---------------------------
# Scale features (optional)
# ---------------------------
scaler = StandardScaler()
x_train_s = scaler.fit_transform(x_train)
x_val_s = scaler.transform(x_val)
x_test_s = scaler.transform(x_test)

# ---------------------------
# Random Forest model
# ---------------------------
rf = RandomForestClassifier(
    n_estimators=200,           # more trees to stabilize predictions
    class_weight='balanced',    # handle churn imbalance
    random_state=2006
)

rf.fit(x_train_s, y_train)

# ---------------------------
# Automatic threshold tuning (maximize F1 on validation)
# ---------------------------
val_probs = rf.predict_proba(x_val_s)[:, 1]
thresholds = [i / 100 for i in range(20, 81)]  # test 0.2 -> 0.8
best_thr = 0.5
best_f1 = -1

for thr in thresholds:
    preds = (val_probs >= thr).astype(int)
    f1 = f1_score(y_val, preds)
    if f1 > best_f1:
        best_f1 = f1
        best_thr = thr

print(f"Selected probability threshold: {best_thr:.2f} (F1 on val = {best_f1:.3f})")

# ---------------------------
# Evaluate on test set using best threshold
# ---------------------------
test_probs = rf.predict_proba(x_test_s)[:, 1]
test_preds = (test_probs >= best_thr).astype(int)

print("\nTest metrics:")
print("Accuracy:", accuracy_score(y_test, test_preds))
print("Precision:", precision_score(y_test, test_preds))
print("Recall:", recall_score(y_test, test_preds))
print("F1:", f1_score(y_test, test_preds))
print("Confusion Matrix:\n", confusion_matrix(y_test, test_preds))

# ---------------------------
# Feature importances
# ---------------------------
importance_df = pd.DataFrame({
    "feature": X.columns,
    "importance": rf.feature_importances_
}).sort_values(by="importance", ascending=False)

print("\nFeature importances:")
print(importance_df)

# ---------------------------
# Save the trained model and scaler for later use
# ---------------------------
joblib.dump(rf, "churn_rf_model.pkl")
joblib.dump(scaler, "scaler.pkl")
joblib.dump(best_thr, "threshold.pkl")  # save the chosen threshold

print("\nModel, scaler, and threshold saved!")
