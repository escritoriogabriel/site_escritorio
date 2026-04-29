@echo off
chcp 65001 >nul
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%..\.."

echo ------------------------------------------
echo  Sincronizador de Posts do Blog
echo ------------------------------------------
echo.
echo  INSTRUCOES:
echo  1. Coloque seus arquivos .md NESTA pasta
echo     (blog\novos_posts\)
echo  2. O arquivo .md DEVE ter front matter YAML
echo     no topo (bloco entre --- e ---)
echo  3. O script processa e publica automaticamente
echo     via git push para o GitHub Pages
echo.
echo ------------------------------------------
echo  Iniciando processamento...
echo ------------------------------------------

python scripts\sync_posts.py

echo.
echo ------------------------------------------
echo  Processo finalizado!
echo  Verifique as mensagens acima para confirmar
echo  se o post foi publicado com sucesso.
echo ------------------------------------------
pause
