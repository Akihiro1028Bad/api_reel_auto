from flask import Blueprint, render_template, request, jsonify
from app.services.cloudinary_service import upload_to_cloudinary
from app.services.instagram_service import create_container, publish_container
from app.utils.logger import setup_logger
import os

main = Blueprint('main', __name__)
logger = setup_logger(__name__)

@main.route('/')
def index():
    """メインページのルート"""
    return render_template('index.html')

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

        # Instagramコンテナの作成
        logger.info("Instagramコンテナを作成中")
        container_id = create_container(cloudinary_url, caption)

        # 投稿の公開
        logger.info(f"コンテナを公開中: {container_id}")
        publish_result = publish_container(container_id)

        logger.info("ビデオのアップロードと投稿が成功しました")
        return jsonify({'message': 'ビデオのアップロードと投稿が成功しました', 'result': publish_result})

    except Exception as e:
        logger.error(f"アップロード処理中にエラーが発生しました: {str(e)}")
        return jsonify({'error': str(e)}), 500