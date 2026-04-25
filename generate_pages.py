import os

# Consolidate CSS content
css_content = """
:root {
    --primary-blue: #172B41;
    --accent-gold: #C9A961;
    --bg-light: #F8F8F8;
    --whatsapp-green: #25D366;
    --text-dark: #333333;
    --text-muted: #666666;
    --white: #FFFFFF;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Inter', sans-serif;
    background-color: var(--bg-light);
    color: var(--text-dark);
    line-height: 1.6;
}

h1, h2, h3, h4 {
    font-family: 'Montserrat', sans-serif;
    font-weight: 700;
}

/* Top Bar */
.top-bar {
    background-color: var(--primary-blue);
    color: white;
    padding: 5px 5%;
    font-size: 0.85rem;
    text-align: right;
}

/* Header & Navigation */
header {
    background-color: var(--white);
    padding: 0 5%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: sticky;
    top: 0;
    z-index: 1000;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    height: 80px;
}

.logo {
    font-family: 'Montserrat', sans-serif;
    font-weight: 700;
    font-size: 1.4rem;
    color: var(--primary-blue);
    text-decoration: none;
}

nav {
    display: flex;
    align-items: center;
    gap: 30px;
}

.nav-links {
    display: flex;
    list-style: none;
    gap: 25px;
}

.nav-links a {
    text-decoration: none;
    color: var(--primary-blue);
    font-weight: 600;
    font-size: 0.95rem;
    transition: color 0.3s;
}

.nav-links a:hover {
    color: var(--accent-gold);
}

/* Dropdown */
.dropdown {
    position: relative;
}

.dropdown-content {
    display: none;
    position: absolute;
    background-color: var(--white);
    min-width: 220px;
    box-shadow: 0 8px 16px rgba(0,0,0,0.1);
    z-index: 1;
    top: 100%;
    border-top: 3px solid var(--accent-gold);
}

.dropdown:hover .dropdown-content {
    display: block;
}

.dropdown-content a {
    color: var(--text-dark);
    padding: 12px 16px;
    display: block;
    font-size: 0.9rem;
}

.dropdown-content a:hover {
    background-color: var(--bg-light);
}

.btn-nav-whatsapp {
    background-color: var(--whatsapp-green);
    color: white !important;
    padding: 10px 20px;
    border-radius: 5px;
    transition: transform 0.3s;
}

.btn-nav-whatsapp:hover {
    transform: translateY(-2px);
    color: white !important;
}

/* Page Header (for subpages) */
.page-header {
    padding: 60px 5%;
    background-color: var(--primary-blue);
    color: white;
    text-align: center;
}

.page-header h1 {
    font-size: 2.5rem;
    margin-bottom: 10px;
}

/* Content Sections */
.content-section {
    padding: 80px 5%;
    max-width: 1000px;
    margin: 0 auto;
}

.cta-box {
    background-color: var(--white);
    padding: 40px;
    border-radius: 10px;
    text-align: center;
    box-shadow: 0 5px 15px rgba(0,0,0,0.05);
    margin-top: 40px;
}

.btn-cta {
    background-color: var(--whatsapp-green);
    color: white;
    padding: 15px 30px;
    border-radius: 8px;
    text-decoration: none;
    font-weight: 700;
    display: inline-block;
    margin-top: 20px;
}

/* Footer */
footer {
    background-color: var(--primary-blue);
    color: white;
    padding: 60px 5% 20px;
    margin-top: 80px;
}

.footer-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 40px;
    margin-bottom: 40px;
}

.footer-col h4 {
    color: var(--accent-gold);
    margin-bottom: 20px;
}

.footer-col a {
    color: #ccc;
    text-decoration: none;
    display: block;
    margin-bottom: 10px;
}

.footer-bottom {
    text-align: center;
    padding-top: 20px;
    border-top: 1px solid rgba(255,255,255,0.1);
    font-size: 0.8rem;
    color: #888;
}

/* Floating WhatsApp */
.whatsapp-float {
    position: fixed;
    bottom: 30px;
    right: 30px;
    background-color: var(--whatsapp-green);
    color: white;
    width: 60px;
    height: 60px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 30px;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.2);
    z-index: 1000;
    text-decoration: none;
}

/* Responsive */
@media (max-width: 768px) {
    header { flex-direction: column; height: auto; padding: 20px; text-align: center; }
    nav { flex-direction: column; gap: 15px; margin-top: 20px; width: 100%; }
    .nav-links { flex-direction: column; align-items: center; gap: 10px; width: 100%; }
    .btn-nav-whatsapp { width: 100%; text-align: center; }
    .top-bar { text-align: center; }
}

/* Hero Section */
.hero {
    padding: 100px 5%;
    text-align: center;
    background: linear-gradient(135deg, #ffffff 0%, #f0f4f8 100%);
    border-bottom: 1px solid #eee;
}

.hero h1 {
    font-size: 3rem;
    color: var(--primary-blue);
    margin-bottom: 1.5rem;
    max-width: 900px;
    margin-left: auto;
    margin-right: auto;
}

.hero p {
    font-size: 1.2rem;
    color: var(--text-muted);
    margin-bottom: 2.5rem;
    max-width: 700px;
    margin-left: auto;
    margin-right: auto;
}

/* Trust Section */
.trust-section {
    padding: 60px 5%;
    background-color: var(--white);
    display: flex;
    justify-content: center;
    gap: 40px;
    flex-wrap: wrap;
    border-bottom: 1px solid #eee;
}

.trust-item {
    display: flex;
    align-items: center;
    gap: 10px;
    font-weight: 600;
    color: var(--primary-blue);
}

.trust-item i {
    color: var(--accent-gold);
    font-size: 1.2rem;
}

/* Specialty Cards */
.specialties {
    padding: 80px 5%;
    text-align: center;
}

.section-title {
    font-size: 2.2rem;
    margin-bottom: 40px;
    color: var(--primary-blue);
}

.grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 30px;
}

.card {
    background: var(--white);
    padding: 40px;
    border-radius: 10px;
    box-shadow: 0 5px 15px rgba(0,0,0,0.05);
    text-decoration: none;
    color: inherit;
    transition: all 0.3s ease;
    border-bottom: 4px solid transparent;
}

.card:hover {
    transform: translateY(-10px);
    border-bottom-color: var(--accent-gold);
}

.card i {
    font-size: 2.5rem;
    color: var(--accent-gold);
    margin-bottom: 20px;
    display: block;
}

.card h3 {
    margin-bottom: 15px;
    color: var(--primary-blue);
}

@media (max-width: 768px) {
    .hero h1 { font-size: 2rem; }
}
"""

template = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{{{TITLE}}}} | Escritório de Advocacia</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=Montserrat:wght@700&display=swap" rel="stylesheet">
    <style>
        {css_content}
    </style>
</head>
<body>

    <div class="top-bar">
        <i class="fas fa-phone"></i> (00) 0000-0000 | <i class="fab fa-whatsapp"></i> (00) 90000-0000
    </div>

    <header>
        <a href="index.html" class="logo">Advocacia Estratégica</a>
        <nav>
            <ul class="nav-links">
                <li><a href="index.html">Início</a></li>
                <li class="dropdown">
                    <a href="#">Áreas de Atuação <i class="fas fa-chevron-down" style="font-size: 0.7rem;"></i></a>
                    <div class="dropdown-content">
                        <a href="trabalhista.html">Direito Trabalhista</a>
                        <a href="previdenciario.html">Direito Previdenciário</a>
                        <a href="civil.html">Direito Civil</a>
                        <a href="familia.html">Direito de Família</a>
                        <a href="consumidor.html">Direito do Consumidor</a>
                        <a href="empresarial.html">Direito Empresarial</a>
                    </div>
                </li>
                <li><a href="sobre.html">Sobre Nós</a></li>
                <li><a href="depoimentos.html">Depoimentos</a></li>
                <li><a href="blog.html">Blog</a></li>
                <li><a href="contato.html">Contato</a></li>
            </ul>
            <a href="https://wa.me/5500000000000" class="btn-nav-whatsapp"><i class="fab fa-whatsapp"></i> Fale no WhatsApp</a>
        </nav>
    </header>

    {{{{BODY}}}}

    <footer>
        <div class="footer-grid">
            <div class="footer-col">
                <h4>Escritório</h4>
                <p>Advocacia Estratégica</p>
                <p>OAB/XX 000.000</p>
            </div>
            <div class="footer-col">
                <h4>Links Úteis</h4>
                <a href="sobre.html">Sobre Nós</a>
                <a href="depoimentos.html">Depoimentos</a>
                <a href="blog.html">Blog</a>
                <a href="contato.html">Contato</a>
            </div>
            <div class="footer-col">
                <h4>Contato</h4>
                <p>(00) 0000-0000</p>
                <p>contato@escritorio.com.br</p>
                <p>Rua Exemplo, 123 - Centro</p>
            </div>
        </div>
        <div class="footer-bottom">
            &copy; 2024 Advocacia Estratégica. Todos os direitos reservados. | Política de Privacidade | LGPD
        </div>
    </footer>

    <a href="https://wa.me/5500000000000" class="whatsapp-float">
        <i class="fab fa-whatsapp"></i>
    </a>

