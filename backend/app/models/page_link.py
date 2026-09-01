from typing import Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class PageLink(Base):
    __tablename__ = "page_links"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    page_id: Mapped[int] = mapped_column(ForeignKey("pages.id", ondelete="CASCADE"), nullable=False)
    linked_page_id: Mapped[Optional[int]] = mapped_column(ForeignKey("pages.id", ondelete="SET NULL"), nullable=True)
    link_text: Mapped[str] = mapped_column(String(255), nullable=False)

    page: Mapped["Page"] = relationship("Page", foreign_keys=[page_id])
    linked_page: Mapped[Optional["Page"]] = relationship("Page", foreign_keys=[linked_page_id])
    