import pandas as pd
import json
import matplotlib.pyplot as plt

def load_external_events():
    """Loads significant external events affecting oil prices."""
    return [
        {"Date": "1990-08-02", "Event": "Iraq Invades Kuwait (Gulf War)"},
        {"Date": "2008-09-15", "Event": "Global Financial Crisis (Lehman Collapse)"},
        {"Date": "2014-11-27", "Event": "OPEC Refuses to Cut Oil Production"},
        {"Date": "2020-03-09", "Event": "COVID-19 Oil Price Crash"},
        {"Date": "2022-02-24", "Event": "Russia-Ukraine War Begins"}
    ]

def analyze_event_impact(input_data_path, change_point_path, output_path):
    """Analyzes the impact of external events on Brent oil prices."""
    
    # Load dataset 
    df = pd.read_csv(input_data_path, parse_dates=['Date'])
    df.set_index('Date', inplace=True)

    # Load detected change points
    with open(change_point_path, "r") as file:
        change_points = json.load(file)
    
    # Convert change points to datetime
    change_point_dates = [pd.to_datetime(cp["Date"]) for cp in change_points]

    # Load external events
    external_events = load_external_events()
    
    # Convert event dates to datetime
    event_dates = [pd.to_datetime(event["Date"]) for event in external_events]

    # Save event analysis results
    results = []
    for event in external_events:
        event_date = pd.to_datetime(event["Date"])
        price_before = df.loc[event_date - pd.Timedelta(days=30): event_date, 'Price'].mean()
        price_after = df.loc[event_date: event_date + pd.Timedelta(days=30), 'Price'].mean()
        price_change = ((price_after - price_before) / price_before) * 100
        
        results.append({
            "Event": event["Event"],
            "Date": event["Date"],
            "Price Before": round(price_before, 2),
            "Price After": round(price_after, 2),
            "Price Change (%)": round(price_change, 2)
        })

    pd.DataFrame(results).to_csv(output_path, index=False)
    print(f"✅ Event Impact Analysis Completed. Results saved to: {output_path}")

if __name__ == "__main__":
    analyze_event_impact("E:/data/Data10/processed_data.csv", "E:/Git_repo/BrentOilPrice-Analysis/results/change_points.json", "E:/Git_repo/BrentOilPrice-Analysis/results/event_impact_analysis.csv")