</body>
</html>
"""

pages = [
    {
        'filename': 'index.html',
        'title': 'Início',
        'body': '''
    <section class="hero">
        <h1>Seu Direito Merece Ser Defendido com Seriedade e Agilidade.</h1>
        <p>Atuação jurídica estratégica, atendimento humanizado e soluções eficientes para proteger seus interesses.</p>
        <a href="https://wa.me/5500000000000" style="background-color: var(--whatsapp-green); color: white; padding: 15px 30px; border-radius: 8px; text-decoration: none; font-weight: 700; display: inline-block;">
            Converse Agora com um Advogado
        </a>
        <p style="margin-top: 10px; font-size: 0.9rem;">Atendimento rápido e personalizado pelo WhatsApp.</p>
    </section>

    <section class="trust-section">
        <div class="trust-item"><i class="fas fa-user-tie"></i> Atendimento direto com advogado</div>
        <div class="trust-item"><i class="fas fa-bolt"></i> Resposta rápida</div>
        <div class="trust-item"><i class="fas fa-globe"></i> Atuação presencial e online</div>
        <div class="trust-item"><i class="fas fa-shield-alt"></i> Sigilo absoluto</div>
    </section>

    <section class="specialties">
        <h2 class="section-title">Nossas Especialidades</h2>
        <div class="grid">
            <a href="trabalhista.html" class="card">
                <i class="fas fa-briefcase"></i>
                <h3>Direito Trabalhista</h3>
                <p>Protegendo seus direitos no ambiente de trabalho.</p>
            </a>
            <a href="previdenciario.html" class="card">
                <i class="fas fa-blind"></i>
                <h3>Direito Previdenciário</h3>
                <p>Garantindo sua aposentadoria e benefícios.</p>
            </a>
            <a href="civil.html" class="card">
                <i class="fas fa-gavel"></i>
                <h3>Direito Civil</h3>
                <p>Soluções para conflitos e proteção de patrimônio.</p>
            </a>
            <a href="familia.html" class="card">
                <i class="fas fa-users"></i>
                <h3>Direito de Família</h3>
                <p>Atendimento humanizado para questões familiares.</p>
            </a>
            <a href="consumidor.html" class="card">
                <i class="fas fa-shopping-cart"></i>
                <h3>Direito do Consumidor</h3>
                <p>Defesa contra abusos e práticas indevidas.</p>
            </a>
            <a href="empresarial.html" class="card">
                <i class="fas fa-building"></i>
                <h3>Direito Empresarial</h3>
                <p>Segurança jurídica para o crescimento do seu negócio.</p>
            </a>
        </div>
    </section>
        '''
    },
    {
        'filename': 'trabalhista.html',
        'title': 'Direito Trabalhista',
        'body': '''
    <section class="page-header">
        <h1>Seus Direitos Trabalhistas Merecem Respeito.</h1>
    </section>
    <section class="content-section">
        <h2>Problemas Atendidos</h2>
        <ul style="margin-top: 20px; margin-left: 20px;">
            <li>Demissão sem justa causa</li>
            <li>Verbas rescisórias</li>
            <li>Horas extras</li>
            <li>Reconhecimento de vínculo</li>
            <li>Assédio moral</li>
        </ul>
        <div class="cta-box">
            <h3>Precisa de ajuda com este assunto?</h3>
            <p>Nossa equipe está pronta para analisar seu caso e oferecer a melhor estratégia jurídica.</p>
            <a href="https://wa.me/5500000000000" class="btn-cta">🟢 Analisar Meu Caso</a>
        </div>
    </section>
        '''
    },
    {
        'filename': 'previdenciario.html',
        'title': 'Direito Previdenciário',
        'body': '''
    <section class="page-header">
        <h1>Seu Benefício Pode Estar Mais Próximo do Que Você Imagina.</h1>
    </section>
    <section class="content-section">
        <h2>Serviços</h2>
        <ul style="margin-top: 20px; margin-left: 20px;">
            <li>Aposentadoria</li>
            <li>Auxílio-doença</li>
            <li>BPC/LOAS</li>
            <li>Revisões</li>
            <li>Planejamento previdenciário</li>
        </ul>
        <div class="cta-box">
            <h3>Precisa de ajuda com este assunto?</h3>
            <p>Nossa equipe está pronta para analisar seu caso e oferecer a melhor estratégia jurídica.</p>
            <a href="https://wa.me/5500000000000" class="btn-cta">🟢 Solicitar Análise Previdenciária</a>
        </div>
    </section>
        '''
    },
    {
        'filename': 'civil.html',
        'title': 'Direito Civil',
        'body': '''
    <section class="page-header">
        <h1>Proteção Jurídica Para Seu Patrimônio e Seus Direitos.</h1>
    </section>
    <section class="content-section">
        <h2>Serviços</h2>
        <ul style="margin-top: 20px; margin-left: 20px;">
            <li>Indenizações</li>
            <li>Cobranças</li>
            <li>Contratos</li>
            <li>Responsabilidade civil</li>
        </ul>
        <div class="cta-box">
            <h3>Precisa de ajuda com este assunto?</h3>
            <p>Nossa equipe está pronta para analisar seu caso e oferecer a melhor estratégia jurídica.</p>
            <a href="https://wa.me/5500000000000" class="btn-cta">🟢 Falar com Especialista</a>
        </div>
    </section>
        '''
    },
    {
        'filename': 'familia.html',
        'title': 'Direito de Família',
        'body': '''
    <section class="page-header">
        <h1>Soluções Humanizadas Para Momentos Delicados.</h1>
    </section>
    <section class="content-section">
        <h2>Serviços</h2>
        <ul style="margin-top: 20px; margin-left: 20px;">
            <li>Divórcio</li>
            <li>Pensão alimentícia</li>
            <li>Guarda</li>
            <li>Inventário</li>
        </ul>
        <div class="cta-box">
            <h3>Precisa de ajuda com este assunto?</h3>
            <p>Nossa equipe está pronta para analisar seu caso e oferecer a melhor estratégia jurídica.</p>
            <a href="https://wa.me/5500000000000" class="btn-cta">🟢 Receber Orientação</a>
        </div>
    </section>
        '''
    },
    {
        'filename': 'consumidor.html',
        'title': 'Direito do Consumidor',
        'body': '''
    <section class="page-header">
        <h1>Quando Seus Direitos São Violados, Nós Atuamos.</h1>
    </section>
    <section class="content-section">
        <h2>Serviços</h2>
        <ul style="margin-top: 20px; margin-left: 20px;">
            <li>Cobrança indevida</li>
            <li>Negativação abusiva</li>
            <li>Produtos defeituosos</li>
            <li>Serviços mal prestados</li>
        </ul>
        <div class="cta-box">
            <h3>Precisa de ajuda com este assunto?</h3>
            <p>Nossa equipe está pronta para analisar seu caso e oferecer a melhor estratégia jurídica.</p>
            <a href="https://wa.me/5500000000000" class="btn-cta">🟢 Resolver Meu Problema</a>
        </div>
    </section>
        '''
    },
    {
        'filename': 'empresarial.html',
        'title': 'Direito Empresarial',
        'body': '''
    <section class="page-header">
        <h1>Segurança Jurídica Para Sua Empresa Crescer.</h1>
    </section>
    <section class="content-section">
        <h2>Serviços</h2>
        <ul style="margin-top: 20px; margin-left: 20px;">
            <li>Contratos</li>
            <li>Cobranças</li>
            <li>Consultoria preventiva</li>
            <li>Recuperação de crédito</li>
        </ul>
        <div class="cta-box">
            <h3>Precisa de ajuda com este assunto?</h3>
            <p>Nossa equipe está pronta para analisar seu caso e oferecer a melhor estratégia jurídica.</p>
            <a href="https://wa.me/5500000000000" class="btn-cta">🟢 Proteger Minha Empresa</a>
        </div>
    </section>
        '''
    },
    {
        'filename': 'sobre.html',
        'title': 'Sobre Nós',
        'body': '''
    <section class="page-header">
        <h1>Advocacia Moderna, Próxima e Eficiente.</h1>
    </section>
    <section class="content-section">
        <p>Nosso compromisso é oferecer soluções jurídicas claras, seguras e personalizadas, sempre com atendimento direto, transparência e foco em resultados.</p>
        <p style="margin-top: 20px;">Aqui, cada cliente é tratado com a atenção que seu caso merece.</p>
        <h2 style="margin-top: 40px;">Diferenciais</h2>
        <ul style="margin-top: 20px; margin-left: 20px;">
            <li>Atendimento humanizado</li>
            <li>Estratégia personalizada</li>
            <li>Comunicação sem juridiquês</li>
            <li>Transparência total</li>
        </ul>
        <div class="cta-box">
            <h3>Precisa de ajuda?</h3>
            <p>Nossa equipe está pronta para analisar seu caso.</p>
            <a href="https://wa.me/5500000000000" class="btn-cta">📞 Agendar Atendimento</a>
        </div>
    </section>
        '''
    },
    {
        'filename': 'depoimentos.html',
        'title': 'Depoimentos',
        'body': '''
    <section class="page-header">
        <h1>Resultados que Geram Confiança</h1>
    </section>
    <section class="content-section">
        <div style="display: grid; gap: 20px; margin-top: 30px;">
            <div style="background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                <p>"Fui atendido rapidamente e tive total clareza sobre meu caso desde o primeiro contato."</p>
            </div>
            <div style="background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                <p>"Profissional extremamente competente, atencioso e transparente."</p>
            </div>
            <div style="background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                <p>"Resolveram meu problema com agilidade e segurança."</p>
            </div>
        </div>
        <div class="cta-box">
            <a href="https://wa.me/5500000000000" class="btn-cta">🟢 Quero Ser Atendido</a>
        </div>
    </section>
        '''
    },
    {
        'filename': 'blog.html',
        'title': 'Blog',
        'body': '''
    <section class="page-header">
        <h1>Informação Jurídica Sem Complicação</h1>
    </section>
    <section class="content-section">
        <p>Em breve, traremos conteúdos exclusivos sobre seus direitos.</p>
        <h2 style="margin-top: 40px;">Categorias</h2>
        <ul style="margin-top: 20px; margin-left: 20px;">
            <li>Direitos Trabalhistas</li>
            <li>Aposentadoria</li>
            <li>Direito do Consumidor</li>
            <li>Família</li>
            <li>Empresarial</li>
        </ul>
        <div class="cta-box">
            <a href="https://wa.me/5500000000000" class="btn-cta">🟢 Ler Mais Artigos</a>
        </div>
    </section>
        '''
    },
    {
        'filename': 'contato.html',
        'title': 'Contato',
        'body': '''
    <section class="page-header">
        <h1>Fale com Nossa Equipe</h1>
    </section>
    <section class="content-section">
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 40px; margin-top: 30px;">
            <div>
                <h3>Envie uma mensagem</h3>
                <form style="display: flex; flex-direction: column; gap: 15px; margin-top: 20px;">
                    <input type="text" placeholder="Nome" style="padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
                    <input type="text" placeholder="Telefone" style="padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
                    <input type="email" placeholder="E-mail" style="padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
                    <select style="padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
                        <option>Área do Direito</option>
                        <option>Trabalhista</option>
                        <option>Previdenciário</option>
                        <option>Civil</option>
                        <option>Família</option>
                        <option>Consumidor</option>
                        <option>Empresarial</option>
                    </select>
                    <textarea placeholder="Mensagem" rows="4" style="padding: 10px; border: 1px solid #ddd; border-radius: 5px;"></textarea>
                </form>
            </div>
            <div>
                <h3>Opções de Contato</h3>
                <ul style="list-style: none; margin-top: 20px; display: flex; flex-direction: column; gap: 15px;">
                    <li><i class="fab fa-whatsapp"></i> WhatsApp: (00) 90000-0000</li>
                    <li><i class="fas fa-phone"></i> Telefone: (00) 0000-0000</li>
                    <li><i class="fas fa-envelope"></i> E-mail: contato@escritorio.com.br</li>
                    <li><i class="fas fa-map-marker-alt"></i> Endereço: Rua Exemplo, 123 - Centro</li>
                </ul>
            </div>
        </div>
        <div class="cta-box">
            <a href="https://wa.me/5500000000000" class="btn-cta">🟢 Enviar Mensagem</a>
        </div>
    </section>
        '''
    }
]

for page in pages:
    content = template.replace('{{TITLE}}', page['title'])
    content = content.replace('{{BODY}}', page['body'])
    
    with open(page['filename'], 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Generated {page['filename']}")
