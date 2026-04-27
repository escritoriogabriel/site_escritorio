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
    padding: 8px 5%;
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

/* Profile Section */
.profile-grid {
    display: grid;
    grid-template-columns: 1fr 1.5fr;
    gap: 60px;
    align-items: center;
}

.profile-image {
    width: 100%;
    aspect-ratio: 3/4;
    background-color: #ddd;
    border-radius: 15px;
    overflow: hidden;
    position: relative;
    box-shadow: 20px 20px 0 var(--accent-gold);
}

.profile-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.profile-placeholder {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100%;
    color: #888;
    font-style: italic;
}

/* Responsive */
@media (max-width: 768px) {
    header { flex-direction: column; height: auto; padding: 20px; text-align: center; }
    nav { flex-direction: column; gap: 15px; margin-top: 20px; width: 100%; }
    .nav-links { flex-direction: column; align-items: center; gap: 10px; width: 100%; }
    .btn-nav-whatsapp { width: 100%; text-align: center; }
    .top-bar { text-align: center; }
    .profile-grid { grid-template-columns: 1fr; gap: 40px; }
}
"""

template = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{{{TITLE}}}} | Advogado Gabriel Corrêa</title>
    <meta name="description" content="{{{{DESCRIPTION}}}}">
    <meta name="keywords" content="advogado, advocacia, direito trabalhista, previdenciário, civil, família, consumidor, empresarial, escritório de advocacia">
    <link rel="canonical" href="https://escritoriogabriel.github.io/site_escritorio/{{{{FILENAME}}}}">
    
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=Montserrat:wght@700&display=swap" rel="stylesheet">
    <style>
        {css_content}
    </style>
</head>
<body>

    <div class="top-bar">
        <i class="fas fa-envelope"></i> <a href="mailto:escritorio.gabrielcorrea@gmail.com" style="color: white; text-decoration: none;">escritorio.gabrielcorrea@gmail.com</a> &nbsp;|&nbsp; <i class="fab fa-whatsapp"></i> <a href="https://wa.me/5547996756766" style="color: white; text-decoration: none;">(47) 99675-6766</a> &nbsp;|&nbsp; <i class="fas fa-map-marker-alt"></i> Atendimento 100% Online
    </div>

    <header>
        <a href="index.html" class="logo">Advogado Gabriel Corrêa</a>
        <nav>
            <ul class="nav-links">
                <li><a href="index.html">Início</a></li>
                <li class="dropdown">
                    <a href="#">Áreas de Atuação <i class="fas fa-chevron-down" style="font-size: 0.7rem;"></i></a>
                    <div class="dropdown-content">
                        <a href="familia.html">Família</a>
                        <a href="contrato.html">Contratos</a>
                        <a href="criminal.html">Criminal</a>
                        <a href="trabalhista.html">Trabalhista</a>
                        <a href="busca-e-apreensao.html">Busca e Apreensão</a>
                    </div>
                </li>
                <li><a href="sobre.html">Sobre</a></li>
                <li><a href="blog.html">Blog</a></li>
                <li><a href="contato.html">Contato</a></li>
            </ul>
            <a href="https://wa.me/5547996756766" class="btn-nav-whatsapp"><i class="fab fa-whatsapp"></i> WhatsApp</a>
        </nav>
    </header>

    <main>
        {{{{BODY}}}}
    </main>

    <footer>
        <div class="footer-grid">
            <div class="footer-col">
                <h4>Advogado Gabriel Corrêa</h4>
                <p>OAB/SC 63.737</p>
                <p>Atendimento 100% Online em todo o Brasil</p>
            </div>
            <div class="footer-col">
                <h4>Links Úteis</h4>
                <a href="index.html">Início</a>
                <a href="sobre.html">Sobre</a>
                <a href="blog.html">Blog</a>
                <a href="contato.html">Contato</a>
            </div>
            <div class="footer-col">
                <h4>Contato</h4>
                <p>(47) 99675-6766</p>
                <p>escritorio.gabrielcorrea@gmail.com</p>
            </div>
        </div>
        <div class="footer-bottom">
            &copy; 2024 Advogado Gabriel Corrêa. Todos os direitos reservados.
        </div>
    </footer>

    <a href="https://wa.me/5547996756766" class="whatsapp-float" aria-label="Falar pelo WhatsApp">
        <i class="fab fa-whatsapp"></i>
    </a>

    <script>
        // FAQ Accordion
        const faqQuestions = document.querySelectorAll('.faq-question');
        faqQuestions.forEach(question => {{
            question.addEventListener('click', () => {{
                const answer = question.nextElementSibling;
                const icon = question.querySelector('i');
                
                if (answer.style.display === 'block') {{
                    answer.style.display = 'none';
                    icon.classList.replace('fa-chevron-up', 'fa-chevron-down');
                }} else {{
                    answer.style.display = 'block';
                    icon.classList.replace('fa-chevron-down', 'fa-chevron-up');
                }}
            }});
        }});
    </script>
</body>
</html>
"""

