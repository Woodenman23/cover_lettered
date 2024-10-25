from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from wikipedia.exceptions import DisambiguationError

from website import IMAGES_PATH

views = Blueprint("views", __name__)


class Section:
    def __init__(self, name: str) -> None:
        self.name = name
        self.title = name.capitalize()
        self.route = "/" + name


section_names = ["about"]

sections = {name: Section(name) for name in section_names}


@views.route("/")
def home():
    return render_template("home.html.j2", sections=sections, logo="default_logo")


@views.route("/about")
def about():
    return render_template("about.html.j2", sections=sections)
