document.addEventListener('DOMContentLoaded', function() {
    const captionList = document.getElementById('captionList');
    const addCaptionBtn = document.getElementById('addCaptionBtn');
    const captionModal = document.getElementById('captionModal');
    const closeModal = captionModal.querySelector('.close');
    const captionForm = document.getElementById('captionForm');
    const modalTitle = document.getElementById('modalTitle');
    const modalMessage = document.getElementById('modalMessage');

    function fetchAndDisplayCaptions() {
        console.log('キャプション一覧を取得しています...');
        showLoading(captionList);
        fetch('/caption/manage')
            .then(response => response.text())
            .then(html => {
                captionList.innerHTML = html;
                setupCaptionEventListeners();
            })
            .catch(error => {
                console.error('キャプション情報の取得に失敗しました:', error);
                showError(captionList, 'キャプション情報の取得に失敗しました。ページをリロードしてください。');
            })
            .finally(() => {
                hideLoading(captionList);
            });
    }

    function setupCaptionEventListeners() {
        const editButtons = document.querySelectorAll('.edit-caption');
        const deleteButtons = document.querySelectorAll('.delete-caption');

        editButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                const captionId = e.target.dataset.id;
                const captionText = e.target.dataset.text;
                openModal('キャプション編集', captionId, captionText);
            });
        });

        deleteButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                const captionId = e.target.dataset.id;
                if (confirm('このキャプションを削除してもよろしいですか？')) {
                    deleteCaption(captionId);
                }
            });
        });
    }

    addCaptionBtn.addEventListener('click', function() {
        console.log('キャプション追加モーダルを開きます');
        openModal('キャプション追加');
    });

    function openModal(title, captionId = null, captionText = '') {
        modalTitle.textContent = title;
        captionForm.reset();
        document.getElementById('captionText').value = captionText;
        modalMessage.textContent = '';
        modalMessage.className = '';
        if (captionId) {
            captionForm.dataset.mode = 'edit';
            captionForm.dataset.captionId = captionId;
        } else {
            captionForm.dataset.mode = 'add';
            delete captionForm.dataset.captionId;
        }
        captionModal.style.display = 'block';
    }

    closeModal.addEventListener('click', function() {
        console.log('モーダルを閉じます');
        captionModal.style.display = 'none';
    });

    window.addEventListener('click', function(event) {
        if (event.target == captionModal) {
            console.log('モーダル外をクリックしてモーダルを閉じます');
            captionModal.style.display = 'none';
        }
    });

    captionForm.addEventListener('submit', function(e) {
        e.preventDefault();
        console.log('キャプションフォームを送信します');
        const formData = new FormData(captionForm);
        const captionText = formData.get('captionText');

        const method = captionForm.dataset.mode === 'edit' ? 'PUT' : 'POST';
        const url = method === 'PUT' 
            ? `/caption/update/${captionForm.dataset.captionId}`
            : '/caption/add';

        showLoading(captionForm);
        fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `text=${encodeURIComponent(captionText)}`,
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                throw new Error(data.error);
            }
            console.log('キャプション登録/更新成功:', data);
            captionModal.style.display = 'none';
            fetchAndDisplayCaptions();
            showSuccess(modalMessage, 'キャプションが正常に登録/更新されました');
        })
        .catch((error) => {
            console.error('キャプション登録/更新エラー:', error);
            showError(modalMessage, 'キャプションの登録/更新に失敗しました。');
        })
        .finally(() => {
            hideLoading(captionForm);
        });
    });

    function deleteCaption(captionId) {
        console.log(`キャプション削除: ${captionId}`);
        showLoading(captionList);
        fetch(`/caption/delete/${captionId}`, { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    throw new Error(data.error);
                }
                console.log('キャプション削除成功:', data);
                fetchAndDisplayCaptions();
                showSuccess(modalMessage, 'キャプションが正常に削除されました');
            })
            .catch(error => {
                console.error('キャプションの削除に失敗しました:', error);
                showError(modalMessage, 'キャプションの削除に失敗しました。もう一度お試しください。');
            })
            .finally(() => {
                hideLoading(captionList);
            });
    }

    function showLoading(element) {
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'loading';
        loadingDiv.textContent = '読み込み中...';
        element.appendChild(loadingDiv);
    }

    function hideLoading(element) {
        const loadingDiv = element.querySelector('.loading');
        if (loadingDiv) {
            loadingDiv.remove();
        }
    }

    function showError(element, message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = message;
        element.appendChild(errorDiv);
        setTimeout(() => {
            errorDiv.remove();
        }, 5000);
    }

    function showSuccess(element, message) {
        const successDiv = document.createElement('div');
        successDiv.className = 'success-message';
        successDiv.textContent = message;
        element.appendChild(successDiv);
        setTimeout(() => {
            successDiv.remove();
        }, 5000);
    }

    // 初期表示
    fetchAndDisplayCaptions();
});