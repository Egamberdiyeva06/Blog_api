from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, ForeignKey, UniqueConstraint

from database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(length=50))
    last_name: Mapped[str] = mapped_column(String(length=50))
    username: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)

    posts: Mapped[list["Post"]] = relationship("Post", back_populates="user", cascade="all, delete-orphan", lazy='selectin')
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="user", lazy='selectin')
    likes: Mapped[list["Like"]] = relationship("Like", back_populates="user", lazy='selectin')
    liked_posts: Mapped[list['Post']] = relationship("Post", secondary='likes', viewonly=True, lazy='selectin')


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(length=100))
    content: Mapped[str] = mapped_column(Text)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user: Mapped["User"] = relationship("User", back_populates="posts")
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="post", cascade="all, delete-orphan", lazy='selectin')
    likes: Mapped[list["Like"]] = relationship("Like", back_populates="post", cascade="all, delete-orphan", lazy='selectin')

    @property
    def likes_count(self) -> int:
        return len(self.likes)

    @property
    def comments_count(self) -> int:
        return len(self.comments)


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    text: Mapped[str] = mapped_column(Text)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id", ondelete="CASCADE"))

    user: Mapped["User"] = relationship(back_populates='comments', lazy='selectin')
    post: Mapped["Post"] = relationship(back_populates='comments', lazy='selectin')


class Like(Base):
    __tablename__ = "likes"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id", ondelete="CASCADE"))

    user: Mapped["User"] = relationship(back_populates="likes", lazy='selectin')
    post: Mapped["Post"] = relationship(back_populates="likes", lazy='selectin')

    __table_args__ = (UniqueConstraint("user_id", "post_id", name = "unique_user_post_like"),)