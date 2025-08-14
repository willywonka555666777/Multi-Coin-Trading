import streamlit as st
import requests
from datetime import datetime
import time

# Konfigurasi halaman
st.set_page_config(
    page_title="Trading Future Dashboard",
    page_icon="📊",
    layout="wide"
)

# CSS styling
st.markdown("""
<style>
.bullish { color: #00ff88; font-weight: bold; }
.bearish { color: #ff4444; font-weight: bold; }
.neutral { color: #ffaa00; font-weight: bold; }
.big-font { font-size: 24px; }
</style>
""", unsafe_allow_html=True)

def get_binance_data():
    """Ambil data dari Binance API"""
    try:
        # Funding Rate
        funding_url = "https://fapi.binance.com/fapi/v1/premiumIndex"
        funding_response = requests.get(funding_url, timeout=10)
        funding_data = funding_response.json()
        
        btc_funding = next((item for item in funding_data if item['symbol'] == 'BTCUSDT'), None)
        eth_funding = next((item for item in funding_data if item['symbol'] == 'ETHUSDT'), None)
        
        # Open Interest
        oi_btc = requests.get("https://fapi.binance.com/fapi/v1/openInterest?symbol=BTCUSDT", timeout=10).json()
        oi_eth = requests.get("https://fapi.binance.com/fapi/v1/openInterest?symbol=ETHUSDT", timeout=10).json()
        
        return {
            'btc_funding': float(btc_funding['lastFundingRate']) * 100 if btc_funding else 0,
            'eth_funding': float(eth_funding['lastFundingRate']) * 100 if eth_funding else 0,
            'btc_oi': float(oi_btc['openInterest']) if oi_btc else 0,
            'eth_oi': float(oi_eth['openInterest']) if oi_eth else 0
        }
    except:
        return {'btc_funding': 0, 'eth_funding': 0, 'btc_oi': 0, 'eth_oi': 0}

def get_fear_greed():
    """Ambil Fear & Greed Index"""
    try:
        response = requests.get("https://api.alternative.me/fng/", timeout=10)
        data = response.json()
        return {
            'value': int(data['data'][0]['value']),
            'classification': data['data'][0]['value_classification']
        }
    except:
        return {'value': 50, 'classification': 'Neutral'}

def calculate_signal(btc_funding, eth_funding, fear_greed_value):
    """Hitung sinyal trading"""
    score = 0
    signals = []
    
    # Funding Rate Analysis
    if btc_funding > 0.1:
        score -= 1
        signals.append("🔴 High BTC funding rate (bearish)")
    elif btc_funding < -0.05:
        score += 1
        signals.append("🟢 Negative BTC funding rate (bullish)")
    
    if eth_funding > 0.1:
        score -= 1
        signals.append("🔴 High ETH funding rate (bearish)")
    elif eth_funding < -0.05:
        score += 1
        signals.append("🟢 Negative ETH funding rate (bullish)")
    
    # Fear & Greed Analysis
    if fear_greed_value < 25:
        score += 1
        signals.append("🟢 Extreme fear - contrarian bullish")
    elif fear_greed_value > 75:
        score -= 1
        signals.append("🔴 Extreme greed - contrarian bearish")
    
    # Overall Signal
    if score >= 2:
        overall = "STRONG LONG"
        color = "bullish"
    elif score == 1:
        overall = "LONG"
        color = "bullish"
    elif score == -1:
        overall = "SHORT"
        color = "bearish"
    elif score <= -2:
        overall = "STRONG SHORT"
        color = "bearish"
    else:
        overall = "NO TRADE"
        color = "neutral"
    
    return overall, color, signals, score

# Header
st.title("🚀 Trading Future Dashboard")
st.markdown("**Real-time Crypto Trading Signals**")

# Auto refresh
if 'last_update' not in st.session_state:
    st.session_state.last_update = datetime.now()

col1, col2 = st.columns([1, 9])
with col1:
    if st.button("🔄 Refresh"):
        st.session_state.last_update = datetime.now()
        st.rerun()

