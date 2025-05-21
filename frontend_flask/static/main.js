document.addEventListener("DOMContentLoaded", function() {
    fetch('/api/get_data')
        .then(response => response.json())
        .then(data => {
            document.getElementById('json-data').textContent = JSON.stringify(data, null, 2);
        })
        .catch(error => {
            document.getElementById('json-data').textContent = 'Erro ao buscar dados: ' + error;
        });
});
