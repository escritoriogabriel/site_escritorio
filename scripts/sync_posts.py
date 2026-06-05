#!/usr/bin/env python3
"""
BLOG POST SYNC - Sistema 100% Estático
Processa arquivos Markdown da pasta /content/blog e gera HTML + index.json
Sem dependência de APIs externas ou tokens
"""

import os
import json
import re
import subprocess
from pathlib import Path
from datetime import datetime
import markdown
import shutil

# Importar processador de imagens
try:
    from process_images import process_markdown_images, process_html_images, optimize_image_html, validate_image_references
except ImportError:
    print("⚠️  Módulo process_images.py não encontrado. Processamento de imagens desabilitado.")
    def process_markdown_images(x): return x
    def process_html_images(x): return x
    def optimize_image_html(x): return x
    def validate_image_references(x): return []

# ===== CONFIGURAÇÕES =====
PROJECT_ROOT = Path(__file__).parent.parent.absolute()
CONTENT_BLOG_DIR = PROJECT_ROOT / "content" / "blog"  # Pasta onde o usuário coloca .md
POSTS_DIR = PROJECT_ROOT / "blog" / "posts"           # Pasta de saída (HTML + MD)
IMAGES_DIR = PROJECT_ROOT / "public" / "images"       # Pasta de imagens locais
INDEX_FILE = POSTS_DIR / "index.json"

# Prefixo do site no GitHub Pages
SITE_PREFIX = "/"

# Imagem padrão caso nenhuma seja encontrada
DEFAULT_POST_IMAGE = "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80"

