from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import get_db
from app.config import settings
from app.deps import require_role


router = APIRouter()

@router.get("/hello")
def hello(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT 1")).scalar()
    return {"status": "ok", "db name": settings.db_name, "db result": result}

@router.get("/test-editor")
def test_editor(current_user: User = Depends(require_role(20))):
    return {"message": f"Hello {current_user.username}, you have editor+ access."}