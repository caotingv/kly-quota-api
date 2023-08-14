# app/controllers/user_controller.py
from app.models.user import User
from app import db

def create_user(username, email):
    new_user = User(username=username, email=email)
    db.session.add(new_user)
    db.session.commit()

def get_all_users():
    return User.query.all()