# Template HTML sofisticado para o post (mantém o design original)
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | Blog Jurídico Gabriel Corrêa</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Montserrat:wght@600;700;800&family=Playfair+Display:wght@700&display=swap" rel="stylesheet">
    <style>
        :root {{ 
            --primary: #172B41; 
            --primary-light: #1f3a52;
            --primary-dark: #0f1f2e;
            --accent: #C9A961; 
            --accent-light: #e0c9a0;
            --text: #2D3748; 
            --text-light: #718096;
            --text-lighter: #a0aec0;
            --bg: #F7FAFC;
            --bg-light: #FFFFFF;
            --border: #e2e8f0;
            --whatsapp: #25D366;
            --success: #48bb78;
            --warning: #ed8936;
        }}
        
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        html {{ scroll-behavior: smooth; }}
        
        body {{ 
            font-family: 'Inter', sans-serif; 
            line-height: 1.8; 
            color: var(--text); 
            background: var(--bg);
        }}

        /* ===== TOP BAR ===== */
        .top-bar {{
            background-color: var(--primary-dark);
            color: white;
            padding: 10px 5%;
            font-size: 0.8rem;
            text-align: right;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }}
        .top-bar a {{ color: var(--accent-light); text-decoration: none; transition: color 0.3s; }}
        .top-bar a:hover {{ color: var(--accent); }}
        .top-bar i {{ margin-right: 5px; }}

        /* ===== HEADER & NAVIGATION ===== */
        header {{ 
            background: var(--bg-light); 
            padding: 0 5%;
            box-shadow: 0 2px 15px rgba(0,0,0,0.08); 
            display: flex; 
            justify-content: space-between; 
            align-items: center;
            position: sticky;
            top: 0;
            z-index: 1000;
            height: 80px;
        }}

        .logo {{
            display: flex;
            align-items: center;
            text-decoration: none;
            transition: transform 0.3s;
        }}
        .logo:hover {{ transform: scale(1.02); }}
        .logo img {{
            height: 36px;
            width: auto;
            max-width: 280px;
        }}

        nav {{
            display: flex;
            align-items: center;
            gap: 32px;
        }}

        .nav-links {{
            display: flex;
            list-style: none;
            gap: 28px;
            align-items: center;
        }}

        .nav-links a {{
            text-decoration: none;
            color: var(--primary);
            font-weight: 600;
            font-size: 0.95rem;
            transition: all 0.3s;
            position: relative;
        }}
        .nav-links a::after {{
            content: '';
            position: absolute;
            bottom: -5px;
            left: 0;
            width: 0;
            height: 2px;
            background: var(--accent);
            transition: width 0.3s;
        }}
        .nav-links a:hover::after {{ width: 100%; }}
        .nav-links a:hover {{ color: var(--accent); }}

        /* Dropdown */
        .dropdown {{ position: relative; }}
        .dropdown-content {{
            display: none;
            position: absolute;
            background-color: var(--bg-light);
            min-width: 280px;
            box-shadow: 0 12px 32px rgba(0,0,0,0.15);
            z-index: 100;
            top: 100%;
            left: 0;
            border-top: 4px solid var(--accent);
            border-radius: 8px;
            margin-top: 8px;
            overflow: hidden;
        }}
        .dropdown:hover .dropdown-content {{ display: block; }}
        .dropdown-content a {{
            color: var(--text);
            padding: 14px 18px;
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 0.9rem;
            border-bottom: 1px solid var(--border);
            transition: all 0.2s;
            position: relative;
        }}
        .dropdown-content a::before {{
            content: '';
            position: absolute;
            left: 0;
            width: 3px;
            height: 100%;
            background: var(--accent);
            transform: scaleY(0);
            transition: transform 0.2s;
        }}
        .dropdown-content a:hover::before {{ transform: scaleY(1); }}
        .dropdown-content a:last-child {{ border-bottom: none; }}
        .dropdown-content a:hover {{ background-color: var(--bg); color: var(--accent); }}

        .btn-nav-whatsapp {{
            background: linear-gradient(135deg, var(--whatsapp) 0%, #1da851 100%);
            color: white !important;
            padding: 12px 24px;
            border-radius: 50px;
            transition: all 0.3s ease;
            white-space: nowrap;
            font-size: 0.9rem;
            font-weight: 700;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            box-shadow: 0 4px 15px rgba(37, 211, 102, 0.3);
            border: none;
            cursor: pointer;
        }}
        .btn-nav-whatsapp:hover {{
            transform: translateY(-3px);
            box-shadow: 0 6px 25px rgba(37, 211, 102, 0.4);
        }}

        /* ===== BREADCRUMB ===== */
        .breadcrumb {{
            background: var(--bg-light);
            padding: 16px 5%;
            border-bottom: 1px solid var(--border);
            font-size: 0.9rem;
        }}
        .breadcrumb a {{
            color: var(--accent);
            text-decoration: none;
            transition: color 0.3s;
        }}
        .breadcrumb a:hover {{ color: var(--primary); }}
        .breadcrumb span {{ color: var(--text-light); margin: 0 8px; }}

        /* ===== HERO SECTION ===== */
        .hero {{
            position: relative;
            width: 100%;
            height: 420px;
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
            overflow: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .hero::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-image: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 600"><defs><pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M 40 0 L 0 0 0 40" fill="none" stroke="rgba(255,255,255,0.03)" stroke-width="1"/></pattern></defs><rect width="1200" height="600" fill="url(%23grid)"/></svg>');
            opacity: 0.5;
        }}
        .hero-image {{
            position: absolute;
            width: 100%;
            height: 100%;
            object-fit: cover;
            opacity: 0.3;
            z-index: 0;
        }}
        .hero-content {{
            position: relative;
            z-index: 10;
            text-align: center;
            color: white;
            padding: 40px 5%;
            max-width: 900px;
        }}
        .hero-category {{
            display: inline-block;
            background: var(--accent);
            color: var(--primary);
            padding: 8px 16px;
            border-radius: 50px;
            font-size: 0.85rem;
            font-weight: 700;
            margin-bottom: 20px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .hero-title {{
            font-family: 'Montserrat', sans-serif;
            font-size: 3rem;
            font-weight: 800;
            line-height: 1.2;
            margin-bottom: 20px;
            text-shadow: 0 2px 10px rgba(0,0,0,0.2);
        }}
        .hero-meta {{
            display: flex;
            justify-content: center;
            gap: 30px;
            flex-wrap: wrap;
            font-size: 0.95rem;
            opacity: 0.95;
        }}
        .hero-meta-item {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        /* ===== MAIN CONTENT ===== */
        .post-wrapper {{
            display: grid;
            grid-template-columns: 1fr 280px;
            gap: 40px;
            max-width: 100%;
            width: 90%;
            margin: 60px auto;
            padding: 0 5%;
        }}

        .post-main {{
            background: var(--bg-light);
            padding: 50px;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        }}

        /* ===== POST CONTENT ===== */
        .post-content {{
            font-size: 1.1rem;
            color: var(--text);
            line-height: 1.9;
        }}

        .post-content h2 {{ 
            font-family: 'Montserrat', sans-serif;
            color: var(--primary); 
            margin: 50px 0 25px 0; 
            font-size: 1.9rem;
            font-weight: 700;
            border-left: 5px solid var(--accent);
            padding-left: 20px;
            transition: all 0.3s;
        }}

        .post-content h3 {{ 
            font-family: 'Montserrat', sans-serif;
            color: var(--primary); 
            margin: 40px 0 18px 0; 
            font-size: 1.4rem;
            font-weight: 700;
        }}

        .post-content h4 {{
            color: var(--primary-light);
            margin: 30px 0 12px 0;
            font-size: 1.15rem;
            font-weight: 600;
        }}

        .post-content p {{ 
            margin-bottom: 22px;
            text-align: justify;
        }}

        /* Listas */
        .post-content ul, .post-content ol {{ 
            margin: 25px 0 25px 30px; 
            padding-left: 20px;
        }}
        .post-content li {{ 
            margin-bottom: 12px;
            line-height: 1.8;
        }}
        .post-content ul li::marker {{
            color: var(--accent);
            font-weight: bold;
        }}

        /* Tabelas */
        .post-content table {{ 
            width: 100%; 
            border-collapse: collapse; 
            margin: 40px 0; 
            font-size: 0.95rem;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            border-radius: 8px;
            overflow: hidden;
        }}
        .post-content th {{ 
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
            color: white; 
            padding: 16px; 
            text-align: left;
            font-weight: 700;
        }}
        .post-content td {{ 
            padding: 14px 16px; 
            border-bottom: 1px solid var(--border); 
            background: var(--bg-light);
        }}
        .post-content tr:hover td {{ background: var(--bg); }}
        .post-content tr:nth-child(even) td {{ background: var(--bg); }}

        /* Blockquotes */
        .post-content blockquote {{ 
            background: linear-gradient(135deg, rgba(201, 169, 97, 0.1) 0%, rgba(201, 169, 97, 0.05) 100%);
            border-left: 5px solid var(--accent); 
            padding: 25px 30px; 
            margin: 40px 0; 
            font-style: italic;
            border-radius: 0 8px 8px 0;
            color: var(--text);
        }}

        /* Imagens */
        .post-content img {{ 
            width: 100%; 
            border-radius: 12px; 
            margin: 40px 0; 
            box-shadow: 0 12px 30px rgba(0,0,0,0.12);
            transition: transform 0.3s;
        }}
        .post-content img:hover {{
            transform: scale(1.02);
        }}

        /* Código */
        .post-content code {{
            background: var(--bg);
            color: var(--primary);
            padding: 2px 6px;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
        }}
        .post-content pre {{
            background: var(--primary-dark);
            color: #e0e0e0;
            padding: 20px;
            border-radius: 8px;
            overflow-x: auto;
            margin: 25px 0;
            font-size: 0.9rem;
        }}
        .post-content pre code {{
            background: none;
            color: #e0e0e0;
            padding: 0;
        }}

        /* ===== SIDEBAR ===== */
        .sidebar {{
            display: flex;
            flex-direction: column;
            gap: 30px;
        }}

        .sidebar-box {{
            background: var(--bg-light);
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.05);
            border-top: 4px solid var(--accent);
        }}

        .sidebar-title {{
            font-family: 'Montserrat', sans-serif;
            font-size: 1.2rem;
            font-weight: 700;
            color: var(--primary);
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .sidebar-title i {{
            color: var(--accent);
        }}

        .tag {{
            display: inline-block;
            background: var(--bg);
            color: var(--primary);
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 0.85rem;
            margin: 5px 5px 5px 0;
            text-decoration: none;
            transition: all 0.3s;
            border: 1px solid var(--border);
        }}
        .tag:hover {{
            background: var(--accent);
            color: white;
            border-color: var(--accent);
        }}

        /* ===== FOOTER ===== */
        footer {{
            background: var(--primary);
            color: white;
            padding: 40px 5%;
            text-align: center;
            margin-top: 80px;
            border-top: 4px solid var(--accent);
        }}

        footer p {{
            margin-bottom: 10px;
        }}

        footer a {{
            color: var(--accent-light);
            text-decoration: none;
            transition: color 0.3s;
        }}

        footer a:hover {{
            color: var(--accent);
        }}

        /* ===== RESPONSIVE ===== */
        @media (max-width: 768px) {{
            .post-wrapper {{
                grid-template-columns: 1fr;
                width: 95%;
                margin: 40px auto;
            }}
            
            .hero-title {{
                font-size: 2rem;
            }}
            
            .post-main {{
                padding: 25px;
            }}
            
            .post-content h2 {{
                font-size: 1.5rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="top-bar">
        <a href="https://wa.me/5547988670233?text=Olá%21%20Vim%20através%20do%20site%20e%20gostaria%20de%20resolver%20um%20problema%20que%20eu%20tenho%21%20%F0%9F%A4%9D" target="_blank">
            <i class="fas fa-phone"></i> Fale com a gente: (47) 98867-0233
        </a>
    </div>

    <header>
        <a href="/" class="logo">
            <img src="/assets/logo.png" alt="Gabriel Corrêa - Advocacia">
        </a>
        <nav>
            <ul class="nav-links">
                <li><a href="/">Home</a></li>
                <li><a href="/blog.html">Blog</a></li>
                <li class="dropdown">
                    <a href="#">Áreas de Atuação</a>
                    <div class="dropdown-content">
                        <a href="/#direito-civil"><i class="fas fa-gavel"></i> Direito Civil</a>
                        <a href="/#direito-trabalhista"><i class="fas fa-briefcase"></i> Direito Trabalhista</a>
                        <a href="/#direito-penal"><i class="fas fa-shield-alt"></i> Direito Penal</a>
                    </div>
                </li>
                <li><a href="/#sobre">Sobre</a></li>
                <li><a href="/#contato">Contato</a></li>
            </ul>
            <a href="https://wa.me/5547988670233?text=Olá%21%20Vim%20através%20do%20site%20e%20gostaria%20de%20resolver%20um%20problema%20que%20eu%20tenho%21%20%F0%9F%A4%9D" class="btn-nav-whatsapp" target="_blank">
                <i class="fab fa-whatsapp"></i> WhatsApp
            </a>
        </nav>
    </header>

    <div class="breadcrumb">
        <a href="/">Home</a>
        <span>/</span>
        <a href="/blog.html">Blog</a>
        <span>/</span>
        <span>{title}</span>
    </div>

    <section class="hero">
        <img src="{image}" alt="{title}" class="hero-image">
        <div class="hero-content">
            <div class="hero-category">{category}</div>
            <h1 class="hero-title">{title}</h1>
            <div class="hero-meta">
                <div class="hero-meta-item">
                    <i class="fas fa-calendar"></i>
                    <span>{date}</span>
                </div>
                <div class="hero-meta-item">
                    <i class="fas fa-user"></i>
                    <span>{author}</span>
                </div>
            </div>
        </div>
    </section>

    <div class="post-wrapper">
        <main class="post-main">
            <article class="post-content">
                {content}
            </article>
        </main>

        <aside class="sidebar">
            <div class="sidebar-box">
                <div class="sidebar-title">
                    <i class="fas fa-tags"></i> Tags
                </div>
                {tags_html}
            </div>

            <div class="sidebar-box">
                <div class="sidebar-title">
                    <i class="fas fa-headset"></i> Precisa de Ajuda?
                </div>
                <p style="font-size: 0.95rem; margin-bottom: 15px;">
                    Fale com o advogado Gabriel Corrêa e resolva seu problema jurídico agora mesmo!
                </p>
                <a href="https://wa.me/5547988670233?text=Olá%21%20Vim%20através%20do%20blog%20e%20gostaria%20de%20resolver%20um%20problema%20que%20eu%20tenho%21%20%F0%9F%A4%9D" class="btn-nav-whatsapp" target="_blank" style="width: 100%; justify-content: center;">
                    <i class="fab fa-whatsapp"></i> Enviar Mensagem
                </a>
            </div>
        </aside>
    </div>

    <footer>
        <p>&copy; 2024 Gabriel Corrêa - Advocacia. Todos os direitos reservados.</p>
        <p><a href="/">Home</a> | <a href="/blog.html">Blog</a> | <a href="/#contato">Contato</a></p>
    </footer>
</body>
</html>
"""


def slugify(text):
    """Converter texto para slug válido"""
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')


def parse_md_with_front_matter(file_path):
    """
    Parsear arquivo Markdown com front matter YAML
    Retorna (metadata_dict, content_string)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verificar se existe front matter
        if not content.startswith('---'):
            print(f"⚠️  Arquivo sem front matter: {file_path}")
            return None, content
        
        # Extrair front matter
        parts = content.split('---', 2)
        if len(parts) < 3:
            print(f"⚠️  Front matter inválido: {file_path}")
            return None, content
        
        front_matter_str = parts[1].strip()
        content_md = parts[2].strip()
        
        # Parse YAML manual (simples)
        metadata = {}
        for line in front_matter_str.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip().strip('"\'')
                
                # Converter tipos
                if value.lower() == 'true':
                    value = True
                elif value.lower() == 'false':
                    value = False
                elif value.startswith('[') and value.endswith(']'):
                    # Parse array simples
                    value = [v.strip().strip('"\'') for v in value[1:-1].split(',')]
                
                metadata[key] = value
        
        return metadata, content_md
    
    except Exception as e:
        print(f"❌ Erro ao parsear {file_path}: {e}")
        return None, ""


def find_image(slug, title, metadata_image=None):
    """
    Encontrar imagem para o post
    Prioridade:
    1. Imagem definida no front matter
    2. Arquivo local com nome do slug
    3. Arquivo local com nome similar ao título
    4. Imagem padrão (Unsplash)
    """
    # Se já existe uma imagem definida no metadata
    if metadata_image:
        # Se for um caminho relativo sem o prefixo, adiciona
        if not metadata_image.startswith('http') and not metadata_image.startswith('/'):
            metadata_image = f"{SITE_PREFIX}{metadata_image}"
        
        # Verifica se o arquivo existe localmente (se for um caminho local)
        if metadata_image.startswith(f"{SITE_PREFIX}public/images/"):
            img_name = metadata_image.split('/')[-1]
            if (IMAGES_DIR / img_name).exists():
                return metadata_image
        
        # Se for URL externa, retorna como está
        if metadata_image.startswith('http'):
            return metadata_image

    # Procurar em /public/images
    if not IMAGES_DIR.exists():
        return DEFAULT_POST_IMAGE
        
    image_files = list(IMAGES_DIR.glob("*"))
    
    # Tenta encontrar por nome de arquivo exato primeiro
    for img_file in image_files:
        if img_file.stem.lower() == slug.lower() or img_file.stem.lower() == slugify(title).lower():
            return f"{SITE_PREFIX}public/images/{img_file.name}"

    # Tenta encontrar por similaridade
    possible_names = [slug, slugify(title)]
    for name in possible_names:
        for img_file in image_files:
            if name.lower() in img_file.stem.lower() or img_file.stem.lower() in name.lower():
                return f"{SITE_PREFIX}public/images/{img_file.name}"
    
    return DEFAULT_POST_IMAGE


def sync_posts():
    """Sincronizar posts Markdown para HTML + JSON"""
    
    print("\n" + "=" * 70)
    print("🚀 SINCRONIZADOR DE POSTS - SISTEMA 100% ESTÁTICO")
    print("=" * 70 + "\n")
    
    # Criar diretórios se não existirem
    POSTS_DIR.mkdir(parents=True, exist_ok=True)
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    CONTENT_BLOG_DIR.mkdir(parents=True, exist_ok=True)
    
    print(f"📁 Pasta de conteúdo: {CONTENT_BLOG_DIR}")
    print(f"📁 Pasta de saída: {POSTS_DIR}")
    print(f"📁 Pasta de imagens: {IMAGES_DIR}\n")
    
    all_posts_metadata = []
    processed_count = 0
    
    # Processar todos os arquivos .md na pasta /content/blog
    md_files = list(CONTENT_BLOG_DIR.glob("*.md"))
    
    if not md_files:
        print(f"⚠️  Nenhum arquivo .md encontrado em {CONTENT_BLOG_DIR}")
        print("   Crie arquivos Markdown com front matter YAML nessa pasta.")
        return
    
    print(f"📄 Encontrados {len(md_files)} arquivo(s) Markdown\n")
    
    for md_file_path in md_files:
        print(f"🔄 Processando: {md_file_path.name}")
        
        # Parsear front matter e conteúdo
        metadata, content_md = parse_md_with_front_matter(md_file_path)
        
        if not metadata or not metadata.get('title'):
            print(f"   ⚠️  Arquivo ignorado (sem título no front matter)\n")
            continue
        
        # Validar referências de imagens
        image_issues = validate_image_references(content_md)
        if image_issues:
            for issue in image_issues:
                print(f"   {issue}")
        
        # Processar referências de imagens em Markdown
        content_md = process_markdown_images(content_md)
        
        # Gerar slug
        slug = slugify(metadata['title'])
        
        # Converter Markdown para HTML
        content_html = markdown.markdown(
            content_md,
            extensions=['extra', 'tables', 'nl2br', 'codehilite']
        )
        
        # Processar referências de imagens em HTML
        content_html = process_html_images(content_html)
        
        # Otimizar HTML de imagens (lazy loading, etc)
        content_html = optimize_image_html(content_html)
        
        # Extrair metadados
        full_date = metadata.get('date', datetime.now().isoformat())
        display_date = full_date.split('T')[0] if 'T' in full_date else full_date
        category = metadata.get('category', metadata.get('categories', 'Direito'))
        if isinstance(category, list):
            category = category[0]
        
        # Encontrar imagem
        image_url = find_image(slug, metadata['title'], metadata.get('image'))
        
        # Extrair tags
        tags = metadata.get('tags', ['Geral'])
        if isinstance(tags, str):
            tags = [tags]
        tags_html = "".join([f'<a href="/blog.html?tag={t}" class="tag">{t}</a>' for t in tags])
        
        # Gerar HTML final
        final_html = HTML_TEMPLATE.format(
            title=metadata['title'],
            author=metadata.get('author', 'Gabriel Corrêa'),
            date=display_date,
            category=category,
            content=content_html,
            image=image_url,
            tags_html=tags_html
        )
        
        # Salvar arquivo HTML
        html_path = POSTS_DIR / f"{slug}.html"
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(final_html)
        
        # Copiar arquivo MD original para a pasta de posts
        md_dest_path = POSTS_DIR / f"{slug}.md"
        shutil.copy(md_file_path, md_dest_path)
        
        # Adicionar metadados ao índice
        post_data = {
            "title": metadata['title'],
            "slug": slug,
            "url": f"{SITE_PREFIX}blog/posts/{slug}.html",
            "date": full_date,
            "author": metadata.get('author', 'Gabriel Corrêa'),
            "excerpt": metadata.get('excerpt', metadata.get('description', 'Clique para ler mais...')),
            "image": image_url,
            "tags": tags,
            "categories": [category] if isinstance(category, str) else category
        }
        all_posts_metadata.append(post_data)
        
        print(f"   ✅ HTML gerado: {html_path.name}")
        print(f"   📋 Slug: {slug}")
        print(f"   🖼️  Imagem: {image_url}\n")
        
        processed_count += 1
    
    # Ordenar por data (mais recentes primeiro)
    all_posts_metadata.sort(key=lambda x: x['date'], reverse=True)
    
    # Salvar índice JSON
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_posts_metadata, f, ensure_ascii=False, indent=2)
    
    print("=" * 70)
    print(f"✅ SINCRONIZAÇÃO CONCLUÍDA!")
    print("=" * 70)
    print(f"Posts processados: {processed_count}")
    print(f"Índice salvo em: {INDEX_FILE}")
    print(f"Posts HTML em: {POSTS_DIR}")
    print("=" * 70 + "\n")
    
    # Sugerir commit
    if processed_count > 0:
        print("📝 Para publicar no GitHub, execute:")
        print("   git add blog/ content/")
        print("   git commit -m 'Novos posts de blog'")
        print("   git push\n")


if __name__ == "__main__":
    sync_posts()
