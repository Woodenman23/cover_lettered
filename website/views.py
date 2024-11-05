from flask import Blueprint, render_template, request, session, flash, redirect, url_for

from ai_api import generate_letter

views = Blueprint("views", __name__)


class Section:
    def __init__(self, name: str) -> None:
        self.name = name
        self.title = " ".join(
            word.capitalize() for word in name.replace("_", " ").split()
        )
        self.route = "/" + name


section_names = ["about", "letter_builder"]

sections = {name: Section(name) for name in section_names}


@views.context_processor
def add_sections():
    return {"sections": sections}


@views.route("/")
def home():
    return render_template("home.html.j2", logo="default_logo")


@views.route("/about")
def about():
    return render_template("about.html.j2")


@views.route("/letter_builder", methods=["POST", "GET"])
def ask():
    if request.method == "POST":
        job_spec = request.form["jobSpec"]
        resume = request.form["resume"]
        result = generate_letter(job_spec, resume)
        if result == None:
            return no_result()
        return render_template(
            "cover_letter.html.j2",
            result=result,
        )
        # TODO: handle API connection error
    return render_template("/letter_builder.html.j2")


@views.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["username"]
        session["user"] = user
        flash("Login Successful!")
        return redirect(url_for("views.profile"))
    else:
        if "user" in session:
            flash("Already Logged In!")
            return redirect(url_for("views.profile"))

        return render_template("login.html.j2")


@views.route("/profile")
def profile():
    if "user" in session:
        return render_template("profile.html.j2", username=session["user"])


@views.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("views.home"))


@views.route("/signup")
def sign_up():
    return render_template("sign-up.html.j2")


def no_result() -> str:
    return render_template(
        "cover_letter.html.j2",
        result="I cannot summarize this, try something else.",
    )
