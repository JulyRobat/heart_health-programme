from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Dialog, User, EmergencyRecord
from datetime import datetime

chat_bp = Blueprint('chat', __name__)


@chat_bp.route('/message', methods=['POST'])
@jwt_required()
def send_chat_message():
    user_id = get_jwt_identity()
    data = request.get_json()
    message = data.get('message')

    if not message:
        return jsonify({'error': '消息不能为空'}), 400

    # 保存用户消息
    user_dialog = Dialog(
        user_id=user_id,
        role='user',
        content=message,
        emotion_score=0.5  # 默认情感分数
    )
    db.session.add(user_dialog)

    # 简单的AI回复（后续可集成Ollama）
    ai_response = "感谢您分享感受。我是AI心理助手，目前系统正在完善中，很快就能为您提供更专业的支持。"

    # 保存AI回复
    ai_dialog = Dialog(
        user_id=user_id,
        role='ai',
        content=ai_response
    )
    db.session.add(ai_dialog)
    db.session.commit()

    return jsonify({
        'response': ai_response,
        'emotion_score': 0.5,
        'emotion_type': 'neutral',
        'emergency_level': 'low',
        'needs_attention': False
    }), 200


@chat_bp.route('/history', methods=['GET'])
@jwt_required()
def get_chat_history():
    user_id = get_jwt_identity()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    dialogs = Dialog.query.filter_by(user_id=user_id) \
        .order_by(Dialog.created_at.desc()) \
        .paginate(page=page, per_page=per_page, error_out=False)

    history = []
    for dialog in dialogs.items:
        history.append({
            'id': dialog.id,
            'role': dialog.role,
            'content': dialog.content,
            'emotion_score': dialog.emotion_score,
            'created_at': dialog.created_at.isoformat()
        })

    return jsonify({
        'history': history[::-1],
        'total': dialogs.total,
        'pages': dialogs.pages,
        'current_page': page
    }), 200