import os
from flask import Flask, render_template
from dotenv import load_dotenv
from extensions import mail

# Load environment variables from .env (if present)
load_dotenv()

# Import blueprint init and db helpers
from enhancements import init_app as init_enhancements
from enhancements.db import close_db, init_db


def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")

    # ---------------- Config ----------------
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key")
    app.config["DATABASE"] = os.environ.get("DATABASE", "placement.db")

    app.config["UPLOAD_FOLDER_RESUMES"] = os.environ.get(
        "UPLOAD_FOLDER_RESUMES", "static/uploads/resumes"
    )
    app.config["UPLOAD_FOLDER_PROFILES"] = os.environ.get(
        "UPLOAD_FOLDER_PROFILES", "static/uploads/profile_pics"
    )

    app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # 5 MB limit

    # Mail config (must exist)
    app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER")
    app.config["MAIL_PORT"] = int(os.environ.get("MAIL_PORT", 587))
    app.config["MAIL_USE_TLS"] = True
    app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
    app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
    app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_USERNAME")

    mail.init_app(app)   # ✅ THIS IS THE KEY LINE

    # ---------------- Ensure folders exist ----------------
    os.makedirs(app.config["UPLOAD_FOLDER_RESUMES"], exist_ok=True)
    os.makedirs(app.config["UPLOAD_FOLDER_PROFILES"], exist_ok=True)

    # ---------------- Blueprints ----------------
    init_enhancements(app)
    print("✅ Enhancements blueprint registered.")

    # ---------------- Database ----------------
    with app.app_context():
        print(f"👉 Using database file: {app.config['DATABASE']}")
        init_db()
        print("✅ Database initialized.")

    # Ensure db is closed after each request
    app.teardown_appcontext(close_db)

    # ---------------- Routes ----------------
    @app.route("/")
    def index():
        return render_template("home.html")

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


