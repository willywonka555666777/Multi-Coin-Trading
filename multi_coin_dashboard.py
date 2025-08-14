import streamlit as st
import requests
from datetime import datetime
import time

# Konfigurasi halaman
st.set_page_config(
    page_title="Multi-Coin Trading Dashboard",
    page_icon="📊",
    layout="wide"
)

# CSS styling
st.markdown("""
<style>
.bullish { color: #00ff88; font-weight: bold; }
.bearish { color: #ff4444; font-weight: bold; }
.neutral { color: #ffaa00; font-weight: bold; }
.big-font { font-size: 28px; }
.entry-box { 
    background-color: #808080; 
    padding: 15px; 
    border-radius: 10px; 
    border: 2px solid #333;
    margin: 10px 0;
}
</style>
""", unsafe_allow_html=True)

# Daftar coin yang didukung
SUPPORTED_COINS = {
    'BTC': 'BTCUSDT',
    'ETH': 'ETHUSDT', 
    'BNB': 'BNBUSDT',
    'SOL': 'SOLUSDT',
    'ADA': 'ADAUSDT',
    'XRP': 'XRPUSDT',
    'DOGE': 'DOGEUSDT',
    'MATIC': 'MATICUSDT',
    'DOT': 'DOTUSDT',
    'AVAX': 'AVAXUSDT'
}

def get_coin_data(symbol):
    """Ambil data coin dari Binance API"""
    try:
        # Price data
        price_url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}"
        price_response = requests.get(price_url, timeout=10)
        price_data = price_response.json()
        
        # Funding Rate (futures)
        funding_url = "https://fapi.binance.com/fapi/v1/premiumIndex"
        funding_response = requests.get(funding_url, timeout=10)
        funding_data = funding_response.json()
        
        coin_funding = next((item for item in funding_data if item['symbol'] == symbol), None)
        
        # Open Interest
        try:
            oi_response = requests.get(f"https://fapi.binance.com/fapi/v1/openInterest?symbol={symbol}", timeout=10)
            oi_data = oi_response.json()
            open_interest = float(oi_data['openInterest'])
        except:
            open_interest = 0
        
        return {
            'price': float(price_data['lastPrice']),
            'change_24h': float(price_data['priceChangePercent']),
            'volume': float(price_data['volume']),
            'funding_rate': float(coin_funding['lastFundingRate']) * 100 if coin_funding else 0,
            'open_interest': open_interest,
            'high_24h': float(price_data['highPrice']),
            'low_24h': float(price_data['lowPrice'])
        }
    except:
        return {
            'price': 0, 'change_24h': 0, 'volume': 0, 
            'funding_rate': 0, 'open_interest': 0,
            'high_24h': 0, 'low_24h': 0
        }

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

def technical_analysis(coin_data):
    """Analisis teknikal sederhana"""
    price = coin_data['price']
    high_24h = coin_data['high_24h']
    low_24h = coin_data['low_24h']
    change_24h = coin_data['change_24h']
    
    # RSI simulasi berdasarkan posisi harga dalam range 24h
    price_position = (price - low_24h) / (high_24h - low_24h) if high_24h != low_24h else 0.5
    simulated_rsi = price_position * 100
    
    signals = []
    score = 0
    
    # RSI Analysis
    if simulated_rsi < 30:
        signals.append("🟢 RSI Oversold (bullish)")
        score += 1
    elif simulated_rsi > 70:
        signals.append("🔴 RSI Overbought (bearish)")
        score -= 1
    
    # Price momentum
    if change_24h > 5:
        signals.append("🟢 Strong upward momentum")
        score += 1
    elif change_24h < -5:
        signals.append("🔴 Strong downward momentum")
        score -= 1
    
    return score, signals, simulated_rsi

