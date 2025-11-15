from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(20), unique=True, nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    emergency_contact = db.Column(db.String(20))
    role = db.Column(db.Enum('student', 'admin'), default='student')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)

    # 关系
    dialogs = db.relationship('Dialog', backref='user', lazy=True)
    emergency_records = db.relationship('EmergencyRecord', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Dialog(db.Model):
    __tablename__ = 'dialogs'

    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    role = db.Column(db.Enum('user', 'ai'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    emotion_score = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class EmergencyRecord(db.Model):
    __tablename__ = 'emergency_records'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    triggered_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.Enum('pending', 'resolved'), default='pending')
    handled_by = db.Column(db.String(50))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class KnowledgeBase(db.Model):
    __tablename__ = 'knowledge_base'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50))
    author = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)