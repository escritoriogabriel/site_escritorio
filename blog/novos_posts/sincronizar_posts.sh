#!/bin/bash

# Obtém o diretório onde o script está localizado
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Navega até a raiz do projeto (dois níveis acima de blog/novos_posts)
cd "$SCRIPT_DIR/../.."

echo "------------------------------------------"
echo " Sincronizador de Posts do Blog"
echo "------------------------------------------"
echo ""
echo " INSTRUÇÕES:"
echo " 1. Coloque seus arquivos .md NESTA pasta"
echo "    (blog/novos_posts/)"
echo " 2. O arquivo .md DEVE ter front matter YAML"
echo "    no topo (bloco entre --- e ---)"
echo " 3. O script processa e publica automaticamente"
echo "    via git push para o GitHub Pages"
echo ""
echo "------------------------------------------"
echo " Iniciando processamento..."
echo "------------------------------------------"

# Executa o script de sincronização
python3 scripts/sync_posts.py

echo ""
echo "------------------------------------------"
echo " Processo finalizado!"
echo " Verifique as mensagens acima para confirmar"
echo " se o post foi publicado com sucesso."
echo "------------------------------------------"

# Pausa para que o usuário possa ver o resultado
read -p "Pressione Enter para fechar..."
