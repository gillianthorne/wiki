from datetime import datetime, timedelta, timezone
import secrets

from fastapi import Response
from sqlalchemy.orm import Session as db_Session

from app.models.user import User
from app.models.session import Session


def create_session(user: User, response: Response, db: db_Session) -> None:
    token = secrets.token_urlsafe(32)
    expires_at = datetime.now(timezone.utc) + timedelta(weeks=2)

    # 2 weeks of 7 days of 24 hours of 60 minutes of 60 seconds
    max_age = 2 * 7 * 24 * 60 * 60

    new_session = Session(id=token, user_id=user.id, expires_at=expires_at)
    db.add(new_session)
    db.commit()

    response.set_cookie(
        key="session_token", 
        value=token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=max_age
    )
