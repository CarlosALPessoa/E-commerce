from flask_sqlalchemy import SQLAlchemy
from argon2 import PasswordHasher

db = SQLAlchemy()
ph = PasswordHasher()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), default="user")

    def set_pw(self, password, ph):
        self.password_hash = ph.hash(password)

    def check_pw(self, password, ph):
        try:
            return ph.verify(self.password_hash, password)
        except:
            return False
