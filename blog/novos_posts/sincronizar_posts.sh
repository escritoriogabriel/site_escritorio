#!/bin/bash

# Obtém o diretório onde o script está localizado
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Navega até a raiz do projeto (dois níveis acima de blog/novos_posts)
cd "$SCRIPT_DIR/../.."

echo "------------------------------------------"
echo "🚀 Iniciando Sincronização de Posts..."
echo "------------------------------------------"

# Executa o script de sincronização
python3 scripts/sync_posts.py

echo "------------------------------------------"
echo "✅ Sincronização concluída!"
echo "------------------------------------------"

# Pausa para que o usuário possa ver o resultado (útil no Windows/Linux desktop)
read -p "Pressione Enter para fechar..."
