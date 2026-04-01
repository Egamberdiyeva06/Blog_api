from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Text
from database import Base

class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(length=100))
    content: Mapped[str] = mapped_column(Text)
