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

        fetch('/upload/process', {
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
            // 結果の詳細を表示
            if (data.results) {
                const resultsList = document.createElement('ul');
                data.results.forEach(result => {
                    const li = document.createElement('li');
                    li.textContent = `アカウント ${result.account_id}: ${result.status} - ${result.message}`;
                    resultsList.appendChild(li);
                });
                messageDiv.appendChild(resultsList);
            }
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