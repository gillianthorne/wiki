from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.mysql import MEDIUMTEXT

from app.database import Base


class PageRevision(Base):
    __tablename__ = "page_revisions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    revision_number: Mapped[int] = mapped_column(nullable=False) 
    content: Mapped[str] = mapped_column(MEDIUMTEXT, nullable=False)
    edited_by_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    page_id: Mapped[int] = mapped_column(ForeignKey("pages.id", ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    edited_by: Mapped[Optional["User"]] = relationship(foreign_keys=[edited_by_id])
    page: Mapped["Page"] = relationship(foreign_keys=[page_id])