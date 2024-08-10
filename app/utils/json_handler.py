import json
import os
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

def read_json(file_path):
    """JSONファイルを読み込む"""
    logger.info(f"JSONファイルを読み込んでいます: {file_path}")
    if not os.path.exists(file_path):
        logger.warning(f"JSONファイルが存在しません: {file_path}")
        return []
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    logger.info("JSONファイルの読み込みが完了しました")
    return data

def write_json(file_path, data):
    """JSONファイルに書き込む"""
    logger.info(f"JSONファイルに書き込んでいます: {file_path}")
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
    logger.info("JSONファイルへの書き込みが完了しました")