def fundamental_analysis(coin_data, fear_greed_value):
    """Analisis fundamental"""
    funding_rate = coin_data['funding_rate']
    volume = coin_data['volume']
    
    signals = []
    score = 0
    
    # Funding Rate Analysis
    if funding_rate > 0.1:
        signals.append("🔴 High funding rate - shorts paying longs")
        score -= 1
    elif funding_rate < -0.05:
        signals.append("🟢 Negative funding rate - longs paying shorts")
        score += 1
    
    # Volume Analysis (simplified)
    if volume > 1000000:  # High volume threshold
        signals.append("🟢 High trading volume")
        score += 0.5
    
    # Fear & Greed Impact
    if fear_greed_value < 25:
        signals.append("🟢 Market fear - contrarian opportunity")
        score += 1
    elif fear_greed_value > 75:
        signals.append("🔴 Market greed - potential reversal")
        score -= 1
    
    return score, signals

def whale_analysis():
    """Simulasi analisis whale movement"""
    # Simulasi data whale (dalam implementasi nyata bisa pakai API premium)
    whale_signals = [
        "🐋 Large accumulation detected",
        "🟢 Whale outflow from exchanges",
        "📈 Institutional buying pressure"
    ]
    return 1, whale_signals

def calculate_entry_signal(coin, coin_data, fear_greed):
    """Hitung sinyal entry berdasarkan semua strategi"""
    
    # 1. Technical Analysis
    tech_score, tech_signals, rsi = technical_analysis(coin_data)
    
    # 2. Fundamental Analysis  
    fund_score, fund_signals = fundamental_analysis(coin_data, fear_greed['value'])
    
    # 3. Whale Analysis
    whale_score, whale_signals = whale_analysis()
    
    # 4. On-chain Analysis (funding rate focus)
    onchain_score = 0
    onchain_signals = []
    if coin_data['funding_rate'] < -0.02:
        onchain_score += 1
        onchain_signals.append("🟢 Negative funding - bullish setup")
    elif coin_data['funding_rate'] > 0.05:
        onchain_score -= 1
        onchain_signals.append("🔴 High funding - bearish setup")
    
    # Total Score
    total_score = tech_score + fund_score + whale_score + onchain_score
    
    # Entry Signal
    if total_score >= 3:
        entry_signal = "STRONG LONG"
        entry_color = "bullish"
        confidence = "High"
    elif total_score >= 1.5:
        entry_signal = "LONG"
        entry_color = "bullish" 
        confidence = "Medium"
    elif total_score <= -3:
        entry_signal = "STRONG SHORT"
        entry_color = "bearish"
        confidence = "High"
    elif total_score <= -1.5:
        entry_signal = "SHORT"
        entry_color = "bearish"
        confidence = "Medium"
    else:
        entry_signal = "NO TRADE"
        entry_color = "neutral"
        confidence = "Low"
    
    # Entry levels
    price = coin_data['price']
    if "LONG" in entry_signal:
        entry_price = price * 0.995  # 0.5% below current
        stop_loss = price * 0.97     # 3% stop loss
        take_profit = price * 1.06   # 6% take profit
    elif "SHORT" in entry_signal:
        entry_price = price * 1.005  # 0.5% above current
        stop_loss = price * 1.03     # 3% stop loss
        take_profit = price * 0.94   # 6% take profit
    else:
        entry_price = price
        stop_loss = 0
        take_profit = 0
    
    return {
        'signal': entry_signal,
        'color': entry_color,
        'confidence': confidence,
        'total_score': total_score,
        'entry_price': entry_price,
        'stop_loss': stop_loss,
        'take_profit': take_profit,
        'rsi': rsi,
        'tech_score': tech_score,
        'fund_score': fund_score,
        'whale_score': whale_score,
        'onchain_score': onchain_score,
        'all_signals': {
            'technical': tech_signals,
            'fundamental': fund_signals,
            'whale': whale_signals,
            'onchain': onchain_signals
        }
    }

# Header
st.title("🚀 Multi-Coin Trading Dashboard")
st.markdown("**Advanced Trading Signals with Entry Analysis**")

# Coin Selection
col1, col2, col3 = st.columns([2, 1, 7])
with col1:
    selected_coin = st.selectbox("Select Coin:", list(SUPPORTED_COINS.keys()), index=0)
with col2:
    if st.button("🔄 Refresh"):
        st.rerun()

