# backend/app/routes/emotion.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Dialog, User  # 只导入存在的模型
from datetime import datetime, timedelta

emotion_bp = Blueprint('emotion', __name__)


@emotion_bp.route('/analysis', methods=['GET'])
@jwt_required()
def get_emotion_analysis():
    """获取用户情感分析数据"""
    user_id = get_jwt_identity()
    days = request.args.get('days', 7, type=int)

    start_date = datetime.utcnow() - timedelta(days=days)

    # 获取用户的情感数据
    emotion_data = db.session.query(
        Dialog.created_at,
        Dialog.emotion_score
    ).filter(
        Dialog.user_id == user_id,
        Dialog.role == 'user',
        Dialog.created_at >= start_date,
        Dialog.emotion_score.isnot(None)
    ).order_by(Dialog.created_at.asc()).all()

    # 处理数据
    timeline = []
    for created_at, score in emotion_data:
        timeline.append({
            'timestamp': created_at.isoformat(),
            'score': float(score),
            'date': created_at.strftime('%m-%d %H:%M')
        })

    # 计算统计信息
    scores = [float(data.emotion_score) for data in emotion_data if data.emotion_score]
    avg_score = sum(scores) / len(scores) if scores else 0.5

    return jsonify({
        'timeline': timeline,
        'statistics': {
            'average_score': avg_score,
            'total_messages': len(scores),
            'positive_count': len([s for s in scores if s > 0.6]),
            'negative_count': len([s for s in scores if s < 0.4])
        }
    }), 200


@emotion_bp.route('/summary', methods=['GET'])
@jwt_required()
def get_emotion_summary():
    """获取情感分析摘要"""
    user_id = get_jwt_identity()

    # 获取最近30天的情感数据
    start_date = datetime.utcnow() - timedelta(days=30)

    emotion_data = db.session.query(
        Dialog.emotion_score
    ).filter(
        Dialog.user_id == user_id,
        Dialog.role == 'user',
        Dialog.created_at >= start_date,
        Dialog.emotion_score.isnot(None)
    ).all()

    scores = [float(data.emotion_score) for data in emotion_data]

    if not scores:
        return jsonify({
            'message': '暂无情感数据',
            'average_score': 0.5,
            'trend': 'stable'
        }), 200

    avg_score = sum(scores) / len(scores)

    # 简单趋势分析
    recent_scores = scores[-7:]  # 最近7天
    if len(recent_scores) >= 2:
        trend = 'improving' if recent_scores[-1] > recent_scores[0] else 'declining'
    else:
        trend = 'stable'

    return jsonify({
        'average_score': avg_score,
        'total_analyzed': len(scores),
        'trend': trend,
        'recommendation': get_recommendation(avg_score, trend)
    }), 200


def get_recommendation(score, trend):
    """根据情感分数和趋势提供建议"""
    if score < 0.3:
        return "检测到情绪较低，建议多与朋友交流或寻求专业帮助"
    elif score < 0.5:
        if trend == 'declining':
            return "情绪有下降趋势，建议关注心理健康"
        else:
            return "情绪正在改善，继续保持"
    else:
        return "情绪状态良好，继续保持积极心态"