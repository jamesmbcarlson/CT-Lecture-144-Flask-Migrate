from database import db, Base
from sqlalchemy.orm import Mapped, mapped_column
from typing import List


class Role(Base):
    __tablename__ = "roles"
    id: Mapped[int] = mapped_column(primary_key=True)
    role_name: Mapped[str] = mapped_column(db.String(100), unique=True, nullable=False)
    customers: Mapped[List["Customer"]] = db.relationship(back_populates='role')