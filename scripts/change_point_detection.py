import pandas as pd
import numpy as np
import pymc as pm
import matplotlib.pyplot as plt

def bayesian_change_point_detection(data): 
    """Detects change points using Bayesian inference."""
    with pm.Model() as model:
        mean_1 = pm.Normal("mean_1", mu=data.mean(), sigma=data.std())
        mean_2 = pm.Normal("mean_2", mu=data.mean(), sigma=data.std())
        tau = pm.DiscreteUniform("tau", lower=0, upper=len(data) - 1)

        idx = np.arange(len(data))
        mean = pm.math.switch(tau >= idx, mean_1, mean_2)
        obs = pm.Normal("obs", mu=mean, sigma=data.std(), observed=data)

        trace = pm.sample(1000, tune=500, return_inferencedata=True)

    return trace, tau

def detect_change_points(input_path, output_path):
    """Runs CPD and saves detected change points."""
    
    # Load data
    df = pd.read_csv(input_path, parse_dates=['Date'])
    df.set_index('Date', inplace=True)

    # Apply Bayesian CPD
    trace, tau = bayesian_change_point_detection(df['Price'])

    # Extract detected change point index
    change_point_index = int(np.median(trace.posterior["tau"]))

    # Save results
    change_points = {"Date": df.index[change_point_index].strftime('%Y-%m-%d')}
    pd.DataFrame([change_points]).to_json(output_path, orient="records")

    print(f"✅ Change Point Detection Completed. Results saved to: {output_path}")

if __name__ == "__main__":
    detect_change_points("E:/data/Data10/processed_data.csv", "E:/Git_repo/BrentOilPrice-Analysis/results/change_points.json")

