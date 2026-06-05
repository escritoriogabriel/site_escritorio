import os
import json
import re
from bs4 import BeautifulSoup

# Caminhos
POSTS_DIR = 'blog/posts'
INDEX_JSON = os.path.join(POSTS_DIR, 'index.json')
MODEL_POST = os.path.join(POSTS_DIR, 'inventario-o-passo-a-passo-completo-para-evitar-problemas-e-brigas-na-familia.html')

def get_model_structure():
    with open(MODEL_POST, 'r', encoding='utf-8') as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    
    # Extrair partes fixas do modelo
    head = soup.head
    top_bar = soup.find('div', class_='top-bar')
    header = soup.find('header')
    footer = soup.find('footer')
    scripts = soup.find_all('script')
    
    # Elementos mobile e flutuantes
    mobile_toc_btn = soup.find('button', id='mobileTocBtn')
    mobile_toc_modal = soup.find('div', id='mobileTocModal')
    floating_whatsapp = soup.find('a', class_='floating-whatsapp')
    
    return {
        'head_tags': head.decode_contents(),
        'top_bar': str(top_bar),
        'header': str(header),
        'footer': str(footer),
        'scripts': "\n".join([str(s) for s in scripts]),
        'mobile_toc_btn': str(mobile_toc_btn),
        'mobile_toc_modal': str(mobile_toc_modal),
        'floating_whatsapp': str(floating_whatsapp)
    }

def reformat_post(file_path, model_parts):
    print(f"Processando: {file_path}")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    
    # Extrair dados específicos do post atual
    title = soup.title.string if soup.title else "Blog Jurídico Gabriel Corrêa"
    hero_category = soup.find('div', class_='hero-category')
    hero_category_text = hero_category.text.strip() if hero_category else "Geral"
    hero_title = soup.find('h1', class_='hero-title')
    hero_title_text = hero_title.text.strip() if hero_title else title.split('|')[0].strip()
    
    hero_meta = soup.find('div', class_='hero-meta')
    hero_meta_html = hero_meta.decode_contents() if hero_meta else ""
    
    # Imagem do hero
    hero_img = soup.find('img', class_='hero-image')
    hero_img_src = hero_img['src'] if hero_img and 'src' in hero_img.attrs else "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80"
    
    # Conteúdo principal do artigo
    article = soup.find('article', class_='post-content')
    if not article:
        # Tentar encontrar por tag article ou div de conteúdo
        article = soup.find('article') or soup.find('div', class_='post-content')
    
    article_html = article.decode_contents() if article else ""
    
    # Tags
    tags_container = soup.find('div', class_='tags-container')
    tags_html = tags_container.decode_contents() if tags_container else ""
    
    # Construir o novo HTML
    new_html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    {model_parts['head_tags']}
    <title>{title}</title>
</head>
<body>
    {model_parts['top_bar']}
    {model_parts['header']}

    <div class="breadcrumb">
        <a href="/index.html">Início</a> <span>/</span> <a href="/blog.html">Blog</a> <span>/</span> <span>{hero_category_text}</span>
    </div>

    <div class="hero">
        <img src="{hero_img_src}" alt="{hero_title_text}" class="hero-image">
        <div class="hero-content">
            <div class="hero-category">{hero_category_text}</div>
            <h1 class="hero-title">{hero_title_text}</h1>
            <div class="hero-meta">
                {hero_meta_html}
            </div>
        </div>
    </div>

    <div class="post-wrapper">
        <div class="post-main">
            <article class="post-content">
                {article_html}
            </article>

            <!-- Posts Relacionados -->
            <div class="related-posts" id="relatedPosts">
                <h2 class="related-posts-title">Posts Relacionados</h2>
                <div class="related-posts-grid" id="relatedPostsGrid">
                    <!-- Preenchido dinamicamente via JavaScript -->
                </div>
            </div>

            <div class="cta-section">
                <div class="cta-content">
                    <h2>Precisa de ajuda com este assunto?</h2>
                    <p>Não deixe seus direitos para depois. Fale agora mesmo com um especialista e tire suas dúvidas.</p>
                    <a href="https://wa.me/5547988670233?text=Ol%C3%A1%21%20Vim%20atrav%C3%A9s%20do%20site%20e%20gostaria%20de%20resolver%20um%20problema%20que%20eu%20tenho%21%20%F0%9F%A4%9D" class="cta-whatsapp">
                        <i class="fab fa-whatsapp"></i> Conversar pelo WhatsApp
                    </a>
                </div>
            </div>
        </div>

        <aside class="sidebar">
            <div class="sidebar-box">
                <div class="sidebar-title">
                    <i class="fas fa-list"></i> Índice
                </div>
                <ul class="toc-list">
                    <!-- Preenchido dinamicamente -->
                </ul>
            </div>

            <div class="sidebar-box">
                <div class="sidebar-title">
                    <i class="fas fa-tags"></i> Tags
                </div>
                <div class="tags-container">
                    {tags_html}
                </div>
            </div>

            <div class="sidebar-box author-card">
                <div class="author-avatar">GC</div>
                <div class="author-info">
                    <div class="author-name">Advogado Gabriel Corrêa</div>
                    <div class="author-role">Advogado Especialista</div>
                </div>
            </div>
        </aside>
    </div>

    {model_parts['mobile_toc_btn']}
    {model_parts['mobile_toc_modal']}
    {model_parts['floating_whatsapp']}
    {model_parts['footer']}
    {model_parts['scripts']}
</body>
</html>"""
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_html)

def main():
    model_parts = get_model_structure()
    
    # Listar todos os posts
    posts = [f for f in os.listdir(POSTS_DIR) if f.endswith('.html') and f != os.path.basename(MODEL_POST)]
    
    for post_file in posts:
        file_path = os.path.join(POSTS_DIR, post_file)
        try:
            reformat_post(file_path, model_parts)
        except Exception as e:
            print(f"Erro ao processar {post_file}: {e}")

if __name__ == "__main__":
    main()
