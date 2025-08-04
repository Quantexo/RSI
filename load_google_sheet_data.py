import pandas as pd

def load_ohlcv_from_public_sheet(sheet_id, gid=0):
    """
    Loads OHLCV data from a public Google Sheet published as CSV.
    Args:
        sheet_id (str): The Google Sheet ID (from the URL).
        gid (int): The sheet/tab GID (default 0 for the first sheet).
    Returns:
        pd.DataFrame: DataFrame with columns ['date', 'symbol', 'open', 'high', 'low', 'close', 'volume']
    """
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
    df = pd.read_csv(url)
    # Optionally, rename columns to lowercase
    df.columns = [col.lower() for col in df.columns]
    return df

# Example usage:
if __name__ == "__main__":
    sheet_id = "1Q_En7VGGfifDmn5xuiF-t_02doPpwl4PLzxb4TBCW0Q"  # Replace with your sheet ID
    df = load_ohlcv_from_public_sheet(sheet_id)
    print(df.head())