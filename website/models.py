from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from website import db


class Users(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column()
    resume = relationship("Resume", back_populates="user")

    cover_letters = relationship(
        "CoverLetters", back_populates="user", cascade="all, delete-orphan"
    )


class CoverLetters(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(db.ForeignKey("users.id"), nullable="False")
    job_title: Mapped[str] = mapped_column()
    company: Mapped[str] = mapped_column()
    cover_letter: Mapped[str] = mapped_column()
    job_spec: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    user = relationship("Users", back_populates="cover_letters", uselist=False)


class Resume(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(db.ForeignKey("users.id"), nullable="False")
    filename: Mapped[str] = mapped_column()
    content: Mapped[str] = mapped_column()
    user = relationship("Users", back_populates="resume")
