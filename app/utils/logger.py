import logging

def setup_logger(name):
    """
    ロガーをセットアップする

    Args:
        name (str): ロガーの名前

    Returns:
        logging.Logger: 設定されたロガーインスタンス
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # ファイルハンドラ
    file_handler = logging.FileHandler('app.log', encoding='utf-8')
    file_handler.setLevel(logging.INFO)

    # コンソールハンドラ
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # フォーマッタ
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # ハンドラをロガーに追加
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger