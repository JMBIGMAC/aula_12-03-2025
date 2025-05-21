document.addEventListener("DOMContentLoaded", function() {
    document.getElementById('login-form').addEventListener('submit', function(e) {
        e.preventDefault();
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        fetch('/api/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.href = '/inicial';
            } else {
                document.getElementById('login-msg').textContent = data.error || 'Falha no login';
            }
        })
        .catch(() => {
            document.getElementById('login-msg').textContent = 'Erro ao tentar logar.';
        });
    });
});
