from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from main import db
from datetime import datetime
from sqlalchemy import Sequence, ForeignKey


class User(db.Model):
    user_id = db.Column(db.Integer, Sequence('user_id_seq'), primary_key=True)
    first_name = db.Column(db.String(64), index=True, nullable=False)
    last_name = db.Column(db.String(64), index=True, nullable=False)
    email = db.Column(db.String(120), index=True, nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)

    posts = relationship('Post', back_populates='user')

    def __repr__(self):
        return '<User full name: {} {}, email: {}>'.format(self.first_name, self.last_name, self.email)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Post(db.Model):
    __searchbale__ = ['title']
    id = db.Column(db.Integer, Sequence('id_seq'), primary_key=True)
    title = db.Column(db.String(100), nullable=False, unique=True)
    content = db.Column(db.Text, nullable=False)
    posted_by = db.Column(db.String(20), nullable=False, default='N/A')
    posted_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    user_id = db.Column(db.Integer, ForeignKey('user.user_id'))
    user = relationship('User', back_populates='posts')

    def __repr__(self):
        return self.title
