# enhancements/routes.py
import io
import os
import json
import csv
import sqlite3
from datetime import datetime
from openai import OpenAI 

from datetime import datetime
from flask import (
    Blueprint, request, jsonify, render_template, make_response,
    redirect, url_for, session, flash, current_app, send_from_directory
)
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

from .api_jobs import fetch_api_jobs
from .resume_checker import analyze_resume
from .db import get_db_conn  # ✅ central db helpers
def init_app(app):
    client = OpenAI(api_key=os.getenv("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"))
    return client

# ----------------- Blueprint -----------------
enhancements_bp = Blueprint("enhancements", __name__, template_folder="../templates")

# ----------------- Config -----------------
DEFAULT_UPLOAD_FOLDER = os.environ.get("RESUME_UPLOAD_FOLDER", "staticuploads/resumes")
os.makedirs(DEFAULT_UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXT = {".pdf", ".docx", ".doc", ".txt"}


def get_upload_folder():
    """Return upload folder from config or fallback"""
    try:
        return current_app.config.get("RESUME_UPLOAD_FOLDER", DEFAULT_UPLOAD_FOLDER)
    except RuntimeError:
        return DEFAULT_UPLOAD_FOLDER

PROFILE_PIC_FOLDER = os.path.join("uploads", "profile_pics")
RESUME_FOLDER = os.path.join("uploads", "resumes")
os.makedirs(PROFILE_PIC_FOLDER, exist_ok=True)
os.makedirs(RESUME_FOLDER, exist_ok=True)
# ------------------ Auth pages ------------------
@enhancements_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        role = request.form.get("role", "student")
        admin_code = request.form.get("admin_code", "").strip()

        # 1️⃣ Basic validation
        if not username or not email or not password or not role:
            flash("All fields are required.", "warning")
            return redirect(url_for("enhancements.register"))

        # 2️⃣ Password strength validation
        if (
            len(password) < 8
            or not any(c.islower() for c in password)
            or not any(c.isupper() for c in password)
            or not any(c.isdigit() for c in password)
            or not any(c in "!@#$%^&*()-_+=<>?/{}[]" for c in password)
        ):
            flash(
                "Password must be at least 8 characters and include uppercase, lowercase, number, and special character.",
                "error",
            )
            return redirect(url_for("enhancements.register"))

        # 3️⃣ Admin verification
        if role == "admin":
            ADMIN_SECRET_CODE = "ADMIN2025"  # change anytime

            if not admin_code:
                flash("Admin verification code is required.", "error")
                return redirect(url_for("enhancements.register"))

            if admin_code != ADMIN_SECRET_CODE:
                flash("Invalid admin verification code.", "error")
                return redirect(url_for("enhancements.register"))

        # 4️⃣ Hash password
        hashed_password = generate_password_hash(password)

        conn = get_db_conn()
        cur = conn.cursor()

        try:
            cur.execute(
                """
                INSERT INTO users (username, email, password, role)
                VALUES (?, ?, ?, ?)
                """,
                (username, email, hashed_password, role),
            )
            conn.commit()

            flash("Registration successful! Please log in.", "success")
            return redirect(url_for("enhancements.login"))

        except sqlite3.IntegrityError:
            flash("Username or email already exists.", "error")
            return redirect(url_for("enhancements.register"))

    # 5️⃣ GET request — layout variables for base.html
    return render_template(
        "register.html",
        show_nav_options=False,  # hide dashboard links
        is_admin=False,          # safe default
        home_url=None,           # not needed here
        current_year=2025
    )

@enhancements_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login_id = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        # 1️⃣ Basic validation
        if not login_id or not password:
            flash("All fields are required.", "warning")
            return redirect(url_for("enhancements.login"))

        conn = get_db_conn()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT id, username, email, password, role
            FROM users
            WHERE email = ? OR username = ?
            """,
            (login_id, login_id),
        )

        user = cur.fetchone()

        # 2️⃣ User exists + password correct
        if user:
            if check_password_hash(user["password"], password):
                session.clear()

                session["user_id"] = user["id"]
                session["username"] = user["username"]
                session["role"] = user["role"]
                if user["role"] == "admin":
                    return redirect(url_for("enhancements.admin_dashboard"))
                else:
                    return redirect(url_for("enhancements.student_dashboard"))
            else:
                flash("Incorrect password.", "error")
                return redirect(url_for("enhancements.login"))

        # 3️⃣ User not found
        flash("User does not exist. Please register first.", "error")
        return redirect(url_for("enhancements.login"))

    # 4️⃣ GET request — hide navbar options
    return render_template(
        "login.html",
        show_nav_options=False,
        is_admin=False,
        home_url=None,
        current_year=2025
    )

# ------------------ Student Dashboard ------------------

@enhancements_bp.route("/student_dashboard")
def student_dashboard():
    # User must be logged in
    if "user_id" not in session:
        return redirect(url_for("enhancements.login"))

    # Only students allowed
    if session.get("role") != "student":
        return redirect(url_for("enhancements.login"))

    return render_template(
        "student_dashboard.html",
        username=session.get("username"),
        role=session.get("role"),

        # Navbar control (VERY IMPORTANT)
        show_nav_options=True,
        is_admin=False,
        home_url=url_for("enhancements.student_dashboard")
    )

@enhancements_bp.route("/app-chat", methods=["POST"])
def app_chat():
    if "user_id" not in session:
        return jsonify({
            "reply": "Please login first so I can help you properly 🙂"
        })

    data = request.get_json(silent=True) or {}
    user_message = data.get("message", "").lower().strip()

    if not user_message:
        return jsonify({"reply": "I’m listening 😊 Tell me what you need help with."})

    greetings = ["hi", "hello", "hey", "good morning", "good evening"]
    if any(word in user_message for word in greetings):
        return jsonify({
            "reply": f"Hi {session.get('username')} 👋 How can I help you today?"
        })

    if "login" in user_message:
        return jsonify({
            "reply": (
                "Having trouble logging in?\n\n"
                "✔ Make sure your email or username is correct\n"
                "✔ Check your password carefully\n"
                "✔ Try refreshing once\n\n"
                "If it still doesn’t work, tell me what error you see."
            )
        })

    if "register" in user_message or "signup" in user_message:
        return jsonify({
            "reply": (
                "For registration:\n\n"
                "• Username & email must be unique\n"
                "• Password should be strong\n"
                "• Admin users need a valid admin code\n\n"
                "Let me know what issue you’re facing."
            )
        })

    if "placement" in user_message:
        return jsonify({
            "reply": (
                "To access placements:\n\n"
                "📌 Login as student\n"
                "📌 Open Placements from dashboard\n"
                "📌 Click on a company to view details\n\n"
                "Is the placements page not opening?"
            )
        })

    if "navbar" in user_message or "menu" in user_message:
        return jsonify({
            "reply": (
                "Navbar appears only after login.\n\n"
                "If you can’t see it:\n"
                "• Refresh the page\n"
                "• Make sure you logged in successfully\n\n"
                "Tell me which page you’re on."
            )
        })

    if "image" in user_message or "photo" in user_message:
        return jsonify({
            "reply": (
                "If images aren’t showing:\n\n"
                "• Refresh the page\n"
                "• Check internet connection\n"
                "• Clear browser cache\n\n"
                "Does it happen on all pages or only one?"
            )
        })

    if "who are you" in user_message or "what can you do" in user_message:
        return jsonify({
            "reply": (
                "I’m your application assistant 🤖\n\n"
                "I can help you with:\n"
                "• Login & registration issues\n"
                "• Dashboard navigation\n"
                "• Placements help\n"
                "• App-related problems"
            )
        })

    return jsonify({
        "reply": (
            "I didn’t fully understand that 🤔\n\n"
            "You can ask me about:\n"
            "• Login problems\n"
            "• Registration issues\n"
            "• Placements\n"
            "• App navigation\n\n"
            "Try rephrasing your question."
        )
    })

# ------------------ Placement search & apply ------------------
@enhancements_bp.route("/placements")
def placements():
    if "user_id" not in session:
        return redirect(url_for("enhancements.login"))

    conn = get_db_conn()
    cur = conn.cursor()

    # ---------------- FILTER INPUTS ----------------
    q = request.args.get("q", "").strip()
    location = request.args.get("location", "").strip()
    job_type = request.args.get("job_type", "").strip()

    # ---------------- BASE QUERY ----------------
    sql = """
        SELECT p.*,
        (
            SELECT COUNT(*) FROM applications a
            WHERE a.user_id = ? AND a.placement_id = p.id
        ) AS applied
        FROM placements p
        WHERE 1 = 1
    """
    params = [session["user_id"]]

    # ---------------- SEARCH FILTER ----------------
    if q:
        sql += " AND (p.company LIKE ? OR p.role LIKE ?)"
        params.extend([f"%{q}%", f"%{q}%"])

    # ---------------- LOCATION FILTER ----------------
    if location:
        sql += " AND p.location LIKE ?"
        params.append(f"%{location}%")

    # ---------------- JOB TYPE FILTER ----------------
    if job_type:
        sql += " AND p.job_type LIKE ?"
        params.append(f"%{job_type}%")

    # ---------------- EXECUTE ----------------
    cur.execute(sql, params)
    jobs = cur.fetchall()

    # ❌ Do NOT close connection here if you still use DB later
    # conn.close()

    return render_template(
        "placements.html",
        jobs=jobs,
        status="success",
        show_nav_options=True,
        is_admin=session.get("role") == "admin",
        home_url=url_for("enhancements.student_dashboard")
    )

@enhancements_bp.route("/apply/<int:placement_id>", methods=["GET", "POST"])
def apply(placement_id):
    db = get_db_conn()
    cur = db.cursor()

    # Get placement
    cur.execute("SELECT * FROM placements WHERE id = ?", (placement_id,))
    placement = cur.fetchone()
    if not placement:
        return "Placement not found", 404

    user_id = session["user_id"]

    # Check if already applied
    cur.execute("""
        SELECT id FROM applications
        WHERE user_id = ? AND placement_id = ?
    """, (user_id, placement_id))
    already = cur.fetchone()

    if already:
        return redirect(url_for("enhancements.placements"))

    # ------------- POST SUBMISSION -------------
    if request.method == "POST":
        student_name = request.form.get("student_name")
        phone = request.form.get("phone")
        course = request.form.get("course")
        skills = request.form.get("skills")
        experience = request.form.get("experience")

        # ---------- Resume Upload ----------
        resume_file = None
        file = request.files.get("resume")

        if file and file.filename != "":
            upload_folder = current_app.config["UPLOAD_FOLDER_RESUMES"]
            os.makedirs(upload_folder, exist_ok=True)

            filename = secure_filename(file.filename)
            resume_path = os.path.join(upload_folder, filename)

            file.save(resume_path)
            resume_file = filename

        # ---------- Ensure user exists ----------
        cur.execute("SELECT id FROM users WHERE id = ?", (user_id,))
        if not cur.fetchone():
            db.close()
            return "User not found in users table.", 400

        # ---------- Insert Applications ----------
        cur.execute("""
            INSERT INTO applications (user_id, placement_id)
            VALUES (?, ?)
        """, (int(user_id), placement_id))

        app_id = cur.lastrowid

        # ---------- Insert Application Details ----------
        cur.execute("""
            INSERT INTO applications
            (application_id, student_name, phone, course, skills, experience, resume_file)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (app_id, student_name, phone, course, skills, experience, resume_file))

        db.commit()
        return redirect(url_for("enhancements.placements"))

    # ---------- GET REQUEST ----------
    return render_template(
        "apply.html",
        placement=placement,
        show_nav_options=True,
        is_admin=False,
        home_url=url_for("enhancements.student_dashboard")
    )
