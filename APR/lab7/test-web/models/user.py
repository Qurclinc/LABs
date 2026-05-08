from sqlalchemy.orm import Mapped, mapped_column
from flask_login import UserMixin

from .base import Base

class User(UserMixin, Base):
    __tablename__ = "users"
    
    login: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)