pages = [
    {
        'filename': 'sobre.html',
        'title': 'Sobre Mim | Advogado Gabriel Corrêa',
        'description': 'Conheça o Dr. Gabriel Corrêa, advogado com foco em soluções jurídicas práticas e eficientes. Proximidade, clareza e compromisso real com cada cliente.',
        'body': '''
    <section class="page-header">
        <h1>Quem Sou Eu</h1>
        <p>Conheça a história e os valores por trás do atendimento.</p>
    </section>

    <section class="content-section">
        <div class="profile-grid">
            <div class="profile-image">
                <img src="assets/img/advogado.jpg" alt="Dr. Gabriel Corrêa" onerror="this.style.display='none'; this.parentElement.innerHTML='<div class=\\'profile-placeholder\\'><i class=\\'fas fa-user-tie\\' style=\\'font-size: 5rem;\\'></i></div>'">
            </div>
            <div>
                <h2 style="font-size: 2.5rem; color: var(--primary-blue); margin-bottom: 20px;">Dr. Gabriel Corrêa</h2>
                <p style="font-size: 1.2rem; font-weight: 600; color: var(--accent-gold); margin-bottom: 20px;">Advogado regularmente inscrito na OAB/SC 63.737</p>
                <p>Acredito que a advocacia se constrói pela proximidade, clareza e compromisso real com cada cliente. Meu trabalho é transformar questões jurídicas complexas em caminhos objetivos, sempre com transparência e diálogo aberto.</p>
                <p style="margin-top: 20px;">Com uma atuação estratégica e focada na resolução de problemas, busco não apenas defender direitos, mas oferecer a segurança jurídica necessária para que você possa ter tranquilidade.</p>
                
                <div style="margin-top: 40px; display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                    <div style="background: var(--white); padding: 20px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
                        <i class="fas fa-graduation-cap" style="color: var(--accent-gold); font-size: 1.5rem; margin-bottom: 10px;"></i>
                        <h4 style="color: var(--primary-blue);">Formação</h4>
                        <p style="font-size: 0.9rem; color: var(--text-muted);">Especialista em Direito do Trabalho e Previdenciário.</p>
                    </div>
                    <div style="background: var(--white); padding: 20px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
                        <i class="fas fa-award" style="color: var(--accent-gold); font-size: 1.5rem; margin-bottom: 10px;"></i>
                        <h4 style="color: var(--primary-blue);">Experiência</h4>
                        <p style="font-size: 0.9rem; color: var(--text-muted);">Anos de atuação focada em resultados e satisfação do cliente.</p>
                    </div>
                </div>
            </div>
        </div>

        <div style="margin-top: 80px; padding: 40px; background-color: var(--primary-blue); color: white; border-radius: 15px; text-align: center;">
            <h3 style="color: var(--accent-gold); margin-bottom: 20px;">Minha Filosofia de Trabalho</h3>
            <p style="font-size: 1.1rem; max-width: 800px; margin: 0 auto;">"Advogar não é apenas lidar com processos, é lidar com vidas e expectativas. Por isso, trato cada caso como se fosse único, com o máximo de dedicação, técnica e, acima de tudo, humanidade."</p>
        </div>

        <div class="cta-box">
            <h3>Precisa de uma análise para o seu caso?</h3>
            <p>Fale diretamente comigo e receba uma orientação clara e segura.</p>
            <a href="https://wa.me/5547996756766" class="btn-cta">Falar com o Dr. Gabriel</a>
        </div>
    </section>
        '''
    },
    {
        'filename': 'familia.html',
        'title': 'Direito de Família | Divórcio, Guarda e Pensão',
        'description': 'Atendimento humanizado em Direito de Família. Especialista em divórcio, pensão alimentícia, guarda e inventário.',
        'body': '''
    <section class="page-header">
        <h1>Soluções Humanizadas Para Momentos Delicados.</h1>
        <p>Em momentos de fragilidade, oferecemos suporte jurídico com empatia e expertise.</p>
    </section>
    <section class="content-section">
        <p>O Direito de Família lida com as relações mais íntimas e complexas da vida humana. Entendemos que cada caso é único e exige uma abordagem sensível, mas ao mesmo tempo estratégica, para proteger seus interesses e os de sua família. Nosso objetivo é buscar soluções que minimizem o desgaste emocional e garantam a melhor resolução possível.</p>
        <h2 style="margin-top: 40px;">Nossos Serviços Incluem:</h2>
        <ul style="margin-top: 20px; margin-left: 20px;">
            <li>**Divórcio Consensual e Litigioso:** Orientação completa para a dissolução do casamento, buscando acordos ou defendendo seus direitos em juízo.</li>
            <li>**Pensão Alimentícia:** Fixação, revisão ou exoneração de pensão para filhos e ex-cônjuges.</li>
            <li>**Guarda e Regulamentação de Visitas:** Definição da guarda dos filhos e do regime de convivência que melhor atenda ao interesse da criança.</li>
            <li>**Inventário e Partilha de Bens:** Condução do processo de sucessão, seja judicial ou extrajudicial, para a correta divisão do patrimônio.</li>
            <li>**Reconhecimento e Dissolução de União Estável:** Regularização ou término de uniões informais.</li>
            <li>**Adoção:** Assessoria jurídica em processos de adoção.</li>
        </ul>
        <div class="cta-box">
            <h3>Sua família merece a melhor proteção jurídica.</h3>
            <p>Fale conosco para uma análise detalhada e encontre a solução que você precisa.</p>
            <a href="https://wa.me/5547996756766" class="btn-cta">🟢 Receber Orientação</a>
        </div>
    </section>
        '''
    },
    {
        'filename': 'contrato.html',
        'title': 'Contratos | Elaboração e Revisão de Contratos',
        'description': 'Segurança jurídica para seus negócios. Elaboração e revisão de contratos de aluguel, compra e venda, prestação de serviços e mais.',
        'body': '''
    <section class="page-header">
        <h1>Segurança Jurídica em Cada Cláusula.</h1>
        <p>Proteja seus interesses com contratos claros, justos e legalmente sólidos.</p>
    </section>
    <section class="content-section">
        <p>Um contrato bem elaborado é a base para qualquer relação comercial ou pessoal segura. Ele previne conflitos, estabelece direitos e deveres e garante que as expectativas de todas as partes sejam atendidas. Oferecemos assessoria completa na elaboração, análise e revisão de contratos, assegurando que seus acordos estejam em conformidade com a legislação e protejam seus interesses.</p>
        <h2 style="margin-top: 40px;">Nossos Serviços Incluem:</h2>
        <ul style="margin-top: 20px; margin-left: 20px;">
            <li>**Elaboração de Contratos Personalizados:** Criamos documentos sob medida para suas necessidades, sejam eles de compra e venda, prestação de serviços, locação, entre outros.</li>
            <li>**Revisão de Contratos:** Analisamos contratos existentes para identificar cláusulas abusivas, riscos e oportunidades de melhoria.</li>
            <li>**Contratos de Aluguel:** Assessoria para locadores e locatários, garantindo um acordo equilibrado e seguro.</li>
            <li>**Contratos de Compra e Venda:** Segurança na aquisição ou alienação de bens móveis e imóveis.</li>
            <li>**Distratos e Rescisões Contratuais:** Orientação para o encerramento de contratos de forma legal e justa.</li>
            <li>**Análise de Contratos Bancários:** Identificação de juros abusivos e cláusulas ilegais.</li>
        </ul>
        <div class="cta-box">
            <h3>Precisa de segurança em seus acordos?</h3>
            <p>Entre em contato para elaborar ou revisar seu contrato com a expertise de um especialista.</p>
            <a href="https://wa.me/5547996756766" class="btn-cta">🟢 Analisar Meu Contrato</a>
        </div>
    </section>
        '''
    },
    {
        'filename': 'criminal.html',
        'title': 'Direito Criminal | Defesa Criminal Estratégica',
        'description': 'Defesa criminal técnica e estratégica. Acompanhamento em delegacias, audiências de custódia e processos criminais.',
        'body': '''
    <section class="page-header">
        <h1>Defesa Técnica e Estratégica em Matéria Criminal.</h1>
        <p>Garantindo seus direitos e a busca pela justiça em momentos críticos.</p>
    </section>
    <section class="content-section">
        <p>Em situações que envolvem o Direito Criminal, a agilidade e a expertise são fundamentais. Atuamos na defesa de indivíduos em todas as fases do processo, desde a investigação policial até o julgamento e recursos. Nosso compromisso é garantir a ampla defesa, o devido processo legal e a proteção dos direitos fundamentais de nossos clientes, buscando sempre a melhor estratégia para cada caso.</p>
        <h2 style="margin-top: 40px;">Nossos Serviços Incluem:</h2>
        <ul style="margin-top: 20px; margin-left: 20px;">
            <li>**Acompanhamento em Delegacia:** Suporte imediato em flagrantes e depoimentos.</li>
            <li>**Audiência de Custódia:** Atuação para garantir a legalidade da prisão e a liberdade provisória.</li>
            <li>**Defesa em Processos Criminais:** Representação em todas as instâncias, desde crimes de menor potencial ofensivo até crimes complexos.</li>
            <li>**Pedidos de Liberdade:** Habeas Corpus, relaxamento de prisão e revogação de preventiva.</li>
            <li>**Recursos Criminais:** Interposição de recursos para reverter decisões desfavoráveis.</li>
            <li>**Atuação em Inquéritos Policiais:** Defesa dos interesses do investigado durante a fase de investigação.</li>
        </ul>
        <div class="cta-box">
            <h3>Precisa de defesa criminal urgente?</h3>
            <p>Entre em contato imediatamente. A agilidade pode ser crucial para o seu caso.</p>
            <a href="https://wa.me/5547996756766" class="btn-cta">🟢 Falar com Advogado</a>
        </div>
    </section>
        '''
    },
    {
        'filename': 'trabalhista.html',
        'title': 'Direito Trabalhista | Especialista em Causas do Trabalho',
        'description': 'Advogado trabalhista especializado em rescisões, horas extras, assédio moral e reconhecimento de vínculo. Defenda seus direitos trabalhistas.',
        'body': '''
    <section class="page-header">
        <h1>Seus Direitos Trabalhistas Merecem Respeito.</h1>
        <p>Defendemos o trabalhador para garantir o cumprimento da lei e a justa reparação.</p>
    </section>
    <section class="content-section">
        <p>O Direito Trabalhista é a área que protege a relação entre empregados e empregadores. Se você se sente lesado em seus direitos, seja por demissão injusta, falta de pagamento de verbas, assédio ou qualquer outra irregularidade, estamos aqui para ajudar. Atuamos de forma estratégica para garantir que você receba tudo o que lhe é devido, buscando a reparação justa e o reconhecimento de seus direitos.</p>
        <h2 style="margin-top: 40px;">Problemas Atendidos:</h2>
        <ul style="margin-top: 20px; margin-left: 20px;">
            <li>**Demissão sem Justa Causa:** Cálculo e recebimento de todas as verbas rescisórias.</li>
            <li>**Verbas Rescisórias:** Férias, 13º salário, FGTS, seguro-desemprego não pagos.</li>
            <li>**Horas Extras:** Cobrança de horas trabalhadas além da jornada legal, incluindo adicionais noturnos e feriados.</li>
            <li>**Reconhecimento de Vínculo Empregatício:** Para trabalhadores sem carteira assinada.</li>
            <li>**Assédio Moral e Sexual:** Proteção e indenização por danos sofridos no ambiente de trabalho.</li>
            <li>**Acidente de Trabalho e Doenças Ocupacionais:** Busca por indenizações e benefícios previdenciários.</li>
            <li>**Reversão de Justa Causa:** Análise e defesa em casos de demissão por justa causa indevida.</li>
        </ul>
        <div class="cta-box">
            <h3>Precisa de ajuda com seus direitos trabalhistas?</h3>
            <p>Estou pronto para analisar seu caso e oferecer a melhor estratégia jurídica.</p>
            <a href="https://wa.me/5547996756766" class="btn-cta">🟢 Analisar Meu Caso</a>
        </div>
    </section>
        '''
    },
    {
        'filename': 'busca-e-apreensao.html',
        'title': 'Busca e Apreensão | Defesa em Ações de Veículos',
        'description': 'Defesa em ações de busca e apreensão de veículos. Revisão de contratos de financiamento e proteção do seu patrimônio.',
        'body': '''
    <section class="page-header">
        <h1>Proteja Seu Veículo de Busca e Apreensão Abusiva.</h1>
        <p>Atuação rápida e eficaz para evitar a perda do seu bem.</p>
    </section>
    <section class="content-section">
        <p>A ação de busca e apreensão de veículos é um processo delicado que exige atuação jurídica especializada e ágil. Se você está enfrentando essa situação, é crucial agir rapidamente para proteger seu patrimônio. Oferecemos defesa completa para reverter a apreensão, revisar contratos de financiamento com juros abusivos e buscar soluções que garantam a manutenção da posse do seu veículo.</p>
        <h2 style="margin-top: 40px;">Nossos Serviços Incluem:</h2>
        <ul style="margin-top: 20px; margin-left: 20px;">
            <li>**Defesa em Ação de Busca e Apreensão:** Medidas judiciais para suspender ou reverter a apreensão do veículo.</li>
            <li>**Revisão de Juros Abusivos:** Análise do contrato de financiamento para identificar e contestar cobranças indevidas.</li>
            <li>**Negociação de Dívidas de Financiamento:** Busca por acordos favoráveis para quitar o débito e evitar a perda do bem.</li>
            <li>**Liminares para Manutenção de Posse:** Ações urgentes para impedir a apreensão ou reaver o veículo.</li>
            <li>**Proteção do Patrimônio:** Estratégias para resguardar seus bens em situações de endividamento.</li>
            <li>**Consultoria Preventiva:** Orientação para evitar problemas com financiamentos e garantir a segurança do seu veículo.</li>
        </ul>
        <div class="cta-box">
            <h3>Seu veículo corre risco de busca e apreensão?</h3>
            <p>Não perca tempo! Entre em contato para uma análise urgente do seu caso.</p>
            <a href="https://wa.me/5547996756766" class="btn-cta">🟢 Proteger Meu Veículo</a>
        </div>
    </section>
        '''
    },
    {
        'filename': 'depoimentos.html',
        'title': 'Depoimentos | O que nossos clientes dizem',
        'description': 'Confira os depoimentos de quem já utilizou nossos serviços e comprove nosso compromisso com resultados.',
        'body': '''
    <section class="page-header">
        <h1>O Que Nossos Clientes Dizem</h1>
        <p>A satisfação de quem confia no nosso trabalho é o nosso maior prêmio.</p>
    </section>
    <section class="content-section">
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 30px;">
            <div style="background: var(--white); padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
                <div style="color: var(--accent-gold); margin-bottom: 15px;"><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i></div>
                <p style="font-style: italic; color: var(--text-muted);">"Excelente atendimento! O Dr. Gabriel foi muito atencioso e resolveu meu problema trabalhista com muita agilidade."</p>
                <p style="margin-top: 20px; font-weight: 700; color: var(--primary-blue);">— João Silva</p>
            </div>
            <div style="background: var(--white); padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
                <div style="color: var(--accent-gold); margin-bottom: 15px;"><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i></div>
                <p style="font-style: italic; color: var(--text-muted);">"Consegui minha aposentadoria graças ao planejamento previdenciário feito pelo escritório. Recomendo muito!"</p>
                <p style="margin-top: 20px; font-weight: 700; color: var(--primary-blue);">— Maria Oliveira</p>
            </div>
            <div style="background: var(--white); padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
                <div style="color: var(--accent-gold); margin-bottom: 15px;"><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i></div>
                <p style="font-style: italic; color: var(--text-muted);">"Atendimento transparente e direto. Me senti segura durante todo o processo do meu divórcio."</p>
                <p style="margin-top: 20px; font-weight: 700; color: var(--primary-blue);">— Ana Santos</p>
            </div>
        </div>
        <div class="cta-box">
            <h3>Quer ser nosso próximo caso de sucesso?</h3>
            <p>Fale conosco agora e receba uma avaliação inicial.</p>
            <a href="https://wa.me/5547996756766" class="btn-cta">🟢 Iniciar Atendimento</a>
        </div>
    </section>
        '''
    },
    {
        'filename': 'contato.html',
        'title': 'Contato | Fale com o Dr. Gabriel Corrêa',
        'description': 'Entre em contato para uma avaliação jurídica. Atendimento ágil via WhatsApp, e-mail ou formulário.',
        'body': '''
    <section class="page-header">
        <h1>Fale Conosco</h1>
        <p>Estamos prontos para atender você com agilidade e transparência.</p>
    </section>
    <section class="content-section">
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 40px;">
            <div>
                <h2 style="color: var(--primary-blue); margin-bottom: 20px;">Canais de Atendimento</h2>
                <div style="margin-bottom: 20px;">
                    <p style="font-weight: 700; color: var(--primary-blue);"><i class="fab fa-whatsapp" style="color: var(--whatsapp-green); margin-right: 10px;"></i> WhatsApp</p>
                    <p><a href="https://wa.me/5547996756766" style="color: var(--text-dark); text-decoration: none;">(47) 99675-6766</a></p>
                </div>
                <div style="margin-bottom: 20px;">
                    <p style="font-weight: 700; color: var(--primary-blue);"><i class="fas fa-envelope" style="color: var(--accent-gold); margin-right: 10px;"></i> E-mail</p>
                    <p><a href="mailto:escritorio.gabrielcorrea@gmail.com" style="color: var(--text-dark); text-decoration: none;">escritorio.gabrielcorrea@gmail.com</a></p>
                </div>
                <div style="margin-bottom: 20px;">
                    <p style="font-weight: 700; color: var(--primary-blue);"><i class="fas fa-clock" style="color: var(--accent-gold); margin-right: 10px;"></i> Horário de Atendimento</p>
                    <p>Segunda a Sexta: 08h às 18h</p>
                    <p>Atendimento Online 24h</p>
                </div>
            </div>
            <div style="background: var(--white); padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
                <h3 style="color: var(--primary-blue); margin-bottom: 20px;">Envie uma Mensagem</h3>
                <form onsubmit="window.location.href='https://wa.me/5547996756766?text=' + encodeURIComponent('Olá, gostaria de uma avaliação para o meu caso.'); return false;">
                    <div style="margin-bottom: 15px;">
                        <input type="text" placeholder="Seu Nome" style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 5px;" required>
                    </div>
                    <div style="margin-bottom: 15px;">
                        <input type="tel" placeholder="Seu WhatsApp" style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 5px;" required>
                    </div>
                    <div style="margin-bottom: 15px;">
                        <textarea placeholder="Descreva brevemente seu caso" style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 5px; height: 100px;" required></textarea>
                    </div>
                    <button type="submit" style="width: 100%; background: var(--whatsapp-green); color: white; border: none; padding: 15px; border-radius: 5px; font-weight: 700; cursor: pointer;">Enviar pelo WhatsApp</button>
                </form>
            </div>
        </div>
    </section>
        '''
    }
]

for page in pages:
    content = template.replace('{{TITLE}}', page['title'])
    content = content.replace('{{DESCRIPTION}}', page['description'])
    content = content.replace('{{FILENAME}}', page['filename'])
    content = content.replace('{{BODY}}', page['body'])
    
    with open(page['filename'], 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Generated {page['filename']}")
