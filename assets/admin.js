/**
 * ADMIN PANEL - Painel Administrativo do Chat Widget
 * Acesso por URL secreta
 */

class AdminPanel {
    constructor() {
        this.secretUrl = this.generateSecretUrl();
        this.verifyAccess();
        this.init();
    }

    /**
     * Gerar URL secreta
     */
    generateSecretUrl() {
        const stored = localStorage.getItem('adminSecretUrl');
        if (stored) return stored;

        const randomId = Math.random().toString(36).substring(2, 15) + 
                        Math.random().toString(36).substring(2, 15);
        const secret = `admin-${randomId}`;
        localStorage.setItem('adminSecretUrl', secret);
        return secret;
    }

    /**
     * Verificar acesso ao painel
     */
    verifyAccess() {
        const currentPath = window.location.pathname;
        const currentHash = window.location.hash.substring(1);
        const storedSecret = localStorage.getItem('adminSecretUrl');

        // Se não há chave armazenada, permitir primeiro acesso (criar chave)
        if (!storedSecret) {
            return true;
        }

        // Se há chave armazenada, verificar se está na URL
        if (!currentPath.includes('admin.html')) {
            this.showAccessDenied();
            return false;
        }

        return true;
    }

    /**
     * Mostrar página de acesso negado
     */
    showAccessDenied() {
        document.body.innerHTML = `
            <div style="display: flex; align-items: center; justify-content: center; min-height: 100vh; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); font-family: Inter, sans-serif;">
                <div style="background: white; padding: 40px; border-radius: 15px; text-align: center; box-shadow: 0 20px 60px rgba(0,0,0,0.3);">
                    <i class="fas fa-lock" style="font-size: 3rem; color: #e74c3c; margin-bottom: 20px;"></i>
                    <h1 style="color: #172B41; margin-bottom: 10px;">Acesso Negado</h1>
                    <p style="color: #666; margin-bottom: 20px;">Você não tem permissão para acessar este painel.</p>
                    <a href="/" style="color: #25D366; text-decoration: none; font-weight: 600;">Voltar para o site</a>
                </div>
            </div>
        `;
    }

    /**
     * Inicializar painel
     */
    init() {
        this.loadConfig();
        this.setupNavigation();
        this.setupForms();
        this.loadDashboard();
        this.loadMessages();
        this.loadFlowSteps();
        this.loadLeads();
        this.updateAdminUrl();
    }

    /**
     * Carregar configurações
     */
    loadConfig() {
        const config = JSON.parse(localStorage.getItem('chatWidgetConfig') || '{}');
        
        // Preencher formulário de configurações
        document.getElementById('businessName').value = config.businessName || '';
        document.getElementById('whatsapp').value = config.whatsapp || '';
        document.getElementById('primaryColor').value = config.primaryColor || '#172B41';
        document.getElementById('accentColor').value = config.accentColor || '#C9A961';
        document.getElementById('mode').value = config.mode || 'flow';
        document.getElementById('autoOpenDelay').value = config.autoOpenDelay || 5000;
        document.getElementById('socialProof').value = config.socialProof || '';

        // Preencher IA
        document.getElementById('apiKey').value = config.apiKey || '';
        document.getElementById('systemPrompt').value = config.systemPrompt || '';
        document.getElementById('model').value = config.model || 'gpt-3.5-turbo';
        document.getElementById('temperature').value = config.temperature || 0.7;

        // Atualizar hex colors
        this.updateColorHex('primaryColor');
        this.updateColorHex('accentColor');
    }

    /**
     * Atualizar hex color
     */
    updateColorHex(inputId) {
        const input = document.getElementById(inputId);
        const hexInput = document.getElementById(inputId + 'Hex');
        if (hexInput) {
            hexInput.value = input.value;
        }
    }

    /**
     * Configurar navegação
     */
    setupNavigation() {
        const navItems = document.querySelectorAll('.admin-nav-item');
        navItems.forEach(item => {
            item.addEventListener('click', () => {
                const section = item.getAttribute('data-section');
                this.switchSection(section);
            });
        });
    }

    /**
     * Alternar seção
     */
    switchSection(sectionId) {
        // Remover active de todas as seções
        document.querySelectorAll('.admin-section').forEach(s => {
            s.classList.remove('active');
        });
        document.querySelectorAll('.admin-nav-item').forEach(n => {
            n.classList.remove('active');
        });

        // Ativar seção selecionada
        document.getElementById(sectionId).classList.add('active');
        document.querySelector(`[data-section="${sectionId}"]`).classList.add('active');

        // Recarregar dados se necessário
        if (sectionId === 'leads') this.loadLeads();
        if (sectionId === 'messages') this.loadMessages();
        if (sectionId === 'flow') this.loadFlowSteps();
    }

    /**
     * Configurar formulários
     */
    setupForms() {
        // Formulário de configurações
        document.getElementById('settingsForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.saveSettings();
        });

