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

# 1. Page title at the very top
st.title("Stock Close Price Viewer")

# 2. Load data
sheet_id = "1Q_En7VGGfifDmn5xuiF-t_02doPpwl4PLzxb4TBCW0Q"  # Replace with your sheet ID
df = load_ohlcv_from_public_sheet(sheet_id)

required_cols = {'date', 'symbol', 'close'}
if not required_cols.issubset(df.columns):
    st.error("Missing required columns in the data.")
    st.stop()

df['date'] = pd.to_datetime(df['date'], errors='coerce')

# 3. Search bar directly below the title
symbols = sorted(df['symbol'].dropna().unique())
selected_symbol = st.selectbox("Select Company Symbol", symbols, key="symbol_select")

filtered_df = df[df['symbol'] == selected_symbol]

if filtered_df.empty:
    st.warning("No data for selected symbol.")
else:
    # 4. Chart uses full width and is larger
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
        plot_bgcolor="white",
        height=700,  # Make the chart bigger
        margin=dict(l=40, r=40, t=60, b=40)
    )

    # 5. Show chart with full width (no columns)
    st.plotly_chart(fig, use_container_width=True)