# ------------------ Profile ------------------
@enhancements_bp.route("/profile", methods=["GET", "POST"])
def profile():
    if "user_id" not in session:
        return redirect(url_for("enhancements.login"))

    conn = get_db_conn()
    cur = conn.cursor()

    # -------- NAVBAR + USER VALIDATION --------
    cur.execute("SELECT id, role, username, email FROM users WHERE id = ?", (session["user_id"],))
    user_row = cur.fetchone()

    if not user_row:
        flash("User not found. Please login again.", "danger")
        return redirect(url_for("enhancements.login"))

    username = user_row["username"]
    email = user_row["email"]

    # -------- PROFILE UPDATE --------
    if request.method == "POST":

        fields = {
            "full_name": request.form.get("full_name", "").strip(),
            "phone": request.form.get("phone", "").strip(),
            "gender": request.form.get("gender", "").strip(),
            "course": request.form.get("course", "").strip(),
            "branch": request.form.get("branch", "").strip(),
            "passing_year": request.form.get("passing_year", "").strip(),
            "cgpa": request.form.get("cgpa", "").strip(),
            "bio": request.form.get("bio", "").strip(),
            "skills": request.form.get("skills", "").strip(),
            "certifications": request.form.get("certifications", "").strip(),
            "linkedin": request.form.get("linkedin", "").strip(),
            "github": request.form.get("github", "").strip()
        }

        # -------- PROFILE PIC --------
        profile_pic_file = request.files.get("profile_pic")
        profile_pic_filename = None
        if profile_pic_file and profile_pic_file.filename:
            profile_pic_filename = secure_filename(profile_pic_file.filename)
            profile_pic_file.save(os.path.join(PROFILE_PIC_FOLDER, profile_pic_filename))

        # -------- RESUME --------
        resume_file = request.files.get("resume")
        resume_filename = None
        if resume_file and resume_file.filename:
            resume_filename = secure_filename(resume_file.filename)
            resume_file.save(os.path.join(RESUME_FOLDER, resume_filename))

        # -------- CHECK PROFILE EXISTS --------
        cur.execute("SELECT id FROM profiles WHERE user_id = ?", (session["user_id"],))
        profile_exists = cur.fetchone()

        if profile_exists:
            cur.execute("""
                UPDATE profiles
                SET full_name = COALESCE(NULLIF(?, ''), full_name),
                    phone = COALESCE(NULLIF(?, ''), phone),
                    gender = COALESCE(NULLIF(?, ''), gender),
                    course = COALESCE(NULLIF(?, ''), course),
                    branch = COALESCE(NULLIF(?, ''), branch),
                    passing_year = COALESCE(NULLIF(?, ''), passing_year),
                    cgpa = COALESCE(NULLIF(?, ''), cgpa),
                    bio = COALESCE(NULLIF(?, ''), bio),
                    skills = COALESCE(NULLIF(?, ''), skills),
                    certifications = COALESCE(NULLIF(?, ''), certifications),
                    linkedin = COALESCE(NULLIF(?, ''), linkedin),
                    github = COALESCE(NULLIF(?, ''), github),
                    profile_pic = COALESCE(?, profile_pic),
                    resume = COALESCE(?, resume)
                WHERE user_id = ?
            """, (
                fields["full_name"], fields["phone"], fields["gender"],
                fields["course"], fields["branch"], fields["passing_year"],
                fields["cgpa"], fields["bio"], fields["skills"],
                fields["certifications"], fields["linkedin"], fields["github"],
                profile_pic_filename, resume_filename,
                session["user_id"]
            ))

        else:
            cur.execute("""
                INSERT INTO profiles 
                (user_id, full_name, phone, gender, course, branch, passing_year, cgpa,
                 bio, skills, certifications, linkedin, github, profile_pic, resume)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                session["user_id"],
                fields["full_name"], fields["phone"], fields["gender"],
                fields["course"], fields["branch"], fields["passing_year"],
                fields["cgpa"], fields["bio"], fields["skills"],
                fields["certifications"], fields["linkedin"], fields["github"],
                profile_pic_filename, resume_filename
            ))

        conn.commit()
        flash("✅ Profile updated successfully!", "success")
        return redirect(url_for("enhancements.profile"))

    # -------- PROFILE FETCH --------
    cur.execute("""
        SELECT u.username, u.email,
               p.full_name, p.phone, p.gender, p.course, p.branch,
               p.passing_year, p.cgpa, p.bio,
               p.skills, p.certifications,
               p.linkedin, p.github,
               p.profile_pic, p.resume
        FROM users u
        LEFT JOIN profiles p ON u.id = p.user_id
        WHERE u.id = ?
    """, (session["user_id"],))

    row = cur.fetchone()
    conn.close()

    if not row:
        flash("User data could not be loaded.", "danger")
        return redirect(url_for("enhancements.login"))

    user = {
        "username": row["username"],
        "email": row["email"],
        "full_name": row["full_name"],
        "phone": row["phone"],
        "gender": row["gender"],
        "course": row["course"],
        "branch": row["branch"],
        "passing_year": row["passing_year"],
        "cgpa": row["cgpa"],
        "bio": row["bio"],
        "skills": row["skills"],
        "certifications": row["certifications"],
        "linkedin": row["linkedin"],
        "github": row["github"],
        "profile_pic": row["profile_pic"],
        "resume": row["resume"]
    }

    return render_template(
        "profile.html",
        user=user,
        show_nav_options=True,
        is_admin=False,
        home_url=url_for("enhancements.student_dashboard")
    )
# ------------------ Practice ------------------

@enhancements_bp.route("/practice")
def practice():
    return render_template("practice.html",
        show_nav_options=True,
        is_admin=False,
        home_url=url_for("enhancements.student_dashboard")
    )
#--------logout--------
@enhancements_bp.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("enhancements.login"))

#---------about--------
@enhancements_bp.route("/about")
def about():
    role = session.get("role")

    # Default values (if no login)
    is_admin = False
    home_url = url_for("enhancements.student_dashboard")

    if role == "admin":
        is_admin = True
        home_url = url_for("enhancements.admin_dashboard")
    elif role == "student":
        is_admin = False
        home_url = url_for("enhancements.student_dashboard")

    return render_template(
        "about.html",
        show_nav_options=True,
        is_admin=is_admin,
        home_url=home_url
    )
@enhancements_bp.route("/rate", methods=["GET", "POST"])
def rate():
    conn = get_db_conn()
    cur = conn.cursor()

    user_id = session.get("user_id")
    role = session.get("role")

    # -------------------- POST: Submit / Update Rating --------------------
    if request.method == "POST":
        if not user_id:
            flash("You must be logged in to rate.", "warning")
            conn.close()
            return redirect(url_for("enhancements.login"))

        # --- Check if user actually exists (Prevents FOREIGN KEY crash) ---
        user_exists = cur.execute(
            "SELECT id FROM users WHERE id = ?", (user_id,)
        ).fetchone()

        if not user_exists:
            session.clear()
            flash("Your account session is invalid. Please login again.", "danger")
            conn.close()
            return redirect(url_for("enhancements.login"))

        # Get form data
        rating = int(request.form.get("rating", 0))
        comment = request.form.get("comment", "").strip()

        # Validation
        if rating == 0:
            flash("Please select a rating before submitting.", "warning")
            conn.close()
            return redirect(url_for("enhancements.rate"))

        if not comment:
            flash("Feedback cannot be empty. Please write something.", "warning")
            conn.close()
            return redirect(url_for("enhancements.rate"))

        if not (1 <= rating <= 5):
            flash("Invalid rating. Please select between 1 and 5 stars.", "danger")
            conn.close()
            return redirect(url_for("enhancements.rate"))

        # Check if already rated
        existing = cur.execute(
            "SELECT id FROM feedback WHERE user_id = ?", (user_id,)
        ).fetchone()

        if existing:
            cur.execute(
                """
                UPDATE feedback
                SET rating = ?, comment = ?, created_at = CURRENT_TIMESTAMP
                WHERE user_id = ?
                """,
                (rating, comment, user_id),
            )
            flash("Your feedback has been updated! ⭐", "success")
        else:
            cur.execute(
                "INSERT INTO feedback (user_id, rating, comment) VALUES (?, ?, ?)",
                (user_id, rating, comment),
            )
            flash("Thanks for your feedback! ⭐", "success")

        conn.commit()
        conn.close()
        return redirect(url_for("enhancements.rate"))

    # -------------------- GET: Show Ratings --------------------
    feedbacks = cur.execute(
        """
        SELECT f.id, f.rating, f.comment, f.created_at, u.username
        FROM feedback f 
        LEFT JOIN users u ON f.user_id = u.id
        ORDER BY f.created_at DESC
        """
    ).fetchall()

    conn.close()

    # -------- Navbar Logic --------
    return render_template(
        "rate.html",
        feedbacks=feedbacks,
        show_nav_options=True,
        is_admin=(role == "admin"),
        home_url=(
            url_for("enhancements.admin_dashboard")
            if role == "admin"
            else url_for("enhancements.student_dashboard")
        ),
    )


# ------------------ Admin Pages ------------------

@enhancements_bp.route("/admin_dashboard")
def admin_dashboard():
    conn = get_db_conn()
    cur = conn.cursor()

    # Count students
    cur.execute("SELECT COUNT(*) FROM users WHERE role='student'")
    student_count = cur.fetchone()[0]

    # Count placements
    cur.execute("SELECT COUNT(*) FROM placements")
    placement_count = cur.fetchone()[0]

    # Count applications
    cur.execute("SELECT COUNT(*) FROM applications")
    application_count = cur.fetchone()[0]

    conn.close()

    counts = {
        "students": student_count,
        "placements": placement_count,
        "applications": application_count
    }

    username = session.get("username", "Admin")
    return render_template("admin_dashboard.html", counts=counts, username=username)
@enhancements_bp.route("/admin/students")
def admin_students():
    conn = get_db_conn()
    cur = conn.cursor()

    # Fetch all required student details
    cur.execute("""
        SELECT 
            id,
            username,
            email,
            phone,
            skills
        FROM users
        WHERE role = 'student'
        ORDER BY id DESC
    """)

    students = cur.fetchall()
    conn.close()

    return render_template("admin/students.html", students=students)


@enhancements_bp.route("/admin/placements")
def admin_placements():
    conn = get_db_conn()
    conn.row_factory = sqlite3.Row   # ⭐ IMPORTANT
    cur = conn.cursor()

    cur.execute("""
        SELECT 
            id,
            company,
            role,
            location,
            deadline
        FROM placements
    """)

    placements = cur.fetchall()
    conn.close()

    return render_template(
        "admin/placements.html",
        placements=placements
    )

def applications():
    """
    Enhanced admin applications view:
    - supports search (q), status filter
    - supports pagination (page, per_page)
    - computes total_applications and status_counts for badges
    - returns applications as list of dicts with keys used by template
    """
    # read query params
    q = (request.args.get("q") or "").strip()
    status_filter = (request.args.get("status") or "").strip()
    try:
        page = max(1, int(request.args.get("page", 1)))
    except ValueError:
        page = 1
    try:
        per_page = max(1, int(request.args.get("per_page", 20)))
    except ValueError:
        per_page = 20

    offset = (page - 1) * per_page

    conn = get_db_conn()
    cur = conn.cursor()

    # Build base WHERE and params for both count and fetch queries
    where_clauses = ["1=1"]
    params = []

    if q:
        where_clauses.append("(u.email LIKE ? OR p.company LIKE ? OR p.role LIKE ?)")
        q_like = f"%{q}%"
        params.extend([q_like, q_like, q_like])

    if status_filter:
        where_clauses.append("a.status = ?")
        params.append(status_filter)

    where_sql = " AND ".join(where_clauses)

    # Total count
    count_sql = f"""
        SELECT COUNT(*) AS cnt
        FROM applications a
        JOIN users u ON a.user_id = u.id
        JOIN placements p ON a.placement_id = p.id
        WHERE {where_sql}
    """
    cur.execute(count_sql, params)
    total_row = cur.fetchone()
    total_applications = total_row[0] if total_row else 0

    # Status counts (for badges)
    status_counts_sql = f"""
        SELECT a.status, COUNT(*) as cnt
        FROM applications a
        JOIN users u ON a.user_id = u.id
        JOIN placements p ON a.placement_id = p.id
        WHERE {where_sql}
        GROUP BY a.status
    """
    cur.execute(status_counts_sql, params)
    status_counts_rows = cur.fetchall()
    status_counts = {}
    for r in status_counts_rows:
        # r[0] is status, r[1] is count
        status_counts[r[0]] = r[1]

    # Fetch paginated application rows, include resume filename and user/profile info
    fetch_sql = f"""
        SELECT 
            a.id,
            u.id AS user_id,
            u.email AS student_email,
            u.profile_pic AS profile_pic,
            p.company || ' - ' || p.role AS placement_name,
            COALESCE(a.status, 'Applied') AS status,
            a.applied_at,
            r.filename AS resume
        FROM applications a
        JOIN users u ON a.user_id = u.id
        JOIN placements p ON a.placement_id = p.id
        LEFT JOIN resumes r ON r.user_id = u.id
        WHERE {where_sql}
        ORDER BY a.applied_at DESC
        LIMIT ? OFFSET ?
    """
    fetch_params = params + [per_page, offset]
    cur.execute(fetch_sql, fetch_params)
    rows = cur.fetchall()

    # Convert rows to list of dicts the template expects
    applications = []
    for row in rows:
        # row could be sqlite3.Row (supports both dict-style and index)
        applied_at = row["applied_at"] if "applied_at" in row.keys() else row[5]
        # Format applied_at if it's a datetime-like string or object
        applied_str = ""
        if applied_at:
            try:
                # if it's stored as ISO string, try parse
                if isinstance(applied_at, str):
                    # try common formats, else show raw string
                    try:
                        dt = datetime.fromisoformat(applied_at)
                        applied_str = dt.strftime("%Y-%m-%d %H:%M")
                    except Exception:
                        applied_str = applied_at
                else:
                    # assume datetime-like object
                    applied_str = applied_at.strftime("%Y-%m-%d %H:%M")
            except Exception:
                applied_str = str(applied_at)

        # build optional student_profile_url if you have such a route (replace name if different)
        try:
            profile_url = url_for("enhancements.view_student", student_id=row["user_id"])
        except Exception:
            profile_url = None

        applications.append({
            "id": row["id"],
            "user_id": row["user_id"],
            "student_email": row["student_email"],
            "placement_name": row["placement_name"],
            "status": row["status"],
            "applied_at": applied_str,
            "resume": row["resume"],
            "profile_pic": row["profile_pic"],
            "student_profile_url": profile_url
        })

    # compute pagination helpers
    page_start = offset + 1 if total_applications > 0 else 0
    page_end = min(offset + len(applications), total_applications)

    has_prev = page > 1
    has_next = (offset + per_page) < total_applications

    # Close cursor (we rely on teardown_appcontext(close_db) for final connection close)
    cur.close()

    return render_template(
        "admin/applications.html",
        applications=applications,
        total_applications=total_applications,
        status_counts=status_counts,
        page=page,
        per_page=per_page,
        page_start=page_start,
        page_end=page_end,
        has_prev=has_prev,
        has_next=has_next
    )


@enhancements_bp.route("/admin/export_applications_csv")
def export_applications_csv():
    """
    Export applications matching the same filters (q, status) to CSV.
    """
    q = (request.args.get("q") or "").strip()
    status_filter = (request.args.get("status") or "").strip()

    conn = get_db_conn()
    cur = conn.cursor()

    where_clauses = ["1=1"]
    params = []

    if q:
        where_clauses.append("(u.email LIKE ? OR p.company LIKE ? OR p.role LIKE ?)")
        q_like = f"%{q}%"
        params.extend([q_like, q_like, q_like])

    if status_filter:
        where_clauses.append("a.status = ?")
        params.append(status_filter)

    where_sql = " AND ".join(where_clauses)

    fetch_sql = f"""
        SELECT 
            a.id,
            u.id AS user_id,
            u.email AS student_email,
            p.company AS company,
            p.role AS role,
            COALESCE(a.status, 'Applied') AS status,
            a.applied_at,
            r.filename AS resume
        FROM applications a
        JOIN users u ON a.user_id = u.id
        JOIN placements p ON a.placement_id = p.id
        LEFT JOIN resumes r ON r.user_id = u.id
        WHERE {where_sql}
        ORDER BY a.applied_at DESC
    """
    cur.execute(fetch_sql, params)
    rows = cur.fetchall()
    cur.close()

    # Create CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["application_id", "user_id", "student_email", "company", "role", "status", "applied_at", "resume_filename"])
    for r in rows:
        applied_at = r["applied_at"]
        if applied_at and not isinstance(applied_at, str):
            try:
                applied_at = applied_at.strftime("%Y-%m-%d %H:%M")
            except Exception:
                applied_at = str(applied_at)
        writer.writerow([r["id"], r["user_id"], r["student_email"], r["company"], r["role"], r["status"], applied_at, r["resume"]])

    csv_data = output.getvalue()
    output.close()

    # Return as file response
    response = make_response(csv_data)
    response.headers["Content-Disposition"] = "attachment; filename=applications_export.csv"
    response.headers["Content-Type"] = "text/csv; charset=utf-8"
    return response

@enhancements_bp.route("/admin/view_students")
def view_students():
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, username, email FROM users WHERE role='student'")
    students = cur.fetchall()
    conn.close()
    return render_template("admin/view_students.html", students=students)



# ---------------- Manage Students ----------------
from flask import request, redirect, url_for, flash

# ✅ Manage Students (list all)
@enhancements_bp.route("/manage_students")
def manage_students():
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, username, email 
        FROM users 
        WHERE role = 'student'
        ORDER BY created_at DESC
    """)
    students = cur.fetchall()
    conn.close()
    return render_template("manage_students.html", students=students)


