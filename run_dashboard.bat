@echo off
echo Starting Trading Future Dashboard...
echo.
echo Installing requirements...
pip install streamlit requests plotly
echo.
echo Starting Streamlit dashboard...
echo Dashboard will open at: http://localhost:8501
echo.
streamlit run simple_dashboard.py --server.port 8501 --server.address localhost
pause