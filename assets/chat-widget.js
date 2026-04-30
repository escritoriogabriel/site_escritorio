/**
 * CHAT WIDGET - Sistema de Atendimento Inteligente
 * Compatível com GitHub Pages (localStorage)
 * Sem dependências externas obrigatórias
 */

class ChatWidget {
    constructor() {
        this.config = this.loadConfig();
        this.isOpen = false;
        this.conversationHistory = [];
        this.currentFlowStep = 0;
        this.flowData = {};
        this.mode = this.config.mode || 'flow'; // 'flow' ou 'ia'
        this.init();
    }

    /**
     * Carregar configurações do localStorage
     */
    loadConfig() {
        const defaultConfig = {
            businessName: 'Advogado Gabriel Corrêa',
            whatsapp: '5547988670233',
            primaryColor: '#172B41',
            accentColor: '#C9A961',
            mode: 'flow', // 'flow' ou 'ia'
            apiKey: '',
            systemPrompt: 'Você é um assistente jurídico profissional e amigável.',
            temperature: 0.7,
            model: 'gpt-3.5-turbo',
            autoOpenDelay: 5000,
            pageMessages: {
                '/': 'Olá! Precisa de auxílio jurídico? Nossa equipe está pronta para ajudar.',
                '/sobre.html': 'Conheça melhor nosso trabalho. Tem alguma dúvida?',
                '/previdenciario.html': 'Quer revisar sua aposentadoria ou benefícios? Podemos ajudar.',
                '/trabalhista.html': 'Teve seus direitos trabalhistas violados? Converse conosco.',
                '/civil.html': 'Precisa de orientação em direito civil? Fale conosco.',
                '/familia.html': 'Está enfrentando questões familiares? Fale agora com um especialista.',
                '/consumidor.html': 'Sofreu cobrança indevida? Podemos ajudar a resolver.',
                '/empresarial.html': 'Precisa de consultoria jurídica empresarial? Vamos conversar.',
                '/contato.html': 'Pronto para dar o próximo passo? Fale conosco agora.'
            },
            flowSteps: [
                { type: 'message', text: 'Olá! Bem-vindo ao atendimento do Advogado Gabriel Corrêa. Como posso ajudar?' },
                { type: 'input', label: 'Qual é seu nome?', key: 'name', required: true },
                { type: 'input', label: 'Qual é sua área de interesse?', key: 'area', required: true },
                { type: 'input', label: 'Descreva brevemente seu caso:', key: 'description', required: true },
                { type: 'input', label: 'Qual é seu WhatsApp?', key: 'phone', required: true },
                { type: 'message', text: 'Perfeito! Vamos conectar você com nosso advogado agora.' }
            ],
            socialProof: 'Mais de 500 clientes já confiaram em nosso trabalho.'
        };

        const saved = localStorage.getItem('chatWidgetConfig');
        return saved ? { ...defaultConfig, ...JSON.parse(saved) } : defaultConfig;
    }

    /**
     * Salvar configurações no localStorage
     */
    saveConfig() {
        localStorage.setItem('chatWidgetConfig', JSON.stringify(this.config));
    }

    /**
     * Inicializar o widget
     */
    init() {
        this.createWidgetHTML();
        this.attachEventListeners();
        this.scheduleAutoOpen();
        this.loadConversationHistory();
    }