# ✅ Edit Student
@enhancements_bp.route("/students/edit_student/<int:student_id>", methods=["GET", "POST"])
def edit_student(student_id):
    conn = get_db_conn()
    cur = conn.cursor()

    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        cur.execute("UPDATE users SET username=?, email=? WHERE id=?", 
                    (username, email, student_id))
        conn.commit()
        conn.close()
        flash("Student updated successfully!", "success")
        return redirect(url_for("enhancements.manage_students"))

    cur.execute("SELECT id, username, email FROM users WHERE id=?", (student_id,))
    student = cur.fetchone()
    conn.close()
    return render_template("students/edit_student.html", student=student)


# ✅ Delete Student
@enhancements_bp.route("/students/delete/<int:student_id>", methods=["POST"])
def delete_student(student_id):
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id=?", (student_id,))
    conn.commit()
    conn.close()
    flash("Student deleted successfully!", "success")
    return redirect(url_for("enhancements.manage_students"))


# ✅ View Student Resumes
@enhancements_bp.route("/students/student_resumes/<int:student_id>")
def student_resumes(student_id):
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM resumes WHERE user_id=?", (student_id,))
    resumes = cur.fetchall()
    conn.close()
    return render_template("students/student_resumes.html", resumes=resumes)
# ---------------- Student Applications ----------------
@enhancements_bp.route("/students/<int:student_id>/applications")
def student_applications(student_id):   # 🔥 renamed
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT a.id, p.company, p.role, a.status, a.applied_at
        FROM applications a
        JOIN placements p ON a.placement_id = p.id
        WHERE a.user_id = ?
        ORDER BY a.applied_at DESC
    """, (student_id,))
    applications = cur.fetchall()
    conn.close()
    return render_template("students/student_applications.html", applications=applications)


# ---------------- Placement Applications ----------------
@enhancements_bp.route("/view_applications/<int:pid>", methods=["GET"])
def view_applications(pid):   # 🔥 renamed
    conn = get_db_conn()
    cur = conn.cursor()

    # Fetch placement
    cur.execute("SELECT * FROM placements WHERE id = ?", (pid,))
    placement = cur.fetchone()
    if not placement:
        flash("❌ Placement not found.", "danger")
        conn.close()
        return redirect(url_for("enhancements.manage_placements"))

    # Fetch applications + join with users
    cur.execute("""
        SELECT a.id, a.status, a.applied_at,
               u.username, u.email, r.filename AS resume
        FROM applications a
        JOIN users u ON a.user_id = u.id
        LEFT JOIN resumes r ON r.user_id = u.id
        WHERE a.placement_id = ?
        ORDER BY a.applied_at DESC
    """, (pid,))
    rows = cur.fetchall()
    conn.close()

    applications = [
        {
            "id": row["id"],
            "status": row["status"],
            "applied_at": row["applied_at"],
            "username": row["username"],
            "email": row["email"],
            "resume": row["resume"]
        }
        for row in rows
    ]

    return render_template(
        "view_applications.html",
        placement=placement,
        applications=applications
    )

@enhancements_bp.route("/admin/questions1")
def admin_questions():
    return render_template("admin/questions1.html")


@enhancements_bp.route("/manage_placements", methods=["GET", "POST"])
def manage_placements():
    conn = get_db_conn()
    cur = conn.cursor()

    if request.method == "POST":
        company = request.form.get("company")
        role = request.form.get("role")
        location = request.form.get("location")
        description = request.form.get("description")
        link = request.form.get("link")

        if company and role and location:
            cur.execute("""
                INSERT INTO placements (company, role, location, description, link)
                VALUES (?, ?, ?, ?, ?)
            """, (company, role, location, description, link))
            conn.commit()
            flash("✅ Placement added successfully!", "success")
        else:
            flash("⚠️ Company, Role, and Location are required.", "danger")

        return redirect(url_for("enhancements.manage_placements"))

    # for GET → fetch all placements
    cur.execute("SELECT * FROM placements ORDER BY created_at DESC")  # ⚠️ requires created_at column
    placements = cur.fetchall()
    conn.close()
    return render_template("manage_placements.html", placements=placements)


@enhancements_bp.route("/edit_placement/<int:pid>", methods=["GET", "POST"])
def edit_placement(pid):
    conn = get_db_conn()
    cur = conn.cursor()

    if request.method == "POST":
        company = request.form.get("company")
        role = request.form.get("role")
        location = request.form.get("location")
        eligibility = request.form.get("eligibility")
        deadline = request.form.get("deadline")
        description = request.form.get("description")
        link = request.form.get("link")

        cur.execute("""
            UPDATE placements 
            SET company=?, role=?, location=?, eligibility=?, deadline=?, description=?, link=? 
            WHERE id=?
        """, (company, role, location, eligibility, deadline, description, link, pid))
        conn.commit()
        conn.close()

        flash("✅ Placement updated!", "success")
        return redirect(url_for("enhancements.manage_placements"))

    cur.execute("SELECT * FROM placements WHERE id=?", (pid,))
    placement = cur.fetchone()
    conn.close()

    return render_template("edit_placement.html", p=placement)


@enhancements_bp.route("/delete_placement/<int:pid>", methods=["POST"])
def delete_placement(pid):
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM placements WHERE id=?", (pid,))
    conn.commit()
    conn.close()
    flash("❌ Placement deleted.", "info")
    return redirect(url_for("enhancements.manage_placements"))



@enhancements_bp.route("/reports")
def reports():
    conn = get_db_conn()
    cur = conn.cursor()

    # Total counts
    cur.execute("SELECT COUNT(*) FROM users WHERE role='student'")
    total_students = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM placements")
    total_placements = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM applications")
    total_applications = cur.fetchone()[0]

    # Application status breakdown
    cur.execute("""
        SELECT status, COUNT(*) as count
        FROM applications
        GROUP BY status
    """)
    status_data = cur.fetchall()
    status_counts = {row["status"]: row["count"] for row in status_data}

    # Success rate: count students with at least 1 'Selected'
    cur.execute("""
        SELECT COUNT(DISTINCT user_id)
        FROM applications
        WHERE status = 'Selected'
    """)
    placed_students = cur.fetchone()[0]

    success_rate = (placed_students / total_students * 100) if total_students > 0 else 0

    conn.close()

    return render_template(
        "reports.html",
        total_students=total_students,
        total_placements=total_placements,
        total_applications=total_applications,
        status_counts=status_counts,
        success_rate=round(success_rate, 2)
    )



@enhancements_bp.route('/api/search_placements')
def api_search_placements():
    """
    API endpoint for live search of placements.
    Returns JSON results.
    """
    query = request.args.get("q", "").strip().lower()
    conn = get_db_conn()
    cursor = conn.cursor()

    if query:
        cursor.execute(
            "SELECT id, title, company, description FROM placements WHERE lower(title) LIKE ? OR lower(company) LIKE ? OR lower(description) LIKE ?",
            (f"%{query}%", f"%{query}%", f"%{query}%")
        )
    else:
        cursor.execute("SELECT id, title, company, description FROM placements")

    rows = cursor.fetchall()
    conn.close()

    results = []
    for row in rows:
        results.append({
            "id": row["id"],
            "title": row["title"],
            "company": row["company"],
            "description": (row["description"][:120] + "...") if row["description"] else ""
        })

    return jsonify({"results": results})

# ------------------ File Routes ------------------

@enhancements_bp.route('/uploads/profile_pics/<filename>')
def uploaded_profile_pic(filename):
    if os.path.exists(os.path.join(PROFILE_PIC_FOLDER, filename)):
        return send_from_directory(PROFILE_PIC_FOLDER, filename)
    abort(404)


@enhancements_bp.route('/uploads/resumes/<filename>')
def uploaded_resume(filename):
    if os.path.exists(os.path.join(RESUME_FOLDER, filename)):
        return send_from_directory(RESUME_FOLDER, filename)
    abort(404)


# ------------------ Resume Review ------------------

def allowed_file(filename):
    return os.path.splitext(filename)[1].lower() in ALLOWED_EXT


@enhancements_bp.route("/resume_review", methods=["GET", "POST"])
def resume_review():
    if request.method == "GET":
        return render_template("resume_review.html")

    file = request.files.get("resume")
    user_id = session.get("user_id")

    if not file or file.filename == "":
        return jsonify({"error": "No file selected"}), 400
    filename = secure_filename(file.filename)
    if not allowed_file(filename):
        return jsonify({"error": "File type not allowed"}), 400

    save_path = os.path.join(
        get_upload_folder(),
        f"{int(datetime.utcnow().timestamp())}_{filename}"
    )
    file.save(save_path)

    result = analyze_resume(save_path)

    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO resumes (user_id, filename, storage_path, verdict, details) VALUES (?, ?, ?, ?, ?)",
        (user_id, filename, save_path, result.get("verdict"), json.dumps(result))
    )
    conn.commit()
    conn.close()

    return jsonify({"result": result})


@enhancements_bp.route("/update_status/<int:app_id>", methods=["POST"])
def update_status(app_id):
    status = request.form.get("status")
    if status not in ["Applied", "Shortlisted", "Selected", "Rejected"]:
        flash("⚠️ Invalid status.", "danger")
        return redirect(request.referrer or url_for("enhancements.admin_dashboard"))

    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("UPDATE applications SET status = ? WHERE id = ?", (status, app_id))
    conn.commit()
    conn.close()

    flash("✅ Application status updated.", "success")
    return redirect(request.referrer or url_for("enhancements.admin_dashboard"))


@enhancements_bp.route('/uploads/<path:filename>')
def uploaded_file(filename):
    folder = current_app.config.get('RESUME_UPLOAD_FOLDER', 'uploads/resumes')
    return send_from_directory(folder, filename, as_attachment=False)


# ------------------ Chatbot ------------------

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@enhancements_bp.route("/ask", methods=["GET", "POST"])
def ask():
    if request.method == "GET":
        return render_template("ask.html")

    data = request.get_json() or {}
    user_question = data.get("question", "").strip()

    if not user_question:
        return jsonify({"answer": "⚠️ Please enter a question."})

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful college placement assistant."},
                {"role": "user", "content": user_question}
            ],
            max_tokens=300,
            temperature=0.7,
        )
        answer = response.choices[0].message.content.strip()
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"answer": f"⚠️ Error fetching answer: {str(e)}"})
@enhancements_bp.route('/chat', methods=['POST'])
def chat_alias():
    """
    Backward compatibility route.
    Proxies requests from /chat to /ask.
    """
    data = request.get_json() or {}
    if "message" in data:
        data["question"] = data.pop("message")
    # Reuse ask_question logic
    return ask()


@enhancements_bp.route("/check_resume", methods=["POST"])
def check_resume():
    try:
        if "resume" not in request.files:
            return jsonify({"error": "No resume uploaded"}), 400

        file = request.files["resume"]

        try:
            text = file.read().decode("utf-8", errors="ignore")
        except Exception as e:
            return jsonify({"error": f"Failed to read file: {str(e)}"}), 400

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an ATS (Applicant Tracking System)."},
                {"role": "user", "content": f"Analyze this resume:\n\n{text}"}
            ]
        )

        feedback = response.choices[0].message.content
        return jsonify({"result": feedback})

    except Exception as e:
        print("❌ Error in check_resume:", str(e))
        return jsonify({"error": str(e)}), 500



# ------------------ Misc -----------------



@enhancements_bp.route("/settings")
def settings():
    return render_template("settings.html")


@enhancements_bp.route("/status")
def status():

    return render_template("status.html")            


























































