from flask import Blueprint, render_template, request, jsonify
from werkzeug.utils import secure_filename
from app.services.cloudinary_service import upload_to_cloudinary
from app.services.instagram_service import create_container, publish_container
from app.services.account_service import AccountService
from app.services.caption_service import caption_service
from app.utils.logger import setup_logger
import os
import random

upload_bp = Blueprint('upload', __name__)
logger = setup_logger(__name__)
account_service = AccountService('data/accounts.json')

ALLOWED_EXTENSIONS = {'mp4', 'mov', 'avi'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@upload_bp.route('/')
def upload_index():
    """アップロードページのルート"""
    logger.info("アップロードページにアクセスしました")
    captions = caption_service.get_all_captions()
    return render_template('upload/upload_index.html', captions=captions)

@upload_bp.route('/process', methods=['POST'])
def process_upload():
    """フォルダからランダムに動画を選択し、アップロードして投稿する"""
    logger.info("アップロード処理を開始します")
    
    if 'folder' not in request.files:
        logger.error("フォルダが選択されていません")
        return jsonify({'error': 'フォルダが選択されていません'}), 400
    
    files = request.files.getlist('folder')
    caption_id = int(request.form.get('caption_id'))
    post_count = int(request.form.get('post_count', 1))
    
    if not files:
        logger.error("フォルダ内にファイルが存在しません")
        return jsonify({'error': 'フォルダ内にファイルが存在しません'}), 400

    # 動画ファイルのみをフィルタリング
    video_files = [f for f in files if allowed_file(f.filename)]
    
    if not video_files:
        logger.error("フォルダ内に適切な動画ファイルが存在しません")
        return jsonify({'error': 'フォルダ内に適切な動画ファイルが存在しません'}), 400

    # キャプションを取得
    captions = caption_service.get_all_captions()
    selected_caption = next((c for c in captions if c['id'] == caption_id), None)
    if not selected_caption:
        logger.error("選択されたキャプションが見つかりません")
        return jsonify({'error': '選択されたキャプションが見つかりません'}), 400

    try:
        # 投稿フラグがオンのアカウントを取得
        accounts = [acc for acc in account_service.get_all_accounts() if acc['post_flag']]
        results = []

        for _ in range(post_count):
            for account in accounts:
                # ランダムに動画ファイルを選択
                if not video_files:  # すべての動画が使用された場合、リストをリセット
                    video_files = [f for f in files if allowed_file(f.filename)]
                selected_video = random.choice(video_files)
                video_files.remove(selected_video)  # 選択された動画をリストから削除

                logger.info(f"選択された動画ファイル: {selected_video.filename}")

                # Cloudinaryにアップロード
                logger.info(f"動画をCloudinaryにアップロード中: {selected_video.filename}")
                cloudinary_url = upload_to_cloudinary(selected_video)

                try:
                    # Instagramコンテナの作成
                    logger.info(f"Instagramコンテナを作成中: {account['instagram_user_id']}")
                    container_id = create_container(cloudinary_url, selected_caption['text'])

                    # 投稿の公開
                    logger.info(f"コンテナを公開中: {container_id}")
                    publish_result = publish_container(container_id)
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

        logger.info(f"すべてのアカウントへの投稿処理が完了しました。投稿数: {post_count}")
        return jsonify({'message': '投稿処理が完了しました', 'results': results})

    except Exception as e:
        logger.error(f"アップロード処理中にエラーが発生しました: {str(e)}")
        return jsonify({'error': str(e)}), 500