    /**
     * Criar HTML do widget
     */
    createWidgetHTML() {
        const widgetHTML = `
            <button class="chat-widget-button" id="chatWidgetBtn" aria-label="Abrir chat">
                <i class="fab fa-whatsapp"></i>
            </button>

            <div class="chat-invite" id="chatInvite">
                <button class="chat-invite-close" id="closeInvite">&times;</button>
                <div class="chat-invite-title">Podemos ajudar?</div>
                <div class="chat-invite-text">${this.config.socialProof}</div>
                <button class="chat-invite-button" id="acceptInvite">Falar Agora</button>
            </div>

            <div class="chat-widget-container" id="chatContainer">
                <div class="chat-widget-header">
                    <div>
                        <h3>${this.config.businessName}</h3>
                        <div class="status">
                            <span class="status-dot"></span>
                            Online agora
                        </div>
                    </div>
                    <button class="chat-widget-close" id="closeChat" aria-label="Fechar chat">
                        <i class="fas fa-times"></i>
                    </button>
                </div>

                <div class="chat-widget-messages" id="chatMessages"></div>

                <div class="chat-widget-input-area" id="chatInputArea">
                    <input type="text" class="chat-widget-input" id="chatInput" placeholder="Digite sua mensagem..." />
                    <button class="chat-widget-send" id="chatSendBtn" aria-label="Enviar">
                        <i class="fas fa-paper-plane"></i>
                    </button>
                </div>
            </div>
        `;

        const container = document.createElement('div');
        container.id = 'chatWidgetRoot';
        container.innerHTML = widgetHTML;
        document.body.appendChild(container);

        // Injetar CSS se não existir
        if (!document.getElementById('chatWidgetStyles')) {
            const link = document.createElement('link');
            link.id = 'chatWidgetStyles';
            link.rel = 'stylesheet';
            link.href = '/assets/chat-widget.css';
            document.head.appendChild(link);
        }
    }

    /**
     * Anexar event listeners
     */
    attachEventListeners() {
        const chatBtn = document.getElementById('chatWidgetBtn');
        const closeBtn = document.getElementById('closeChat');
        const sendBtn = document.getElementById('chatSendBtn');
        const input = document.getElementById('chatInput');
        const closeInvite = document.getElementById('closeInvite');
        const acceptInvite = document.getElementById('acceptInvite');

        chatBtn?.addEventListener('click', () => this.toggleChat());
        closeBtn?.addEventListener('click', () => this.closeChat());
        sendBtn?.addEventListener('click', () => this.sendMessage());
        input?.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        closeInvite?.addEventListener('click', () => this.closeInvite());
        acceptInvite?.addEventListener('click', () => this.openChat());

        // Detectar intenção de saída (anti-abandono)
        document.addEventListener('mouseleave', () => this.showExitIntent());
    }

    /**
     * Alternar abertura/fechamento do chat
     */
    toggleChat() {
        if (this.isOpen) {
            this.closeChat();
        } else {
            this.openChat();
        }
    }

    /**
     * Abrir chat
     */
    openChat() {
        this.isOpen = true;
        const container = document.getElementById('chatContainer');
        container?.classList.add('open');
        document.getElementById('chatInvite')?.classList.remove('show');
        document.getElementById('chatInput')?.focus();

        // Se é a primeira vez, iniciar fluxo
        if (this.conversationHistory.length === 0) {
            this.startFlow();
        }
    }

    /**
     * Fechar chat
     */
    closeChat() {
        this.isOpen = false;
        const container = document.getElementById('chatContainer');
        container?.classList.remove('open');
    }

    /**
     * Fechar convite
     */
    closeInvite() {
        document.getElementById('chatInvite')?.classList.remove('show');
        sessionStorage.setItem('chatInviteClosed', 'true');
    }

    /**
     * Agendar abertura automática
     */
    scheduleAutoOpen() {
        if (sessionStorage.getItem('chatOpened')) return;

        setTimeout(() => {
            if (!this.isOpen && !sessionStorage.getItem('chatInviteClosed')) {
                this.showInvite();
            }
        }, this.config.autoOpenDelay);
    }

    /**
     * Mostrar convite
     */
    showInvite() {
        const invite = document.getElementById('chatInvite');
        if (invite) {
            invite.classList.add('show');
        }
    }

    /**
     * Detectar intenção de saída
     */
    showExitIntent() {
        if (!this.isOpen && !sessionStorage.getItem('exitIntentShown')) {
            setTimeout(() => {
                if (!this.isOpen) {
                    this.showInvite();
                    sessionStorage.setItem('exitIntentShown', 'true');
                }
            }, 2000);
        }
    }

    /**
     * Iniciar fluxo de conversa
     */
    startFlow() {
        this.currentFlowStep = 0;
        this.flowData = {};
        this.showFlowStep();
    }

