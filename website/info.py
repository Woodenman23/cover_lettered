from flask import Blueprint, jsonify

from website.models import Users, CoverLetters

info = Blueprint("info", __name__)


@info.route("/coverletters")
def coverletters():
    cover_letters = CoverLetters.query.all()
    cover_letters_data = [
        {
            "id": letter.id,
            "job_title": letter.job_title,
            "company": letter.company,
            "cover_letter": letter.cover_letter,
            "job_spec": letter.job_spec,
            "created_at": letter.created_at,
            "user": (
                {
                    "id": letter.user.id,
                    "name": letter.user.name,
                    "email": letter.user.email,
                }
                if letter.user
                else None
            ),
        }
        for letter in cover_letters
    ]
    return jsonify(cover_letters_data)


@info.route("/user_data")
def user_data():
    users = Users.query.all()
    users_data = [
        {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "resume": user.resume if user.resume else "",
            "cover_letters": [
                {
                    "id": letter.id,
                    "user_id": letter.user_id,
                    "job_title": letter.job_title,
                    "company": letter.company,
                    "cover_letter": letter.cover_letter,
                    "job_spec": letter.job_spec,
                    "created_at": letter.created_at,
                }
                for letter in user.cover_letters
            ],
        }
        for user in users
    ]
    return jsonify(users_data)
