// Estado global da aplicação
let currentCampanha = null;
let currentPersonagem = null;

// Inicialização da aplicação
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    setupNavigation();
    loadCampanhas();
    setupForms();
}

// Configuração da navegação
function setupNavigation() {
    const navButtons = document.querySelectorAll('.nav-btn');
    navButtons.forEach(button => {
        button.addEventListener('click', function() {
            const section = this.dataset.section;
            showSection(section);
            
            // Atualizar botão ativo
            navButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
        });
    });
}

function showSection(sectionName) {
    // Esconder todas as seções
    const sections = document.querySelectorAll('.content-section');
    sections.forEach(section => section.classList.remove('active'));
    
    // Mostrar seção selecionada
    const targetSection = document.getElementById(sectionName);
    if (targetSection) {
        targetSection.classList.add('active');
        
        // Carregar dados específicos da seção
        switch(sectionName) {
            case 'campanhas':
                loadCampanhas();
                break;
            case 'personagens':
                loadPersonagens();
                break;
            case 'itens':
                loadItens();
                break;
            case 'missoes':
                loadMissoes();
                break;
            case 'npcs':
                loadNPCs();
                break;
            case 'historico':
                loadHistorico();
                break;
        }
    }
}

// Funções de modal
function showModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'block';
        
        // Carregar dados necessários para o modal
        if (modalId === 'personagemModal') {
            loadCampanhasSelect('campanhaPersonagem');
        }
    }
}

function hideModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'none';
        
        // Limpar formulário
        const form = modal.querySelector('form');
        if (form) {
            form.reset();
            // Limpar campos hidden
            const hiddenInputs = form.querySelectorAll('input[type="hidden"]');
            hiddenInputs.forEach(input => input.value = '');
        }
    }
}

// Configuração dos formulários
function setupForms() {
    // Formulário de campanhas
    const campanhaForm = document.getElementById('campanhaForm');
    if (campanhaForm) {
        campanhaForm.addEventListener('submit', handleCampanhaSubmit);
    }
}

