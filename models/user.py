from flask_login import UserMixin
from models import db
from sqlalchemy import func
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    nama_lengkap = db.Column(db.String(80), nullable=False, unique=True)
    username = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    role = db.Column(db.String(20), nullable=False, default='user')
    create_at = db.Column(db.DateTime(), nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=func.now(), onupdate=func.now())

    @property
    def data(self):
        return {
            'id': self.id,
            'nama_lengkap': self.nama_lengkap,
            'username': self.username,
            'email': self.email,
            'role': self.role
        }

    def set_password(self, password):
        self.password = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_all(cls):
        r = cls.query.all()
        result = []
        for i in r:
            result.append(i.data)
        return result

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)

    def get_id(self):
        return str(self.id)
    
    @classmethod
    def get_total_users(cls):
        return cls.query.count()