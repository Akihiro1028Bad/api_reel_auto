from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from app.services.caption_service import caption_service
from app.utils.logger import setup_logger

caption_bp = Blueprint('caption', __name__)
logger = setup_logger(__name__)

@caption_bp.route('/manage')
def manage_captions():
    """キャプション管理ページを表示する"""
    logger.info("キャプション管理ページにアクセスしました")
    captions = caption_service.get_all_captions()
    return render_template('caption/manage_captions.html', captions=captions)

@caption_bp.route('/add', methods=['POST'])
def add_caption():
    """新しいキャプションを追加する"""
    text = request.form.get('text')
    if not text:
        logger.error("キャプションのテキストが空です")
        return jsonify({'error': 'キャプションのテキストは必須です'}), 400
    
    logger.info(f"新しいキャプションを追加します: {text}")
    new_caption = caption_service.add_caption(text)
    return jsonify(new_caption)

@caption_bp.route('/update/<int:caption_id>', methods=['POST'])
def update_caption(caption_id):
    """キャプションを更新する"""
    text = request.form.get('text')
    if not text:
        logger.error("更新するキャプションのテキストが空です")
        return jsonify({'error': 'キャプションのテキストは必須です'}), 400
    
    logger.info(f"キャプションを更新します: ID {caption_id}")
    updated_caption = caption_service.update_caption(caption_id, text)
    if updated_caption:
        return jsonify(updated_caption)
    else:
        return jsonify({'error': 'キャプションが見つかりません'}), 404

@caption_bp.route('/delete/<int:caption_id>', methods=['POST'])
def delete_caption(caption_id):
    """キャプションを削除する"""
    logger.info(f"キャプションを削除します: ID {caption_id}")
    if caption_service.delete_caption(caption_id):
        return jsonify({'success': True})
    else:
        return jsonify({'error': 'キャプションが見つかりません'}), 404