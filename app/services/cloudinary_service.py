import cloudinary
import cloudinary.uploader
from app.config import Config
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

# Cloudinary設定
cloudinary.config(
    cloud_name=Config.CLOUDINARY_CLOUD_NAME,
    api_key=Config.CLOUDINARY_API_KEY,
    api_secret=Config.CLOUDINARY_API_SECRET
)

def upload_to_cloudinary(video_file):
    """
    動画をCloudinaryにアップロードする

    Args:
        video_file (FileStorage): アップロードする動画ファイル

    Returns:
        str: アップロードされた動画のCloudinary URL
    """
    try:
        logger.info(f"Cloudinaryにビデオをアップロード中: {video_file.filename}")
        result = cloudinary.uploader.upload(video_file, resource_type="video")
        logger.info(f"ビデオのアップロードに成功しました。URL: {result['url']}")
        return result['url']
    except Exception as e:
        logger.error(f"Cloudinaryへのアップロード中にエラーが発生しました: {str(e)}")
        raise