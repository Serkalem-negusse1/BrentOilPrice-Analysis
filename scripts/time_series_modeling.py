import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from arch import arch_model
import numpy as np

def train_arima_model(data, order=(1,1,1)):
    """Trains an ARIMA model and returns the fitted model."""
    model = ARIMA(data, order=order)
    fitted_model = model.fit()
    return fitted_model

def train_garch_model(data, p=1, q=1):
    """Trains a GARCH model and returns the fitted model."""
    model = arch_model(data, vol='Garch', p=p, q=q, dist='normal')
    fitted_model = model.fit(disp="off")
    return fitted_model

def generate_forecasts(input_path, output_path):
    """Trains models and generates forecasts for Brent oil prices."""
    
    # Load data
    df = pd.read_csv(input_path, parse_dates=['Date'])
    df.set_index('Date', inplace=True)

    # Train ARIMA model
    arima_model = train_arima_model(df['Price'])
    arima_forecast = arima_model.forecast(steps=30)

    # Train GARCH model
    garch_model = train_garch_model(df['Price'])
    garch_forecast = garch_model.forecast(start=len(df)-30).variance.values[-30:]

    # Save results
    forecast_df = pd.DataFrame({
        "Date": pd.date_range(start=df.index[-1], periods=30, freq="D"),
        "ARIMA_Forecast": arima_forecast.values,
        "GARCH_Forecast": np.sqrt(garch_forecast)  # Convert variance to std deviation
    })
    forecast_df.to_csv(output_path, index=False)

    print(f"✅ Forecasting Completed. Results saved to: {output_path}")

if __name__ == "__main__":
    generate_forecasts("E:/data/Data10/processed_data.csv", "E:/Git_repo/BrentOilPrice-Analysis/results/forecasting_results.csv")