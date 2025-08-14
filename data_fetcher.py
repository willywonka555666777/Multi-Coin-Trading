import requests
from datetime import datetime, timedelta
import time

class DataFetcher:
    def __init__(self):
        self.session = requests.Session()
        
    def get_binance_funding_rate(self):
        """Ambil funding rate dari Binance"""
        try:
            url = "https://fapi.binance.com/fapi/v1/premiumIndex"
            response = self.session.get(url, timeout=10)
            data = response.json()
            
            # Filter untuk BTC dan ETH
            btc_data = next((item for item in data if item['symbol'] == 'BTCUSDT'), None)
            eth_data = next((item for item in data if item['symbol'] == 'ETHUSDT'), None)
            
            return {
                'BTC': float(btc_data['lastFundingRate']) * 100 if btc_data else 0,
                'ETH': float(eth_data['lastFundingRate']) * 100 if eth_data else 0,
                'timestamp': datetime.now()
            }
        except:
            return {'BTC': 0, 'ETH': 0, 'timestamp': datetime.now()}
    
    def get_binance_oi(self):
        """Ambil Open Interest dari Binance"""
        try:
            url = "https://fapi.binance.com/fapi/v1/openInterest"
            symbols = ['BTCUSDT', 'ETHUSDT']
            oi_data = {}
            
            for symbol in symbols:
                response = self.session.get(url, params={'symbol': symbol}, timeout=10)
                data = response.json()
                oi_data[symbol.replace('USDT', '')] = float(data['openInterest'])
            
            return oi_data
        except:
            return {'BTC': 0, 'ETH': 0}
    
    def get_fear_greed_index(self):
        """Ambil Fear & Greed Index"""
        try:
            url = "https://api.alternative.me/fng/"
            response = self.session.get(url, timeout=10)
            data = response.json()
            
            return {
                'value': int(data['data'][0]['value']),
                'classification': data['data'][0]['value_classification'],
                'timestamp': datetime.now()
            }
        except:
            return {'value': 50, 'classification': 'Neutral', 'timestamp': datetime.now()}
    
    def get_crypto_news(self):
        """Ambil crypto news dari CoinDesk RSS (free)"""
        try:
            # Simulasi news sentiment (dalam implementasi nyata bisa pakai RSS parser)
            news_items = [
                {"title": "Bitcoin Price Analysis", "sentiment": "bullish", "time": datetime.now()},
                {"title": "Ethereum Network Update", "sentiment": "neutral", "time": datetime.now()},
                {"title": "Market Volatility Alert", "sentiment": "bearish", "time": datetime.now()}
            ]
            return news_items
        except:
            return []
    
    def get_whale_alerts(self):
        """Simulasi whale alerts (API gratis terbatas)"""
        try:
            # Simulasi data whale movement
            whale_data = [
                {"amount": 1500, "symbol": "BTC", "type": "exchange_inflow", "time": datetime.now()},
                {"amount": 25000, "symbol": "ETH", "type": "exchange_outflow", "time": datetime.now()},
                {"amount": 800, "symbol": "BTC", "type": "large_transfer", "time": datetime.now()}
            ]
            return whale_data
        except:
            return []
    
    def calculate_signal_score(self, funding_rate, fear_greed, oi_change=0):
        """Hitung skor sinyal berdasarkan data"""
        score = 0
        signals = []
        
        # Funding Rate Signal
        if funding_rate['BTC'] > 0.1:
            score -= 1
            signals.append("High funding rate (bearish)")
        elif funding_rate['BTC'] < -0.05:
            score += 1
            signals.append("Negative funding rate (bullish)")
        
        # Fear & Greed Signal
        if fear_greed['value'] < 25:
            score += 1
            signals.append("Extreme fear (contrarian bullish)")
        elif fear_greed['value'] > 75:
            score -= 1
            signals.append("Extreme greed (contrarian bearish)")
        
        # Determine overall signal
        if score >= 2:
            overall = "STRONG LONG"
        elif score == 1:
            overall = "LONG"
        elif score == -1:
            overall = "SHORT"
        elif score <= -2:
            overall = "STRONG SHORT"
        else:
            overall = "NO TRADE"
        
        return {
            'score': score,
            'signals': signals,
            'overall': overall,
            'timestamp': datetime.now()
        }