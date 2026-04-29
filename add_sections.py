import json
from pathlib import Path

# Carregar o índice de posts
with open('blog/posts/index.json', 'r', encoding='utf-8') as f:
    posts_data = json.load(f)

# Mapeamento de páginas para categorias de posts
page_categories = {
    'familia.html': ['Direito de Família'],
    'criminal.html': ['Direito Criminal'],
    'contrato.html': ['Contratos'],
    'busca-e-apreensao.html': ['Busca e Apreensão'],
    'trabalhista.html': ['Direito Trabalhista'],
    'trabalhista-empregado.html': ['Direito Trabalhista'],
    'trabalhista-empresa.html': ['Direito Trabalhista'],
}

def get_related_posts(category, limit=3):
    """Retorna posts relacionados a uma categoria"""
    related = [p for p in posts_data if category in p.get('categories', [])]
    return related[:limit]

def create_posts_section(posts):
    """Cria HTML para a seção de posts relacionados"""
    if not posts:
        return ""
    
    html = '''
            <section class="related-posts-section">
                <div class="related-posts-wrapper">
                    <h2>Publicações Relacionadas</h2>
                    <p class="related-posts-subtitle">Confira artigos do nosso blog que podem te interessar.</p>
                    <div class="related-posts-grid">
'''
    
    for post in posts:
        html += f'''
                        <a href="{post['url']}" class="related-post-card">
                            <div class="related-post-image">
                                <img src="{post.get('image', 'https://images.unsplash.com/photo-1589829545856-d10d557cf95f?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80')}" alt="{post['title']}">
                            </div>
                            <div class="related-post-content">
                                <h3>{post['title']}</h3>
                                <p>{post.get('excerpt', '')}</p>
                                <div class="related-post-meta">
                                    <span><i class="far fa-calendar"></i> {post['date'][:10]}</span>
                                </div>
                            </div>
                        </a>
'''
    
    html += '''
                    </div>
                </div>
            </section>
'''
    return html

def create_contact_section():
    """Cria HTML para a seção de contato"""
    return '''
            <section class="contact-section-area">
                <div class="contact-content">
                    <h2>Pronto para resolver sua situação?</h2>
                    <p>Não deixe seus direitos para depois. Fale agora mesmo com um especialista e receba uma orientação personalizada.</p>
                    <a href="https://wa.me/5547996756766" class="btn-primary"><i class="fab fa-whatsapp"></i> Fale Conosco Agora</a>
                </div>
            </section>
'''

# CSS para as novas seções
CSS_TO_ADD = '''

/* ===== RELATED POSTS SECTION ===== */
.related-posts-section {
    padding: 80px 5%;
    background-color: var(--white);
}

.related-posts-wrapper {
    max-width: 1000px;
    margin: 0 auto;
}

.related-posts-section h2 {
    font-size: 2rem;
    color: var(--primary-blue);
    margin-bottom: 10px;
    text-align: center;
}

.related-posts-subtitle {
    text-align: center;
    color: var(--text-muted);
    font-size: 1rem;
    margin-bottom: 50px;
}

.related-posts-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 30px;
}

.related-post-card {
    background: var(--white);
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    transition: all 0.3s ease;
    text-decoration: none;
    color: inherit;
    display: flex;
    flex-direction: column;
    border: 1px solid #f0f0f0;
}

.related-post-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 12px 30px rgba(0,0,0,0.15);
    border-color: var(--accent-gold);
}

.related-post-image {
    width: 100%;
    height: 200px;
    overflow: hidden;
    background: var(--bg-light);
}

.related-post-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.3s ease;
}

.related-post-card:hover .related-post-image img {
    transform: scale(1.05);
}

.related-post-content {
    padding: 24px;
    display: flex;
    flex-direction: column;
    gap: 12px;
    flex-grow: 1;
}

.related-post-content h3 {
    font-size: 1.1rem;
    color: var(--primary-blue);
    line-height: 1.4;
    margin: 0;
}

.related-post-content p {
    font-size: 0.9rem;
    color: var(--text-muted);
    line-height: 1.6;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    margin: 0;
}

.related-post-meta {
    display: flex;
    gap: 16px;
    font-size: 0.8rem;
    color: var(--text-muted);
    margin-top: auto;
}

.related-post-meta span {
    display: flex;
    align-items: center;
    gap: 6px;
}

.related-post-meta i {
    color: var(--accent-gold);
}

/* ===== CONTACT SECTION AREA ===== */
.contact-section-area {
    padding: 80px 5%;
    background: linear-gradient(135deg, #0f1f30 0%, #172B41 50%, #1a3350 100%);
    text-align: center;
    color: white;
    position: relative;
    overflow: hidden;
}

.contact-section-area::before {
    content: '';
    position: absolute;
    top: -100px;
    left: -100px;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(201,169,97,0.08) 0%, transparent 70%);
    border-radius: 50%;
    pointer-events: none;
}

.contact-section-area::after {
    content: '';
    position: absolute;
    bottom: -80px;
    right: -80px;
    width: 350px;
    height: 350px;
    background: radial-gradient(circle, rgba(37,211,102,0.06) 0%, transparent 70%);
    border-radius: 50%;
    pointer-events: none;
}

.contact-content {
    max-width: 700px;
    margin: 0 auto;
    position: relative;
    z-index: 1;
}

.contact-section-area h2 {
    font-size: 2.2rem;
    margin-bottom: 16px;
    color: white;
}

.contact-section-area p {
    font-size: 1.05rem;
    color: rgba(255,255,255,0.85);
    margin-bottom: 36px;
}

.btn-primary {
    background-color: var(--whatsapp-green);
    color: white;
    padding: 16px 32px;
    border-radius: 10px;
    text-decoration: none;
    font-weight: 700;
    font-size: 1rem;
    display: inline-flex;
    align-items: center;
    gap: 10px;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(37,211,102,0.3);
    border: none;
    cursor: pointer;
}

.btn-primary:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 25px rgba(37,211,102,0.4);
    background-color: #22c55e;
}

@media (max-width: 768px) {
    .related-posts-grid {
        grid-template-columns: 1fr;
    }
    
    .related-posts-section h2 {
        font-size: 1.6rem;
    }
    
    .contact-section-area h2 {
        font-size: 1.6rem;
    }
    
    .contact-section-area p {
        font-size: 0.95rem;
    }
}
'''

# Processar cada página
for page_file, categories in page_categories.items():
    page_path = Path(page_file)
    if not page_path.exists():
        print(f"⚠️  Página não encontrada: {page_file}")
        continue
    
    # Ler o arquivo
    with open(page_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Obter posts relacionados
    related_posts = get_related_posts(categories[0])
    
    # Criar seções
    posts_section = create_posts_section(related_posts)
    contact_section = create_contact_section()
    
    # Encontrar o ponto de inserção (antes de </main>)
    insertion_point = content.find('    </main>')
    
    if insertion_point != -1:
        # Inserir as seções
        new_content = content[:insertion_point] + posts_section + contact_section + content[insertion_point:]
        
        # Atualizar CSS se necessário
        if 'related-posts-section' not in content:
            # Encontrar o </style>
            style_end = new_content.find('    </style>')
            if style_end != -1:
                new_content = new_content[:style_end] + CSS_TO_ADD + new_content[style_end:]
        
        # Salvar o arquivo
        with open(page_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✅ Atualizado: {page_file}")
    else:
        print(f"⚠️  Não foi possível encontrar </main> em: {page_file}")

print("\n🎉 Processo concluído!")
