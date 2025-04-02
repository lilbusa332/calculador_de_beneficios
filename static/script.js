// Funções para manipulação de abas
function openTab(tabName) {
    // Esconder todos os conteúdos de abas
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.style.display = 'none';
    });
    
    // Remover classe 'active' de todos os botões
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Mostrar a aba selecionada e marcar o botão como ativo
    document.getElementById(tabName).style.display = 'block';
    event.currentTarget.classList.add('active');
    
    // Armazenar a aba selecionada
    localStorage.setItem('lastActiveTab', tabName);
}

// Máscaras para formulários
function applyMasks() {
    // Máscara para CPF
    const cpfInput = document.getElementById('cpf');
    if (cpfInput) {
        cpfInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            
            if (value.length > 3) {
                value = value.replace(/^(\d{3})/, '$1.');
            }
            if (value.length > 7) {
                value = value.replace(/^(\d{3})\.(\d{3})/, '$1.$2.');
            }
            if (value.length > 11) {
                value = value.replace(/^(\d{3})\.(\d{3})\.(\d{3})/, '$1.$2.$3-');
            }
            
            e.target.value = value.substring(0, 14);
        });
    }
    
    // Máscara para telefone
    const telInput = document.getElementById('telefone');
    if (telInput) {
        telInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            
            if (value.length > 0) {
                value = '(' + value.substring(0, 2) + ') ' + value.substring(2);
            }
            if (value.length > 10) {
                value = value.substring(0, 10) + '-' + value.substring(10);
            }
            
            e.target.value = value.substring(0, 15);
        });
    }
    
    // Máscara para CEP
    const cepInput = document.getElementById('cep');
    if (cepInput) {
        cepInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            
            if (value.length > 5) {
                value = value.substring(0, 5) + '-' + value.substring(5);
            }
            
            e.target.value = value.substring(0, 9);
            
            // Buscar CEP se completo
            if (value.length === 8) {
                fetch(`https://viacep.com.br/ws/${value}/json/`)
                    .then(response => response.json())
                    .then(data => {
                        if (!data.erro) {
                            document.getElementById('endereco').value = data.logradouro || '';
                            document.getElementById('cidade').value = data.localidade || '';
                            document.getElementById('estado').value = data.uf || '';
                        }
                    });
            }
        });
    }
}

// Formulário de cálculo de benefício
function setupBenefitForm() {
    const form = document.getElementById('calculoForm');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = {
                renda: document.getElementById('renda').value,
                dependentes: document.getElementById('dependentes').value,
                tipo_beneficio: document.getElementById('tipo_beneficio').value
            };
            
            fetch('/calcular-beneficio', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const resultadoContainer = document.getElementById('resultadoContainer');
                    const resultadoValor = document.getElementById('resultadoValor');
                    const pdfLink = document.getElementById('pdfLink');
                    
                    resultadoValor.innerHTML = `
                        <p>Benefício calculado em: <strong>R$ ${data.valor_beneficio.toFixed(2).replace('.', ',')}</strong></p>
                        <p>Data: ${data.data_calculo}</p>
                    `;
                    
                    pdfLink.href = data.pdf_url;
                    resultadoContainer.classList.remove('hidden');
                    
                    // Recarregar o histórico
                    window.location.reload();
                } else {
                    alert('Erro: ' + data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Ocorreu um erro ao calcular o benefício');
            });
        });
    }
}

// Fechar mensagens flash
function setupFlashMessages() {
    document.querySelectorAll('.flash .close-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            this.parentElement.remove();
        });
    });
    
    // Fechar automaticamente após 5 segundos
    setTimeout(() => {
        document.querySelectorAll('.flash').forEach(flash => {
            flash.style.animation = 'fadeOut 0.5s forwards';
            setTimeout(() => flash.remove(), 500);
        });
    }, 5000);
}

// Inicialização quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', function() {
    // Restaurar aba ativa
    const lastActiveTab = localStorage.getItem('lastActiveTab');
    if (lastActiveTab) {
        const tabBtn = document.querySelector(`.tab-btn[onclick="openTab('${lastActiveTab}')"]`);
        if (tabBtn) tabBtn.click();
    }
    
    applyMasks();
    setupBenefitForm();
    setupFlashMessages();
    
    // Animação de fadeOut para mensagens flash
    const style = document.createElement('style');
    style.textContent = `
        @keyframes fadeOut {
            from { opacity: 1; transform: translateY(0); }
            to { opacity: 0; transform: translateY(-20px); }
        }
    `;
    document.head.appendChild(style);
});