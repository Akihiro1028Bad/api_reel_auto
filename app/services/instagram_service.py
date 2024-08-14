import requests
from app.config import Config
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

def create_container(video_url, caption):
    """
    Instagram APIを使用してコンテナを作成する
    """
    url = f"https://graph.facebook.com/v20.0/{Config.INSTAGRAM_BUSINESS_ACCOUNT_ID}/media"
    params = {
        'video_url': video_url,
        'media_type': 'REELS',
        'caption': caption,
        'access_token': Config.INSTAGRAM_ACCESS_TOKEN
    }

    try:
        logger.info("Instagramコンテナを作成中")
        response = requests.post(url, params=params)
        response.raise_for_status()
        container_id = response.json().get('id')
        logger.info(f"コンテナの作成に成功しました。ID: {container_id}")
        return container_id
    except requests.RequestException as e:
        logger.error(f"Instagramコンテナの作成中にエラーが発生しました: {str(e)}")
        raise

import time

def check_media_status(container_id):
    """
    メディアのステータスをチェックする
    """
    url = f"https://graph.facebook.com/v20.0/{container_id}"
    params = {
        'fields': 'status_code',
        'access_token': Config.INSTAGRAM_ACCESS_TOKEN
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        status = response.json().get('status_code')
        return status
    except requests.RequestException as e:
        logger.error(f"メディアステータスのチェック中にエラーが発生しました: {str(e)}")
        raise

def publish_container(container_id):
    """
    作成されたコンテナを公開する
    """
    max_attempts = 10
    wait_time = 5  # 5秒待機

    for attempt in range(max_attempts):
        status = check_media_status(container_id)
        if status == 'FINISHED':
            break
        elif status == 'ERROR':
            logger.error("メディアの処理中にエラーが発生しました")
            raise Exception("Media processing error")
        elif attempt == max_attempts - 1:
            logger.error("メディアの準備ができませんでした")
            raise Exception("Media not ready after maximum attempts")
        else:
            logger.info(f"メディアの準備中... {attempt + 1}/{max_attempts}")
            time.sleep(wait_time)

    url = f"https://graph.facebook.com/v17.0/{Config.INSTAGRAM_BUSINESS_ACCOUNT_ID}/media_publish"
    params = {
        'creation_id': container_id,
        'access_token': Config.INSTAGRAM_ACCESS_TOKEN
    }

    try:
        logger.info(f"コンテナを公開中: {container_id}")
        response = requests.post(url, params=params)
        response.raise_for_status()
        result = response.json()
        logger.info(f"コンテナの公開に成功しました。結果: {result}")
        return result
    except requests.RequestException as e:
        logger.error(f"Instagramコンテナの公開中にエラーが発生しました: {str(e)}")
        error_details = response.json() if response.content else "No error details available"
        logger.error(f"エラーの詳細: {error_details}")
        raise