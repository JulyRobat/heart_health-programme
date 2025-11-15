from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import Config

db = SQLAlchemy()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 初始化扩展
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)

    # 注册蓝图
    from app.routes.auth import auth_bp
    from app.routes.chat import chat_bp
    from app.routes.admin import admin_bp
    from app.routes.knowledge import knowledge_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(chat_bp, url_prefix='/api/chat')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(knowledge_bp, url_prefix='/api/knowledge')

    return app