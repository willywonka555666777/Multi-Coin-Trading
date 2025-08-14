@echo off
echo Starting Multi-Coin Trading Dashboard...
echo.
echo Installing requirements...
pip install streamlit requests plotly
echo.
echo Starting Multi-Coin Dashboard...
echo Dashboard will open at: http://localhost:8501
echo.
streamlit run multi_coin_dashboard.py --server.port 8501 --server.address localhost
pause