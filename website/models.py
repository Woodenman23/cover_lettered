from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from flask_login import UserMixin

from website import db, login_manager


class Users(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column()
    resume: Mapped[str] = mapped_column(nullable="True")

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


@login_manager.user_loader
def load_user(id):
    return db.session.get(Users, int(id))
