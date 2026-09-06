from datetime import datetime, timezone

from fastapi import Cookie, Depends, HTTPException
from sqlalchemy import Select
from sqlalchemy.orm import Session as db_Session

from app.database import get_db
from app.models.user import User
from app.models.session import Session


def get_current_user(session_token: str | None = Cookie(default=None), db: db_Session = Depends(get_db)) -> User:
    if not session_token:
        raise HTTPException(401, "You aren't currently logged in.")

    session = db.get(Session, session_token)
    if not session:
        raise HTTPException(401, "You aren't currently logged in.")
    
    if session.expires_at.timestamp() <= datetime.now(timezone.utc).timestamp():
        raise HTTPException(401, "Session expired. Log in again.")

    user = db.get(User, session.user_id)

    return user


def require_role(min_rank: int):
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role.rank < min_rank:
            raise HTTPException(403, "You do not have permissions to perform that action. If you think you should, please contact your wiki administrator.")
        return current_user
    return role_checker