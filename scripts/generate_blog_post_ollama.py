#!/usr/bin/env python3
"""
BLOG POST GENERATOR PRO - Gera posts de blog localmente com Ollama (GRATUITO)
Altamente configurável com suporte a temas, links de referência e instruções personalizadas
Compatível com GitHub Pages (site estático)
"""

import os
import sys
import json
import datetime
import re
import argparse
import requests
from pathlib import Path
from urllib.parse import urlparse

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None

# Configurações - Usar caminhos relativos para compatibilidade com GitHub Actions
SCRIPT_DIR = Path(__file__).parent.absolute()
PROJECT_ROOT = SCRIPT_DIR.parent.absolute()
BLOG_DIR = PROJECT_ROOT / "blog"
POSTS_DIR = BLOG_DIR / "posts"
IMAGES_DIR = BLOG_DIR / "images"
CONFIG_FILE = SCRIPT_DIR / "blog_config.json"

# Configurações do Ollama
OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "phi3")

def setup_directories():
    """Criar diretórios se não existirem"""
    try:
        POSTS_DIR.mkdir(parents=True, exist_ok=True)
        IMAGES_DIR.mkdir(parents=True, exist_ok=True)
        print(f"✅ Diretórios criados/verificados")
        return True
    except Exception as e:
        print(f"❌ Erro ao criar diretórios: {e}")
        return False

def load_config():
    """Carregar configurações do arquivo JSON"""
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            config = json.load(f)
            print(f"✅ Configurações carregadas de: {CONFIG_FILE}")
            return config
    except FileNotFoundError:
        print(f"⚠️  Arquivo de configuração não encontrado: {CONFIG_FILE}")
        return {}
    except Exception as e:
        print(f"❌ Erro ao carregar configurações: {e}")
        return {}

def fetch_link_content(url):
    """Buscar e extrair conteúdo de um link (Web Scraping)"""
    if not url:
        return None
    
    try:
        if BeautifulSoup is None:
            print("⚠️  BeautifulSoup não está instalado. Pulando leitura de link.")
            print("    Para ativar: pip install beautifulsoup4")
            return None
        
        print(f"🔗 Buscando conteúdo de: {url}")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remover scripts e estilos
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Extrair texto
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        # Limitar a 2000 caracteres para não sobrecarregar o prompt
        content = text[:2000]
        print(f"✅ Conteúdo extraído ({len(content)} caracteres)")
        return content
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao buscar link: {e}")
        return None
    except Exception as e:
        print(f"❌ Erro ao processar conteúdo do link: {e}")
        return None

def test_ollama_connection():
    """Testar se o Ollama está acessível"""
    try:
        print("🔍 Testando conexão com Ollama...")
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            if models:
                print(f"✅ Ollama conectado! Modelos disponíveis: {len(models)}")
                model_names = [m.get('name', 'desconhecido') for m in models]
                print(f"   Modelos: {', '.join(model_names[:3])}...")
                return True
            else:
                print("⚠️  Ollama está rodando, mas nenhum modelo foi encontrado.")
                print("   Tente rodar: ollama run phi3")
                return False
        else:
            print(f"❌ Ollama respondeu com erro: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Não consegui conectar ao Ollama em http://localhost:11434")
        print("   Certifique-se de que o Ollama está rodando no seu computador.")
        print("   No Windows, abra o aplicativo Ollama.")
        print("   No Mac/Linux, tente: ollama serve")
        return False
    except Exception as e:
        print(f"❌ Erro ao testar Ollama: {e}")
        return False

