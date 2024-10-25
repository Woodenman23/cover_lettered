from flask import Flask
from pathlib import Path
from flask_sqlalchemy import SQLAlchemy

PROJECT_ROOT = Path(__file__).parent.parent
IMAGES_PATH = PROJECT_ROOT / "website/static/images"


def create_app() -> Flask:
    app = Flask(__name__)
    
    from .views import views

    app.register_blueprint(views, url_prefix="/")

  
    return app