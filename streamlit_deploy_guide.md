# 🚀 Deploy ke Streamlit Cloud

## Langkah Deploy:

### 1. Upload ke GitHub
```bash
# Buat repo baru di GitHub
# Upload semua file dari folder c:\futur
```

### 2. File yang dibutuhkan:
- ✅ `multi_coin_dashboard.py` (file utama)
- ✅ `requirements.txt` 
- ✅ `README.md`

### 3. Deploy ke Streamlit Cloud:
1. Buka: https://share.streamlit.io
2. Login dengan GitHub
3. Click "New app"
4. Pilih repository Anda
5. Main file: `multi_coin_dashboard.py`
6. Click "Deploy"

## 🔧 File Siap Deploy:

### requirements.txt (sudah ada):
```
streamlit
requests
plotly
```

### Main file: multi_coin_dashboard.py (sudah ada)

## 🌐 Setelah Deploy:
- URL otomatis: `https://[app-name].streamlit.app`
- Auto-update saat push ke GitHub
- Gratis untuk public repo

## ⚠️ Tips:
- Pastikan semua import sudah benar
- Test lokal dulu sebelum deploy
- Public repo = gratis, private repo = berbayar