from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class PagePermission(Base):
    __tablename__ = "page_permissions"

    page_id: Mapped[int] = mapped_column(ForeignKey("pages.id", ondelete="CASCADE"), nullable=False, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, primary_key=True)
    permission_level: Mapped[str] = mapped_column(Enum("view", "edit"), nullable=False)

    page: Mapped["Page"] = relationship(foreign_keys=[page_id])
    user: Mapped["User"] = relationship(foreign_keys=[user_id])