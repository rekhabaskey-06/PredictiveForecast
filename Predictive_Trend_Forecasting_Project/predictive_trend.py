"""
Predictive Model to Forecast Future Trends
Example: Sales Trend Prediction using Linear Regression

Run:
    python predictive_trend.py

Input:
    historical_data.csv
    Columns: Date, Sales

Output:
    Model evaluation metrics
    Future forecast CSV
    Prediction graph
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# -----------------------------
# Step 1: Load historical data
# -----------------------------
DATA_FILE = "historical_data.csv"

data = pd.read_csv(DATA_FILE)

# -----------------------------
# Step 2: Clean and preprocess
# -----------------------------
data["Date"] = pd.to_datetime(data["Date"], errors="coerce")
data["Sales"] = pd.to_numeric(data["Sales"], errors="coerce")

# Remove invalid/missing rows and duplicate records
data = data.dropna(subset=["Date", "Sales"])
data = data.drop_duplicates()
data = data.sort_values("Date").reset_index(drop=True)

# Sequential time feature
data["Time"] = np.arange(len(data))

# -----------------------------
# Step 3: Train/test split
# -----------------------------
# For time-series data, keep chronological order.
split_index = int(len(data) * 0.80)

train = data.iloc[:split_index]
test = data.iloc[split_index:]

X_train = train[["Time"]]
y_train = train["Sales"]

X_test = test[["Time"]]
y_test = test["Sales"]

# -----------------------------
# Step 4: Train model
# -----------------------------
model = LinearRegression()
model.fit(X_train, y_train)

# -----------------------------
# Step 5: Test prediction
# -----------------------------
test_prediction = model.predict(X_test)

mae = mean_absolute_error(y_test, test_prediction)
rmse = np.sqrt(mean_squared_error(y_test, test_prediction))
r2 = r2_score(y_test, test_prediction)

print("=" * 55)
print("PREDICTIVE MODEL TO FORECAST FUTURE TRENDS")
print("=" * 55)
print(f"Training records : {len(train)}")
print(f"Testing records  : {len(test)}")
print(f"MAE              : {mae:.2f}")
print(f"RMSE             : {rmse:.2f}")
print(f"R² Score         : {r2:.4f}")
print("=" * 55)

# -----------------------------
# Step 6: Forecast future data
# -----------------------------
future_periods = 12
last_date = data["Date"].max()

future_dates = pd.date_range(
    start=last_date + pd.DateOffset(months=1),
    periods=future_periods,
    freq="MS"
)

future_time = np.arange(len(data), len(data) + future_periods)
future_prediction = model.predict(future_time.reshape(-1, 1))

forecast = pd.DataFrame({
    "Date": future_dates,
    "Predicted_Sales": np.round(future_prediction, 2)
})

forecast.to_csv("future_forecast.csv", index=False)

print("\nFuture Forecast:")
print(forecast.to_string(index=False))

# -----------------------------
# Step 7: Visualize predictions
# -----------------------------
plt.figure(figsize=(12, 6))

plt.plot(
    data["Date"],
    data["Sales"],
    marker="o",
    label="Historical Sales"
)

plt.plot(
    test["Date"],
    test_prediction,
    marker="o",
    linestyle="--",
    label="Test Prediction"
)

plt.plot(
    future_dates,
    future_prediction,
    marker="o",
    linestyle="--",
    label="Future Forecast"
)

plt.axvline(
    test["Date"].iloc[0],
    linestyle=":",
    label="Train/Test Split"
)

plt.title("Sales Trend Prediction and Future Forecast")
plt.xlabel("Date")
plt.ylabel("Sales")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig("prediction_graph.png", dpi=300)
plt.show()

# -----------------------------
# Step 8: Actual vs predicted
# -----------------------------
plt.figure(figsize=(10, 5))
plt.plot(test["Date"], y_test.values, marker="o", label="Actual Sales")
plt.plot(test["Date"], test_prediction, marker="o", linestyle="--",
         label="Predicted Sales")
plt.title("Actual vs Predicted Sales")
plt.xlabel("Date")
plt.ylabel("Sales")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig("actual_vs_predicted.png", dpi=300)
plt.show()
