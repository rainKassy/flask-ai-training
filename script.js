document.getElementById('trainButton').addEventListener('click', function() {
    const epochs = document.getElementById('epochs').value;
    const batch_size = document.getElementById('batch_size').value;

    fetch('/train', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ epochs: parseInt(epochs), batch_size: parseInt(batch_size) })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('status').textContent = 'Status: ' + data.status;
    })
    .catch(error => console.error('Error:', error));
});

document.getElementById('stopButton').addEventListener('click', function() {
    fetch('/stop', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('status').textContent = 'Status: ' + data.status;
    })
    .catch(error => console.error('Error:', error));
});

// Обновление статуса и прогресса тренировки каждые 1 секунду
setInterval(function() {
    fetch('/status')
        .then(response => response.json())
        .then(data => {
            document.getElementById('status').textContent = 'Status: ' + data.status;

            // Если статус содержит прогресс, обновляем прогресс-бар
            if (data.status.includes("progress")) {
                let progress = parseInt(data.status.match(/\d+/)[0]); // Извлекаем процент
                document.getElementById('progress-bar').style.width = progress + '%';
            }
        })
        .catch(error => console.error('Error:', error));
}, 1000);

