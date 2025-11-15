from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import User, Dialog, EmergencyRecord, KnowledgeBase
from sqlalchemy import func
from datetime import datetime, timedelta
from functools import wraps

admin_bp = Blueprint('admin', __name__)


def admin_required(f):
    @wraps(f)  # 使用 wraps 保留原始函数信息
    @jwt_required()
    def decorated_function(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user or user.role != 'admin':
            return jsonify({'error': '需要管理员权限'}), 403
        return f(*args, **kwargs)

    return decorated_function


@admin_bp.route('/dashboard', methods=['GET'])
@admin_required
def admin_dashboard():  # 使用唯一的函数名
    """管理员仪表板数据"""
    # 基础统计
    total_users = User.query.count()
    today_logins = User.query.filter(
        User.last_login >= datetime.utcnow().date()
    ).count()

    total_dialogs = Dialog.query.count()
    pending_emergencies = EmergencyRecord.query.filter_by(status='pending').count()

    return jsonify({
        'user_stats': {
            'total_users': total_users,
            'today_logins': today_logins
        },
        'dialog_stats': {
            'total_dialogs': total_dialogs
        },
        'emergency_stats': {
            'pending_emergencies': pending_emergencies
        }
    }), 200


@admin_bp.route('/users', methods=['GET'])
@admin_required
def get_users_list():  # 使用唯一的函数名
    """获取用户列表"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    users = User.query.paginate(page=page, per_page=per_page, error_out=False)

    user_list = []
    for user in users.items:
        user_list.append({
            'id': user.id,
            'student_id': user.student_id,
            'username': user.username,
            'last_login': user.last_login.isoformat() if user.last_login else None,
            'created_at': user.created_at.isoformat()
        })

    return jsonify({
        'users': user_list,
        'total': users.total,
        'pages': users.pages,
        'current_page': page
    }), 200


@admin_bp.route('/emergencies', methods=['GET'])
@admin_required
def get_emergencies_list():  # 使用唯一的函数名
    """获取紧急情况列表"""
    emergencies = EmergencyRecord.query.filter_by(status='pending').all()

    emergency_list = []
    for emergency in emergencies:
        emergency_list.append({
            'id': emergency.id,
            'user_id': emergency.user_id,
            'username': emergency.user.username,
            'triggered_at': emergency.triggered_at.isoformat(),
            'status': emergency.status
        })

    return jsonify({'emergencies': emergency_list}), 200


@admin_bp.route('/emergencies/<int:emergency_id>/resolve', methods=['PUT'])
@admin_required
def resolve_emergency_record(emergency_id):  # 使用唯一的函数名
    """处理紧急情况"""
    data = request.get_json()
    emergency = EmergencyRecord.query.get(emergency_id)

    if not emergency:
        return jsonify({'error': '紧急记录不存在'}), 404

    emergency.status = 'resolved'
    emergency.handled_by = data.get('handler', '系统管理员')
    emergency.notes = data.get('notes', '')

    db.session.commit()

    return jsonify({'message': '处理完成'}), 200