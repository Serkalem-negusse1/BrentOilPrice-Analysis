from flask import Flask, jsonify, request, render_template_string
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

@app.route("/")
def index():
    """Root endpoint to serve the front-end interface."""
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Detecting Change Points in Oil Prices Using Bayesian Inference</title>
        <style>
            body { font-family: Arial, sans-serif; padding: 20px; background-color: #f5f7fa; }
            h1 { color: #4b8d99; font-size: 36px; text-align: center; margin-bottom: 20px; }
            p { font-size: 18px; color: #555; text-align: center; }
            .api-links {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                justify-items: center;
                margin-top: 20px;
            }
            .api-link {
                padding: 15px 30px;
                background-color: #007BFF;
                color: white;
                font-size: 18px;
                text-decoration: none;
                border-radius: 8px;
                text-align: center;
                box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
                transition: background-color 0.3s ease, transform 0.2s ease;
            }
            .api-link:hover {
                background-color: #0056b3;
                transform: translateY(-3px);
            }
            .endpoint { margin-top: 30px; padding: 15px; background-color: #ffffff; border-radius: 8px; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1); }
            pre { white-space: pre-wrap; word-wrap: break-word; background-color: #f4f4f9; padding: 20px; border-radius: 8px; }
        </style>
    </head>
    <body>
        <h1>Detecting Change Points in Oil Prices Using Bayesian Inference</h1>
                                  Prepared by: Serkalem Negusse
        <p>Click on the links below to access the API data:</p>
        <div class="api-links">
            <a href="#" class="api-link" onclick="fetchData('historical_prices')">Historical Prices</a>
            <a href="#" class="api-link" onclick="fetchData('forecast')">Forecast</a>
            <a href="#" class="api-link" onclick="fetchData('change_points')">Change Points</a>
            <a href="#" class="api-link" onclick="fetchData('event_impact')">Event Impact</a>
        </div>

        <div class="endpoint" id="endpoint-content">
            <h2>Data will appear here</h2>
        </div>

        <script>
            function fetchData(endpoint) {
                fetch(`/${endpoint}`)
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('endpoint-content').innerHTML = '<h2>API Response</h2><pre>' + JSON.stringify(data, null, 2) + '</pre>';
                    })
                    .catch(error => {
                        document.getElementById('endpoint-content').innerHTML = '<h2>Error</h2><p>Could not fetch data from the API. Please try again later.</p>';
                    });
            }
        </script>
    </body>
    </html>
    """)

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
