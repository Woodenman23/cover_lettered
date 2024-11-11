from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash

from website.models import Users
from website import db

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        email = request.form["email"]
        session["email"] = email
        found_user = Users.query.filter_by(email=email).first()
        if found_user:
            if check_password_hash(found_user.password, request.form["password"]):
                session["user"] = found_user.name
                session["user_id"] = found_user.id
                flash("Login Successful!")
                return redirect(url_for("views.profile"))
            else:
                flash("Password incorrect, please try again.")
                return render_template("login.html.j2")
        flash(f"No user profile found for {email}, sign up!")
        return redirect(url_for("auth.sign_up"))
    else:
        if "user" in session:
            flash("Already Logged In!")
            return redirect(url_for("views.profile"))
        return render_template("login.html.j2")


@auth.route("/signup", methods=["POST", "GET"])
def sign_up():
    email = None
    if request.method == "POST":
        session.permanent = True
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        password2 = request.form["password2"]
        found_user = Users.query.filter_by(email=email).first()
        if found_user:
            flash("Account already exists, please login.")
            return redirect(url_for("auth.login"))
        elif "@" not in email:
            flash("Invalid Email", category="error")
        elif password != password2:
            flash("Passwords do not match.", category="error")
        elif not valid_password(password):
            flash(
                "Password must include both upper and lower case letters and a number.",
                category="error",
            )
        else:
            usr = Users(
                name=name,
                email=email,
                password=generate_password_hash(password),
            )
            db.session.add(usr)
            db.session.commit()

            session["email"] = usr.email
            session["user"] = usr.name
            session["user_id"] = usr.id
            flash(f"Welcome {name}!")
            return redirect(url_for("views.profile"))

    return render_template("sign-up.html.j2")


def valid_password(password: str) -> bool:
    has_cap, has_lower, has_int = False, False, False

    for letter in password:
        if letter.isupper():
            has_cap = True
        if letter.islower():
            has_lower = True
        if letter.isdigit():
            has_int = True

    if has_int == has_cap == has_lower == True:
        return True
    return False