// Handlers dos formulários
async function handleCampanhaSubmit(e) {
    e.preventDefault();
    
    const campanhaId = document.getElementById('campanhaId').value;
    const nomeCampanha = document.getElementById('nomeCampanha').value;
    const nomeMestre = document.getElementById('nomeMestre').value;
    
    const data = {
        nome_campanha: nomeCampanha,
        nome_mestre: nomeMestre
    };
    
    try {
        let response;
        if (campanhaId) {
            // Atualizar campanha existente
            response = await fetch(`/api/campanhas/${campanhaId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });
        } else {
            // Criar nova campanha
            response = await fetch('/api/campanhas', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });
        }
        
        if (response.ok) {
            hideModal('campanhaModal');
            loadCampanhas();
            showNotification('Campanha salva com sucesso!', 'success');
        } else {
            const error = await response.json();
            showNotification(error.error || 'Erro ao salvar campanha', 'error');
        }
    } catch (error) {
        showNotification('Erro de conexão', 'error');
    }
}

// Funções de carregamento de dados
async function loadCampanhas() {
    try {
        const response = await fetch('/api/campanhas');
        const data = await response.json();
        
        const container = document.getElementById('campanhas-list');
        if (data.campanhas && data.campanhas.length > 0) {
            container.innerHTML = data.campanhas.map(campanha => `
                <div class="card">
                    <h3><i class="fas fa-flag"></i> ${campanha.nome_campanha}</h3>
                    <p><strong>Mestre:</strong> ${campanha.nome_mestre}</p>
                    <div class="card-actions">
                        <button class="btn btn-primary" onclick="editCampanha(${campanha.id})">
                            <i class="fas fa-edit"></i> Editar
                        </button>
                        <button class="btn btn-danger" onclick="deleteCampanha(${campanha.id})">
                            <i class="fas fa-trash"></i> Excluir
                        </button>
                    </div>
                </div>
            `).join('');
        } else {
            container.innerHTML = `
                <div class="empty-state">
                    <i class="fas fa-flag"></i>
                    <h3>Nenhuma campanha encontrada</h3>
                    <p>Crie sua primeira campanha para começar!</p>
                </div>
            `;
        }
        
        // Atualizar selects de campanha
        updateCampanhaSelects(data.campanhas || []);
    } catch (error) {
        showNotification('Erro ao carregar campanhas', 'error');
    }
}

async function loadPersonagens() {
    const campanhaId = document.getElementById('campanha-select-personagens').value;
    const url = campanhaId ? `/api/personagens?campanha_id=${campanhaId}` : '/api/personagens';
    
    try {
        const response = await fetch(url);
        const data = await response.json();
        
        const container = document.getElementById('personagens-list');
        if (data.personagens && data.personagens.length > 0) {
            container.innerHTML = data.personagens.map(personagem => `
                <div class="card">
                    <h3><i class="fas fa-user"></i> ${personagem.nome}</h3>
                    <p><strong>Classe:</strong> ${personagem.classe || 'Não definida'}</p>
                    <p><strong>Nível:</strong> ${personagem.nivel || 'Não definido'}</p>
                    <p><strong>Pontos de Vida:</strong> ${personagem.pontos_vida || 'Não definido'}</p>
                    <div class="card-actions">
                        <button class="btn btn-primary" onclick="editPersonagem(${personagem.id})">
                            <i class="fas fa-edit"></i> Editar
                        </button>
                        <button class="btn btn-danger" onclick="deletePersonagem(${personagem.id})">
                            <i class="fas fa-trash"></i> Excluir
                        </button>
                    </div>
                </div>
            `).join('');
        } else {
            container.innerHTML = `
                <div class="empty-state">
                    <i class="fas fa-user-friends"></i>
                    <h3>Nenhum personagem encontrado</h3>
                    <p>Crie seu primeiro personagem!</p>
                </div>
            `;
        }
    } catch (error) {
        showNotification('Erro ao carregar personagens', 'error');
    }
}

async function loadItens() {
    // Implementação similar para itens
    const container = document.getElementById('itens-list');
    container.innerHTML = `
        <div class="empty-state">
            <i class="fas fa-sword"></i>
            <h3>Funcionalidade em desenvolvimento</h3>
            <p>Em breve você poderá gerenciar itens aqui!</p>
        </div>
    `;
}

async function loadMissoes() {
    // Implementação similar para missões
    const container = document.getElementById('missoes-list');
    container.innerHTML = `
        <div class="empty-state">
            <i class="fas fa-scroll"></i>
            <h3>Funcionalidade em desenvolvimento</h3>
            <p>Em breve você poderá gerenciar missões aqui!</p>
        </div>
    `;
}

async function loadNPCs() {
    // Implementação similar para NPCs
    const container = document.getElementById('npcs-list');
    container.innerHTML = `
        <div class="empty-state">
            <i class="fas fa-users"></i>
            <h3>Funcionalidade em desenvolvimento</h3>
            <p>Em breve você poderá gerenciar NPCs aqui!</p>
        </div>
    `;
}

async function loadHistorico() {
    // Implementação similar para histórico
    const container = document.getElementById('historico-list');
    container.innerHTML = `
        <div class="empty-state">
            <i class="fas fa-history"></i>
            <h3>Funcionalidade em desenvolvimento</h3>
            <p>Em breve você poderá gerenciar o histórico de sessões aqui!</p>
        </div>
    `;
}

// Funções auxiliares
function updateCampanhaSelects(campanhas) {
    const selects = [
        'campanha-select-personagens',
        'campanha-select-missoes',
        'campanha-select-npcs',
        'campanha-select-historico'
    ];
    
    selects.forEach(selectId => {
        const select = document.getElementById(selectId);
        if (select) {
            select.innerHTML = '<option value="">Selecione uma campanha</option>';
            campanhas.forEach(campanha => {
                select.innerHTML += `<option value="${campanha.id}">${campanha.nome_campanha}</option>`;
            });
        }
    });
}

async function loadCampanhasSelect(selectId) {
    try {
        const response = await fetch('/api/campanhas');
        const data = await response.json();
        
        const select = document.getElementById(selectId);
        if (select && data.campanhas) {
            select.innerHTML = '<option value="">Selecione uma campanha</option>';
            data.campanhas.forEach(campanha => {
                select.innerHTML += `<option value="${campanha.id}">${campanha.nome_campanha}</option>`;
            });
        }
    } catch (error) {
        showNotification('Erro ao carregar campanhas', 'error');
    }
}

// Funções de edição e exclusão
async function editCampanha(id) {
    try {
        const response = await fetch(`/api/campanhas/${id}`);
        const campanha = await response.json();
        
        document.getElementById('campanhaId').value = campanha.id;
        document.getElementById('nomeCampanha').value = campanha.nome_campanha;
        document.getElementById('nomeMestre').value = campanha.nome_mestre;
        document.getElementById('campanhaModalTitle').textContent = 'Editar Campanha';
        
        showModal('campanhaModal');
    } catch (error) {
        showNotification('Erro ao carregar dados da campanha', 'error');
    }
}

async function deleteCampanha(id) {
    if (confirm('Tem certeza que deseja excluir esta campanha?')) {
        try {
            const response = await fetch(`/api/campanhas/${id}`, {
                method: 'DELETE'
            });
            
            if (response.ok) {
                loadCampanhas();
                showNotification('Campanha excluída com sucesso!', 'success');
            } else {
                showNotification('Erro ao excluir campanha', 'error');
            }
        } catch (error) {
            showNotification('Erro de conexão', 'error');
        }
    }
}

// Sistema de notificações
function showNotification(message, type = 'info') {
    // Criar elemento de notificação
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    // Adicionar estilos
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        border-radius: 8px;
        color: white;
        font-weight: 500;
        z-index: 10000;
        animation: slideInRight 0.3s ease;
    `;
    
    // Definir cor baseada no tipo
    switch(type) {
        case 'success':
            notification.style.backgroundColor = '#28a745';
            break;
        case 'error':
            notification.style.backgroundColor = '#dc3545';
            break;
        default:
            notification.style.backgroundColor = '#17a2b8';
    }
    
    // Adicionar ao DOM
    document.body.appendChild(notification);
    
    // Remover após 3 segundos
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

// Adicionar estilos de animação
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

