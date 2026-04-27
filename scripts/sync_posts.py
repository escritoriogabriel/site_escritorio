import os
import json
import re
from pathlib import Path
import markdown

# Configurações
PROJECT_ROOT = Path(__file__).parent.parent.absolute()
POSTS_DIR = PROJECT_ROOT / "blog" / "posts"
INDEX_FILE = POSTS_DIR / "index.json"

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

def parse_md(md_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    fm_match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)', text, re.DOTALL)
    if not fm_match:
        return None, text
    
    fm_text = fm_match.group(1)
    content_md = fm_match.group(2)
    
    metadata = {}
    for line in fm_text.split('\n'):
        if ':' in line:
            key, val = line.split(':', 1)
            metadata[key.strip()] = val.strip().strip('"').strip("'")
            
    return metadata, content_md

def sync():
    print(f"🔍 Sincronizando posts em: {POSTS_DIR}")
    
    md_files = list(POSTS_DIR.glob("*.md"))
    updated_index = []
    
    # Processar cada arquivo Markdown encontrado
    for md_file in md_files:
        print(f"📄 Processando: {md_file.name}")
        metadata, content_md = parse_md(md_file)
        
        if not metadata:
            print(f"⚠️  Aviso: Front matter não encontrado em {md_file.name}. Pulando.")
            continue
            
        real_slug = md_file.stem
        content_html = markdown.markdown(content_md, extensions=['extra'])
        
        # Formatar data para exibição
        full_date = metadata.get('date', '2026-04-27T00:00:00.000000')
        display_date = full_date.split('T')[0]
        
        # Gerar o arquivo HTML
        final_html = HTML_TEMPLATE.format(
            title=metadata.get('title', 'Sem Título'),
            author=metadata.get('author', 'Gabriel Corrêa'),
            date=display_date,
            content=content_html
        )
        
        html_file = POSTS_DIR / f"{real_slug}.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(final_html)
        
        # Adicionar ao novo índice
        post_data = {
            "title": metadata.get('title', 'Sem Título'),
            "slug": real_slug,
            "url": f"/site_escritorio/blog/posts/{real_slug}.html",
            "date": full_date,
            "author": metadata.get('author', 'Gabriel Corrêa'),
            "excerpt": metadata.get('excerpt', 'Clique para ler mais...'),
            "image": f"/site_escritorio/blog/images/{real_slug}.jpg",
            "tags": [t.strip() for t in metadata.get('tags', '').replace("[", "").replace("]", "").replace('"', '').split(",")] if metadata.get('tags') else ["Direito"],
            "categories": ["Direito"]
        }
        updated_index.append(post_data)
        print(f"✅ HTML gerado e índice preparado para: {real_slug}")

    # Ordenar por data (mais recente primeiro)
    updated_index.sort(key=lambda x: x['date'], reverse=True)

    # Salvar o índice limpo e atualizado
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        json.dump(updated_index, f, ensure_ascii=False, indent=2)
    
    print(f"\n✨ Sincronização concluída!")
    print(f"📋 Total de posts no índice: {len(updated_index)}")

if __name__ == "__main__":
    sync()
