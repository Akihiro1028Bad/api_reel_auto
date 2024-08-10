from flask import Blueprint, render_template, request, jsonify
from app.services.cloudinary_service import upload_to_cloudinary
from app.services.instagram_service import create_container, publish_container
from app.services.account_service import AccountService
from app.utils.logger import setup_logger
import os

# Blueprintの作成
main = Blueprint('main', __name__)

# ロガーの設定
logger = setup_logger(__name__)

# アカウントサービスのインスタンスを作成
account_service = AccountService('data/accounts.json')

@main.route('/')
def index():
    """メインページのルート"""
    logger.info("メインページにアクセスしました")
    return render_template('index.html')

@main.route('/account-management')
def account_management():
    """アカウント管理ページのルート"""
    logger.info("アカウント管理ページにアクセスしました")
    return render_template('account/account_management.html')

@main.route('/accounts', methods=['GET'])
def get_accounts():
    """登録されているすべてのアカウント情報を取得"""
    logger.info("全アカウント情報の取得リクエストを受信しました")
    accounts = account_service.get_all_accounts()
    logger.info(f"{len(accounts)}件のアカウント情報を返送します")
    return jsonify(accounts)

@main.route('/accounts', methods=['POST'])
def add_account():
    """新しいアカウントを追加"""
    logger.info("新規アカウント追加リクエストを受信しました")
    account_data = request.json
    logger.debug(f"受信したアカウントデータ: {account_data}")
    account_service.add_account(account_data)
    logger.info("アカウントが正常に追加されました")
    return jsonify({"message": "アカウントが正常に追加されました"}), 201

@main.route('/accounts/<account_id>', methods=['PUT'])
def update_account(account_id):
    """既存のアカウント情報を更新"""
    logger.info(f"アカウント更新リクエストを受信しました: {account_id}")
    updated_data = request.json
    logger.debug(f"更新データ: {updated_data}")
    account_service.update_account(account_id, updated_data)
    logger.info("アカウント情報が正常に更新されました")
    return jsonify({"message": "アカウント情報が正常に更新されました"})

@main.route('/accounts/<account_id>', methods=['DELETE'])
def delete_account(account_id):
    """アカウントを削除"""
    logger.info(f"アカウント削除リクエストを受信しました: {account_id}")
    account_service.delete_account(account_id)
    logger.info("アカウントが正常に削除されました")
    return jsonify({"message": "アカウントが正常に削除されました"})

@main.route('/accounts/<account_id>/toggle-flag', methods=['POST'])
def toggle_post_flag(account_id):
    """アカウントの投稿フラグを切り替え"""
    logger.info(f"投稿フラグ切り替えリクエストを受信しました: {account_id}")
    account_service.toggle_post_flag(account_id)
    logger.info("投稿フラグが正常に切り替えられました")
    return jsonify({"message": "投稿フラグが正常に切り替えられました"})

@main.route('/upload', methods=['POST'])
def upload():
    """動画アップロードと投稿のエンドポイント"""
    try:
        logger.info("アップロードリクエストを受信しました")
        
        if 'video' not in request.files:
            logger.error("ビデオファイルが送信されていません")
            return jsonify({'error': 'ビデオファイルが送信されていません'}), 400
        
        video = request.files['video']
        caption = request.form.get('caption', '')
        
        if video.filename == '':
            logger.error("ファイルが選択されていません")
            return jsonify({'error': 'ファイルが選択されていません'}), 400

        # Cloudinaryにアップロード
        logger.info(f"ビデオをCloudinaryにアップロード中: {video.filename}")
        cloudinary_url = upload_to_cloudinary(video)

        # 投稿フラグがオンのアカウントに順次投稿
        accounts = account_service.get_all_accounts()
        results = []
        for account in accounts:
            if account['post_flag']:
                try:
                    # Instagramコンテナの作成
                    logger.info(f"Instagramコンテナを作成中: {account['instagram_user_id']}")
                    container_id = create_container(cloudinary_url, caption, account)

                    # 投稿の公開
                    logger.info(f"コンテナを公開中: {container_id}")
                    publish_result = publish_container(container_id, account)
                    results.append({
                        'account_id': account['instagram_user_id'],
                        'status': 'success',
                        'message': '投稿が成功しました'
                    })
                except Exception as e:
                    logger.error(f"アカウント {account['instagram_user_id']} への投稿中にエラーが発生しました: {str(e)}")
                    results.append({
                        'account_id': account['instagram_user_id'],
                        'status': 'error',
                        'message': str(e)
                    })

        logger.info("すべてのアカウントへの投稿処理が完了しました")
        return jsonify({'message': '投稿処理が完了しました', 'results': results})

    except Exception as e:
        logger.error(f"アップロード処理中にエラーが発生しました: {str(e)}")
        return jsonify({'error': str(e)}), 500