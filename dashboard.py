import streamlit as st
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
from data_fetcher import DataFetcher

# Konfigurasi halaman
st.set_page_config(
    page_title="Trading Future Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS untuk styling
st.markdown("""
<style>
.metric-card {
    background-color: #1e1e1e;
    padding: 1rem;
    border-radius: 0.5rem;
    border: 1px solid #333;
}
.bullish { color: #00ff88; }
.bearish { color: #ff4444; }
.neutral { color: #ffaa00; }
</style>
""", unsafe_allow_html=True)

# Inisialisasi data fetcher
@st.cache_resource
def init_data_fetcher():
    return DataFetcher()

data_fetcher = init_data_fetcher()

# Header
st.title("🚀 Trading Future Dashboard")
st.markdown("**Real-time Crypto Trading Signals & Analysis**")

# Auto refresh setiap 30 detik
if 'last_update' not in st.session_state:
    st.session_state.last_update = datetime.now()

# Tombol refresh manual
col1, col2, col3 = st.columns([1, 1, 8])
with col1:
    if st.button("🔄 Refresh"):
        st.session_state.last_update = datetime.now()
        st.rerun()

with col2:
    auto_refresh = st.checkbox("Auto Refresh", value=True)

# Auto refresh logic
if auto_refresh:
    time_diff = (datetime.now() - st.session_state.last_update).seconds
    if time_diff > 30:  # Refresh setiap 30 detik
        st.session_state.last_update = datetime.now()
        st.rerun()

# Fetch data
with st.spinner("Loading data..."):
    funding_data = data_fetcher.get_binance_funding_rate()
    oi_data = data_fetcher.get_binance_oi()
    fear_greed = data_fetcher.get_fear_greed_index()
    news_data = data_fetcher.get_crypto_news()
    whale_data = data_fetcher.get_whale_alerts()
    signal_analysis = data_fetcher.calculate_signal_score(funding_data, fear_greed)

# Main Signal Panel
st.markdown("### 🎯 Trading Signal")
col1, col2, col3, col4 = st.columns(4)

with col1:
    signal_color = "bullish" if "LONG" in signal_analysis['overall'] else "bearish" if "SHORT" in signal_analysis['overall'] else "neutral"
    st.markdown(f"<h2 class='{signal_color}'>{signal_analysis['overall']}</h2>", unsafe_allow_html=True)
    st.write(f"Score: {signal_analysis['score']}")

with col2:
    st.metric("Fear & Greed", f"{fear_greed['value']}", fear_greed['classification'])

with col3:
    st.metric("BTC Funding", f"{funding_data['BTC']:.4f}%", 
              "Bullish" if funding_data['BTC'] < 0 else "Bearish")

with col4:
    st.metric("ETH Funding", f"{funding_data['ETH']:.4f}%",
              "Bullish" if funding_data['ETH'] < 0 else "Bearish")

st.divider()

# 4 Panel Layout
col1, col2 = st.columns(2)

# Panel 1: On-Chain Data
with col1:
    st.markdown("### 📈 On-Chain Metrics")
    
    # Funding Rate Chart
    fig_funding = go.Figure()
    fig_funding.add_trace(go.Bar(
        x=['BTC', 'ETH'],
        y=[funding_data['BTC'], funding_data['ETH']],
        marker_color=['#f7931a', '#627eea'],
        text=[f"{funding_data['BTC']:.4f}%", f"{funding_data['ETH']:.4f}%"],
        textposition='auto'
    ))
    fig_funding.update_layout(
        title="Funding Rate (%)",
        height=300,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_funding, use_container_width=True)
    
    # Open Interest
    st.markdown("**Open Interest**")
    st.write(f"BTC: {oi_data['BTC']:,.0f}")
    st.write(f"ETH: {oi_data['ETH']:,.0f}")

# Panel 2: Whale Movement
with col2:
    st.markdown("### 🐋 Whale Activity")
    
    if whale_data:
        for whale in whale_data[:3]:  # Show top 3
            whale_type = whale['type'].replace('_', ' ').title()
            color = "🔴" if "inflow" in whale['type'] else "🟢"
            st.write(f"{color} {whale['amount']:,.0f} {whale['symbol']} - {whale_type}")
    else:
        st.write("No recent whale activity")
    
    # Fear & Greed Gauge
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = fear_greed['value'],
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Fear & Greed Index"},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 25], 'color': "red"},
                {'range': [25, 75], 'color': "yellow"},
                {'range': [75, 100], 'color': "green"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    fig_gauge.update_layout(height=300, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_gauge, use_container_width=True)

# Panel 3: Institution & ETF (Simulasi)
col3, col4 = st.columns(2)

with col3:
    st.markdown("### 🏛️ Institution Data")
    st.write("📊 **ETF Flows (Simulated)**")
    st.write("• BTC ETF: +$125M inflow")
    st.write("• ETH ETF: +$45M inflow")
    st.write("")
    st.write("📋 **CME Futures**")
    st.write("• Large Specs: Net Long")
    st.write("• Commercials: Net Short")

# Panel 4: News & Sentiment
with col4:
    st.markdown("### 📰 News & Sentiment")
    
    if news_data:
        for news in news_data[:3]:
            sentiment_color = "🟢" if news['sentiment'] == 'bullish' else "🔴" if news['sentiment'] == 'bearish' else "🟡"
            st.write(f"{sentiment_color} {news['title']}")
    
    st.write("")
    st.write("**Signal Analysis:**")
    for signal in signal_analysis['signals']:
        st.write(f"• {signal}")

# Footer dengan timestamp
st.divider()
st.markdown(f"**Last Update:** {st.session_state.last_update.strftime('%H:%M:%S')} | **Next Refresh:** {auto_refresh}")

# Sidebar dengan pengaturan
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    st.write("**Refresh Interval:** 30 seconds")
    st.write("**Data Sources:**")
    st.write("• Binance API (Funding, OI)")
    st.write("• Alternative.me (Fear & Greed)")
    st.write("• Simulated (Whale, News)")
    
    st.markdown("### 📊 Signal Scoring")
    st.write("**Bullish Signals:**")
    st.write("• Negative funding rate")
    st.write("• Extreme fear (<25)")
    st.write("• Whale accumulation")
    
    st.write("**Bearish Signals:**")
    st.write("• High funding rate (>0.1%)")
    st.write("• Extreme greed (>75)")
    st.write("• Whale distribution")