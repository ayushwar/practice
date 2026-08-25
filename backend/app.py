import os

from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

from database import init_db
from routes.mood_routes import mood_bp

load_dotenv()


def create_app():
    app = Flask(__name__)

    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "sqlite:///" + os.path.join(basedir, "mahila_mitra.db")
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    init_db(app)

    # Allow the Vite dev server (and any deployed frontend) to call the API.
    CORS(app)

    app.register_blueprint(mood_bp)

    return app


app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
