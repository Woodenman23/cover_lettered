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
from flask_login import logout_user, current_user

from website import db
from website.models import CoverLetters
from ai_api import generate_letter_text


views = Blueprint("views", __name__)


@views.route("/")
def home():
    if current_user.is_authenticated:
        return render_template("home.html.j2", current_user=True)
    else:
        return render_template("home.html.j2", current_user=False)


@views.route("/about")
def about():
    return render_template("about.html.j2")


@views.route("/session_data")
def session_data():
    return jsonify(dict(session))


@views.route("/builder", methods=["POST", "GET"])
def builder():
    if request.method == "POST":
        job_title = request.form["jobTitle"].capitalize()
        job_spec = request.form["jobSpec"]
        company = request.form["company"].capitalize()
        resume = current_user.resume

        if not resume:
            letter_text = "Please upload a resume to produce a cover letter."

        letter_text = generate_letter_text(
            resume,
            job_title,
            company,
            job_spec,
        )
        cover_letter = CoverLetters(
            user_id=current_user.id,
            job_title=job_title,
            company=company,
            cover_letter=letter_text,
            job_spec=job_spec,
        )
        db.session.add(cover_letter)
        db.session.commit()

        return render_template(
            "cover_letter.html.j2",
            result=letter_text,
        )
        # TODO: handle API connection error
    return render_template("/letter_builder.html.j2")


@views.route("/profile", methods=["POST", "GET"])
def profile():
    if current_user is not None:
        latest_letter = (
            CoverLetters.query.filter_by(user_id=session["user_id"])
            .order_by(desc(CoverLetters.created_at))
            .first()
        )
        if latest_letter:
            latest_letter_content = latest_letter.cover_letter
        else:
            latest_letter_content = "No cover letter found."

        resume_content = current_user.resume

        return render_template(
            "profile.html.j2",
            username=current_user.name,
            resume=resume_content,
            latest_letter=latest_letter_content,
        )
    else:
        flash("Please log in to view your profile!")
    return redirect(url_for("auth.login"))


@views.route("/resume")
def resume():
    if current_user.resume is not None:
        resume_content = current_user.resume
        return render_template("resume.html.j2", resume_content=resume_content)
    flash("No resume found for user, please upload one!")
    return redirect(url_for("uploads.upload"))


@views.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("email", None)
    session.pop("user_id", None)
    logout_user()
    return redirect(url_for("views.home"))
