# E-commerce Forecasting: XGBoost (optional Clustering)

**Forecasting daily number of items sold for each product cluster from event logs in an e-commerce dataset using XGBoost**

---

## Problem & Goal
- **Task:** Predict **number of items sold** for **each product cluster**.
- **Why it matters:** Better forecasts help with **inventory** decisions.
- **Models used:** **XGBoost**

---

## Data
- **Source:** (https://www.kaggle.com/datasets/carrie1/ecommerce-data/data)
- **Cleaning:**
  - records with InvoiceNo started with 'A' are excluded
  - canceled order quantities were extracted from the completed ones. There were no clear rule for InvoiceNo generation for cancelled orders. So to be able to detect which canceled order belong to which completed order special keys were created and records excluded based on that
- **Target:** `Quantity`
- **Features (examples):**
  - lags (t-1, t-7, t-28), rolling means (last7 days, 28 days, 56 days), sin-cos transformation, clusters
- **Important:** No raw data is committed to Git.

---

## Results
- Most of the orders given from UK so country is not included in the analysis, clustering showed there were two main product clusters. We proceeded with predicting number of products sold daily for each cluster. However since only one year of data was available data was sparse thus model overfitted and no actions taken to improve the model.
