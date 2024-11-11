from flask import request, render_template, Blueprint, session
import pypandoc
from pathlib import Path
from flask_login import current_user

from website import PROJECT_ROOT, db

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

            md_content = convert_docx_to_md(file_path)
            save_to_database(md_content)
            return render_template("resume.html.j2", markdown_content=md_content)

    return render_template("upload_resume.html.j2")


@uploads.route("/resume")
def resume() -> None:
    markdown_content = session["user"].resume
    return render_template("resume.html.j2", markdown_content=markdown_content)


def convert_docx_to_md(path: Path) -> str:
    return pypandoc.convert_file(str(path), "md")


def save_to_database(resume_md: str) -> None:
    current_user.resume = resume_md
    db.session.commit()
