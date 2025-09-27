// Função para alternar entre telas
function showScreen(screenId) {
    // Oculta todas as telas
    document.querySelectorAll('.content > div').forEach(screen => {
        screen.classList.add('hidden');
    });

    // Mostra a tela solicitada
    document.getElementById(screenId).classList.remove('hidden');

    // Atualiza o cabeçalho conforme a tela
    updateHeader(screenId);
}

// Função para voltar para a tela de telemetria
function goBackToTelemetry() {
    if (document.getElementById('telemetry-screen').classList.contains('hidden')) {
        showScreen('telemetry-screen');
    } else {
        showScreen('main-menu-screen');
    }
}

// Função para atualizar o cabeçalho conforme a tela
function updateHeader(screenId) {
    const headerTitle = document.getElementById('header-title');
    const headerSubtitle = document.getElementById('header-subtitle');

    switch (screenId) {
        case 'login-screen':
            headerTitle.textContent = 'Elite Motorsport';
            headerSubtitle.textContent = 'Desempenho de alto nível';
            break;
        case 'main-menu-screen':
            headerTitle.textContent = 'Menu Principal';
            headerSubtitle.textContent = 'Selecione uma opção';
            break;
        case 'settings-screen':
            headerTitle.textContent = 'Configurações';
            headerSubtitle.textContent = 'Ajustes do sistema';
            break;
        case 'telemetry-screen':
            headerTitle.textContent = 'Telemetria';
            headerSubtitle.textContent = 'Monitoramento em tempo real';
            break;
        case 'telemetry-config-screen':
            headerTitle.textContent = 'Config. Telemetria';
            headerSubtitle.textContent = 'Ajuste os parâmetros';
            break;
        case 'data-export-screen':
            headerTitle.textContent = 'Exportar Dados';
            headerSubtitle.textContent = 'Exporte dados de telemetria';
            break;
        case 'account-screen':
            headerTitle.textContent = 'Minha Conta';
            headerSubtitle.textContent = 'Perfil do usuário';
            break;
    }
}

// Função para alternar idioma
function changeLanguage(lang) {
    alert(`Idioma alterado para ${lang === 'pt' ? 'Português' : 'English'}`);
    // Aqui viria a lógica real de internacionalização
}

// Função para simular dados de telemetria em tempo real
function simulateTelemetry() {
    if (!document.getElementById('telemetry-screen').classList.contains('hidden')) {
        // Gera valores aleatórios para os medidores
        document.getElementById('rpm-value').textContent =
            Math.floor(Math.random() * 3000 + 3000).toLocaleString();

        document.getElementById('temp-value').textContent =
            Math.floor(Math.random() * 20 + 80) + '°C';

        document.getElementById('voltage-value').textContent =
            (Math.random() * 1.5 + 12.5).toFixed(1) + 'V';

        document.getElementById('fuel-value').textContent =
            Math.floor(Math.random() * 10 + 70) + '%';
    }
}

// Inicializa com a tela de login visível
document.addEventListener('DOMContentLoaded', function () {
    showScreen('login-screen');

    // Simula dados de telemetria a cada 2 segundos
    setInterval(simulateTelemetry, 2000);
});