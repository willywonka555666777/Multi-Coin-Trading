import streamlit as st
import requests
from datetime import datetime
import time

st.set_page_config(page_title="Trading Dashboard", page_icon="📊", layout="wide")

st.markdown("""
<style>
.bullish { color: #00ff88; font-weight: bold; }
.bearish { color: #ff4444; font-weight: bold; }
.neutral { color: #ffaa00; font-weight: bold; }
.big-font { font-size: 28px; }
.entry-box { background-color: #808080; padding: 15px; border-radius: 10px; margin: 10px 0; }
</style>
""", unsafe_allow_html=True)

# CoinCap API mapping
COINS = {
    'BTC': 'bitcoin',
    'ETH': 'ethereum', 
    'SOL': 'solana',
    'BNB': 'binance-coin',
    'ADA': 'cardano',
    'XRP': 'xrp',
    'DOGE': 'dogecoin'
}

@st.cache_data(ttl=60)  # Cache for 1 minute
def get_coincap_data(coin_id):
    """Get data from CoinCap API (free, reliable)"""
    try:
        # CoinCap API - no rate limits
        url = f"https://api.coincap.io/v2/assets/{coin_id}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()['data']
            return {
                'price': float(data['priceUsd']),
                'change_24h': float(data['changePercent24Hr']),
                'volume': float(data['volumeUsd24Hr']),
                'market_cap': float(data['marketCapUsd'])
            }
        else:
            return None
    except:
        return None

def get_fear_greed():
    """Get Fear & Greed from alternative API"""
    try:
        response = requests.get("https://api.alternative.me/fng/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            return {
                'value': int(data['data'][0]['value']),
                'classification': data['data'][0]['value_classification']
            }
    except:
        pass
    return {'value': 50, 'classification': 'Neutral'}

def calculate_signal(coin_data, fear_greed):
    """Calculate trading signal"""
    score = 0
    signals = []
    
    # Price momentum
    if coin_data['change_24h'] > 5:
        score += 1
        signals.append('🟢 Strong bullish momentum (+5%)')
    elif coin_data['change_24h'] < -5:
        score -= 1
        signals.append('🔴 Strong bearish momentum (-5%)')
    elif coin_data['change_24h'] > 2:
        signals.append('🟡 Moderate bullish trend')
    elif coin_data['change_24h'] < -2:
        signals.append('🟡 Moderate bearish trend')
    
    # Volume analysis
    if coin_data['volume'] > 1000000000:  # $1B+
        score += 0.5
        signals.append('🟢 High volume confirmation')
    
    # Fear & Greed
    if fear_greed['value'] < 25:
        score += 1
        signals.append('🟢 Extreme fear - contrarian bullish')
    elif fear_greed['value'] > 75:
        score -= 1
        signals.append('🔴 Extreme greed - potential reversal')
    
    # Market cap stability (for large caps)
    if coin_data['market_cap'] > 100000000000:  # $100B+
        score += 0.5
        signals.append('🟢 Large cap stability')
    
    # Signal determination
    if score >= 2:
        return {'signal': 'STRONG LONG', 'color': 'bullish', 'confidence': 'High', 'score': score, 'signals': signals}
    elif score >= 1:
        return {'signal': 'LONG', 'color': 'bullish', 'confidence': 'Medium', 'score': score, 'signals': signals}
    elif score <= -2:
        return {'signal': 'STRONG SHORT', 'color': 'bearish', 'confidence': 'High', 'score': score, 'signals': signals}
    elif score <= -1:
        return {'signal': 'SHORT', 'color': 'bearish', 'confidence': 'Medium', 'score': score, 'signals': signals}
    else:
        return {'signal': 'NO TRADE', 'color': 'neutral', 'confidence': 'Low', 'score': score, 'signals': signals}

# Main app
st.title("🚀 Real-Time Trading Dashboard")
st.success("✅ CoinCap API - Real data, no limits!")

# Coin selection
col1, col2 = st.columns([2, 8])
with col1:
    selected_coin = st.selectbox("Select Coin:", list(COINS.keys()))
    if st.button("🔄 Refresh"):
        st.cache_data.clear()
        st.rerun()

# Get real data
with st.spinner("Loading real-time data..."):
    coin_data = get_coincap_data(COINS[selected_coin])
    fear_greed = get_fear_greed()

if coin_data:
    analysis = calculate_signal(coin_data, fear_greed)
    
    # Main display
    st.markdown("### 🎯 Trading Signal")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"<div class='{analysis['color']} big-font'>{analysis['signal']}</div>", unsafe_allow_html=True)
        st.write(f"**Confidence:** {analysis['confidence']}")
    
    with col2:
        st.metric(f"{selected_coin} Price", f"${coin_data['price']:,.2f}", f"{coin_data['change_24h']:+.2f}%")
    
    with col3:
        st.metric("24h Volume", f"${coin_data['volume']:,.0f}")
    
    with col4:
        st.metric("Fear & Greed", fear_greed['value'], fear_greed['classification'])
    
    # Entry setup
    if analysis['signal'] != "NO TRADE":
        entry = coin_data['price'] * 0.995 if "LONG" in analysis['signal'] else coin_data['price'] * 1.005
        stop = coin_data['price'] * 0.97 if "LONG" in analysis['signal'] else coin_data['price'] * 1.03
        target = coin_data['price'] * 1.06 if "LONG" in analysis['signal'] else coin_data['price'] * 0.94
        
        st.markdown(f"""
        <div class="entry-box">
        <h3>📍 Entry Setup for {selected_coin}</h3>
        <p><strong>Signal:</strong> <span class="{analysis['color']}">{analysis['signal']}</span></p>
        <p><strong>Entry Price:</strong> ${entry:,.2f}</p>
        <p><strong>Stop Loss:</strong> ${stop:,.2f} (3% risk)</p>
        <p><strong>Take Profit:</strong> ${target:,.2f} (6% target)</p>
        <p><strong>Risk/Reward:</strong> 1:2 | <strong>Score:</strong> {analysis['score']:.1f}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if analysis['confidence'] == 'High':
            st.success("🎯 High confidence setup - Consider 2-3% position size")
        else:
            st.warning("⚠️ Medium confidence - Consider 1-2% position size")
    
    st.divider()
    
    # Analysis panels
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Market Data")
        st.write(f"**Price:** ${coin_data['price']:,.2f}")
        st.write(f"**24h Change:** {coin_data['change_24h']:+.2f}%")
        st.write(f"**24h Volume:** ${coin_data['volume']:,.0f}")
        st.write(f"**Market Cap:** ${coin_data['market_cap']:,.0f}")
    
    with col2:
        st.markdown("### 🎯 Signal Analysis")
        for signal in analysis['signals']:
            st.write(signal)
        if not analysis['signals']:
            st.write("• No strong signals detected")
        st.write(f"**Total Score:** {analysis['score']:.1f}")
    
    st.write(f"**Last Update:** {datetime.now().strftime('%H:%M:%S')} | **Source:** CoinCap API")

else:
    st.error("❌ Failed to load data. Please try again.")
    st.info("💡 Try refreshing or select different coin")