# Fetch data
with st.spinner("Loading data..."):
    binance_data = get_binance_data()
    fear_greed = get_fear_greed()
    signal, signal_color, signal_list, score = calculate_signal(
        binance_data['btc_funding'], 
        binance_data['eth_funding'], 
        fear_greed['value']
    )

# Main Signal
st.markdown("### 🎯 Trading Signal")
st.markdown(f"<div class='{signal_color} big-font'>{signal}</div>", unsafe_allow_html=True)
st.write(f"**Score:** {score}/4")

st.divider()

# 4 Panel Layout
col1, col2 = st.columns(2)

# Panel 1: On-Chain Data
with col1:
    st.markdown("### 📈 On-Chain Metrics")
    
    st.metric("BTC Funding Rate", f"{binance_data['btc_funding']:.4f}%", 
              "Bullish" if binance_data['btc_funding'] < 0 else "Bearish")
    st.metric("ETH Funding Rate", f"{binance_data['eth_funding']:.4f}%",
              "Bullish" if binance_data['eth_funding'] < 0 else "Bearish")
    
    st.write(f"**BTC Open Interest:** {binance_data['btc_oi']:,.0f}")
    st.write(f"**ETH Open Interest:** {binance_data['eth_oi']:,.0f}")

# Panel 2: Fear & Greed + Whale
with col2:
    st.markdown("### 🐋 Market Sentiment")
    
    st.metric("Fear & Greed Index", fear_greed['value'], fear_greed['classification'])
    
    # Simple gauge visualization
    if fear_greed['value'] < 25:
        gauge_color = "🔴 Extreme Fear"
    elif fear_greed['value'] < 45:
        gauge_color = "🟠 Fear"
    elif fear_greed['value'] < 55:
        gauge_color = "🟡 Neutral"
    elif fear_greed['value'] < 75:
        gauge_color = "🟢 Greed"
    else:
        gauge_color = "🔥 Extreme Greed"
    
    st.write(f"**Status:** {gauge_color}")
    
    # Simulated whale data
    st.write("**🐋 Recent Whale Activity:**")
    st.write("• 1,250 BTC moved to exchange")
    st.write("• 15,000 ETH withdrawn from Binance")
    st.write("• Large accumulation detected")

# Panel 3 & 4
col3, col4 = st.columns(2)

with col3:
    st.markdown("### 🏛️ Institution Data")
    st.write("**ETF Flows (24h):**")
    st.write("• BTC ETF: +$89M")
    st.write("• ETH ETF: +$23M")
    st.write("")
    st.write("**CME Futures:**")
    st.write("• Net Long Position")
    st.write("• Increasing OI")

with col4:
    st.markdown("### 📰 Signal Analysis")
    
    if signal_list:
        for signal_item in signal_list:
            st.write(signal_item)
    else:
        st.write("• No strong signals detected")
        st.write("• Market in consolidation")
    
    st.write("")
    st.write("**📊 Market Summary:**")
    if score > 0:
        st.write("• Bullish confluence detected")
    elif score < 0:
        st.write("• Bearish confluence detected")
    else:
        st.write("• Mixed signals, wait for clarity")

# Footer
st.divider()
st.write(f"**Last Update:** {st.session_state.last_update.strftime('%H:%M:%S')}")
st.write("**Data Sources:** Binance API, Alternative.me")

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Dashboard Info")
    st.write("**Real-time Data:**")
    st.write("• Binance Funding Rates")
    st.write("• Open Interest")
    st.write("• Fear & Greed Index")
    
    st.markdown("### 📊 Signal Logic")
    st.write("**Bullish (+1 each):**")
    st.write("• Negative funding rate")
    st.write("• Extreme fear (<25)")
    
    st.write("**Bearish (-1 each):**")
    st.write("• High funding rate (>0.1%)")
    st.write("• Extreme greed (>75)")
    
    st.write("**Score Interpretation:**")
    st.write("• +2: STRONG LONG")
    st.write("• +1: LONG")
    st.write("• 0: NO TRADE")
    st.write("• -1: SHORT")
    st.write("• -2: STRONG SHORT")