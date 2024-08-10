document.addEventListener('DOMContentLoaded', function() {
    const menuIcon = document.querySelector('.menu-icon');
    const navLinks = document.querySelector('.nav-links');

    // メニューアイコンのクリックイベント
    menuIcon.addEventListener('click', function() {
        navLinks.classList.toggle('show');
        menuIcon.classList.toggle('active');
    });

    // ウィンドウのリサイズイベント
    window.addEventListener('resize', function() {
        if (window.innerWidth > 768) {
            navLinks.classList.remove('show');
            menuIcon.classList.remove('active');
        }
    });

    console.log('ナビゲーションの初期化が完了しました。');
});