def generate_post_content_ollama(tema, instrucoes_customizadas, conteudo_link, config):
    """Gerar conteúdo completo do post usando Ollama"""
    
    # Construir o prompt base
    prompt_base = f"""Você é um advogado especialista em direito brasileiro e um excelente redator de conteúdo para blog. Seu objetivo é criar um artigo de blog informativo, envolvente e focado em conversão para o escritório de advocacia Gabriel Corrêa.

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

TEMA DO ARTIGO: {tema}

ESTRUTURA OBRIGATÓRIA:
1. Introdução (2-3 parágrafos explicando o problema)
2. Seção 1: [Subtítulo relevante] (3-4 parágrafos)
3. Seção 2: [Subtítulo relevante] (3-4 parágrafos)
4. Seção 3: [Subtítulo relevante] (3-4 parágrafos)
5. FAQ - Perguntas Frequentes (3-5 Q&A)
6. Conclusão (2-3 parágrafos com CTA)

EXEMPLO DE CTA:
**Precisa de ajuda profissional?** Fale agora com o Advogado Gabriel Corrêa pelo WhatsApp: [📞 (47) 99675-6766](https://wa.me/5547996756766)
"""

    # Adicionar conteúdo do link se disponível
    if conteudo_link:
        prompt_base += f"\n\nCONTEÚDO DE REFERÊNCIA (do link fornecido):\n{conteudo_link}\n\nUse este conteúdo como inspiração e contexto para o artigo, mas reescreva com suas próprias palavras e foco em direito."

    # Adicionar instruções customizadas se fornecidas
    if instrucoes_customizadas:
        prompt_base += f"\n\nINSTRUÇÕES ADICIONAIS DO USUÁRIO:\n{instrucoes_customizadas}"

    prompt_base += "\n\nGere o artigo completo em Markdown, pronto para publicação."

    try:
        print(f"🤖 Gerando conteúdo para: '{tema}' com Ollama ({OLLAMA_MODEL})...")
        print(f"   Conectando a: {OLLAMA_API_URL}")
        
        payload = {
            "model": OLLAMA_MODEL,
            "prompt": prompt_base,
            "stream": False
        }
        headers = {"Content-Type": "application/json"}
        
        # Tentar a requisição com timeout mais longo
        response = requests.post(OLLAMA_API_URL, headers=headers, json=payload, timeout=600)
        
        if response.status_code == 404:
            print("❌ Erro 404: Endpoint não encontrado ou modelo não está carregado.")
            print(f"   Modelo: {OLLAMA_MODEL}")
            print("   Tente rodar no terminal: ollama run " + OLLAMA_MODEL)
            return None
        
        response.raise_for_status()
        
        result = response.json()
        content = result.get('response', '')
        
        if not content:
            print("❌ Ollama retornou uma resposta vazia.")
            print("   Tente novamente ou reinicie o Ollama.")
            return None
        
        print(f"✅ Conteúdo gerado com sucesso ({len(content)} caracteres)")
        return content
        
    except requests.exceptions.ConnectionError:
        print("❌ Erro de conexão com Ollama.")
        print("   Certifique-se de que o Ollama está rodando no seu computador.")
        print("   No Windows: Abra o aplicativo Ollama")
        print("   No Mac/Linux: tente rodar 'ollama serve' em outro terminal")
        return None
    except requests.exceptions.Timeout:
        print("❌ Timeout ao conectar com Ollama (levou mais de 10 minutos).")
        print("   Tente novamente com um prompt mais curto.")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"❌ Erro HTTP ao gerar conteúdo: {e}")
        print(f"   Status: {response.status_code}")
        print(f"   Resposta: {response.text[:200]}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao gerar conteúdo com Ollama: {e}")
        return None
    except Exception as e:
        print(f"❌ Erro inesperado ao gerar conteúdo: {e}")
        import traceback
        traceback.print_exc()
        return None

def extract_metadata(content, tema):
    """Extrair metadados do conteúdo gerado"""
    
    try:
        # Extrair primeiro parágrafo como excerpt
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip() and not p.startswith('#')]
        excerpt = (paragraphs[0][:200] + "...") if paragraphs else "Artigo jurídico informativo"
        
        # Gerar slug do título
        slug = re.sub(r'[^a-z0-9]+', '-', tema.lower()).strip('-')
        
        return {
            'title': tema,
            'excerpt': excerpt,
            'slug': slug,
            'keywords': [tema.lower()],
            'category': 'Direito'
        }
    except Exception as e:
        print(f"❌ Erro ao extrair metadados: {e}")
        return None

