document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('uploadForm');
    const messageDiv = document.getElementById('message');
    const progressBar = document.getElementById('progress');
    const progressIndicator = progressBar.querySelector('.progress');

    function log(message) {
        console.log(`[${new Date().toISOString()}] ${message}`);
    }

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const formData = new FormData(form);
        messageDiv.textContent = '';
        messageDiv.className = '';
        progressBar.style.display = 'block';
        progressIndicator.style.width = '0%';

        log('フォームの送信を開始します');

        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('ネットワークレスポンスが正常ではありません');
            }
            return response.json();
        })
        .then(data => {
            messageDiv.textContent = data.message;
            messageDiv.className = 'success';
            progressIndicator.style.width = '100%';
            log(`アップロード成功: ${data.message}`);
        })
        .catch(error => {
            messageDiv.textContent = 'エラー: ' + error.message;
            messageDiv.className = 'error';
            progressIndicator.style.width = '100%';
            log(`アップロードエラー: ${error.message}`);
        })
        .finally(() => {
            setTimeout(() => {
                progressBar.style.display = 'none';
            }, 1000);
        });
    });
});