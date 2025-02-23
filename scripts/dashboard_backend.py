from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import json

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# Load datasets
df = pd.read_csv("E:/data/Data10/processed_data.csv", parse_dates=['Date'])
forecast_df = pd.read_csv("E:/Git_repo/BrentOilPrice-Analysis/results/forecasting_results.csv", parse_dates=['Date'])
events_df = pd.read_csv("E:/Git_repo/BrentOilPrice-Analysis/results/event_impact_analysis.csv", parse_dates=['Date'])

# Convert date columns to string format to ensure JSON serializability
df["Date"] = df["Date"].dt.strftime('%Y-%m-%d')
forecast_df["Date"] = forecast_df["Date"].dt.strftime('%Y-%m-%d')
events_df["Date"] = events_df["Date"].dt.strftime('%Y-%m-%d')

# Load detected change points
with open("E:/Git_repo/BrentOilPrice-Analysis/results/change_points.json", "r") as file:
    change_points = json.load(file)

@app.route("/historical_prices", methods=["GET"])
def get_historical_prices():
    """Returns historical Brent Oil prices with optional date filtering."""
    start_date = request.args.get("start", min(df["Date"]).strftime('%Y-%m-%d') if hasattr(df["Date"].min(), 'strftime') else df["Date"].min())
    end_date = request.args.get("end", max(df["Date"]).strftime('%Y-%m-%d') if hasattr(df["Date"].max(), 'strftime') else df["Date"].max())
    filtered_df = df[(df["Date"] >= start_date) & (df["Date"] <= end_date)]
    return jsonify(filtered_df.to_dict(orient="records"))

@app.route("/forecast", methods=["GET"])
def get_forecast():
    """Returns predicted Brent Oil prices."""
    return jsonify(forecast_df.to_dict(orient="records"))

@app.route("/change_points", methods=["GET"])
def get_change_points():
    """Returns detected change points in oil prices."""
    return jsonify(change_points)

@app.route("/event_impact", methods=["GET"])
def get_event_impact():
    """Returns external event impact on oil prices."""
    return jsonify(events_df.to_dict(orient="records"))

if __name__ == "__main__":
    app.run(debug=True, port=5000)