def create_blog_post(content, metadata):
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
        
        slug = metadata['slug']
        return {
            'title': metadata['title'],
            'slug': slug,
            'url': f"/site_escritorio/blog/posts/{slug}.html",
            'date': datetime.datetime.now().isoformat(),
            'author': "Advogado Gabriel Corrêa",
            'excerpt': metadata['excerpt'],
            'image': f"/site_escritorio/blog/images/{slug}.jpg",
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
    """Função principal com argumentos de linha de comando"""
    
    parser = argparse.ArgumentParser(
        description="Gerador de Posts de Blog com Ollama (Local e Gratuito)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  
  # Gerar post com tema específico
  python generate_blog_post_ollama.py --tema "Revisão da Vida Toda no INSS"
  
  # Gerar post com tema e link de referência
  python generate_blog_post_ollama.py --tema "Demissão Sem Justa Causa" --link "https://exemplo.com/noticia"
  
  # Gerar post com instruções customizadas
  python generate_blog_post_ollama.py --tema "Pensão Alimentícia" --instrucoes "Foque em direitos das crianças e valores mínimos"
  
  # Combinar tudo
  python generate_blog_post_ollama.py --tema "Indenização por Dano Moral" --link "https://exemplo.com/caso" --instrucoes "Inclua exemplos de valores recentes"
        """
    )
    
    parser.add_argument('--tema', type=str, help='Tema específico para o artigo (obrigatório)')
    parser.add_argument('--link', type=str, help='Link de referência para usar como contexto')
    parser.add_argument('--instrucoes', type=str, help='Instruções customizadas para a IA')
    parser.add_argument('--modelo', type=str, default=OLLAMA_MODEL, help=f'Modelo Ollama a usar (padrão: {OLLAMA_MODEL})')
    
    args = parser.parse_args()
    
    # Validar argumentos
    if not args.tema:
        parser.print_help()
        print("\n❌ Erro: O argumento --tema é obrigatório!")
        sys.exit(1)
    
    print("\n" + "=" * 70)
    print("🚀 GERADOR DE POSTS DO BLOG - OLLAMA PRO (LOCAL E GRATUITO)")
    print("=" * 70 + "\n")
    
    try:
        # Setup
        if not setup_directories():
            sys.exit(1)
        
        # Testar conexão com Ollama
        if not test_ollama_connection():
            print("\n⚠️  Não foi possível conectar ao Ollama. Abortando...")
            sys.exit(1)
        
        config = load_config()
        
        # Buscar conteúdo do link se fornecido
        conteudo_link = None
        if args.link:
            conteudo_link = fetch_link_content(args.link)
        
        # Gerar conteúdo
        content = generate_post_content_ollama(args.tema, args.instrucoes, conteudo_link, config)
        if not content:
            print("❌ Falha ao gerar conteúdo. Abortando...")
            sys.exit(1)
        
        # Extrair metadados
        metadata = extract_metadata(content, args.tema)
        if not metadata:
            print("❌ Falha ao extrair metadados. Abortando...")
            sys.exit(1)
        
        # Criar post
        post_metadata = create_blog_post(content, metadata)
        if not post_metadata:
            print("❌ Falha ao criar post. Abortando...")
            sys.exit(1)
        
        # Criar imagem placeholder
        slug = metadata['slug']
        create_placeholder_image(slug)
        
        # Atualizar índice
        update_posts_index(post_metadata)
        
        print("\n" + "=" * 70)
        print("✅ POST GERADO COM SUCESSO!")
        print("=" * 70)
        print(f"Título: {post_metadata['title']}")
        print(f"Slug: {post_metadata['slug']}")
        print(f"Data: {post_metadata['date']}")
        slug = metadata['slug']
        print(f"Arquivo: {POSTS_DIR / f'{slug}.md'}")
        print("\n📌 Próximos passos:")
        print("  1. Revise o conteúdo gerado")
        print("  2. Substitua a imagem placeholder por uma real")
        print("  3. Faça git add, commit e push para publicar no blog")
        print("=" * 70 + "\n")
        
        sys.exit(0)
        
    except Exception as e:
        print(f"\n❌ ERRO GERAL: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
