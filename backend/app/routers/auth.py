from fastapi import APIRouter, Cookie, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.schemas.auth import LoginRequest, SignupRequest
from app.crud.auth import correct_password, correct_signup_code, create_user, get_user, is_username_taken, remove_session, username_exists
from app.services.auth import create_session

router = APIRouter()

@router.post("/signup")
def signup(response: Response, request: SignupRequest, db: Session = Depends(get_db)):
    if not correct_signup_code(request.signup_code):
        raise HTTPException(403, "Incorrect signup code. Please try again or contact the Wiki admin for the code.")

    if is_username_taken(db, request.username):
        raise HTTPException(409, "That username is taken. Please try another.")

    new_user = create_user(db, request.username, request.password)

    create_session(new_user, response, db)

    return {
        "success": "account created",
        "username": new_user.username
    }
    
@router.post("/login")
def login(response: Response, request: LoginRequest, db: Session = Depends(get_db)):
    if not username_exists(db, request.username):
        raise HTTPException(401, "Incorrect username or password.")

    if not correct_password(db, request.username, request.password):
        raise HTTPException(401, "Incorrect username or password.")

    user = get_user(db, request.username)

    create_session(user, response, db)

    return {
        "success": "logged in",
        "username": user.username
    }

@router.post("/logout")
def logout(response: Response, session_token: str | None = Cookie(default=None), db: Session = Depends(get_db)):
    if session_token:
       remove_session(db, session_token)

    response.delete_cookie("session_token")

    return {"success": "logged out"}