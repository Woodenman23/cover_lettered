from flask import Flask
from pathlib import Path
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


class Section:
    def __init__(self, name: str) -> None:
        self.name = name
        self.title = " ".join(
            word.capitalize() for word in name.replace("_", " ").split()
        )
        self.route = "/" + name


PROJECT_ROOT = Path(__file__).parent.parent
IMAGES_PATH = PROJECT_ROOT / "website/static/images"


def get_secret(secret_name):
    secret_path = f"/run/secrets/{secret_name}"
    try:
        with open(secret_path, "r") as secret_file:
            return secret_file.read().strip()
    except FileNotFoundError:
        print(f"Secret {secret_name} not found!")
        return None


OPEN_AI_API_TOKEN = get_secret("open_ai_token")

db = SQLAlchemy()
login_manager = LoginManager()

section_names = ["about"]
SECTIONS = {name: Section(name) for name in section_names}


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "1234"
    app.permanent_session_lifetime = timedelta(days=3)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.sqlite3"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.context_processor(add_sections)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    from website.views import views
    from website.auth import auth
    from website.info import info
    from website.uploads import uploads

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(info, url_prefix="/")
    app.register_blueprint(uploads, url_prefix="/")

    with app.app_context():
        # db.drop_all()  # FOR DEV ENVIRONMENT ONLY
        db.create_all()

    return app


def add_sections():
    return {"sections": SECTIONS}
