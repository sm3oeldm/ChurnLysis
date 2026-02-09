# Churn Prediction Dashboard

A **real-time churn prediction dashboard** for analyzing user behavior in a game platform.
The project includes a **Random Forest model** with automatic threshold tuning and a **Streamlit dashboard** to visualize high-risk users and predicted churn probabilities.

---

## **Project Overview**

* **Input:** User activity logs (sessions, matches played, rage quits, inactivity gaps)
* **Processing:** Features are extracted, scaled, and fed into a trained Random Forest model
* **Output:** Predicted churn probabilities for each user and visualizations for analysis

**Key Features:**

* Random Forest model with automatic threshold tuning
* Streamlit dashboard with:

  * Predictions table for new users
  * Probability histogram
  * Clean, human-readable feature names
* Dockerized for portability
* Easy to run locally or via Docker

---

## **Repository Structure**

```
ChurnLysis/
├─ data/
│   ├─ processed/features_dataset.csv      # Sample dataset for testing
│   └─ new_users.csv                       # Sample new users for prediction
├─ scripts/
│   ├─ dashboard.py
│   ├─ train_model.py
│   ├─ train_tree.py
│   └─ predict_new_users.py
├─ churn_rf_model.pkl                      # Trained Random Forest model
├─ scaler.pkl                              # Feature scaler
├─ threshold.pkl                            # Optimal threshold
├─ requirements.txt
├─ Dockerfile
└─ README.md
```

> Note: Large files (Docker image, raw logs) are **not included** in this repo. Docker image is on Docker Hub.

---

## **Setup Instructions (Local Python Environment)**

1. Clone the repository:

```bash
git clone https://github.com/sm3oeldm/ChurnLysis.git
cd ChurnLysis
```

2. Create a virtual environment and activate it:

```bash
python -m venv venv
.\venv\Scripts\activate   # Windows
source venv/bin/activate  # macOS/Linux
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the Streamlit dashboard locally:

```bash
streamlit run scripts/dashboard.py
```

* Open your browser at `http://localhost:8501`

---

## **Run with Docker (Recommended)**

1. Pull the Docker image from Docker Hub:

```bash
docker pull sm3oeldm/churn-dashboard:latest
```

2. Run the container:

```bash
docker run -p 8501:8501 sm3oeldm/churn-dashboard:latest
```

3. Open your browser at `http://localhost:8501`

* Works on any machine with Docker installed.

---

## **Testing Predictions**

1. Use the included `data/new_users.csv` as sample input:

```csv
session_length_sec,matches_played,rage_quits,max_inactivity_gap_sec
3600,10,0,60
1800,5,0,30
7200,20,1,120
```

2. Load it in the dashboard or via `predict_new_users.py` to see churn probabilities.

* Users with low inactivity gaps, normal session lengths, and no rage quits typically **do not churn**.

---

## **Model Details**

* **Algorithm:** Random Forest Classifier
* **Threshold:** Automatically tuned on validation set for best F1 score
* **Important Features:**

  * `Max Inactivity Gap Sec`
  * `Session Length Sec`
  * `Rage Quits`
  * `Matches Played`

---

## **Demo Guide (Optional)**

To quickly demo the dashboard to someone:

1. Pull the Docker image:

```bash
docker pull sm3oeldm/churn-dashboard:latest
```

2. Run the container:

```bash
docker run -p 8501:8501 sm3oeldm/churn-dashboard:latest
```

3. Open `http://localhost:8501`
4. Upload `new_users.csv` in the dashboard
5. Show predicted churn probabilities and histogram

* This allows anyone to **see predictions in real time** without installing Python or dependencies.

---

## **Notes**

* Large Docker images (>100MB) are hosted on **Docker Hub**, not GitHub.
* Keep sensitive or raw data out of the repo for security and size reasons.
* Anyone can run this project by pulling the Docker image or running locally with Python.

---

## **Contact**

Developed by **Sameer Eldam**

* GitHub: [https://github.com/sm3oeldm](https://github.com/sm3oeldm)
* LinkedIn / Email: sm3oeldm@gmail.com
