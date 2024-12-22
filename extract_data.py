import requests
import pandas as pd

def get_stock_data(symbol, api_key, outputsize='full'):
    """
    Fetches historical stock data from Alpha Vantage API.

    Args:
        symbol: Stock symbol (e.g., 'AAPL').
        api_key: Your Alpha Vantage API key.
        outputsize: Size of the dataset ('compact' or 'full').

    Returns:
        pandas.DataFrame: DataFrame containing the historical stock data.
    """
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}&outputsize={outputsize}"
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for bad status codes

    data = response.json()
    if 'Time Series (Daily)' not in data:
        raise ValueError(f"No 'Time Series (Daily)' data found for {symbol}")

    df = pd.DataFrame.from_dict(data['Time Series (Daily)'], orient='index', dtype=float)
    df.index = pd.to_datetime(df.index)
    df.columns = ['open', 'high', 'low', 'close', 'volume']
    return df

# Example usage:
if __name__ == "__main__":
    api_key = "YOUR_API_KEY"  # Replace with your actual API key
    symbol = "AAPL"
    df = get_stock_data(symbol, api_key)
    print(df.head())
    df.to_csv(f"{symbol}_data.csv", index_label="Date")
