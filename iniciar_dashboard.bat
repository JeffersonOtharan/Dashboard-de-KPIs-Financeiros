@echo off
echo ========================================
echo   DASHBOARD KPIs FINANCEIROS
echo ========================================
echo.
echo Iniciando o dashboard...
echo.
echo Aguarde alguns segundos...
echo.
python -m streamlit run dashboard_app.py --server.port 8501
pause
