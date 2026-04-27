import os
import json
import re
from pathlib import Path
import markdown

# Configurações
PROJECT_ROOT = Path(__file__).parent.parent.absolute()
POSTS_DIR = PROJECT_ROOT / "blog" / "posts"
INDEX_FILE = POSTS_DIR / "index.json"

# Template HTML básico para o post (simplificado para manter o estilo do site)
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
    
    # Extrair Front Matter
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
    
    if not INDEX_FILE.exists():
        print("⚠️  Arquivo index.json não encontrado.")
        return

    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        posts_index = json.load(f)

    for post in posts_index:
        slug = post['slug']
        md_file = POSTS_DIR / f"{slug}.md"
        html_file = POSTS_DIR / f"{slug}.html"
        
        if md_file.exists():
            print(f"📄 Processando: {slug}")
            metadata, content_md = parse_md(md_file)
            
            # Converter MD para HTML
            content_html = markdown.markdown(content_md, extensions=['extra'])
            
            # Formatar data
            date_str = post['date'].split('T')[0]
            
            # Gerar HTML final
            final_html = HTML_TEMPLATE.format(
                title=post['title'],
                author=post.get('author', 'Gabriel Corrêa'),
                date=date_str,
                content=content_html
            )
            
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(final_html)
            print(f"✅ Gerado: {html_file.name}")
        else:
            print(f"❓ Markdown não encontrado para o slug: {slug}")

if __name__ == "__main__":
    sync()
