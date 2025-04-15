from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    followers: Mapped[List["Follower"]] = relationship("follower", back_populates="user")
    post: Mapped[List["Post"]] = relationship("post", back_populates="user")
    comment: Mapped[List["Comment"]] = relationship("comment", back_populates="user")


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active,
            
        }
    def serialize_with_relationships(self):
        return {
            **self.serialize(),
            "followers": [f.serialize() for f in self.followers],
            "posts": [p.serialize() for p in self.posts],
            "comments": [c.serialize() for c in self.comments]
        }


class Follower(db.Model):
    __tablename__ = "follower"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_from_id: Mapped[int] = mapped_column(Integer, nullable=False)
    user_to_id: Mapped[int] = mapped_column(Integer, nullable=False)

    # Relacion
    user_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("users.id"))
    # Relación con User
    user: Mapped["User"] = relationship("user", back_populates="followers")

    def serialize(self):
        return {
            "id": self.id,
            "user_from_id": self.user_from_id,
            "user_to_id": self.user_to_id,
            "user_id": self.user_id
        }


class Post(db.Model):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)

     # Relacion
    user_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("users.id"))
    # media_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("media.id"))
    # Relación con User
    user: Mapped["User"] = relationship("user", back_populates="post")
    comment: Mapped[List["Comment"]] = relationship("comment", back_populates="post")

    # #Relacion con Media
    media: Mapped[List["Media"]] = relationship("media", back_populates="post")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "content": self.content
        }
    def serialize_with_relationships(self):
        return {
            **self.serialize(),
            "user": self.user.serialize(),
            "comments": [c.serialize() for c in self.comments],
            "media": [m.serialize() for m in self.media]
        }


class Comment(db.Model):
    __tablename__ = "comment"

    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(200))
    author_id: Mapped[int] = mapped_column(Integer, nullable=False)
    post_id: Mapped[int] = mapped_column(Integer, nullable=False)

    # Relacion
    user_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("users.id"))
    comment_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("users.id"))
    # Relación con User
    user: Mapped["User"] = relationship("user", back_populates="comment")

    # Relacion
    user_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("post.id"))
    # Relación con post
    post: Mapped["Post"] = relationship("post", back_populates="comment")

    def serialize(self):
        return {
            "id": self.id,
            "comment_text": self.comment_text,
            "author_id": self.author_id,
            "post_id": self.post_id,
            "user": self.user.serialize() if self.user else None
        }

class Media(db.Model):
    __tablename__ = "media"

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[Enum] = mapped_column(String(200))
    url: Mapped[str] = mapped_column(String(255), nullable=False)
    post_id: Mapped[int] = mapped_column(Integer, nullable=False)

    # Relacion
    post_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("post.id"))
    # Relación con User
    user: Mapped["Media"] = relationship("media", back_populates="post")

    def serialize(self):
        return {
            "id": self.id,
            "type": self.type,
            "url": self.url,
            "post_id": self.post_id
        }

