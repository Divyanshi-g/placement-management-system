import os
from flask import Flask, render_template
from enhancements import init_app as init_enhancements
from enhancements.db import close_db, init_db
def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key")    # ---------------- Config ----------------
    app.config["DATABASE"] = os.environ.get("DATABASE", "placement.db")
    app.config["UPLOAD_FOLDER_RESUMES"] = os.environ.get(
        "UPLOAD_FOLDER_RESUMES", "static/uploads/resumes")
    app.config["UPLOAD_FOLDER_PROFILES"] = os.environ.get(
        "UPLOAD_FOLDER_PROFILES", "static/uploads/profile_pics")
    app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # 5 MB limit
    os.makedirs(app.config["UPLOAD_FOLDER_RESUMES"], exist_ok=True)      # ---------------- Ensure folders exist ----------------
    os.makedirs(app.config["UPLOAD_FOLDER_PROFILES"], exist_ok=True)
    init_enhancements(app)         # ---------------- Blueprints ----------------
    print("✅ Enhancements blueprint registered.")
    with app.app_context():                          # ---------------- Database ----------------
        print(f"👉 Using database file: {app.config['DATABASE']}")
        init_db()
        print("✅ Database initialized.")
    # Ensure db is closed after each request
    app.teardown_appcontext(close_db)
    @app.route("/")          # ---------------- Routes ----------------
    def index():
        return render_template("home.html")
    return app
app = create_app()
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)



