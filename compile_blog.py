#!/usr/bin/env python3
"""
compile_blog.py — Gerador de Site Estático para o Blog Jurídico
================================================================
Uso:
    python3 compile_blog.py

Fluxo:
    1. Lê todos os arquivos .md da pasta blog/posts/
    2. Parseia o Front Matter YAML de cada arquivo
    3. Converte o corpo Markdown para HTML
    4. Injeta o HTML no template post_template.html
    5. Gera posts relacionados por categoria/tag
    6. Salva o .html final em blog/posts/
    7. Atualiza blog/posts/index.json com todos os metadados

Dependências:
    pip install markdown

Formato esperado dos arquivos .md (Front Matter YAML):
    ---
    title: "Título do Post"
    excerpt: "Resumo breve para aparecer no card."
    date: "2026-06-05"
    image: "assets/img/blog/nome-da-imagem.jpg"
    categories: ["Direito Digital", "Direito Civil"]
    tags: ["Redes Sociais", "Bloqueio", "Advocacia"]
    ---
    [Conteúdo do post em Markdown...]
"""

import os
import json
import re
import markdown
import html
from datetime import datetime


# =====================================================================
# CONFIGURAÇÕES
# =====================================================================

# Pasta onde ficam os arquivos .md dos posts
POSTS_DIR = 'blog/posts/'

# Arquivo de template HTML que envolve cada post
TEMPLATE_FILE = 'post_template.html'

# Arquivo de índice JSON consumido pelo blog.html
INDEX_FILE = os.path.join(POSTS_DIR, 'index.json')

# Imagem padrão caso o post não defina nenhuma
DEFAULT_IMAGE = "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80"


# =====================================================================
# FUNÇÕES AUXILIARES
# =====================================================================

def parse_front_matter(content):
    """
    Extrai o Front Matter YAML do topo do arquivo Markdown.

    Retorna:
        metadata (dict): dicionário com os campos do cabeçalho
        body (str): corpo do post em Markdown, sem o cabeçalho

    O Front Matter deve estar delimitado por '---' no início e no fim.
    Exemplo:
        ---
        title: "Meu Post"
        date: "2026-06-05"
        ---
        Conteúdo aqui...
    """
    metadata = {}
    body = content

    # Tenta encontrar o bloco delimitado por ---
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)', content, re.DOTALL)
    if match:
        front_matter_raw = match.group(1)
        body = match.group(2)

        # Parseia cada linha do Front Matter
        for line in front_matter_raw.split('\n'):
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            # Separa chave: valor
            key_match = re.match(r'^([a-zA-Z0-9_-]+):\s*(.*)', line)
            if not key_match:
                continue

            key = key_match.group(1)
            value = key_match.group(2).strip()

            # Remove aspas externas se houver
            if (value.startswith('"') and value.endswith('"')) or \
               (value.startswith("'") and value.endswith("'")):
                value = value[1:-1]

            # Detecta listas inline: ["Item 1", "Item 2"]
            if value.startswith('[') and value.endswith(']'):
                items_str = value[1:-1]
                items = []
                for item in items_str.split(','):
                    item = item.strip()
                    if (item.startswith('"') and item.endswith('"')) or \
                       (item.startswith("'") and item.endswith("'")):
                        item = item[1:-1]
                    if item:
                        items.append(item)
                metadata[key] = items
            else:
                metadata[key] = value

    # --- Normalização e fallbacks ---

    # Suporte ao campo 'category' (singular) como alias de 'categories'
    if 'categories' not in metadata and 'category' in metadata:
        cat = metadata['category']
        metadata['categories'] = [cat] if isinstance(cat, str) else cat

    # Garante que 'categories' seja sempre uma lista
    if 'categories' not in metadata:
        metadata['categories'] = ['Geral']
    elif isinstance(metadata['categories'], str):
        metadata['categories'] = [metadata['categories']]

    # Garante que 'tags' seja sempre uma lista
    if 'tags' not in metadata:
        metadata['tags'] = []
    elif isinstance(metadata['tags'], str):
        metadata['tags'] = [metadata['tags']]

    # Data padrão: hoje
    if 'date' not in metadata or not metadata['date']:
        metadata['date'] = datetime.now().strftime('%Y-%m-%d')

    # Título padrão
    if 'title' not in metadata or not metadata['title']:
        metadata['title'] = 'Post sem título'

    # Suporte ao campo 'description' como alias de 'excerpt'
    if 'excerpt' not in metadata and 'description' in metadata:
        metadata['excerpt'] = metadata['description']
    if 'excerpt' not in metadata:
        metadata['excerpt'] = ''

    # Imagem padrão
    if 'image' not in metadata or not metadata['image']:
        metadata['image'] = DEFAULT_IMAGE

    return metadata, body


