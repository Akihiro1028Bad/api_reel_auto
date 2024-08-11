from flask import Blueprint, render_template, request, jsonify
from app.services.scheduler_service import scheduler_service
from app.utils.logger import setup_logger
import json

schedule_bp = Blueprint('schedule', __name__)
logger = setup_logger(__name__)

@schedule_bp.route('/schedule-management')
def schedule_management():
    """スケジュール管理ページを表示する"""
    logger.info("スケジュール管理ページにアクセスしました")
    return render_template('schedule/schedule_management.html')

@schedule_bp.route('/schedules/', methods=['GET'])
def get_schedules():
    """現在のスケジュールを取得する"""
    logger.info("現在のスケジュール情報を取得します")
    try:
        with open(scheduler_service.schedule_file, 'r') as f:
            schedules = json.load(f)
        return jsonify(schedules)
    except FileNotFoundError:
        logger.warning("スケジュールファイルが見つかりません")
        return jsonify({"schedule": []})
    except json.JSONDecodeError:
        logger.error("スケジュールファイルの形式が不正です")
        return jsonify({"error": "スケジュールファイルの形式が不正です"}), 500
    except Exception as e:
        logger.error(f"スケジュール情報の取得中にエラーが発生しました: {str(e)}")
        return jsonify({"error": "スケジュール情報の取得に失敗しました"}), 500

@schedule_bp.route('/schedules/', methods=['POST'])
def update_schedules():
    """スケジュールを更新する"""
    logger.info("スケジュールの更新リクエストを受信しました")
    try:
        new_schedules = request.json
        scheduler_service.save_schedule(new_schedules)
        return jsonify({"message": "スケジュールが正常に更新されました"})
    except Exception as e:
        logger.error(f"スケジュールの更新中にエラーが発生しました: {str(e)}")
        return jsonify({"error": "スケジュールの更新に失敗しました"}), 500