        // Formulário de IA
        document.getElementById('iaForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.saveIASettings();
        });

        // Formulário de mensagem
        document.getElementById('addMessageForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.addMessage();
        });

        // Formulário de fluxo
        document.getElementById('addFlowStepForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.addFlowStep();
        });

        // Color pickers
        document.getElementById('primaryColor').addEventListener('change', () => {
            this.updateColorHex('primaryColor');
        });
        document.getElementById('accentColor').addEventListener('change', () => {
            this.updateColorHex('accentColor');
        });
    }

    /**
     * Salvar configurações
     */
    saveSettings() {
        const config = JSON.parse(localStorage.getItem('chatWidgetConfig') || '{}');
        
        config.businessName = document.getElementById('businessName').value;
        config.whatsapp = document.getElementById('whatsapp').value;
        config.primaryColor = document.getElementById('primaryColor').value;
        config.accentColor = document.getElementById('accentColor').value;
        config.mode = document.getElementById('mode').value;
        config.autoOpenDelay = parseInt(document.getElementById('autoOpenDelay').value);
        config.socialProof = document.getElementById('socialProof').value;

        localStorage.setItem('chatWidgetConfig', JSON.stringify(config));
        this.showSuccessMessage();
    }

    /**
     * Salvar configurações de IA
     */
    saveIASettings() {
        const config = JSON.parse(localStorage.getItem('chatWidgetConfig') || '{}');
        
        config.apiKey = document.getElementById('apiKey').value;
        config.systemPrompt = document.getElementById('systemPrompt').value;
        config.model = document.getElementById('model').value;
        config.temperature = parseFloat(document.getElementById('temperature').value);

        localStorage.setItem('chatWidgetConfig', JSON.stringify(config));
        this.showSuccessMessage();
    }

    /**
     * Mostrar mensagem de sucesso
     */
    showSuccessMessage() {
        const msg = document.getElementById('successMessage');
        msg.classList.add('show');
        setTimeout(() => msg.classList.remove('show'), 3000);
    }

    /**
     * Carregar dashboard
     */
    loadDashboard() {
        const leads = JSON.parse(localStorage.getItem('chatWidgetLeads') || '[]');
        const convertidos = leads.filter(l => l.status === 'convertido').length;
        
        document.getElementById('leadsCount').textContent = leads.length;
        document.getElementById('conversionsCount').textContent = convertidos;
    }

    /**
     * Atualizar URL do painel
     */
    updateAdminUrl() {
        const baseUrl = window.location.origin + window.location.pathname.split('/admin')[0];
        const adminUrl = `${baseUrl}/admin.html#${this.secretUrl}`;
        document.getElementById('adminUrl').value = adminUrl;
    }

    /**
     * Copiar URL do painel
     */
    copyAdminUrl() {
        const url = document.getElementById('adminUrl');
        url.select();
        document.execCommand('copy');
        alert('URL copiada para a área de transferência!');
    }

    /**
     * Gerar nova URL secreta
     */
    generateNewSecretUrl() {
        if (confirm('Tem certeza? A URL anterior deixará de funcionar.')) {
            localStorage.removeItem('adminSecretUrl');
            this.secretUrl = this.generateSecretUrl();
            this.updateAdminUrl();
            this.showSuccessMessage();
        }
    }

    /**
     * Adicionar mensagem por página
     */
    addMessage() {
        const config = JSON.parse(localStorage.getItem('chatWidgetConfig') || '{}');
        const page = document.getElementById('messagePage').value;
        const message = document.getElementById('messageText').value;

        if (!config.pageMessages) config.pageMessages = {};
        config.pageMessages[page] = message;

        localStorage.setItem('chatWidgetConfig', JSON.stringify(config));
        this.closeModal('addMessageModal');
        this.loadMessages();
        this.showSuccessMessage();
    }

    /**
     * Carregar mensagens
     */
    loadMessages() {
        const config = JSON.parse(localStorage.getItem('chatWidgetConfig') || '{}');
        const messages = config.pageMessages || {};
        const tbody = document.getElementById('messagesTableBody');
        tbody.innerHTML = '';

        Object.entries(messages).forEach(([page, message]) => {
            const row = `
                <tr>
                    <td><strong>${page}</strong></td>
                    <td>${message.substring(0, 50)}...</td>
                    <td>
                        <button class="btn btn-secondary btn-small" onclick="adminPanel.editMessage('${page}')">
                            <i class="fas fa-edit"></i> Editar
                        </button>
                        <button class="btn btn-danger btn-small" onclick="adminPanel.deleteMessage('${page}')">
                            <i class="fas fa-trash"></i> Deletar
                        </button>
                    </td>
                </tr>
            `;
            tbody.insertAdjacentHTML('beforeend', row);
        });
    }

    /**
     * Deletar mensagem
     */
    deleteMessage(page) {
        if (confirm('Tem certeza que deseja deletar esta mensagem?')) {
            const config = JSON.parse(localStorage.getItem('chatWidgetConfig') || '{}');
            delete config.pageMessages[page];
            localStorage.setItem('chatWidgetConfig', JSON.stringify(config));
            this.loadMessages();
        }
    }

    /**
     * Adicionar etapa do fluxo
     */
    addFlowStep() {
        const config = JSON.parse(localStorage.getItem('chatWidgetConfig') || '{}');
        if (!config.flowSteps) config.flowSteps = [];

        const type = document.getElementById('flowStepType').value;
        const content = document.getElementById('flowStepContent').value;

        const step = {
            type: type,
            text: content,
            label: type === 'input' ? content : undefined,
            key: type === 'input' ? `field_${Date.now()}` : undefined
        };

        config.flowSteps.push(step);
        localStorage.setItem('chatWidgetConfig', JSON.stringify(config));
        this.closeModal('addFlowStepModal');
        this.loadFlowSteps();
        this.showSuccessMessage();
    }

    /**
     * Carregar etapas do fluxo
     */
    loadFlowSteps() {
        const config = JSON.parse(localStorage.getItem('chatWidgetConfig') || '{}');
        const steps = config.flowSteps || [];
        const container = document.getElementById('flowStepsContainer');
        container.innerHTML = '';

        steps.forEach((step, index) => {
            const stepHTML = `
                <div class="flow-step">
                    <div class="flow-step-content">
                        <div class="flow-step-type">${step.type}</div>
                        <div class="flow-step-text">${step.text || step.label}</div>
                    </div>
                    <button class="btn btn-danger btn-small" onclick="adminPanel.deleteFlowStep(${index})">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            `;
            container.insertAdjacentHTML('beforeend', stepHTML);
        });
    }

    /**
     * Deletar etapa do fluxo
     */
    deleteFlowStep(index) {
        if (confirm('Tem certeza que deseja deletar esta etapa?')) {
            const config = JSON.parse(localStorage.getItem('chatWidgetConfig') || '{}');
            config.flowSteps.splice(index, 1);
            localStorage.setItem('chatWidgetConfig', JSON.stringify(config));
            this.loadFlowSteps();
        }
    }

    /**
     * Carregar leads
     */
    loadLeads() {
        const leads = JSON.parse(localStorage.getItem('chatWidgetLeads') || '[]');
        const tbody = document.getElementById('leadsTableBody');
        tbody.innerHTML = '';

        leads.forEach(lead => {
            const date = new Date(lead.timestamp).toLocaleDateString('pt-BR');
            const statusBadge = `<span class="status-badge status-${lead.status}">${lead.status}</span>`;
            
            const row = `
                <tr>
                    <td><strong>${lead.name || 'Não informado'}</strong></td>
                    <td>${lead.area || 'Não informado'}</td>
                    <td>${lead.phone || 'Não informado'}</td>
                    <td>${date}</td>
                    <td>${statusBadge}</td>
                    <td>
                        <button class="btn btn-secondary btn-small" onclick="adminPanel.viewLead(${lead.id})">
                            <i class="fas fa-eye"></i> Ver
                        </button>
                    </td>
                </tr>
            `;
            tbody.insertAdjacentHTML('beforeend', row);
        });
    }

    /**
     * Exportar leads em CSV
     */
    exportLeadsCSV() {
        const leads = JSON.parse(localStorage.getItem('chatWidgetLeads') || '[]');
        
        const headers = ['Nome', 'Área', 'Telefone', 'E-mail', 'Descrição', 'Data', 'Status'];
        const rows = leads.map(lead => [
            lead.name || '',
            lead.area || '',
            lead.phone || '',
            lead.email || '',
            lead.description || '',
            new Date(lead.timestamp).toLocaleDateString('pt-BR'),
            lead.status || ''
        ]);

        let csv = headers.join(',') + '\n';
        rows.forEach(row => {
            csv += row.map(cell => `"${cell}"`).join(',') + '\n';
        });

        const blob = new Blob([csv], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `leads_${new Date().toISOString().split('T')[0]}.csv`;
        a.click();
    }

    /**
     * Limpar todos os dados
     */
    clearAllData() {
        if (confirm('ATENÇÃO: Isto irá deletar TODOS os dados. Tem certeza?')) {
            if (confirm('Esta ação é irreversível. Tem certeza mesmo?')) {
                localStorage.clear();
                sessionStorage.clear();
                alert('Todos os dados foram limpos.');
                location.reload();
            }
        }
    }
}

// Funções globais para modais
function openAddMessageModal() {
    document.getElementById('addMessageModal').classList.add('show');
}

function openAddFlowStepModal() {
    document.getElementById('addFlowStepModal').classList.add('show');
}

function closeModal(modalId) {
    document.getElementById(modalId).classList.remove('show');
}

// Fechar modal ao clicar fora
document.addEventListener('click', (e) => {
    if (e.target.classList.contains('modal')) {
        e.target.classList.remove('show');
    }
});

// Inicializar painel
let adminPanel;
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        adminPanel = new AdminPanel();
        window.adminPanel = adminPanel;
    });
} else {
    adminPanel = new AdminPanel();
    window.adminPanel = adminPanel;
}

// Funções globais
function copyAdminUrl() {
    adminPanel.copyAdminUrl();
}

function generateNewSecretUrl() {
    adminPanel.generateNewSecretUrl();
}

function clearAllData() {
    adminPanel.clearAllData();
}

function exportLeadsCSV() {
    adminPanel.exportLeadsCSV();
}
