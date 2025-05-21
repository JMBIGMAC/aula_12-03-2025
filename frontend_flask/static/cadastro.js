document.addEventListener("DOMContentLoaded", function() {
    document.getElementById('cadastro-form').addEventListener('submit', function(e) {
        e.preventDefault();
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        const email = document.getElementById('email').value;
        fetch('/api/cadastro', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password, email })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success && data.redirect) {
                window.location.href = data.redirect;
            } else {
                document.getElementById('cadastro-msg').textContent = data.error || 'Erro no cadastro';
            }
        })
        .catch(() => {
            document.getElementById('cadastro-msg').textContent = 'Erro ao tentar cadastrar.';
        });
    });
});
