from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import db
from app.models import User
from datetime import datetime

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    student_id = data.get('student_id')
    password = data.get('password')

    if not student_id or not password:
        return jsonify({'error': '学号和密码不能为空'}), 400

    user = User.query.filter_by(student_id=student_id).first()

    if user and user.check_password(password):
        user.last_login = datetime.utcnow()
        db.session.commit()

        # 生成JWT令牌
        access_token = create_access_token(
            identity=user.id,
            additional_claims={'role': user.role, 'username': user.username}
        )

        return jsonify({
            'message': '登录成功',
            'access_token': access_token,
            'user': {
                'id': user.id,
                'username': user.username,
                'student_id': user.student_id,
                'role': user.role
            }
        }), 200
    else:
        return jsonify({'error': '学号或密码错误'}), 401


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    student_id = data.get('student_id')
    username = data.get('username')
    password = data.get('password')
    emergency_contact = data.get('emergency_contact')

    if not all([student_id, username, password]):
        return jsonify({'error': '请填写完整信息'}), 400

    if User.query.filter_by(student_id=student_id).first():
        return jsonify({'error': '该学号已注册'}), 400

    user = User(
        student_id=student_id,
        username=username,
        emergency_contact=emergency_contact,
        role='student'
    )
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({'message': '注册成功'}), 201