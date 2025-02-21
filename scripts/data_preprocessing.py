import pandas as pd

def parse_date(date_str):
    """Attempts to parse different date formats."""
    try:
        return pd.to_datetime(date_str, format='%d-%b-%y')  # Format 1: '17-Apr-02'
    except ValueError:
        return pd.to_datetime(date_str, format='%b %d, %Y')  # Format 2: 'May 18, 2020'

def load_and_preprocess_data(input_path, output_path):
    """Loads, cleans, and preprocesses Brent oil price data."""
    
    # Load dataset
    df = pd.read_csv(input_path)

    # Convert Date column to datetime format
    df['Date'] = df['Date'].apply(parse_date)

    # Sort by date
    df = df.sort_values(by='Date')

    # Check for duplicates and remove them
    df = df.drop_duplicates()

    # Handle missing values (forward-fill method)
    df['Price'].fillna(method='ffill', inplace=True)

    # Save cleaned dataset
    df.to_csv(output_path, index=False)
    print(f"✅ Data Preprocessing Completed. Processed data saved to: {output_path}")

if __name__ == "__main__":
    load_and_preprocess_data("E:/data/Data10/BrentOilPrices.csv", "E:/data/Data10/processed_data.csv")
