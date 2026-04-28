@echo off
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%..\.."

echo ------------------------------------------
echo 🚀 Iniciando Sincronização de Posts...
echo ------------------------------------------

python scripts\sync_posts.py

echo ------------------------------------------
echo ✅ Sincronização concluida!
echo ------------------------------------------

pause
