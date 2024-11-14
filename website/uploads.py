from flask import request, render_template, Blueprint, flash
from pathlib import Path
from flask_login import current_user
import mammoth

from website import PROJECT_ROOT, db
from ai_api import generate_letter_text

upload_folder = PROJECT_ROOT / "website/uploads"

uploads = Blueprint("uploads", __name__)


@uploads.route("/upload", methods=["GET", "POST"])
def upload() -> None:
    if request.method == "POST":
        if "file" not in request.files:
            return "No file part"

        file = request.files["file"]
        if file.filename == "":
            return "No selected file"

        if file.filename.endswith(".docx"):
            file_path = upload_folder / file.filename
            file.save(str(file_path))

            resume_content = convert_docx_to_html(file_path)

            save_to_database(resume_content)
            return render_template("resume.html.j2", resume_content=resume_content)

    return render_template("upload_resume.html.j2")


@uploads.route("/demo", methods=["POST", "GET"])
def demo():
    if request.method == "POST":
        job_title = request.form["jobTitle"].capitalize()
        job_spec = request.form["jobSpec"]
        company = request.form["company"].capitalize()
        if request.method == "POST":
            if "file" not in request.files:
                flash("No resume uploaded.")
                return render_template("demo.html.j2")
            file = request.files["file"]
            if file.filename == "":
                flash("No resume uploaded.")
                return render_template("demo.html.j2")
            if file.filename.endswith(".docx"):
                file_path = upload_folder / file.filename
                file.save(str(file_path))
                resume_content = convert_docx_to_html(file_path)

            letter_text = generate_letter_text(
                resume_content,
                job_title,
                company,
                job_spec,
            )
            return render_template(
                "cover_letter.html.j2",
                result=letter_text,
            )
        # TODO: handle API connection error
    return render_template("/demo.html.j2")


def convert_docx_to_html(path: Path) -> str:
    with open(str(path), "rb") as docx_file:
        result = mammoth.convert_to_html(docx_file)
        html = result.value
        # TODO: use messages to produce logs
        # messages = result.messages
        return html


def save_to_database(resume_md: str) -> None:
    current_user.resume = resume_md
    db.session.commit()
