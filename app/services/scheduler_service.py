import json
from apscheduler.schedulers.background import BackgroundScheduler
from app.services.instagram_service import create_container, publish_container
from app.services.cloudinary_service import upload_to_cloudinary
from app.utils.logger import setup_logger
import random
import os

logger = setup_logger(__name__)

class SchedulerService:
    def __init__(self, schedule_file='data/schedule.json', accounts_file='data/accounts.json', videos_folder='uploads'):
        self.schedule_file = schedule_file
        self.accounts_file = accounts_file
        self.videos_folder = videos_folder
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        self.ensure_json_files_exist()
        self.load_and_set_schedules()

    def ensure_json_files_exist(self):
        """JSONファイルが存在しない場合、デフォルトの内容で作成する"""
        # スケジュールファイルの確認と作成
        if not os.path.exists(self.schedule_file):
            logger.info(f"スケジュールファイルが見つかりません。新規作成します: {self.schedule_file}")
            default_schedule = {"schedule": []}
            self.save_schedule(default_schedule)

        # アカウントファイルの確認と作成
        if not os.path.exists(self.accounts_file):
            logger.info(f"アカウントファイルが見つかりません。新規作成します: {self.accounts_file}")
            default_accounts = []
            with open(self.accounts_file, 'w') as f:
                json.dump(default_accounts, f, indent=2)

    def load_and_set_schedules(self):
        """スケジュールをJSONファイルから読み込み、設定する"""
        logger.info("スケジュールの読み込みと設定を開始します")
        try:
            with open(self.schedule_file, 'r') as f:
                schedules = json.load(f)
            
            # 既存のジョブをすべて削除
            self.scheduler.remove_all_jobs()

            for schedule in schedules['schedule']:
                if schedule['enabled']:
                    hour, minute = map(int, schedule['time'].split(':'))
                    self.scheduler.add_job(self.post_video, 'cron', hour=hour, minute=minute)
                    logger.info(f"スケジュールを設定しました: {schedule['time']}")
        except json.JSONDecodeError:
            logger.error(f"スケジュールファイルの形式が不正です: {self.schedule_file}")
        except Exception as e:
            logger.error(f"スケジュールの読み込み中にエラーが発生しました: {str(e)}")

    def save_schedule(self, schedules):
        """スケジュールをJSONファイルに保存する"""
        logger.info("スケジュールの保存を開始します")
        try:
            with open(self.schedule_file, 'w') as f:
                json.dump(schedules, f, indent=2)
            logger.info("スケジュールを正常に保存しました")
            self.load_and_set_schedules()  # スケジュールを再読み込みして設定
        except Exception as e:
            logger.error(f"スケジュールの保存中にエラーが発生しました: {str(e)}")

    def post_video(self):
        """動画を投稿する"""
        logger.info("自動投稿プロセスを開始します")
        try:
            # アカウント情報を読み込む
            with open(self.accounts_file, 'r') as f:
                accounts = json.load(f)
            
            # 投稿可能なアカウントをフィルタリング
            active_accounts = [acc for acc in accounts if acc['post_flag']]
            
            if not active_accounts:
                logger.warning("投稿可能なアカウントがありません")
                return

            # ランダムにビデオを選択
            video_files = [f for f in os.listdir(self.videos_folder) if f.endswith(('.mp4', '.mov', '.avi'))]
            if not video_files:
                logger.warning("投稿可能な動画ファイルがありません")
                return
            
            selected_video = random.choice(video_files)
            video_path = os.path.join(self.videos_folder, selected_video)

            # Cloudinaryにアップロード
            cloudinary_url = upload_to_cloudinary(video_path)

            # キャプションを取得（ここではダミーのキャプションを使用）
            caption = "自動投稿されたビデオです"

            # 各アクティブアカウントに投稿
            for account in active_accounts:
                try:
                    container_id = create_container(cloudinary_url, caption)
                    publish_container(container_id)
                    logger.info(f"アカウント {account['instagram_user_id']} に正常に投稿しました")
                except Exception as e:
                    logger.error(f"アカウント {account['instagram_user_id']} への投稿中にエラーが発生しました: {str(e)}")

        except Exception as e:
            logger.error(f"自動投稿プロセス中にエラーが発生しました: {str(e)}")

scheduler_service = SchedulerService()