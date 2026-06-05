#!/usr/bin/env python3
"""
PROCESSADOR DE IMAGENS - Lógica de renderização de imagens em posts
Suporta:
- Imagens locais em /public/images
- URLs externas (Unsplash, Pexels, etc)
- Otimização de imagens locais
"""

import os
import re
from pathlib import Path
from urllib.parse import urlparse

PROJECT_ROOT = Path(__file__).parent.parent.absolute()
PUBLIC_IMAGES_DIR = PROJECT_ROOT / "public" / "images"
CONTENT_BLOG_DIR = PROJECT_ROOT / "content" / "blog"

# Prefixo do site
SITE_PREFIX = "/"


def is_valid_image_url(url):
    """Verificar se a URL é válida"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False


def resolve_image_path(image_ref):
    """
    Resolver referência de imagem para URL final
    Suporta:
    - Caminhos relativos: "imagem.jpg" -> "/public/images/imagem.jpg"
    - Caminhos absolutos: "/public/images/imagem.jpg" -> "/public/images/imagem.jpg"
    - URLs externas: "https://..." -> "https://..."
    """
    
    # Se for URL externa, retornar como está
    if is_valid_image_url(image_ref):
        return image_ref
    
    # Se for caminho absoluto, retornar como está
    if image_ref.startswith('/'):
        return image_ref
    
    # Se for caminho relativo, adicionar prefixo
    if not image_ref.startswith('http'):
        # Verificar se o arquivo existe em /public/images
        img_path = PUBLIC_IMAGES_DIR / image_ref
        if img_path.exists():
            return f"{SITE_PREFIX}public/images/{image_ref}"
        
        # Caso contrário, assumir que é um caminho relativo
        return f"{SITE_PREFIX}public/images/{image_ref}"
    
    return image_ref


def process_markdown_images(markdown_content):
    """
    Processar todas as referências de imagens em um conteúdo Markdown
    Converte referências locais para URLs completas
    """
    
    # Padrão para imagens Markdown: ![alt](caminho)
    image_pattern = r'!\[([^\]]*)\]\(([^\)]+)\)'
    
    def replace_image(match):
        alt_text = match.group(1)
        image_ref = match.group(2)
        
        # Resolver caminho da imagem
        resolved_url = resolve_image_path(image_ref)
        
        return f"![{alt_text}]({resolved_url})"
    
    # Substituir todas as referências de imagens
    processed_content = re.sub(image_pattern, replace_image, markdown_content)
    
    return processed_content


def process_html_images(html_content):
    """
    Processar todas as referências de imagens em conteúdo HTML
    Adiciona atributos de otimização (lazy loading, etc)
    """
    
    # Padrão para imagens HTML: <img src="..." alt="...">
    img_pattern = r'<img\s+([^>]*?)src="([^"]+)"([^>]*)>'
    
    def replace_img(match):
        before = match.group(1)
        src = match.group(2)
        after = match.group(3)
        
        # Resolver caminho da imagem
        resolved_src = resolve_image_path(src)
        
        # Adicionar atributos de otimização se não existirem
        if 'loading=' not in before + after:
            after = f' loading="lazy"{after}'
        
        if 'alt=' not in before + after:
            after = f' alt="Imagem do post"{after}'
        
        return f'<img {before}src="{resolved_src}"{after}>'
    
    # Substituir todas as referências de imagens
    processed_content = re.sub(img_pattern, replace_img, html_content, flags=re.IGNORECASE)
    
    return processed_content


def validate_image_references(markdown_content):
    """
    Validar referências de imagens em Markdown
    Retorna lista de problemas encontrados
    """
    
    issues = []
    image_pattern = r'!\[([^\]]*)\]\(([^\)]+)\)'
    
    for match in re.finditer(image_pattern, markdown_content):
        alt_text = match.group(1)
        image_ref = match.group(2)
        
        # Verificar se é URL externa válida
        if is_valid_image_url(image_ref):
            continue
        
        # Verificar se é caminho local que existe
        if not image_ref.startswith('/'):
            img_path = PUBLIC_IMAGES_DIR / image_ref
            if not img_path.exists():
                issues.append(f"⚠️  Imagem não encontrada: {image_ref}")
        
    return issues


def optimize_image_html(html_content):
    """
    Otimizar HTML de imagens:
    - Adicionar lazy loading
    - Adicionar srcset para responsividade (opcional)
    - Adicionar atributos de acessibilidade
    """
    
    # Adicionar lazy loading
    html_content = re.sub(
        r'<img\s+([^>]*?)src=',
        r'<img \1loading="lazy" src=',
        html_content,
        flags=re.IGNORECASE
    )
    
    # Remover duplicatas de loading="lazy"
    html_content = re.sub(
        r'loading="lazy"\s+loading="lazy"',
        r'loading="lazy"',
        html_content,
        flags=re.IGNORECASE
    )
    
    return html_content


if __name__ == "__main__":
    print("🖼️  Processador de Imagens - Módulo de Utilitários")
    print("Este módulo é importado por sync_posts.py")
    print("\nFunções disponíveis:")
    print("- resolve_image_path(image_ref): Resolver referência para URL final")
    print("- process_markdown_images(content): Processar imagens em Markdown")
    print("- process_html_images(content): Processar imagens em HTML")
    print("- validate_image_references(content): Validar referências de imagens")
    print("- optimize_image_html(content): Otimizar HTML de imagens")
