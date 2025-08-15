import streamlit as st
from datetime import datetime
import random

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

# Demo data
COINS = {
    'BTC': {'price': 43250, 'change': 2.45},
    'ETH': {'price': 2650, 'change': 1.85},
    'SOL': {'price': 98.45, 'change': 3.25},
    'BNB': {'price': 315, 'change': -0.75}
}

st.title("🚀 Trading Dashboard - Demo Mode")
st.success("✅ Demo Mode - No API limits!")

# Coin selection
selected_coin = st.selectbox("Select Coin:", list(COINS.keys()))
if st.button("🔄 Refresh"):
    st.rerun()

# Get data with random variation
base = COINS[selected_coin]
price = base['price'] * random.uniform(0.98, 1.02)
change = base['change'] + random.uniform(-0.5, 0.5)
funding = random.uniform(-0.05, 0.15)
fear_greed = random.randint(20, 80)

# Calculate signal
score = 0
signals = []

if change > 3:
    score += 1
    signals.append('🟢 Strong bullish momentum')
elif change < -3:
    score -= 1
    signals.append('🔴 Strong bearish momentum')

if funding > 0.1:
    score -= 1
    signals.append('🔴 High funding rate')
elif funding < -0.02:
    score += 1
    signals.append('🟢 Negative funding rate')

if fear_greed < 30:
    score += 1
    signals.append('🟢 Extreme fear - bullish')
elif fear_greed > 70:
    score -= 1
    signals.append('🔴 Extreme greed - bearish')

# Signal determination
if score >= 2:
    signal, color, confidence = 'STRONG LONG', 'bullish', 'High'
elif score >= 1:
    signal, color, confidence = 'LONG', 'bullish', 'Medium'
elif score <= -2:
    signal, color, confidence = 'STRONG SHORT', 'bearish', 'High'
elif score <= -1:
    signal, color, confidence = 'SHORT', 'bearish', 'Medium'
else:
    signal, color, confidence = 'NO TRADE', 'neutral', 'Low'

# Display
st.markdown("### 🎯 Trading Signal")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"<div class='{color} big-font'>{signal}</div>", unsafe_allow_html=True)
    st.write(f"**Confidence:** {confidence}")

with col2:
    st.metric(f"{selected_coin} Price", f"${price:,.2f}", f"{change:+.2f}%")

with col3:
    st.metric("Funding Rate", f"{funding:.4f}%")

with col4:
    st.metric("Fear & Greed", fear_greed)

# Entry setup
if signal != "NO TRADE":
    entry = price * 0.995 if "LONG" in signal else price * 1.005
    stop = price * 0.97 if "LONG" in signal else price * 1.03
    target = price * 1.06 if "LONG" in signal else price * 0.94
    
    st.markdown(f"""
    <div class="entry-box">
    <h3>📍 Entry Setup</h3>
    <p><strong>Signal:</strong> <span class="{color}">{signal}</span></p>
    <p><strong>Entry:</strong> ${entry:,.2f}</p>
    <p><strong>Stop Loss:</strong> ${stop:,.2f}</p>
    <p><strong>Take Profit:</strong> ${target:,.2f}</p>
    <p><strong>R:R Ratio:</strong> 1:2</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# Analysis
col1, col2 = st.columns(2)
with col1:
    st.markdown("### 📊 Market Data")
    st.write(f"Price: ${price:,.2f}")
    st.write(f"24h Change: {change:+.2f}%")
    st.write(f"Funding Rate: {funding:.4f}%")

with col2:
    st.markdown("### 🎯 Signals")
    for s in signals:
        st.write(s)
    if not signals:
        st.write("• No strong signals")
    st.write(f"**Score:** {score}")

st.write(f"**Last Update:** {datetime.now().strftime('%H:%M:%S')}")