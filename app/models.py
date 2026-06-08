from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    role = db.Column(db.String(20), default='user')


class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False) # Tên file khi lưu trên server
    original_name = db.Column(db.String(255), nullable=False) # Tên file gốc người dùng đặt
    file_type = db.Column(db.String(50)) # Ví dụ: PDF, DOCX
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Quan hệ ngược: Để sau này khi muốn xem user đó đăng những file nào
    owner = db.relationship('User', backref=db.backref('documents', lazy=True))