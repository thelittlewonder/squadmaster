from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


class Employee(UserMixin, db.Model):

    __tablename__ = 'employees'

    employeeid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), index=True, unique=True)
    email = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    department_id = db.Column(db.integer, db.ForeignKey(departments.id))
    role_id = db.Column(db.integer, db.ForeignKey(roles.id))
    is_admin = db.Column(db.Boolean, default=False)


@property
def password(self):
    raise AttributeError('password is not a readable attribute.')


@password.setter
def password(self, password):
    self.password_hash = generate_password_hash(password)


def verifypassword(self, password):
    return check_password_hash(self.password_hash, password)


def __repr__(self):
    return '<Employee: {}>'.format(self.username)


@login_manager.user_loader
def load_user(user_id):
    return Employee.query.get(int(user_id))

    

