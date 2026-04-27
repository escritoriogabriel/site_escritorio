import os
import json
import re
from pathlib import Path
import markdown
import shutil

# Configurações de diretórios
PROJECT_ROOT = Path(__file__).parent.parent.absolute()
NEW_POSTS_DIR = PROJECT_ROOT / "blog" / "novos_posts"
POSTS_DIR = PROJECT_ROOT / "blog" / "posts"
IMAGES_DIR = PROJECT_ROOT / "blog" / "images"
INDEX_FILE = POSTS_DIR / "index.json"

# Imagem padrão caso nenhuma seja encontrada
DEFAULT_POST_IMAGE = "/site_escritorio/assets/img/default-blog-post.jpg"

# Template HTML básico para o post
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | Blog Jurídico</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=Montserrat:wght@700&display=swap" rel="stylesheet">
    <style>
        :root {{ --primary-blue: #172B41; --accent-gold: #C9A961; --text-dark: #333; --bg-light: #f8f8f8; }}
        body {{ font-family: 'Inter', sans-serif; line-height: 1.6; color: var(--text-dark); background: var(--bg-light); margin: 0; padding: 0; }}
        header {{ background: #fff; padding: 20px 5%; box-shadow: 0 2px 5px rgba(0,0,0,0.1); display: flex; justify-content: space-between; align-items: center; }}
        .logo {{ font-family: 'Montserrat', sans-serif; font-weight: 700; color: var(--primary-blue); text-decoration: none; font-size: 1.2rem; }}
        .container {{ max-width: 800px; margin: 40px auto; background: #fff; padding: 40px; border-radius: 8px; box-shadow: 0 2px 15px rgba(0,0,0,0.05); }}
        .post-header {{ margin-bottom: 30px; border-bottom: 2px solid var(--accent-gold); padding-bottom: 20px; }}
        .post-header h1 {{ color: var(--primary-blue); margin: 0 0 10px 0; }}
        .post-meta {{ color: #666; font-size: 0.9rem; }}
        .post-content h2 {{ color: var(--primary-blue); margin-top: 30px; }}
        .post-content img {{ max-width: 100%; border-radius: 8px; margin: 20px 0; }}
        .btn-back {{ display: inline-block; margin-bottom: 20px; color: var(--primary-blue); text-decoration: none; font-weight: 600; }}
        footer {{ background: var(--primary-blue); color: #fff; padding: 40px 5%; text-align: center; margin-top: 60px; }}
        .cta-whatsapp {{ background: #25D366; color: #fff; padding: 15px 25px; border-radius: 8px; text-decoration: none; font-weight: 700; display: inline-block; margin-top: 30px; }}
    </style>
</head>
<body>
    <header>
        <a href="../../index.html" class="logo">Advogado Gabriel Corrêa</a>
        <a href="../../blog.html" style="text-decoration: none; color: var(--primary-blue); font-weight: 600;">Voltar ao Blog</a>
    </header>
    <div class="container">
        <a href="../../blog.html" class="btn-back"><i class="fas fa-arrow-left"></i> Voltar</a>
        <article>
            <div class="post-header">
                <h1>{title}</h1>
                <div class="post-meta">Por {author} | {date}</div>
            </div>
            <div class="post-content">
                {content}
            </div>
            <div style="text-align: center;">
                <a href="https://wa.me/5547996756766" class="cta-whatsapp"><i class="fab fa-whatsapp"></i> Falar com Dr. Gabriel pelo WhatsApp</a>
            </div>
        </article>
    </div>
    <footer>
        &copy; 2025 Advogado Gabriel Corrêa. Todos os direitos reservados.
    </footer>
</body>
</html>"""

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s-]+', '-', text).strip('-')
    return text

def parse_md_with_front_matter(md_path):
    """Extrai o front matter e o conteúdo Markdown com detecção robusta."""
    try:
        with open(md_path, 'r', encoding='utf-8') as f:
            text = f.read()
    except UnicodeDecodeError:
        with open(md_path, 'r', encoding='latin-1') as f:
            text = f.read()

    # Regex robusta: Procura por blocos entre --- mesmo que não comecem na linha 1
    # ou que tenham espaços/texto antes.
    fm_pattern = re.compile(r'---\s*\n(.*?)\n---\s*\n', re.DOTALL)
    fm_match = fm_pattern.search(text)
    
    if not fm_match:
        # Tenta uma alternativa: se não achar ---, procura por metadados soltos no topo
        # Mas para o site funcionar bem, o Front Matter é o ideal.
        return None, text
    
    fm_text = fm_match.group(1)
    # O conteúdo é tudo que vem DEPOIS do fechamento do Front Matter
    content_md = text[fm_match.end():].strip()
    
    metadata = {}
    for line in fm_text.split('\n'):
        if ':' in line:
            key, val = line.split(':', 1)
            key = key.strip().lower()
            val = val.strip().strip('"').strip("'")
            
            if key in ['tags', 'categories']:
                val = [item.strip() for item in val.replace('[', '').replace(']', '').replace('"', '').split(',') if item.strip()]
            metadata[key] = val
            
    return metadata, content_md

def sync_posts():
    print(f"🔍 Iniciando sincronização de posts...")
    
    POSTS_DIR.mkdir(parents=True, exist_ok=True)
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    NEW_POSTS_DIR.mkdir(parents=True, exist_ok=True)

    all_posts_metadata = []
    processed_slugs = set()

    # 1. Processar novos posts
    for md_file_path in NEW_POSTS_DIR.glob("*.md"):
        print(f"🆕 Analisando: {md_file_path.name}")
        metadata, content_md = parse_md_with_front_matter(md_file_path)
        
        if not metadata or not metadata.get('title'):
            print(f"⚠️  Aviso: Não encontrei o bloco de metadados (---) ou o título em {md_file_path.name}.")
            print(f"   Certifique-se de que o post gerado pela IA começa com os metadados entre ---")
            continue
        
        slug = slugify(metadata['title'])
        dest_md_path = POSTS_DIR / f"{slug}.md"
        dest_html_path = POSTS_DIR / f"{slug}.html"

        try:
            # Se já existir um arquivo com o mesmo slug, removemos para evitar erro no move
            if dest_md_path.exists():
                dest_md_path.unlink()
            shutil.move(str(md_file_path), str(dest_md_path))
            print(f"➡️ Post organizado: {dest_md_path.name}")
        except Exception as e:
            print(f"❌ Erro ao organizar arquivo: {e}")
            continue

        content_html = markdown.markdown(content_md, extensions=['extra'])
        full_date = metadata.get('date', '2026-04-27T00:00:00.000000')
        display_date = full_date.split('T')[0]

        post_image_path = IMAGES_DIR / f"{slug}.jpg"
        image_url = f"/site_escritorio/blog/images/{slug}.jpg" if post_image_path.exists() else DEFAULT_POST_IMAGE

        final_html = HTML_TEMPLATE.format(
            title=metadata['title'],
            author=metadata.get('author', 'Gabriel Corrêa'),
            date=display_date,
            content=content_html
        )
        
        with open(dest_html_path, 'w', encoding='utf-8') as f:
            f.write(final_html)
        
        post_data = {
            "title": metadata['title'],
            "slug": slug,
            "url": f"/site_escritorio/blog/posts/{slug}.html",
            "date": full_date,
            "author": metadata.get('author', 'Gabriel Corrêa'),
            "excerpt": metadata.get('excerpt', 'Clique para ler mais...'),
            "image": image_url,
            "tags": metadata.get('tags', ['Geral']),
            "categories": metadata.get('categories', ['Geral'])
        }
        all_posts_metadata.append(post_data)
        processed_slugs.add(slug)

    # 2. Re-processar existentes para manter o index.json atualizado
    for md_file_path in POSTS_DIR.glob("*.md"):
        slug = md_file_path.stem
        if slug in processed_slugs: continue

        metadata, content_md = parse_md_with_front_matter(md_file_path)
        if not metadata or not metadata.get('title'): continue

        content_html = markdown.markdown(content_md, extensions=['extra'])
        full_date = metadata.get('date', '2026-04-27T00:00:00.000000')
        display_date = full_date.split('T')[0]
        post_image_path = IMAGES_DIR / f"{slug}.jpg"
        image_url = f"/site_escritorio/blog/images/{slug}.jpg" if post_image_path.exists() else DEFAULT_POST_IMAGE

        final_html = HTML_TEMPLATE.format(
            title=metadata['title'],
            author=metadata.get('author', 'Gabriel Corrêa'),
            date=display_date,
            content=content_html
        )
        
        with open(POSTS_DIR / f"{slug}.html", 'w', encoding='utf-8') as f:
            f.write(final_html)

        post_data = {
            "title": metadata['title'],
            "slug": slug,
            "url": f"/site_escritorio/blog/posts/{slug}.html",
            "date": full_date,
            "author": metadata.get('author', 'Gabriel Corrêa'),
            "excerpt": metadata.get('excerpt', 'Clique para ler mais...'),
            "image": image_url,
            "tags": metadata.get('tags', ['Geral']),
            "categories": metadata.get('categories', ['Geral'])
        }
        all_posts_metadata.append(post_data)

    all_posts_metadata.sort(key=lambda x: x['date'], reverse=True)
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_posts_metadata, f, ensure_ascii=False, indent=2)
    
    print(f"\n✨ Sincronização concluída! Total de posts: {len(all_posts_metadata)}")

if __name__ == "__main__":
    sync_posts()