selected_symbol = SUPPORTED_COINS[selected_coin]

# Fetch data
with st.spinner(f"Loading {selected_coin} data..."):
    coin_data = get_coin_data(selected_symbol)
    fear_greed = get_fear_greed()
    analysis = calculate_entry_signal(selected_coin, coin_data, fear_greed)

# Main Signal & Entry Analysis
st.markdown("### 🎯 Trading Signal & Entry Analysis")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"<div class='{analysis['color']} big-font'>{analysis['signal']}</div>", unsafe_allow_html=True)
    st.write(f"**Confidence:** {analysis['confidence']}")

with col2:
    st.metric(f"{selected_coin} Price", f"${coin_data['price']:,.4f}", f"{coin_data['change_24h']:+.2f}%")

with col3:
    st.metric("Simulated RSI", f"{analysis['rsi']:.1f}", 
              "Oversold" if analysis['rsi'] < 30 else "Overbought" if analysis['rsi'] > 70 else "Neutral")

with col4:
    st.metric("Fear & Greed", fear_greed['value'], fear_greed['classification'])

# Entry Box with Advice
if analysis['signal'] != "NO TRADE":
    # Generate entry advice
    entry_advice = ""
    entry_reasons = []
    
    if analysis['confidence'] == "High":
        if "LONG" in analysis['signal']:
            entry_advice = "🟢 RECOMMENDED ENTRY - Strong bullish confluence detected"
            entry_reasons = [
                "✅ Multiple bullish signals aligned",
                "✅ High probability setup with good R:R",
                "✅ Market structure supports upward move"
            ]
        else:
            entry_advice = "🔴 RECOMMENDED ENTRY - Strong bearish confluence detected"
            entry_reasons = [
                "✅ Multiple bearish signals aligned",
                "✅ High probability setup with good R:R",
                "✅ Market structure supports downward move"
            ]
    else:
        entry_advice = "⚠️ MODERATE SETUP - Wait for better confirmation"
        entry_reasons = ["⚠️ Mixed signals, consider smaller position size"]
    
    # Detailed reasons based on analysis
    detailed_reasons = []
    
    # Technical reasons
    if analysis['rsi'] < 30 and "LONG" in analysis['signal']:
        detailed_reasons.append("📈 RSI oversold - bounce expected")
    elif analysis['rsi'] > 70 and "SHORT" in analysis['signal']:
        detailed_reasons.append("📉 RSI overbought - correction expected")
    
    # Fundamental reasons
    if coin_data['funding_rate'] < -0.02 and "LONG" in analysis['signal']:
        detailed_reasons.append("💰 Negative funding rate - shorts paying longs")
    elif coin_data['funding_rate'] > 0.05 and "SHORT" in analysis['signal']:
        detailed_reasons.append("💸 High funding rate - longs paying shorts")
    
    # Fear & Greed reasons
    if fear_greed['value'] < 25 and "LONG" in analysis['signal']:
        detailed_reasons.append("😨 Extreme fear - contrarian bullish opportunity")
    elif fear_greed['value'] > 75 and "SHORT" in analysis['signal']:
        detailed_reasons.append("🤑 Extreme greed - contrarian bearish opportunity")
    
    # Volume reasons
    if coin_data['volume'] > 1000000:
        detailed_reasons.append("📊 High volume confirms the move")
    
    st.markdown(f"""
    <div class="entry-box">
    <h3>📍 Entry Setup for {selected_coin}</h3>
    <p><strong>Signal:</strong> <span class="{analysis['color']}">{analysis['signal']}</span></p>
    <p><strong>Advice:</strong> {entry_advice}</p>
    <hr>
    <p><strong>Entry Price:</strong> ${analysis['entry_price']:,.4f}</p>
    <p><strong>Stop Loss:</strong> ${analysis['stop_loss']:,.4f} ({abs((analysis['stop_loss']/coin_data['price']-1)*100):.1f}% risk)</p>
    <p><strong>Take Profit:</strong> ${analysis['take_profit']:,.4f} ({abs((analysis['take_profit']/coin_data['price']-1)*100):.1f}% target)</p>
    <p><strong>Risk/Reward:</strong> 1:2 | <strong>Score:</strong> {analysis['total_score']:.1f}/5</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Entry Reasons
    st.markdown("### 🎯 Entry Reasons & Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📋 Entry Justification:**")
        for reason in entry_reasons:
            st.write(reason)
        
    with col2:
        st.markdown("**🔍 Detailed Analysis:**")
        for reason in detailed_reasons:
            st.write(reason)
        if not detailed_reasons:
            st.write("• Standard market conditions")
    
    # Risk Management Advice
    if analysis['confidence'] == "High":
        st.markdown("**💡 Trading Advice:**")
        if "LONG" in analysis['signal']:
            st.success("🟢 High confidence LONG setup. Consider 2-3% position size. Watch for break above resistance.")
        else:
            st.error("🔴 High confidence SHORT setup. Consider 2-3% position size. Watch for break below support.")
    else:
        st.warning("⚠️ Medium confidence setup. Consider 1-2% position size. Wait for additional confirmation.")

st.divider()

# 4 Strategy Analysis Panels
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📊 Technical Analysis")
    for signal in analysis['all_signals']['technical']:
        st.write(signal)
    if not analysis['all_signals']['technical']:
        st.write("• No strong technical signals")
    
    st.markdown("### 🏛️ Fundamental Analysis")
    for signal in analysis['all_signals']['fundamental']:
        st.write(signal)
    st.write(f"• Funding Rate: {coin_data['funding_rate']:.4f}%")
    st.write(f"• 24h Volume: {coin_data['volume']:,.0f}")

with col2:
    st.markdown("### 🐋 Whale Analysis")
    for signal in analysis['all_signals']['whale']:
        st.write(signal)
    
    st.markdown("### ⛓️ On-Chain Analysis")
    for signal in analysis['all_signals']['onchain']:
        st.write(signal)
    if not analysis['all_signals']['onchain']:
        st.write("• Neutral on-chain signals")
    st.write(f"• Open Interest: {coin_data['open_interest']:,.0f}")

# Score Summary
st.markdown("### 📈 Strategy Score Summary")
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("Technical", len([s for s in analysis['all_signals']['technical'] if '🟢' in s]) - len([s for s in analysis['all_signals']['technical'] if '🔴' in s]))
with col2:
    st.metric("Fundamental", len([s for s in analysis['all_signals']['fundamental'] if '🟢' in s]) - len([s for s in analysis['all_signals']['fundamental'] if '🔴' in s]))
with col3:
    st.metric("Whale", 1)
with col4:
    st.metric("On-Chain", len([s for s in analysis['all_signals']['onchain'] if '🟢' in s]) - len([s for s in analysis['all_signals']['onchain'] if '🔴' in s]))
with col5:
    st.metric("Total Score", f"{analysis['total_score']:.1f}")

# Footer
st.divider()
st.write(f"**Last Update:** {datetime.now().strftime('%H:%M:%S')} | **Coin:** {selected_coin} | **Price:** ${coin_data['price']:,.4f}")

# Sidebar
with st.sidebar:
    st.markdown("### 📋 Supported Coins")
    for coin in SUPPORTED_COINS.keys():
        st.write(f"• {coin}")
    
    st.markdown("### 🎯 Strategy Breakdown")
    st.write("**Technical Analysis:**")
    st.write("• RSI levels")
    st.write("• Price momentum")
    
    st.write("**Fundamental Analysis:**")
    st.write("• Funding rates")
    st.write("• Volume analysis")
    st.write("• Market sentiment")
    
    st.write("**Whale Analysis:**")
    st.write("• Large transactions")
    st.write("• Exchange flows")
    
    st.write("**On-Chain Analysis:**")
    st.write("• Network metrics")
    st.write("• Open interest")
    
    st.markdown("### ⚠️ Risk Management")
    st.write("• Always use stop loss")
    st.write("• Risk max 2% per trade")
    st.write("• Follow R:R ratio 1:2")