def get_related_posts_html(current_post, all_posts):
    """
    Gera o bloco HTML de 'Leia também' com até 3 posts relacionados.

    A relevância é calculada por:
        - 2 pontos para cada categoria em comum
        - 1 ponto para cada tag em comum

    Os posts são ordenados por pontuação (maior primeiro) e depois por data.
    O post atual é excluído da lista.

    Retorna:
        str: HTML da seção de posts relacionados, ou '' se não houver nenhum.
    """
    scored = []
    current_categories = set(current_post.get('categories', []))
    current_tags = set(current_post.get('tags', []))

    for post in all_posts:
        # Ignora o próprio post
        if post['slug'] == current_post['slug']:
            continue

        post_cats = set(post.get('categories', []))
        post_tags = set(post.get('tags', []))

        score = (
            len(current_categories & post_cats) * 2 +
            len(current_tags & post_tags)
        )

        if score > 0:
            scored.append((score, post.get('date', ''), post))

    # Ordena por score desc, depois data desc
    scored.sort(key=lambda x: (x[0], x[1]), reverse=True)
    top_related = [item[2] for item in scored[:3]]

    if not top_related:
        return ''

    # Monta o HTML da seção
    cards_html = ''
    for post in top_related:
        img = post.get('image', DEFAULT_IMAGE)
        if not img.startswith('http') and not img.startswith('/'):
            img = '/' + img

        title_escaped = html.escape(post.get('title', ''))
        category_escaped = html.escape((post.get('categories') or ['Geral'])[0])

        cards_html += f'''
        <a href="/blog/posts/{post['slug']}.html" class="related-card">
            <div class="related-img-wrapper">
                <img src="{img}" alt="{title_escaped}" loading="lazy">
            </div>
            <div class="related-content">
                <span class="related-category">{category_escaped}</span>
                <h4>{title_escaped}</h4>
            </div>
        </a>'''

    return f'''
    <section class="related-posts-section">
        <div class="related-posts-container">
            <h3 class="related-title">Leia também:</h3>
            <div class="related-grid">
                {cards_html}
            </div>
        </div>
    </section>'''


def format_display_date(date_str):
    """
    Converte uma data no formato ISO (YYYY-MM-DD ou YYYY-MM-DDTHH:MM:SS)
    para o formato brasileiro (DD/MM/AAAA).

    Retorna a string original se não conseguir converter.
    """
    try:
        # Remove parte de horário se houver
        date_only = date_str.split('T')[0].strip()
        date_obj = datetime.strptime(date_only, '%Y-%m-%d')
        return date_obj.strftime('%d/%m/%Y')
    except Exception:
        return date_str


def resolve_image_url(image_path):
    """
    Garante que o caminho da imagem seja uma URL absoluta ou relativa à raiz.
    URLs externas (http/https) são retornadas sem modificação.
    Caminhos relativos recebem '/' como prefixo.
    """
    if not image_path:
        return DEFAULT_IMAGE
    if image_path.startswith('http') or image_path.startswith('/'):
        return image_path
    return '/' + image_path


# =====================================================================
# FUNÇÃO PRINCIPAL
# =====================================================================

