from flask import Blueprint, render_template, request, session, flash, redirect, url_for

from website import db
from website.models import CoverLetters
from ai_api import generate_letter_text


views = Blueprint("views", __name__)


with open("cover_letter.txt", "r") as file:
    latest_letter = file.read()


@views.route("/")
def home():
    return render_template("home.html.j2", logo="default_logo")


@views.route("/about")
def about():
    return render_template("about.html.j2")


@views.route("/builder", methods=["POST", "GET"])
def builder():
    global latest_letter
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

        print(letter_text)

        latest_letter = letter_text
        if latest_letter == None:
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
        return render_template(
            "profile.html.j2",
            username=session["user"],
            email=session["email"],
            latest_letter=latest_letter,
        )
    else:
        flash("Please log in to view your profile!")
    return redirect(url_for("auth.login"))


@views.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("email", None)
    session.pop("user_id", None)
    return redirect(url_for("views.home"))


def no_result() -> str:
    return render_template(
        "cover_letter.html.j2",
        result="I cannot summarize this, try something else.",
    )
