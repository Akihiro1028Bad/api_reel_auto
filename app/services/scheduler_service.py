import json
from apscheduler.schedulers.background import BackgroundScheduler
from app.services.instagram_service import create_container, publish_container
from app.services.cloudinary_service import upload_to_cloudinary
from app.utils.logger import setup_logger
import random
import os
import time

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
        """複数の動画を各アカウントにランダムで投稿する"""
        logger.info("自動投稿プロセスを開始します")
        
        # 投稿数を設定（必要に応じて変更可能）
        POSTS_PER_ACCOUNT = 3
        
        # 固定キャプションを設定（三重引用符を使用）
        CAPTION = """ストーリーもみた方がいいよ

        #カップル
        #恋愛
        #低身長女子
        #低身長コーデ
        #低身長ファッション
        #女子
        #女子大生
        #うらあか男子と繋がりたい"""

        try:
            # 1分から60分の間でランダムに待機時間を設定
            wait_time = random.randint(60, 3600)  # 60秒（1分）から3600秒（60分）の間
            # アカウント情報を読み込む
            with open(self.accounts_file, 'r') as f:
                accounts = json.load(f)
            
            # 投稿可能なアカウントをフィルタリング
            active_accounts = [acc for acc in accounts if acc['post_flag']]
            
            if not active_accounts:
                logger.warning("投稿可能なアカウントがありません")
                return

            # 利用可能な全ての動画ファイルをリストアップ
            all_video_files = [f for f in os.listdir(self.videos_folder) if f.endswith(('.mp4', '.mov', '.avi'))]
            if len(all_video_files) < POSTS_PER_ACCOUNT:
                logger.warning(f"投稿可能な動画ファイルが足りません。必要数: {POSTS_PER_ACCOUNT}, 現在の数: {len(all_video_files)}")
                return

            # 各アクティブアカウントに投稿
            for account in active_accounts:
                logger.info(f"アカウント {account['instagram_user_id']} の投稿を開始します")
                
                # このアカウント用にランダムに動画を選択
                selected_videos = random.sample(all_video_files, POSTS_PER_ACCOUNT)
                
                for video in selected_videos:
                    try:
                        # 1分から10分のランダムな待機時間を設定
                        wait_time = random.randint(60, 600)
                        logger.info(f"次の投稿まで {wait_time} 秒待機します")
                        time.sleep(wait_time)

                        video_path = os.path.join(self.videos_folder, video)
                        
                        # Cloudinaryにアップロード
                        cloudinary_url = upload_to_cloudinary(video_path)
                        
                        # Instagramコンテナを作成して公開
                        container_id = create_container(cloudinary_url, CAPTION)
                        publish_container(container_id)
                        
                        logger.info(f"アカウント {account['instagram_user_id']} に動画 {video} を正常に投稿しました")
                    
                    except Exception as e:
                        logger.error(f"アカウント {account['instagram_user_id']} への動画 {video} の投稿中にエラーが発生しました: {str(e)}")
                
                logger.info(f"アカウント {account['instagram_user_id']} の全ての投稿が完了しました")

        except Exception as e:
            logger.error(f"自動投稿プロセス全体でエラーが発生しました: {str(e)}")

scheduler_service = SchedulerService()