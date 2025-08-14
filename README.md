# 📊 Trading Future Dashboard

Dashboard trading cryptocurrency yang menggabungkan sinyal on-chain, whale movement, institusi, dan news dalam satu tampilan cockpit.

## 🚀 Fitur Utama

### 4 Panel Trading:
1. **On-Chain Metrics** - Funding rate, Open Interest, Fear & Greed Index
2. **Whale Activity** - Transaksi besar dan pergerakan whale
3. **Institution Data** - ETF flows dan CME futures (simulasi)
4. **News & Sentiment** - Berita crypto dan analisis sentimen

### Signal Scoring:
- **STRONG LONG/SHORT** - Sinyal kuat berdasarkan confluence
- **LONG/SHORT** - Sinyal sedang
- **NO TRADE** - Tidak ada sinyal jelas

## 📡 Data Sources (API Gratis)

- **Binance API** - Funding rate & Open Interest
- **Alternative.me** - Fear & Greed Index
- **Simulasi** - Whale alerts & News (untuk demo)

## 🛠️ Instalasi & Penggunaan

### Cara 1: Otomatis
```bash
# Double-click file run_dashboard.bat
```

### Cara 2: Manual
```bash
# Install dependencies
pip install -r requirements.txt

# Jalankan dashboard
streamlit run dashboard.py
```

Dashboard akan terbuka di: http://localhost:8501

## ⚙️ Konfigurasi

- **Auto Refresh**: 30 detik
- **Manual Refresh**: Tombol refresh
- **Real-time Updates**: Data diperbarui otomatis

## 📈 Signal Logic

### Bullish Signals (+1 point each):
- Funding rate negatif (shorts bayar longs)
- Fear & Greed Index < 25 (extreme fear)
- Whale accumulation pattern

### Bearish Signals (-1 point each):
- Funding rate > 0.1% (longs bayar shorts)
- Fear & Greed Index > 75 (extreme greed)
- Whale distribution pattern

### Score Interpretation:
- **+2 atau lebih**: STRONG LONG
- **+1**: LONG
- **0**: NO TRADE
- **-1**: SHORT
- **-2 atau kurang**: STRONG SHORT

## 🔧 Pengembangan Lanjutan

Untuk implementasi production:
1. Tambah API key untuk data premium
2. Implementasi database untuk historical data
3. Tambah alert system (email/telegram)
4. Integrasi dengan exchange untuk auto-trading
5. Backtest engine untuk validasi strategi

## ⚠️ Disclaimer

Dashboard ini untuk edukasi dan analisis. Selalu lakukan riset sendiri sebelum trading. Cryptocurrency trading memiliki risiko tinggi.