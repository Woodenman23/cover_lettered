from flask import Flask
from pathlib import Path
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

PROJECT_ROOT = Path(__file__).parent.parent
IMAGES_PATH = PROJECT_ROOT / "website/static/images"
OPEN_AI_API_TOKEN = (Path.home() / ".ssh/openai").read_text().strip()

db = SQLAlchemy()


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "1234"
    app.permanent_session_lifetime = timedelta(days=3)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.sqlite3"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    from .views import views

    app.register_blueprint(views, url_prefix="/")

    with app.app_context():
        # db.drop_all()  # FOR DEV ENVIRONMENT ONLY
        db.create_all()

    return app
