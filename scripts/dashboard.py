import streamlit as st
import pandas as pd
import joblib
import numpy as np
import altair as alt

rf = joblib.load("churn_rf_model.pkl")
scaler = joblib.load("scaler.pkl")
threshold = joblib.load("threshold.pkl")

st.set_page_config(page_title="Churn Prediction Dashboard", layout="wide")
st.title("Churn Prediction Dashboard")

st.markdown("""
This dashboard predicts **user churn** based on session features.
You can upload a CSV file with new users to see their churn probabilities.
""")

uploaded_file = st.file_uploader("Upload new users CSV", type=["csv"])

if uploaded_file is not None:
    new_users = pd.read_csv(uploaded_file)

    # Make sure required features exist
    required_features = ['session_length_sec', 'matches_played', 'rage_quits', 'max_inactivity_gap_sec']
    if not all(f in new_users.columns for f in required_features):
        st.error(f"CSV must contain columns: {required_features}")
    else:
        X_new = new_users[required_features]
        X_new_s = scaler.transform(X_new)

        probs = rf.predict_proba(X_new_s)[:, 1]
        new_users['churn_prob'] = probs

        new_users['predicted_churn'] = np.where(probs >= threshold, 1, 0)

        new_users_sorted = new_users.sort_values(by='churn_prob', ascending=False)

        st.subheader("Predicted Churn for Users")
        st.dataframe(new_users_sorted)

        st.subheader("Churn Summary")
        st.write(f"Total users: {len(new_users)}")
        st.write(f"Predicted churn: {new_users['predicted_churn'].sum()}")
        st.write(f"High-risk users (>={threshold*100:.0f}% probability): {(new_users['churn_prob'] >= threshold).sum()}")

        csv = new_users_sorted.to_csv(index=False).encode()
        st.download_button("Download Predictions CSV", csv, "predicted_churn.csv", "text/csv")

        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(4, 2.5))  
        ax.hist(new_users['churn_prob'], bins=10, color='skyblue', edgecolor='black')
        ax.set_xlabel("Churn Probability")
        ax.set_ylabel("Number of Users")
        ax.set_title("Distribution of Churn Probabilities")
        plt.tight_layout()

        col1, col2 = st.columns([1, 3])
        with col1:
            st.pyplot(fig)

st.subheader("Feature Importance (Random Forest)")

feature_map = {
    'session_length_sec': 'Session Length (sec)',
    'matches_played': 'Matches Played',
    'rage_quits': 'Rage Quits',
    'max_inactivity_gap_sec': 'Max Inactivity Gap (sec)'
}

importance_df = pd.DataFrame({
    "feature": list(feature_map.keys()),
    "importance": rf.feature_importances_
}).sort_values(by='importance', ascending=False)
importance_df['feature_pretty'] = importance_df['feature'].map(feature_map)

chart = (
    alt.Chart(importance_df)
    .mark_bar()
    .encode(
        x=alt.X('importance:Q', title='Importance'),
        y=alt.Y('feature_pretty:N', sort='-x', title='Feature'),
        tooltip=[
            alt.Tooltip('feature_pretty:N', title='Feature'),
            alt.Tooltip('importance:Q', title='Importance', format='.3f')
        ]
    )
    .properties(height=220)
)

st.altair_chart(chart, use_container_width=True)