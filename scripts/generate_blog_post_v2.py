#!/usr/bin/env python3
"""
BLOG POST GENERATOR - Gera posts de blog automaticamente com Google Gemini (GRATUITO)
Compatível com GitHub Pages (site estático)
Usa a nova biblioteca oficial: google-genai
"""

import os
import sys
import json
import datetime
import re
import random
from pathlib import Path

try:
    from google import genai
except ImportError:
    print("❌ Erro: google-genai não está instalado. Execute: pip install google-genai")
    sys.exit(1)

# Configurações - Usar caminhos relativos para compatibilidade com GitHub Actions
SCRIPT_DIR = Path(__file__).parent.absolute()
PROJECT_ROOT = SCRIPT_DIR.parent.absolute()
BLOG_DIR = PROJECT_ROOT / "blog"
POSTS_DIR = BLOG_DIR / "posts"
IMAGES_DIR = BLOG_DIR / "images"
CONFIG_FILE = SCRIPT_DIR / "blog_config.json"

print(f"📁 Script Dir: {SCRIPT_DIR}")
print(f"📁 Project Root: {PROJECT_ROOT}")
print(f"📁 Blog Dir: {BLOG_DIR}")
print(f"📁 Posts Dir: {POSTS_DIR}")

# Criar diretórios se não existirem
try:
    POSTS_DIR.mkdir(parents=True, exist_ok=True)
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    print(f"✅ Diretórios criados/verificados")
except Exception as e:
    print(f"❌ Erro ao criar diretórios: {e}")
    sys.exit(1)

# Inicializar cliente Google Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("❌ Erro: GEMINI_API_KEY não está configurada!")
    sys.exit(1)

print(f"✅ Google Gemini API Key carregada")

try:
    client = genai.Client(api_key=GEMINI_API_KEY)
except Exception as e:
    print(f"❌ Erro ao inicializar Google Gemini: {e}")
    sys.exit(1)

def load_config():
    """Carregar configurações do arquivo JSON"""
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            config = json.load(f)
            print(f"✅ Configurações carregadas de: {CONFIG_FILE}")
            return config
    except FileNotFoundError:
        print(f"❌ Arquivo de configuração não encontrado: {CONFIG_FILE}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erro ao carregar configurações: {e}")
        sys.exit(1)

def select_topic(config):
    """Selecionar um tópico aleatório da lista"""
    if not config.get('blog_topics'):
        print("❌ Nenhum tópico encontrado na configuração")
        sys.exit(1)
    return random.choice(config['blog_topics'])

def generate_post_content(topic, config):
    """Gerar conteúdo completo do post usando Google Gemini"""
    
    prompt = f"""Você é um advogado especialista em direito brasileiro e um excelente redator de conteúdo para blog. Seu objetivo é criar um artigo de blog informativo, envolvente e focado em conversão para o escritório de advocacia Gabriel Corrêa.

INSTRUÇÕES CRÍTICAS:
1. O artigo DEVE ser em Markdown puro (sem HTML)
2. Use ## para subtítulos (não use #)
3. Inclua pelo menos 3 subtítulos principais
4. Adicione uma seção FAQ com 3-5 perguntas e respostas
5. Inclua 1-2 links internos no formato [Texto](/site_escritorio/pagina.html)
6. Inclua 1-2 links externos para fontes confiáveis
7. Termine com um CTA claro para o WhatsApp
8. Use negrito (**texto**) para destacar pontos importantes
9. Use listas com - para melhor legibilidade

DETALHES DO ARTIGO:
- Tópico: {topic['title']}
- Palavras-chave: {', '.join(topic['keywords'])}
- Público-alvo: {topic['target_audience']}
- Categoria: {topic['category']}
- Foco: Informar, educar e converter para contato via WhatsApp

ESTRUTURA OBRIGATÓRIA:
1. Introdução (2-3 parágrafos explicando o problema)
2. Seção 1: [Subtítulo relevante] (3-4 parágrafos)
3. Seção 2: [Subtítulo relevante] (3-4 parágrafos)
4. Seção 3: [Subtítulo relevante] (3-4 parágrafos)
5. FAQ - Perguntas Frequentes (3-5 Q&A)
6. Conclusão (2-3 parágrafos com CTA)

EXEMPLO DE CTA:
**Precisa de ajuda profissional?** Fale agora com o Advogado Gabriel Corrêa pelo WhatsApp: [📞 (47) 99675-6766](https://wa.me/5547996756766)

Gere o artigo completo em Markdown, pronto para publicação.
"""

    try:
        print(f"🤖 Gerando conteúdo para: {topic['title']}...")
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        content = response.text
        print(f"✅ Conteúdo gerado com sucesso ({len(content)} caracteres)")
        return content
    except Exception as e:
        print(f"❌ Erro ao gerar conteúdo: {e}")
        return None

