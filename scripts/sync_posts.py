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

# Prefixo do site no GitHub Pages
SITE_PREFIX = "/"

# Imagem padrão caso nenhuma seja encontrada
DEFAULT_POST_IMAGE = "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80"

# Template HTML sofisticado para o post
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | Blog Jurídico Gabriel Corrêa</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Montserrat:wght@700&family=Playfair+Display:wght@700&display=swap" rel="stylesheet">
    <style>
        :root {{ 
            --primary: #172B41; 
            --accent: #C9A961; 
            --text: #2D3748; 
            --text-light: #718096;
            --bg: #F7FAFC; 
            --white: #FFFFFF;
            --whatsapp: #25D366;
        }}
        
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{ 
            font-family: 'Inter', sans-serif; 
            line-height: 1.8; 
            color: var(--text); 
            background: var(--bg); 
        }}

        header {{ 
            background: var(--white); 
            padding: 20px 5%; 
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); 
            display: flex; 
            justify-content: space-between; 
            align-items: center;
            position: sticky;
            top: 0;
            z-index: 100;
        }}

        .logo {{ 
            font-family: 'Playfair Display', serif; 
            font-weight: 700; 
            color: var(--primary); 
            text-decoration: none; 
            font-size: 1.5rem; 
        }}

        .container {{ 
            max-width: 900px; 
            margin: 60px auto; 
            background: var(--white); 
            padding: 60px; 
            border-radius: 16px; 
            box-shadow: 0 20px 25px -5px rgba(0,0,0,0.05); 
        }}

        .btn-back {{ 
            display: inline-flex; 
            align-items: center; 
            gap: 8px;
            margin-bottom: 40px; 
            color: var(--primary); 
            text-decoration: none; 
            font-weight: 600;
            font-size: 0.9rem;
            transition: transform 0.2s;
        }}
        .btn-back:hover {{ transform: translateX(-5px); color: var(--accent); }}

        .post-header {{ margin-bottom: 50px; text-align: center; }}
        .post-header h1 {{ 
            font-family: 'Montserrat', sans-serif;
            color: var(--primary); 
            font-size: 2.5rem;
            line-height: 1.2;
            margin-bottom: 20px; 
        }}
        .post-meta {{ 
            color: var(--text-light); 
            font-size: 0.95rem; 
            display: flex;
            justify-content: center;
            gap: 20px;
        }}
        .post-meta span {{ display: flex; align-items: center; gap: 6px; }}

        .post-content {{ font-size: 1.15rem; color: #333; }}
        .post-content h2 {{ 
            color: var(--primary); 
            margin: 50px 0 25px 0; 
            font-size: 1.8rem;
            border-left: 5px solid var(--accent);
            padding-left: 20px;
        }}
        .post-content h3 {{ color: var(--primary); margin: 35px 0 15px 0; font-size: 1.4rem; }}
        .post-content p {{ margin-bottom: 25px; }}
        
        /* Estilização de Tabelas */
        .post-content table {{ 
            width: 100%; 
            border-collapse: collapse; 
            margin: 40px 0; 
            font-size: 1rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            border-radius: 8px;
            overflow: hidden;
        }}
        .post-content th {{ background: var(--primary); color: white; padding: 15px; text-align: left; }}
        .post-content td {{ padding: 15px; border-bottom: 1px solid #edf2f7; background: #fff; }}
        .post-content tr:nth-child(even) td {{ background: #f8fafc; }}

        /* Citações / Destaques */
        .post-content blockquote {{ 
            background: #f0f4f8; 
            border-left: 5px solid var(--primary); 
            padding: 30px; 
            margin: 40px 0; 
            font-style: italic;
            border-radius: 0 8px 8px 0;
        }}
        
        .post-content img {{ 
            width: 100%; 
            border-radius: 12px; 
            margin: 40px 0; 
            box-shadow: 0 10px 15px rgba(0,0,0,0.1);
        }}

        .post-content ul, .post-content ol {{ margin-bottom: 25px; padding-left: 30px; }}
        .post-content li {{ margin-bottom: 12px; }}

        .cta-section {{ 
            margin-top: 80px; 
            padding: 50px; 
            background: linear-gradient(135deg, var(--primary) 0%, #2a4365 100%); 
            color: white; 
            border-radius: 16px; 
            text-align: center; 
        }}
        .cta-section h2 {{ margin-bottom: 20px; color: white; border: none; padding: 0; font-size: 2rem; }}
        .cta-whatsapp {{ 
            background: var(--whatsapp); 
            color: white; 
            padding: 18px 35px; 
            border-radius: 50px; 
            text-decoration: none; 
            font-weight: 700; 
            display: inline-flex; 
            align-items: center; 
            gap: 12px;
            font-size: 1.1rem;
            transition: transform 0.3s, box-shadow 0.3s;
            margin-top: 20px;
        }}
        .cta-whatsapp:hover {{ transform: translateY(-3px); box-shadow: 0 10px 20px rgba(37, 211, 102, 0.3); }}

        footer {{ background: var(--primary); color: #a0aec0; padding: 60px 5%; text-align: center; margin-top: 100px; }}
        
        @media (max-width: 768px) {{
            .container {{ padding: 30px; margin: 20px; }}
            .post-header h1 {{ font-size: 1.8rem; }}
            .post-content {{ font-size: 1.05rem; }}
        }}
    </style>
</head>
<body>
    <header>
        <a href="../../index.html" class="logo">Advogado Gabriel Corrêa</a>
        <a href="../../blog.html" style="text-decoration: none; color: var(--primary); font-weight: 600;">Blog</a>
    </header>
    
    <div class="container">
        <a href="../../blog.html" class="btn-back"><i class="fas fa-arrow-left"></i> Voltar para o Blog</a>
        
        <article>
            <div class="post-header">
                <h1>{title}</h1>
                <div class="post-meta">
                    <span><i class="far fa-user"></i> {author}</span>
                    <span><i class="far fa-calendar-alt"></i> {date}</span>
                    <span><i class="far fa-folder"></i> {category}</span>
                </div>
            </div>
            
            <div class="post-content">
                {content}
            </div>
            
            <div class="cta-section">
                <h2>Precisa de ajuda com este assunto?</h2>
                <p>Não deixe seus direitos para depois. Fale agora mesmo com um especialista e tire suas dúvidas.</p>
                <a href="https://wa.me/5547996756766" class="cta-whatsapp">
                    <i class="fab fa-whatsapp"></i> Conversar pelo WhatsApp
                </a>
            </div>
        </article>
    </div>

    <footer>
        <p>&copy; 2026 Advogado Gabriel Corrêa. Todos os direitos reservados.</p>
        <p style="font-size: 0.8rem; margin-top: 10px;">Atendimento em todo o Brasil.</p>
    </footer>
</body>
</html>"""

def slugify(text):
    text = text.lower()
    text = re.sub(r'[áàâãä]', 'a', text)
    text = re.sub(r'[éèêë]', 'e', text)
    text = re.sub(r'[íìîï]', 'i', text)
    text = re.sub(r'[óòôõö]', 'o', text)
    text = re.sub(r'[úùûü]', 'u', text)
    text = re.sub(r'[ç]', 'c', text)
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s-]+', '-', text).strip('-')
    return text

def parse_md_with_front_matter(md_path):
    try:
        with open(md_path, 'r', encoding='utf-8') as f:
            text = f.read()
    except UnicodeDecodeError:
        with open(md_path, 'r', encoding='latin-1') as f:
            text = f.read()

    fm_pattern = re.compile(r'---\s*\n(.*?)\n---\s*\n', re.DOTALL)
    fm_match = fm_pattern.search(text)
    
    if not fm_match:
        return None, text
    
    fm_text = fm_match.group(1)
    content_md = text[fm_match.end():].strip()
    
    metadata = {}
    for line in fm_text.split('\n'):
        if ':' in line:
            key, val = line.split(':', 1)
            key = key.strip().lower()
            val = val.strip().strip('"').strip("'")
            if key in ['tags', 'categories', 'category']:
                val = [item.strip() for item in val.replace('[', '').replace(']', '').replace('"', '').split(',') if item.strip()]
            metadata[key] = val
    
    if metadata.get('title'):
        content_md = re.sub(r'^#\s+.*?\n', '', content_md, flags=re.MULTILINE).strip()
        content_md = re.sub(r'^#+.*?\n', '', content_md, count=1).strip()

    return metadata, content_md

def find_image(slug, title):
    if not IMAGES_DIR.exists():
        return DEFAULT_POST_IMAGE
        
    image_files = list(IMAGES_DIR.glob("*"))
    clean_slug = slug.replace('-', '')
    clean_title = slugify(title).replace('-', '')
    possible_names = [slug, slugify(title), clean_slug, clean_title]
    
    for name in possible_names:
        for img_file in image_files:
            if name.lower() in img_file.stem.lower() or img_file.stem.lower() in name.lower():
                # Retorna caminho absoluto para o site no GitHub Pages
                return f"{SITE_PREFIX}blog/images/{img_file.name}"
    
    return DEFAULT_POST_IMAGE

def sync_posts():
    print(f"🔍 Iniciando sincronização sofisticada de posts...")
    
    POSTS_DIR.mkdir(parents=True, exist_ok=True)
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    NEW_POSTS_DIR.mkdir(parents=True, exist_ok=True)

    all_posts_metadata = []
    processed_slugs = set()

    for md_file_path in NEW_POSTS_DIR.glob("*.md"):
        print(f"🆕 Processando: {md_file_path.name}")
        metadata, content_md = parse_md_with_front_matter(md_file_path)
        
        if not metadata or not metadata.get('title'):
            continue
        
        slug = slugify(metadata['title'])
        dest_md_path = POSTS_DIR / f"{slug}.md"
        dest_html_path = POSTS_DIR / f"{slug}.html"

        if dest_md_path.exists(): dest_md_path.unlink()
        shutil.move(str(md_file_path), str(dest_md_path))

        content_html = markdown.markdown(content_md, extensions=['extra', 'tables', 'nl2br'])
        
        full_date = metadata.get('date', '2026-04-27T00:00:00.000000')
        display_date = full_date.split('T')[0]
        category = metadata.get('category') or metadata.get('categories')
        if isinstance(category, list): category = category[0]
        if not category: category = "Direito"

        image_url = find_image(slug, metadata['title'])

        final_html = HTML_TEMPLATE.format(
            title=metadata['title'],
            author=metadata.get('author', 'Gabriel Corrêa'),
            date=display_date,
            category=category,
            content=content_html
        )
        
        with open(dest_html_path, 'w', encoding='utf-8') as f:
            f.write(final_html)
        
        post_data = {
            "title": metadata['title'],
            "slug": slug,
            "url": f"{SITE_PREFIX}blog/posts/{slug}.html",
            "date": full_date,
            "author": metadata.get('author', 'Gabriel Corrêa'),
            "excerpt": metadata.get('excerpt') or metadata.get('description', 'Clique para ler mais...'),
            "image": image_url,
            "tags": metadata.get('tags', ['Geral']),
            "categories": [category]
        }
        all_posts_metadata.append(post_data)
        processed_slugs.add(slug)

    for md_file_path in POSTS_DIR.glob("*.md"):
        slug = md_file_path.stem
        if slug in processed_slugs: continue

        metadata, content_md = parse_md_with_front_matter(md_file_path)
        if not metadata or not metadata.get('title'): continue

        content_html = markdown.markdown(content_md, extensions=['extra', 'tables', 'nl2br'])
        full_date = metadata.get('date', '2026-04-27T00:00:00.000000')
        display_date = full_date.split('T')[0]
        category = metadata.get('category') or metadata.get('categories')
        if isinstance(category, list): category = category[0]
        if not category: category = "Direito"
        
        image_url = find_image(slug, metadata['title'])

        final_html = HTML_TEMPLATE.format(
            title=metadata['title'],
            author=metadata.get('author', 'Gabriel Corrêa'),
            date=display_date,
            category=category,
            content=content_html
        )
        
        with open(POSTS_DIR / f"{slug}.html", 'w', encoding='utf-8') as f:
            f.write(final_html)

        post_data = {
            "title": metadata['title'],
            "slug": slug,
            "url": f"{SITE_PREFIX}blog/posts/{slug}.html",
            "date": full_date,
            "author": metadata.get('author', 'Gabriel Corrêa'),
            "excerpt": metadata.get('excerpt') or metadata.get('description', 'Clique para ler mais...'),
            "image": image_url,
            "tags": metadata.get('tags', ['Geral']),
            "categories": [category]
        }
        all_posts_metadata.append(post_data)

    all_posts_metadata.sort(key=lambda x: x['date'], reverse=True)
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_posts_metadata, f, ensure_ascii=False, indent=2)
    
    print(f"✨ Sincronização concluída!")

if __name__ == "__main__":
    sync_posts()
