document.addEventListener("DOMContentLoaded", function() {
    // Exemplo: checagem de autenticação e exibição de módulos
    fetch('/api/get_user_info')
        .then(response => response.json())
        .then(data => {
            if (data.username) {
                document.getElementById('user-info').textContent = `Usuário: ${data.username} | Grupos: ${data.groups.join(', ')}`;
                let modulos = '';
                if (data.groups.includes('admin')) {
                    modulos += '<a href="/adm">Painel de Administração</a><br>';
                }
                modulos += '<a href="/">Página Inicial</a>';
                document.getElementById('modulos').innerHTML = modulos;
            } else {
                document.getElementById('user-info').textContent = 'Não autenticado.';
            }
        })
        .catch(() => {
            document.getElementById('user-info').textContent = 'Erro ao buscar informações do usuário.';
        });
});
