from flask import Blueprint, render_template, request, jsonify
from app.services.account_service import AccountService
from app.utils.logger import setup_logger

account_bp = Blueprint('account', __name__)
logger = setup_logger(__name__)
account_service = AccountService('data/accounts.json')

@account_bp.route('/account-management')
def account_management():
    """アカウント管理ページのルート"""
    logger.info("アカウント管理ページにアクセスしました")
    return render_template('account/account_management.html')

@account_bp.route('/accounts', methods=['GET'])
def get_accounts():
    """登録されているすべてのアカウント情報を取得"""
    logger.info("全アカウント情報の取得リクエストを受信しました")
    try:
        accounts = account_service.get_all_accounts()
        logger.info(f"{len(accounts)}件のアカウント情報を返送します")
        return jsonify(accounts)
    except Exception as e:
        logger.error(f"アカウント情報の取得中にエラーが発生しました: {str(e)}")
        return jsonify({"error": "アカウント情報の取得に失敗しました"}), 500

@account_bp.route('/accounts', methods=['POST'])
def add_account():
    """新しいアカウントを追加"""
    logger.info("新規アカウント追加リクエストを受信しました")
    account_data = request.json
    logger.debug(f"受信したアカウントデータ: {account_data}")
    try:
        account_service.add_account(account_data)
        logger.info("アカウントが正常に追加されました")
        return jsonify({"message": "アカウントが正常に追加されました"}), 201
    except Exception as e:
        logger.error(f"アカウントの追加中にエラーが発生しました: {str(e)}")
        return jsonify({"error": "アカウントの追加に失敗しました"}), 500

@account_bp.route('/accounts/<account_id>', methods=['PUT'])
def update_account(account_id):
    """既存のアカウント情報を更新"""
    logger.info(f"アカウント更新リクエストを受信しました: {account_id}")
    updated_data = request.json
    logger.debug(f"更新データ: {updated_data}")
    try:
        account_service.update_account(account_id, updated_data)
        logger.info("アカウント情報が正常に更新されました")
        return jsonify({"message": "アカウント情報が正常に更新されました"})
    except Exception as e:
        logger.error(f"アカウントの更新中にエラーが発生しました: {str(e)}")
        return jsonify({"error": "アカウントの更新に失敗しました"}), 500

@account_bp.route('/accounts/<account_id>', methods=['DELETE'])
def delete_account(account_id):
    """アカウントを削除"""
    logger.info(f"アカウント削除リクエストを受信しました: {account_id}")
    try:
        account_service.delete_account(account_id)
        logger.info("アカウントが正常に削除されました")
        return jsonify({"message": "アカウントが正常に削除されました"})
    except Exception as e:
        logger.error(f"アカウントの削除中にエラーが発生しました: {str(e)}")
        return jsonify({"error": "アカウントの削除に失敗しました"}), 500

@account_bp.route('/accounts/<account_id>/toggle-flag', methods=['POST'])
def toggle_post_flag(account_id):
    """アカウントの投稿フラグを切り替え"""
    logger.info(f"投稿フラグ切り替えリクエストを受信しました: {account_id}")
    try:
        account_service.toggle_post_flag(account_id)
        logger.info("投稿フラグが正常に切り替えられました")
        return jsonify({"message": "投稿フラグが正常に切り替えられました"})
    except Exception as e:
        logger.error(f"投稿フラグの切り替え中にエラーが発生しました: {str(e)}")
        return jsonify({"error": "投稿フラグの切り替えに失敗しました"}), 500

@account_bp.route('/accounts/<account_id>', methods=['GET'])
def get_account(account_id):
    """特定のアカウント情報を取得"""
    logger.info(f"アカウント情報取得リクエストを受信しました: {account_id}")
    try:
        account = account_service.get_account(account_id)
        if account:
            logger.info("アカウント情報を正常に取得しました")
            return jsonify(account)
        else:
            logger.warning(f"アカウントが見つかりません: {account_id}")
            return jsonify({"error": "アカウントが見つかりません"}), 404
    except Exception as e:
        logger.error(f"アカウント情報の取得中にエラーが発生しました: {str(e)}")
        return jsonify({"error": "アカウント情報の取得に失敗しました"}), 500