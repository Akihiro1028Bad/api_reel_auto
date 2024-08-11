import json
from app.utils.json_handler import read_json, write_json
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

class CaptionService:
    def __init__(self, json_file_path):
        self.json_file_path = json_file_path
        self.captions = self.load_captions()

    def load_captions(self):
        """JSONファイルからキャプションを読み込む"""
        logger.info(f"キャプションをファイルから読み込んでいます: {self.json_file_path}")
        return read_json(self.json_file_path)

    def save_captions(self):
        """キャプションをJSONファイルに保存する"""
        logger.info(f"キャプションをファイルに保存しています: {self.json_file_path}")
        write_json(self.json_file_path, self.captions)

    def get_all_captions(self):
        """すべてのキャプションを取得する"""
        logger.info("すべてのキャプションを取得しています")
        return self.captions

    def add_caption(self, text):
        """新しいキャプションを追加する"""
        logger.info(f"新しいキャプションを追加しています: {text}")
        new_id = max([caption['id'] for caption in self.captions] + [0]) + 1
        new_caption = {
            'id': new_id,
            'text': text
        }
        self.captions.append(new_caption)
        self.save_captions()
        return new_caption

    def update_caption(self, caption_id, new_text):
        """指定されたIDのキャプションを更新する"""
        logger.info(f"キャプションを更新しています: ID {caption_id}")
        for caption in self.captions:
            if caption['id'] == caption_id:
                caption['text'] = new_text
                self.save_captions()
                return caption
        logger.warning(f"更新するキャプションが見つかりません: ID {caption_id}")
        return None

    def delete_caption(self, caption_id):
        """指定されたIDのキャプションを削除する"""
        logger.info(f"キャプションを削除しています: ID {caption_id}")
        self.captions = [c for c in self.captions if c['id'] != caption_id]
        self.save_captions()
        return True

caption_service = CaptionService('data/captions.json')