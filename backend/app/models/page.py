from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Page(Base):
    __tablename__ = "pages"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    current_revision_id: Mapped[Optional[int]] = mapped_column(ForeignKey("page_revisions.id", ondelete="SET NULL"), nullable=True)
    locked_by_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    locked_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    current_revision: Mapped[Optional["PageRevision"]] = relationship(foreign_keys=[current_revision_id])
    locked_by: Mapped[Optional["User"]] = relationship(foreign_keys=[locked_by_id])