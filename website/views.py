from flask import Blueprint, render_template, request, session, flash, redirect, url_for

from ai_api import generate_letter
from website.models import Users
from website import db

views = Blueprint("views", __name__)


class Section:
    def __init__(self, name: str) -> None:
        self.name = name
        self.title = " ".join(
            word.capitalize() for word in name.replace("_", " ").split()
        )
        self.route = "/" + name


with open("cover_letter.txt", "r") as file:
    latest_letter = file.read()

section_names = ["about"]

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


@views.route("/builder", methods=["POST", "GET"])
def builder():
    global latest_letter
    if request.method == "POST":
        job_spec = request.form["jobSpec"]
        with open("resume.txt", "r") as file:
            resume = file.read()
        result = generate_letter(resume, job_spec)
        latest_letter = result
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
        email = request.form["email"]
        session["email"] = email
        found_user = Users.query.filter_by(email=email).first()
        if found_user:
            print(found_user.password)
            if str(found_user.password) == request.form["password"]:
                session["user"] = found_user.name
                flash("Login Successful!")
                return redirect(url_for("views.profile"))
            else:
                flash("Password incorrect, please try again.")
                return render_template("login.html.j2")
        flash(f"No user profile found for {email}, sign up!")
        return redirect(url_for("views.sign_up"))
    else:
        if "user" in session:
            flash("Already Logged In!")
            return redirect(url_for("views.profile"))
        return render_template("login.html.j2")


@views.route("/signup", methods=["POST", "GET"])
def sign_up():
    email = None
    if request.method == "POST":
        session.permanent = True
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        found_user = Users.query.filter_by(email=email).first()
        if found_user:
            flash("Account already exists, please login.")
            return redirect(url_for("views.login"))
        usr = Users(name=name, email=email, password=password)
        session["email"] = usr.email
        session["user"] = usr.name

        db.session.add(usr)
        db.session.commit()
        flash(f"Welcome {name}!")
        return redirect(url_for("views.profile"))
    return render_template("sign-up.html.j2")


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
    return redirect(url_for("views.login"))


@views.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("email", None)
    return redirect(url_for("views.home"))


def no_result() -> str:
    return render_template(
        "cover_letter.html.j2",
        result="I cannot summarize this, try something else.",
    )
