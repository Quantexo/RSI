import streamlit as st
import pandas as pd
import plotly.graph_objects as go

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
    df.columns = [col.lower() for col in df.columns]
    return df

# --- Streamlit App ---

st.set_page_config(page_title="Close Price Chart", layout="wide")
st.title("Stock Close Price Viewer")

# Load data
sheet_id = "1Q_En7VGGfifDmn5xuiF-t_02doPpwl4PLzxb4TBCW0Q"  # Replace with your sheet ID
df = load_ohlcv_from_public_sheet(sheet_id)

# Ensure required columns exist
required_cols = {'date', 'symbol', 'close'}
if not required_cols.issubset(df.columns):
    st.error("Missing required columns in the data.")
    st.stop()

# Convert date column to datetime
df['date'] = pd.to_datetime(df['date'], errors='coerce')

# Company selection
symbols = sorted(df['symbol'].dropna().unique())
selected_symbol = st.selectbox("Select Company Symbol", symbols)

# Filter data for selected symbol
filtered_df = df[df['symbol'] == selected_symbol]

if filtered_df.empty:
    st.warning("No data for selected symbol.")
else:
    # Create the close price line chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=filtered_df['date'],
        y=filtered_df['close'],
        mode='lines',
        name='Close Price',
        line=dict(color='royalblue', width=2)
    ))
    fig.update_layout(
        title=f"Close Price for {selected_symbol}",
        xaxis_title="Date",
        yaxis_title="Close Price",
        plot_bgcolor="white"
    )

    # Center the chart using columns
    left, center, right = st.columns([1, 2, 1])
    with center:
        st.plotly_chart(fig, use_container_width=True)