document.addEventListener('DOMContentLoaded', function() {
    const scheduleForm = document.getElementById('scheduleForm');
    const scheduleList = document.getElementById('scheduleList');
    const messageDiv = document.getElementById('message');

    // スケジュールを取得して表示する
    function fetchAndDisplaySchedules() {
        console.log('スケジュール情報を取得しています...');
        fetch('/schedule/schedules')
            .then(response => response.json())
            .then(data => {
                scheduleList.innerHTML = '';
                data.schedule.forEach((schedule, index) => {
                    const li = document.createElement('li');
                    li.innerHTML = `
                        <input type="time" value="${schedule.time}" name="time_${index}">
                        <input type="checkbox" ${schedule.enabled ? 'checked' : ''} name="enabled_${index}">
                        <button type="button" class="delete-btn" data-index="${index}">削除</button>
                    `;
                    scheduleList.appendChild(li);
                });
                setupDeleteButtons();
            })
            .catch(error => {
                console.error('スケジュール情報の取得に失敗しました:', error);
                showMessage('スケジュール情報の取得に失敗しました。', 'error');
            });
    }

    // 削除ボタンのイベントリスナーを設定
    function setupDeleteButtons() {
        const deleteButtons = document.querySelectorAll('.delete-btn');
        deleteButtons.forEach(button => {
            button.addEventListener('click', function() {
                const index = this.dataset.index;
                this.closest('li').remove();
            });
        });
    }

    // スケジュールを保存する
    scheduleForm.addEventListener('submit', function(e) {
        e.preventDefault();
        console.log('スケジュールを保存します');
        
        const schedules = [];
        const items = scheduleList.querySelectorAll('li');
        items.forEach(item => {
            const time = item.querySelector('input[type="time"]').value;
            const enabled = item.querySelector('input[type="checkbox"]').checked;
            schedules.push({ time, enabled });
        });

        fetch('/schedule/schedules/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ schedule: schedules }),
        })
        .then(response => response.json())
        .then(data => {
            console.log('スケジュールが保存されました:', data);
            showMessage('スケジュールが正常に保存されました', 'success');
        })
        .catch(error => {
            console.error('スケジュールの保存に失敗しました:', error);
            showMessage('スケジュールの保存に失敗しました', 'error');
        });
    });

    // 新しいスケジュールを追加する
    document.getElementById('addScheduleBtn').addEventListener('click', function() {
        const li = document.createElement('li');
        li.innerHTML = `
            <input type="time" name="time_new">
            <input type="checkbox" name="enabled_new" checked>
            <button type="button" class="delete-btn">削除</button>
        `;
        scheduleList.appendChild(li);
        setupDeleteButtons();
    });

    // メッセージを表示する
    function showMessage(message, type) {
        messageDiv.textContent = message;
        messageDiv.className = type;
        setTimeout(() => {
            messageDiv.textContent = '';
            messageDiv.className = '';
        }, 5000);
    }

    // 初期表示
    fetchAndDisplaySchedules();
});