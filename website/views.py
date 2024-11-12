from flask import (
    Blueprint,
    render_template,
    request,
    session,
    flash,
    redirect,
    url_for,
    jsonify,
)
from sqlalchemy import desc
from flask_login import logout_user

from website import db
from website.models import CoverLetters
from ai_api import generate_letter_text


views = Blueprint("views", __name__)


@views.route("/")
def home():
    return render_template("home.html.j2", logo="default_logo")


@views.route("/about")
def about():
    return render_template("about.html.j2")


@views.route("/session_data")
def session_data():
    return jsonify(dict(session))


@views.route("/builder", methods=["POST", "GET"])
def builder():
    if request.method == "POST":
        job_title = request.form["jobTitle"]
        job_spec = request.form["jobSpec"]
        company = request.form["company"]

        with open("resume.txt", "r") as file:
            resume = file.read()
        letter_text = generate_letter_text(
            resume,
            job_title,
            company,
            job_spec,
        )
        cover_letter = CoverLetters(
            user_id=session["user_id"],
            job_title=job_title,
            company=company,
            cover_letter=letter_text,
            job_spec=job_spec,
        )
        db.session.add(cover_letter)
        db.session.commit()
        if letter_text is None:
            return no_result()
        return render_template(
            "cover_letter.html.j2",
            result=letter_text,
        )
        # TODO: handle API connection error
    return render_template("/letter_builder.html.j2")


@views.route("/profile", methods=["POST", "GET"])
def profile():
    if "user" in session:
        latest_letter = (
            CoverLetters.query.filter_by(user_id=session["user_id"])
            .order_by(desc(CoverLetters.created_at))
            .first()
        )

        # Check if a cover letter was found before accessing its content
        if latest_letter:
            latest_letter_content = latest_letter.cover_letter
        else:
            latest_letter_content = "No cover letter found."

        return render_template(
            "profile.html.j2",
            username=session["user"],
            email=session["email"],
            latest_letter=latest_letter_content,
        )
    else:
        flash("Please log in to view your profile!")
    return redirect(url_for("auth.login"))


@views.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("email", None)
    session.pop("user_id", None)
    logout_user()
    return redirect(url_for("views.home"))


def no_result() -> str:
    return render_template(
        "cover_letter.html.j2",
        result="I cannot summarize this, try something else.",
    )
