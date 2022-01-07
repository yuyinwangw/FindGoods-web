from flask import current_app
from flask_login import UserMixin, AnonymousUserMixin
from sqlalchemy.orm import relationship, backref
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from . import db, login_manager


# class User(UserMixin):
#     pass


class Plform(db.Model):
    __tablename__ = 'plform'

    PFNO = db.Column(db.String(10), primary_key=True, nullable=False)
    PFNAME = db.Column(db.String(60), nullable=False)
    item = relationship("Item", backref=backref('plform', order_by=PFNO))

    def __repr__(self):
        return "<Plate Form Name %s>" % self.PFNAME


class Item(db.Model):
    __tablename__ = 'item'

    ITEMNO = db.Column(db.String(11), primary_key=True, nullable=False)
    ITEMNAME = db.Column(db.String(100), nullable=False)
    PFNO = db.Column(db.SmallInteger, db.ForeignKey('plform.PFNAME'))
    ITEMID = db.Column(db.SmallInteger, nullable=False)
    PRICE = db.Column(db.Float)
    BRAND = db.Column(db.String(16))
    CATE = db.Column(db.String(45))
    URL = db.Column(db.Text, nullable=False)
    IMG_URL = db.Column(db.Text, nullable=False)
    IMG_PATH = db.Column(db.Text, nullable=False)
    TAGS = db.Column(db.String(100))

    def __repr__(self):
        return "<Item %s>" % self.ITEMNAME


class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.String(10), primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(64), unique=True, index=True)
    sex = db.Column(db.String(8))
    age = db.Column(db.SmallInteger)
    area = db.Column(db.String(128))
    career = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    def __repr__(self):
        return '<User %r>' % self.username


class AnonymousUser(AnonymousUserMixin):
    def is_administrator(self):
        return False


login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    # user_test = User()
    # user_test.id = user_id
    return User.query.get(user_id)