    /**
     * Mostrar etapa do fluxo
     */
    showFlowStep() {
        const step = this.config.flowSteps[this.currentFlowStep];
        if (!step) {
            this.finishFlow();
            return;
        }

        if (step.type === 'message') {
            this.addBotMessage(step.text);
            this.currentFlowStep++;
            setTimeout(() => this.showFlowStep(), 1000);
        } else if (step.type === 'input') {
            this.showInputBlock(step);
        }
    }

    /**
     * Mostrar bloco de input
     */
    showInputBlock(step) {
        const messagesDiv = document.getElementById('chatMessages');
        const blockHTML = `
            <div class="chat-message bot">
                <div class="chat-message-content">
                    <div class="chat-flow-block">
                        <label class="chat-flow-label">${step.label}</label>
                        <input type="text" class="chat-flow-input" id="flowInput" placeholder="Digite aqui..." data-key="${step.key}" />
                    </div>
                </div>
            </div>
        `;
        messagesDiv?.insertAdjacentHTML('beforeend', blockHTML);
        messagesDiv?.scrollTop = messagesDiv?.scrollHeight;

        const input = document.getElementById('flowInput');
        input?.focus();
        input?.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                const value = input.value.trim();
                if (value) {
                    this.flowData[step.key] = value;
                    this.addUserMessage(value);
                    this.currentFlowStep++;
                    setTimeout(() => this.showFlowStep(), 500);
                }
            }
        });
    }

    /**
     * Finalizar fluxo e enviar para WhatsApp
     */
    finishFlow() {
        this.addBotMessage('Perfeito! Vou conectar você com nosso advogado agora.');
        
        // Capturar lead
        this.captureLead(this.flowData);

        // Montar mensagem para WhatsApp
        let message = `Olá! Gostaria de uma orientação jurídica.\n\n`;
        message += `*Nome:* ${this.flowData.name || 'Não informado'}\n`;
        message += `*Área:* ${this.flowData.area || 'Não informado'}\n`;
        message += `*Caso:* ${this.flowData.description || 'Não informado'}\n`;

        const encodedMessage = encodeURIComponent(message);
        const whatsappURL = `https://wa.me/${this.config.whatsapp}?text=${encodedMessage}`;

        setTimeout(() => {
            this.addBotMessage(`Clique abaixo para continuar no WhatsApp:`);
            const messagesDiv = document.getElementById('chatMessages');
            const buttonHTML = `
                <div class="chat-message bot">
                    <div class="chat-message-content">
                        <a href="${whatsappURL}" target="_blank" class="chat-flow-button primary" style="text-decoration: none; display: block;">
                            <i class="fab fa-whatsapp"></i> Continuar no WhatsApp
                        </a>
                    </div>
                </div>
            `;
            messagesDiv?.insertAdjacentHTML('beforeend', buttonHTML);
            messagesDiv?.scrollTop = messagesDiv?.scrollHeight;
        }, 1500);
    }

    /**
     * Capturar lead
     */
    captureLead(data) {
        const leads = JSON.parse(localStorage.getItem('chatWidgetLeads') || '[]');
        const lead = {
            id: Date.now(),
            timestamp: new Date().toISOString(),
            page: window.location.pathname,
            ...data,
            status: 'novo'
        };
        leads.push(lead);
        localStorage.setItem('chatWidgetLeads', JSON.stringify(leads));
    }

    /**
     * Enviar mensagem (modo IA)
     */
    async sendMessage() {
        const input = document.getElementById('chatInput');
        const message = input?.value.trim();

        if (!message) return;

        this.addUserMessage(message);
        input.value = '';

        if (this.mode === 'ia' && this.config.apiKey) {
            await this.sendToAI(message);
        } else {
            this.addBotMessage('Obrigado pela sua mensagem. Nossa equipe retornará em breve!');
        }
    }

    /**
     * Enviar para IA (OpenAI)
     */
    async sendToAI(message) {
        this.showTypingIndicator();

        try {
            const response = await fetch('https://api.openai.com/v1/chat/completions', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.config.apiKey}`
                },
                body: JSON.stringify({
                    model: this.config.model,
                    messages: [
                        { role: 'system', content: this.config.systemPrompt },
                        ...this.conversationHistory.map(msg => ({
                            role: msg.sender === 'user' ? 'user' : 'assistant',
                            content: msg.text
                        })),
                        { role: 'user', content: message }
                    ],
                    temperature: this.config.temperature,
                    max_tokens: 500
                })
            });

            if (!response.ok) {
                throw new Error('Erro na API');
            }

            const data = await response.json();
            const botMessage = data.choices[0].message.content;

            this.removeTypingIndicator();
            this.addBotMessage(botMessage);
        } catch (error) {
            console.error('Erro ao chamar IA:', error);
            this.removeTypingIndicator();
            this.addBotMessage('Desculpe, ocorreu um erro. Tente novamente.');
        }
    }

    /**
     * Adicionar mensagem do usuário
     */
    addUserMessage(text) {
        this.conversationHistory.push({ sender: 'user', text, timestamp: new Date() });
        const messagesDiv = document.getElementById('chatMessages');
        const messageHTML = `
            <div class="chat-message user">
                <div class="chat-message-content">${this.escapeHTML(text)}</div>
                <div class="chat-message-avatar user">Você</div>
            </div>
        `;
        messagesDiv?.insertAdjacentHTML('beforeend', messageHTML);
        messagesDiv?.scrollTop = messagesDiv?.scrollHeight;
        this.saveConversationHistory();
    }

    /**
     * Adicionar mensagem do bot
     */
    addBotMessage(text) {
        this.conversationHistory.push({ sender: 'bot', text, timestamp: new Date() });
        const messagesDiv = document.getElementById('chatMessages');
        const messageHTML = `
            <div class="chat-message bot">
                <div class="chat-message-avatar">
                    <i class="fas fa-robot"></i>
                </div>
                <div class="chat-message-content">${this.escapeHTML(text)}</div>
            </div>
        `;
        messagesDiv?.insertAdjacentHTML('beforeend', messageHTML);
        messagesDiv?.scrollTop = messagesDiv?.scrollHeight;
        this.saveConversationHistory();
    }

    /**
     * Mostrar indicador de digitação
     */
    showTypingIndicator() {
        const messagesDiv = document.getElementById('chatMessages');
        const typingHTML = `
            <div class="chat-message bot" id="typingIndicator">
                <div class="chat-message-avatar">
                    <i class="fas fa-robot"></i>
                </div>
                <div class="chat-message-typing">
                    <span></span><span></span><span></span>
                </div>
            </div>
        `;
        messagesDiv?.insertAdjacentHTML('beforeend', typingHTML);
        messagesDiv?.scrollTop = messagesDiv?.scrollHeight;
    }

    /**
     * Remover indicador de digitação
     */
    removeTypingIndicator() {
        document.getElementById('typingIndicator')?.remove();
    }

    /**
     * Salvar histórico de conversa
     */
    saveConversationHistory() {
        const sessionHistory = this.conversationHistory.map(msg => ({
            ...msg,
            timestamp: msg.timestamp.toISOString()
        }));
        sessionStorage.setItem('chatHistory', JSON.stringify(sessionHistory));
    }

    /**
     * Carregar histórico de conversa
     */
    loadConversationHistory() {
        const saved = sessionStorage.getItem('chatHistory');
        if (saved) {
            this.conversationHistory = JSON.parse(saved).map(msg => ({
                ...msg,
                timestamp: new Date(msg.timestamp)
            }));
        }
    }

    /**
     * Escapar HTML para prevenir XSS
     */
    escapeHTML(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    /**
     * Obter mensagem da página atual
     */
    getPageMessage() {
        const currentPath = window.location.pathname;
        for (const [path, message] of Object.entries(this.config.pageMessages)) {
            if (currentPath.includes(path) || currentPath === path) {
                return message;
            }
        }
        return this.config.pageMessages['/'];
    }
}

// Inicializar widget quando DOM estiver pronto
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.chatWidget = new ChatWidget();
    });
} else {
    window.chatWidget = new ChatWidget();
}
