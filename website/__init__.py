from flask import Flask
from pathlib import Path
from datetime import timedelta


PROJECT_ROOT = Path(__file__).parent.parent
IMAGES_PATH = PROJECT_ROOT / "website/static/images"
OPEN_AI_API_TOKEN = (Path.home() / ".ssh/openai").read_text().strip()


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "1234"
    app.permanent_session_lifetime = timedelta(days=3)

    from .views import views

    app.register_blueprint(views, url_prefix="/")

    return app
