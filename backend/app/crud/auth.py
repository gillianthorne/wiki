import bcrypt
from fastapi import Response
from sqlalchemy import Select, func

from app.config import settings
from app.models.user import User
from app.models.role import Role
from app.models.session import Session

def correct_signup_code(signup_code) -> bool:
    if signup_code == settings.signup_code:
        return True
    
    return False

def is_username_taken(db, username) -> bool:
    # first we check if the username is taken
    username_taken = db.execute(Select(User.username).where(func.lower(User.username) == username.lower())).scalar()

    if username_taken is not None:
        return True

    return False

 
def create_user(db, username, password) -> User:
    role = db.execute(Select(Role.id).where(Role.name == "viewer")).scalar()

    pw_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    pw_hash = bcrypt.hashpw(pw_bytes, salt).decode('utf-8')

    new_user = User(
        username=username,
        password_hash=pw_hash,
        role_id=role
    )

    db.add(new_user)
    db.commit()

    return new_user

def username_exists(db, username) -> bool:
    user = db.execute(Select(User).where(func.lower(User.username) == username.lower())).scalar()

    if user is not None:
        return True

    return False

def correct_password(db, username, password) -> bool:
    stored_password = db.execute(Select(User.password_hash).where(func.lower(User.username) == username.lower())).scalar()
    stored_password_bytes = stored_password.encode('utf-8')
    pw_bytes = password.encode('utf-8')
    password = bcrypt.checkpw(pw_bytes, stored_password_bytes)

    if password:
        return True
    else:
        return False

def get_user(db, username) -> User:
    return db.execute(Select(User).where(func.lower(User.username) == username.lower())).scalar()

def remove_session(db, session_token) -> None:
    session = db.get(Session, session_token)
    if session is not None:
        db.delete(session)
        db.commit()
