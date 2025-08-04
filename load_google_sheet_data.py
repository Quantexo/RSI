import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- Custom CSS for background and controls ---
st.markdown("""
    <style>
    .stApp {
        background-color: #335353;
    }
    .stTextInput>div>div>input, .stSelectbox>div>div>div>input {
        background-color: #222c2c;
        color: #fff;
    }
    .stButton>button {
        background-color: #222c2c;
        color: #fff;
        border: 1px solid #ff4444;
        border-radius: 6px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #ff4444;
        color: #fff;
    }
    </style>
""", unsafe_allow_html=True)

def load_ohlcv_from_public_sheet(sheet_id, gid=0):
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
    df = pd.read_csv(url)
    df.columns = [col.lower() for col in df.columns]
    return df

# --- Example sector/company mapping (customize as needed) ---
sector_to_companies = {
    "Index": ["NEPSE"],
    "Commercial Banks": ["NABIL", "NICA", "SCB"],
    "Hydro Power": ["CHCL", "HDHPC", "RHPL"],
    # ... add your actual mappings
}

# --- Controls Row ---
col1, col2, col3, col4, col5 = st.columns([1.2, 1.2, 1.2, 2, 0.7])

with col1:
    selected_sector = st.selectbox("Sector", list(sector_to_companies.keys()), label_visibility="collapsed")
with col2:
    companies = sector_to_companies[selected_sector]
    selected_company = st.selectbox("Company", companies, label_visibility="collapsed")
with col3:
    symbol_input = st.text_input("Enter Symbol", value="", label_visibility="collapsed", placeholder="Enter Symbol")
with col4:
    search_clicked = st.button("Search")
with col5:
    st.write("")  # Spacer

# --- Data Loading ---
sheet_id = "1Q_En7VGGfifDmn5xuiF-t_02doPpwl4PLzxb4TBCW0Q"
df = load_ohlcv_from_public_sheet(sheet_id)
df['date'] = pd.to_datetime(df['date'], errors='coerce')

# --- Symbol selection logic ---
if search_clicked and symbol_input.strip():
    symbol = symbol_input.strip().upper()
elif selected_company:
    symbol = selected_company
else:
    symbol = None

# --- Info Row ---
if not df.empty:
    st.markdown(
        f"<span style='color:#ccc;font-size:14px;'>🕒 Data fetched: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}</span>",
        unsafe_allow_html=True
    )
    if symbol:
        last_data_date = df[df['symbol'] == symbol]['date'].max()
        st.markdown(
            f"<span style='color:#ccc;font-size:14px;'>🗓️ Latest data point: {last_data_date.strftime('%Y-%m-%d') if pd.notnull(last_data_date) else '-'}" ,
            unsafe_allow_html=True
        )

# --- Chart ---
if symbol and not df[df['symbol'] == symbol].empty:
    filtered_df = df[df['symbol'] == symbol]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=filtered_df['date'],
        y=filtered_df['close'],
        mode='lines',
        name='Close Price',
        line=dict(color='#bfefff', width=2)
    ))
    fig.update_layout(
        height=700,
        plot_bgcolor='#335353',
        paper_bgcolor='#335353',
        font_color='white',
        xaxis=dict(title="Date", showgrid=False, tickangle=-30),
        yaxis=dict(title="Price", showgrid=False),
        margin=dict(l=40, r=40, t=40, b=40),
        title=None,
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Please select a company or enter a symbol and click Search.")