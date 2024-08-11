// アカウント管理機能の JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // DOM要素の取得
    const accountList = document.getElementById('accountList');
    const addAccountBtn = document.getElementById('addAccountBtn');
    const accountModal = document.getElementById('accountModal');
    const closeModal = accountModal.querySelector('.close');
    const accountForm = document.getElementById('accountForm');
    const modalTitle = document.getElementById('modalTitle');
    const modalMessage = document.getElementById('modalMessage');

    // アカウント一覧を取得して表示する関数
    function fetchAndDisplayAccounts() {
        console.log('アカウント一覧を取得しています...');
        showLoading(accountList);
        fetch('/account/accounts')
            .then(response => {
                if (!response.ok) {
                    throw new Error('サーバーエラーが発生しました');
                }
                return response.json();
            })
            .then(accounts => {
                console.log(`${accounts.length}件のアカウント情報を取得しました`);
                accountList.innerHTML = '';
                accounts.forEach(account => {
                    const accountItem = createAccountItem(account);
                    accountList.appendChild(accountItem);
                });
            })
            .catch(error => {
                console.error('アカウント情報の取得に失敗しました:', error);
                showError(accountList, 'アカウント情報の取得に失敗しました。ページをリロードしてください。');
            })
            .finally(() => {
                hideLoading(accountList);
            });
    }

    // アカウント項目のHTML要素を作成する関数
    function createAccountItem(account) {
        const accountItem = document.createElement('div');
        accountItem.className = 'account-item';
        accountItem.dataset.accountId = account.instagram_user_id;
        accountItem.innerHTML = `
            <h3>${account.instagram_user_id}</h3>
            <p>投稿フラグ: ${account.post_flag ? 'オン' : 'オフ'}</p>
            <div class="account-actions">
                <button class="btn btn-primary edit-btn">編集</button>
                <button class="btn btn-danger delete-btn">削除</button>
                <button class="btn btn-secondary toggle-btn">
                    ${account.post_flag ? '投稿オフ' : '投稿オン'}
                </button>
            </div>
        `;

        // 編集ボタンのイベントリスナーを追加
        const editBtn = accountItem.querySelector('.edit-btn');
        editBtn.addEventListener('click', () => editAccount(account.instagram_user_id));

        // 削除ボタンのイベントリスナーを追加
        const deleteBtn = accountItem.querySelector('.delete-btn');
        deleteBtn.addEventListener('click', () => deleteAccount(account.instagram_user_id));

        // トグルボタンのイベントリスナーを追加
        const toggleBtn = accountItem.querySelector('.toggle-btn');
        toggleBtn.addEventListener('click', () => togglePostFlag(account.instagram_user_id));

        return accountItem;
    }

    // アカウント追加モーダルを開く
    addAccountBtn.addEventListener('click', function() {
        console.log('アカウント追加モーダルを開きます');
        openModal('アカウント追加');
    });

    // モーダルを開く関数
    function openModal(title, accountId = null) {
        modalTitle.textContent = title;
        accountForm.reset();
        modalMessage.textContent = '';
        modalMessage.className = '';
        if (accountId) {
            accountForm.dataset.mode = 'edit';
            accountForm.dataset.accountId = accountId;
            fetchAccountDetails(accountId);
        } else {
            accountForm.dataset.mode = 'add';
            delete accountForm.dataset.accountId;
        }
        accountModal.style.display = 'block';
    }

    // アカウント詳細を取得する関数
    function fetchAccountDetails(accountId) {
        console.log(`アカウント詳細を取得しています: ${accountId}`);
        showLoading(accountForm);
        fetch(`/account/accounts/${accountId}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('アカウント情報の取得に失敗しました');
                }
                return response.json();
            })
            .then(account => {
                console.log('アカウント詳細を取得しました:', account);
                document.getElementById('instagramUserId').value = account.instagram_user_id;
                document.getElementById('accessToken').value = account.access_token;
                document.getElementById('businessAccountId').value = account.business_account_id;
                document.getElementById('secretKey').value = account.secret_key;
                document.getElementById('postFlag').checked = account.post_flag;
            })
            .catch(error => {
                console.error('アカウント詳細の取得に失敗しました:', error);
                showError(modalMessage, 'アカウント詳細の取得に失敗しました。もう一度お試しください。');
            })
            .finally(() => {
                hideLoading(accountForm);
            });
    }

    // モーダルを閉じる
    closeModal.addEventListener('click', function() {
        console.log('モーダルを閉じます');
        accountModal.style.display = 'none';
    });

    // モーダル外をクリックして閉じる
    window.addEventListener('click', function(event) {
        if (event.target == accountModal) {
            console.log('モーダル外をクリックしてモーダルを閉じます');
            accountModal.style.display = 'none';
        }
    });

    // アカウントフォームの送信
    accountForm.addEventListener('submit', function(e) {
        e.preventDefault();
        console.log('アカウントフォームを送信します');
        const formData = new FormData(accountForm);
        const accountData = {
            instagram_user_id: formData.get('instagramUserId'),
            access_token: formData.get('accessToken'),
            business_account_id: formData.get('businessAccountId'),
            secret_key: formData.get('secretKey'),
            post_flag: formData.get('postFlag') === 'on'
        };
        console.log('送信するアカウントデータ:', accountData);

        const method = accountForm.dataset.mode === 'edit' ? 'PUT' : 'POST';
        const url = method === 'PUT' ? `/account/accounts/${accountForm.dataset.accountId}` : '/account/accounts/';

        showLoading(accountForm);
        fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(accountData),
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                throw new Error(data.error);
            }
            console.log('アカウント登録/更新成功:', data);
            accountModal.style.display = 'none';
            fetchAndDisplayAccounts();
            showSuccess(modalMessage, 'アカウントが正常に登録/更新されました');
        })
        .catch((error) => {
            console.error('アカウント登録/更新エラー:', error);
            let errorMessage = 'アカウントの登録/更新に失敗しました。';
            if (error.details) {
                errorMessage += `\n詳細: ${error.details}`;
            }
            if (error.traceback) {
                errorMessage += `\n\nエラートレース:\n${error.traceback}`;
            }
            showError(modalMessage, errorMessage);
        })
        .finally(() => {
            hideLoading(accountForm);
        });
    });

    // アカウント編集
    function editAccount(accountId) {
        console.log(`アカウント編集: ${accountId}`);
        openModal('アカウント編集', accountId);
    }

    // アカウント削除
    function deleteAccount(accountId) {
        if (confirm('このアカウントを削除してもよろしいですか？')) {
            console.log(`アカウント削除: ${accountId}`);
            showLoading(accountList);
            fetch(`/account/accounts/${accountId}`, { method: 'DELETE' })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('アカウントの削除に失敗しました');
                    }
                    return response.json();
                })
                .then(data => {
                    console.log('アカウント削除成功:', data);
                    fetchAndDisplayAccounts();
                    showSuccess(modalMessage, 'アカウントが正常に削除されました');
                })
                .catch(error => {
                    console.error('アカウントの削除に失敗しました:', error);
                    showError(modalMessage, 'アカウントの削除に失敗しました。もう一度お試しください。');
                })
                .finally(() => {
                    hideLoading(accountList);
                });
        }
    }

    // 投稿フラグの切り替え
    function togglePostFlag(accountId) {
        console.log(`投稿フラグ切り替え: ${accountId}`);
        showLoading(accountList);
        fetch(`/account/accounts/${accountId}/toggle-flag`, { method: 'POST' })
            .then(response => {
                if (!response.ok) {
                    throw new Error('投稿フラグの切り替えに失敗しました');
                }
                return response.json();
            })
            .then(data => {
                console.log('投稿フラグ切り替え成功:', data);
                fetchAndDisplayAccounts();
                showSuccess(modalMessage, '投稿フラグが正常に切り替えられました');
            })
            .catch(error => {
                console.error('投稿フラグの切り替えに失敗しました:', error);
                showError(modalMessage, '投稿フラグの切り替えに失敗しました。もう一度お試しください。');
            })
            .finally(() => {
                hideLoading(accountList);
            });
    }

    // ローディング表示
    function showLoading(element) {
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'loading';
        loadingDiv.textContent = '読み込み中...';
        element.appendChild(loadingDiv);
    }

    // ローディング非表示
    function hideLoading(element) {
        const loadingDiv = element.querySelector('.loading');
        if (loadingDiv) {
            loadingDiv.remove();
        }
    }

    // エラーメッセージ表示関数を改善
function showError(element, message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.innerHTML = message.replace(/\n/g, '<br>');
    element.appendChild(errorDiv);
    // エラーメッセージを5分後に自動で消す
    setTimeout(() => {
        errorDiv.remove();
    }, 300000);
}

    // 成功メッセージ表示
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
    fetchAndDisplayAccounts();
});