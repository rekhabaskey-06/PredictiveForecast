# Predictive Model to Forecast Future Trends

## Project Description
This project uses historical sales data to predict future sales trends using
Linear Regression.

## Features
- Historical data cleaning
- Missing-value and duplicate handling
- Chronological train/test split
- Linear Regression model
- MAE, RMSE and R² evaluation
- 12-month future forecasting
- Prediction graphs
- CSV export of future predictions

## Installation

```bash
pip install -r requirements.txt
```

## Run

```bash
python predictive_trend.py
```

## Input
`historical_data.csv`

Columns:
- Date
- Sales

## Output
- `future_forecast.csv`
- `prediction_graph.png`
- `actual_vs_predicted.png`

## Model
Linear Regression is used as a simple and explainable baseline model for
forecasting the overall trend.