def extract_metadata(content, topic):
    """Extrair metadados do conteúdo gerado"""
    
    try:
        # Extrair primeiro parágrafo como excerpt
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip() and not p.startswith('#')]
        excerpt = (paragraphs[0][:200] + "...") if paragraphs else "Artigo jurídico informativo"
        
        # Gerar slug do título
        slug = re.sub(r'[^a-z0-9]+', '-', topic['title'].lower()).strip('-')
        
        return {
            'title': topic['title'],
            'excerpt': excerpt,
            'slug': slug,
            'keywords': topic['keywords'],
            'category': topic['category']
        }
    except Exception as e:
        print(f"❌ Erro ao extrair metadados: {e}")
        return None

def create_blog_post(content, metadata, config):
    """Criar arquivo Markdown do post"""
    
    try:
        # Preparar front matter (metadados YAML)
        front_matter = f"""---
title: "{metadata['title']}"
date: {datetime.datetime.now().isoformat()}
author: "Advogado Gabriel Corrêa"
categories: ["{metadata['category']}"]
tags: {json.dumps(metadata['keywords'])}
image: "/site_escritorio/blog/images/{metadata['slug']}.jpg"
excerpt: "{metadata['excerpt']}"
---

"""
        
        # Caminho do arquivo
        filename = POSTS_DIR / f"{metadata['slug']}.md"
        
        # Salvar arquivo
        full_content = front_matter + content
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(full_content)
        
        print(f"✅ Post criado: {filename}")
        
        return {
            'title': metadata['title'],
            'slug': metadata['slug'],
            'url': f"/site_escritorio/blog/posts/{metadata['slug']}.html",
            'date': datetime.datetime.now().isoformat(),
            'author': "Advogado Gabriel Corrêa",
            'excerpt': metadata['excerpt'],
            'image': f"/site_escritorio/blog/images/{metadata['slug']}.jpg",
            'tags': metadata['keywords'],
            'categories': [metadata['category']]
        }
    except Exception as e:
        print(f"❌ Erro ao criar post: {e}")
        return None

def update_posts_index(post_metadata):
    """Atualizar índice JSON de posts"""
    
    try:
        index_file = POSTS_DIR / "index.json"
        
        # Carregar índice existente
        if index_file.exists():
            with open(index_file, 'r', encoding='utf-8') as f:
                posts = json.load(f)
        else:
            posts = []
        
        # Adicionar novo post (evitar duplicatas)
        posts = [p for p in posts if p['slug'] != post_metadata['slug']]
        posts.append(post_metadata)
        
        # Ordenar por data (mais recentes primeiro)
        posts.sort(key=lambda x: x['date'], reverse=True)
        
        # Salvar índice
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump(posts, f, ensure_ascii=False, indent=2)
        
        print(f"📋 Índice atualizado: {index_file}")
    except Exception as e:
        print(f"❌ Erro ao atualizar índice: {e}")

def create_placeholder_image(slug):
    """Criar imagem placeholder para o post"""
    
    try:
        image_path = IMAGES_DIR / f"{slug}.jpg"
        
        # Se a imagem já existe, não sobrescrever
        if image_path.exists():
            print(f"ℹ️  Imagem já existe: {image_path}")
            return
        
        # Criar um arquivo placeholder
        with open(image_path, 'w') as f:
            f.write(f"Placeholder image for post: {slug}\n")
            f.write("Replace this with actual image from Unsplash or Pexels\n")
        
        print(f"🖼️  Placeholder de imagem criado: {image_path}")
    except Exception as e:
        print(f"❌ Erro ao criar placeholder de imagem: {e}")

def main():
    """Função principal"""
    
    print("\n" + "=" * 70)
    print("🚀 GERADOR DE POSTS DO BLOG - GOOGLE GEMINI (GRATUITO)")
    print("=" * 70 + "\n")
    
    try:
        # Carregar configurações
        config = load_config()
        
        # Selecionar tópico
        topic = select_topic(config)
        print(f"📝 Tópico selecionado: {topic['title']}\n")
        
        # Gerar conteúdo
        content = generate_post_content(topic, config)
        if not content:
            print("❌ Falha ao gerar conteúdo. Abortando...")
            sys.exit(1)
        
        # Extrair metadados
        metadata = extract_metadata(content, topic)
        if not metadata:
            print("❌ Falha ao extrair metadados. Abortando...")
            sys.exit(1)
        
        # Criar post
        post_metadata = create_blog_post(content, metadata, config)
        if not post_metadata:
            print("❌ Falha ao criar post. Abortando...")
            sys.exit(1)
        
        # Criar imagem placeholder
        create_placeholder_image(metadata['slug'])
        
        # Atualizar índice
        update_posts_index(post_metadata)
        
        print("\n" + "=" * 70)
        print("✅ POST GERADO COM SUCESSO!")
        print("=" * 70)
        print(f"Título: {post_metadata['title']}")
        print(f"Slug: {post_metadata['slug']}")
        print(f"Data: {post_metadata['date']}")
        print(f"Arquivo: {POSTS_DIR / f'{metadata['slug']}.md'}")
        print("=" * 70 + "\n")
        
        sys.exit(0)
        
    except Exception as e:
        print(f"\n❌ ERRO GERAL: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
