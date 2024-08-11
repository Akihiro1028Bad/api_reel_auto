import json
from app.utils.json_handler import read_json, write_json
from app.utils.logger import setup_logger
import os

logger = setup_logger(__name__)

class AccountService:
    def __init__(self, json_file_path):
        self.json_file_path = json_file_path
        
        # ファイルが存在しない場合は、空のJSONファイルを作成
        if not os.path.exists(json_file_path):
            logger.info(f"アカウントファイルが存在しないため、新規作成します: {json_file_path}")
            write_json(json_file_path, [])

    def get_all_accounts(self):
        """すべてのアカウント情報を取得する"""
        logger.info("すべてのアカウント情報を取得しています")
        return read_json(self.json_file_path)
    
    def get_account(self, account_id):
        """特定のアカウント情報を取得する"""
        logger.info(f"アカウント情報を取得しています: {account_id}")
        accounts = self.get_all_accounts()
        for account in accounts:
            if account['instagram_user_id'] == account_id:
                return account
        return None  # アカウントが見つからない場合はNoneを返す

    def add_account(self, account_data):
        logger.info(f"新しいアカウントを追加しています: {account_data['instagram_user_id']}")
        try:
            accounts = self.get_all_accounts()
            accounts.append(account_data)
            write_json(self.json_file_path, accounts)
            logger.info("アカウントが正常に追加されました")
        except Exception as e:
            logger.error(f"アカウント追加中にエラーが発生しました: {str(e)}")
            logger.exception("詳細なエラー情報:")
            raise

    def update_account(self, account_id, updated_data):
        """既存のアカウント情報を更新する"""
        logger.info(f"アカウント情報を更新しています: {account_id}")
        accounts = self.get_all_accounts()
        for account in accounts:
            if account['instagram_user_id'] == account_id:
                account.update(updated_data)
                break
        write_json(self.json_file_path, accounts)
        logger.info("アカウント情報が正常に更新されました")

    def delete_account(self, account_id):
        """アカウントを削除する"""
        logger.info(f"アカウントを削除しています: {account_id}")
        accounts = self.get_all_accounts()
        accounts = [acc for acc in accounts if acc['instagram_user_id'] != account_id]
        write_json(self.json_file_path, accounts)
        logger.info("アカウントが正常に削除されました")

    def toggle_post_flag(self, account_id):
        """アカウントの投稿フラグを切り替える"""
        logger.info(f"投稿フラグを切り替えています: {account_id}")
        accounts = self.get_all_accounts()
        for account in accounts:
            if account['instagram_user_id'] == account_id:
                account['post_flag'] = not account['post_flag']
                break
        write_json(self.json_file_path, accounts)
        logger.info("投稿フラグが正常に切り替えられました")