def main():
    """
    Ponto de entrada do compilador.

    Etapas:
        1. Valida que as pastas e o template existem.
        2. Primeira passagem: lê todos os .md e coleta metadados.
        3. Ordena os posts por data (mais recente primeiro).
        4. Segunda passagem: gera o HTML final de cada post.
        5. Salva o index.json atualizado.
    """
    print('\n' + '=' * 60)
    print('  COMPILE BLOG — Gerador de Site Estático')
    print('=' * 60 + '\n')

    # Valida diretório de posts
    if not os.path.isdir(POSTS_DIR):
        print(f'[ERRO] Diretório não encontrado: {POSTS_DIR}')
        print('       Certifique-se de executar este script a partir da raiz do projeto.')
        return

    # Valida template
    if not os.path.isfile(TEMPLATE_FILE):
        print(f'[ERRO] Template não encontrado: {TEMPLATE_FILE}')
        print('       O arquivo post_template.html deve estar na raiz do projeto.')
        return

    # Carrega o template HTML
    with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
        template_html = f.read()

    all_posts = []

    # ------------------------------------------------------------------
    # PRIMEIRA PASSAGEM: coleta metadados de todos os .md
    # ------------------------------------------------------------------
    md_files = [f for f in os.listdir(POSTS_DIR) if f.endswith('.md')]

    if not md_files:
        print(f'[AVISO] Nenhum arquivo .md encontrado em {POSTS_DIR}')
        print('        Adicione arquivos Markdown com Front Matter YAML para gerar posts.')
        return

    print(f'Encontrados {len(md_files)} arquivo(s) .md\n')

    for filename in md_files:
        filepath = os.path.join(POSTS_DIR, filename)
        # O slug é o nome do arquivo sem a extensão .md
        slug = filename[:-3]

        with open(filepath, 'r', encoding='utf-8') as f:
            raw_content = f.read()

        metadata, body = parse_front_matter(raw_content)

        # Ignora arquivos sem título (não são posts válidos)
        if not metadata.get('title') or metadata['title'] == 'Post sem título':
            # Ainda assim tenta usar o nome do arquivo como título
            pass

        all_posts.append({
            'slug': slug,
            'url': f'/blog/posts/{slug}.html',
            'title': metadata['title'],
            'excerpt': metadata['excerpt'],
            'date': metadata['date'],
            'image': metadata['image'],
            'categories': metadata['categories'],
            'tags': metadata['tags'],
            '_body': body,  # Prefixo _ indica campo interno, não vai para o index.json
        })

    # Ordena por data decrescente (post mais recente primeiro)
    all_posts.sort(key=lambda x: x.get('date', ''), reverse=True)

    # ------------------------------------------------------------------
    # SEGUNDA PASSAGEM: gera o HTML de cada post
    # ------------------------------------------------------------------
    processed = 0

    for post in all_posts:
        print(f'  Compilando: {post["slug"]}')

        # Converte o corpo Markdown para HTML
        # Extensões usadas:
        #   extra   → tabelas, notas de rodapé, abreviações, etc.
        #   tables  → suporte explícito a tabelas Markdown
        html_body = markdown.markdown(
            post['_body'],
            extensions=['extra', 'tables']
        )

        # Gera o bloco de posts relacionados
        related_html = get_related_posts_html(post, all_posts)

        # Gera as pills de tags
        tags_html = ' '.join([
            f'<span class="post-tag-pill">{html.escape(t)}</span>'
            for t in post.get('tags', [])
        ])

        # Resolve a URL da imagem
        display_image = resolve_image_url(post['image'])

        # Formata a data para exibição
        display_date = format_display_date(post['date'])

        # Categoria principal (primeira da lista)
        main_category = (post.get('categories') or ['Geral'])[0]

        # Substitui os placeholders no template
        # Usa replace sequencial para evitar conflitos com str.format()
        final_html = template_html
        final_html = final_html.replace('{{title}}', html.escape(post['title']))
        final_html = final_html.replace('{{title_raw}}', post['title'])
        final_html = final_html.replace('{{excerpt}}', html.escape(post['excerpt']))
        final_html = final_html.replace('{{date}}', display_date)
        final_html = final_html.replace('{{category}}', html.escape(main_category))
        final_html = final_html.replace('{{tags}}', tags_html)
        final_html = final_html.replace('{{image}}', display_image)
        final_html = final_html.replace('{{content}}', html_body)
        final_html = final_html.replace('{{related_posts}}', related_html)

        # Salva o arquivo HTML final
        out_path = os.path.join(POSTS_DIR, f'{post["slug"]}.html')
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(final_html)

        processed += 1

    # ------------------------------------------------------------------
    # GERA O INDEX.JSON
    # Contém todos os metadados dos posts (sem o corpo), ordenados por data.
    # Este arquivo é consumido pelo blog.html para renderizar os cards.
    # ------------------------------------------------------------------
    index_data = [
        {k: v for k, v in post.items() if not k.startswith('_')}
        for post in all_posts
    ]

    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        json.dump(index_data, f, ensure_ascii=False, indent=2)

    # ------------------------------------------------------------------
    # RELATÓRIO FINAL
    # ------------------------------------------------------------------
    print('\n' + '=' * 60)
    print(f'  Compilação concluída com sucesso!')
    print('=' * 60)
    print(f'  Posts processados : {processed}')
    print(f'  HTMLs gerados em  : {POSTS_DIR}')
    print(f'  Índice salvo em   : {INDEX_FILE}')
    print('=' * 60)
    print('\nPara publicar no GitHub Pages, execute:')
    print('  git add blog/posts/ post_template.html compile_blog.py blog.html')
    print('  git commit -m "feat: atualiza posts do blog"')
    print('  git push\n')


if __name__ == '__main__':
    main()
