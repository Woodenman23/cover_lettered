from flask import Blueprint, render_template, request
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


@views.route("/")
def home():
    return render_template("home.html.j2", sections=sections, logo="default_logo")


@views.route("/about")
def about():
    return render_template("about.html.j2", sections=sections)


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
            sections=sections,
        )
        # TODO: handle API connection error
    return render_template("/letter_builder.html.j2", sections=sections)


def no_result() -> str:
    return render_template(
        "cover_letter.html.j2",
        result="I cannot summarize this, try something else.",
        sections=sections,
    )
