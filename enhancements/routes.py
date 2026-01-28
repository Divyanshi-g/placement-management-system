# enhancements/routes.py
import io
import os
import json
import csv
import uuid
import sqlite3
import requests
import random, smtplib
from extensions import mail
from flask_mail import Message
from datetime import datetime, timedelta
from openai import OpenAI
from flask import (
    Blueprint, request, jsonify, render_template, make_response,
    redirect, url_for, session, flash, current_app, send_from_directory, abort
)
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

from .resume_checker import analyze_resume
from .db import get_db_conn  # ✅ central db helpers
enhancements_bp = Blueprint("enhancements", __name__, template_folder="../templates")

otp_store = {}

# ----------------- AI Function -----------------
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")  # Load once globally

def generate_ai_answer(question):
    if not OPENROUTER_API_KEY:
        return "⚠️ OpenRouter API key is not set."

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://your-deployed-site.com",  # 🔴 change this
        "X-Title": "Placement Management System"
    }

    payload = {
        "model": "openai/gpt-4o-mini",   # ✅ FIXED MODEL
        "messages": [
            {"role": "system", "content": "You are a helpful college placement assistant."},
            {"role": "user", "content": question}
        ],
        "max_tokens": 300,
        "temperature": 0.7
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)

        # 🔍 DEBUG (important)
        if response.status_code != 200:
            return f"⚠️ OpenRouter Error {response.status_code}: {response.text}"

        data = response.json()
        return data["choices"][0]["message"]["content"].strip()

    except requests.exceptions.RequestException as e:
        return f"⚠️ Network error: {str(e)}"
    except (KeyError, IndexError):
        return "⚠️ Unexpected response format from OpenRouter."



def chat_with_ai(user_message, role="student"):
    system_prompt = (
        "You are an admin assistant helping with students, placements, reports."
        if role == "admin"
        else
        "You are a student placement assistant helping with careers and interviews."
    )

    payload = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
    }

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://placement-management-system",
        "X-Title": "Placement Management System",
        "Content-Type": "application/json"
    }

    r = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=30
    )

    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]


HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
HF_MODEL = "google/flan-t5-base"

def call_huggingface(prompt):
    url = f"https://api-inference.huggingface.co/models/{HF_MODEL}"
    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_KEY}"
    }
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 300
        }
    }

    r = requests.post(url, headers=headers, json=payload, timeout=30)
    r.raise_for_status()
    data = r.json()

    if isinstance(data, list):
        return data[0].get("generated_text", "")
    return "Unable to analyze resume."

@enhancements_bp.route("/check_resume", methods=["POST"])
def check_resume():
    try:
        if "resume" not in request.files:
            return jsonify({"error": "No resume uploaded"}), 400

        user_id = session.get("user_id")
        if not user_id:
            return jsonify({"error": "Login required"}), 401

        file = request.files["resume"]
        filename = secure_filename(file.filename)

        save_path = os.path.join(
            get_upload_folder(),
            f"{int(datetime.utcnow().timestamp())}_{filename}"
        )
        file.save(save_path)

        # ---- BASIC LOCAL ANALYSIS ----
        from enhancements.resume_checker import analyze_resume
        local_result = analyze_resume(save_path)

        # ---- HUGGINGFACE ATS ----
        hf_feedback = "AI feedback unavailable."
        if HUGGINGFACE_API_KEY:
            prompt = f"""
You are an ATS resume checker.
Give feedback in bullet points and improvement suggestions.

Resume analysis:
{json.dumps(local_result)}
"""
            try:
                hf_feedback = call_huggingface(prompt)
            except Exception:
                pass  # silently fail AI, do NOT break UI

        # ---- SAVE TO DB ----
        conn = get_db_conn()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO resumes (user_id, filename, storage_path, verdict, details)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                user_id,
                filename,
                save_path,
                local_result.get("verdict"),
                json.dumps({
                    "basic": local_result,
                    "hf_feedback": hf_feedback
                })
            )
        )
        conn.commit()
        conn.close()

        # ---- RESPONSE MATCHES JS ----
        return jsonify({
            "result": f"""
ATS Verdict: {local_result.get("verdict")}

Score: {local_result.get("score_percent", "N/A")}%

AI Feedback:
{hf_feedback}
"""
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

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
            ADMIN_SECRET_CODE = "ADMIN2026"  # change anytime

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
        show_back_button=True,
         back_url=url_for("index"),
        current_year=2026
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
        show_back_button=True,
        back_url=url_for("enhancements.register"),
        current_year=2026
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
        home_url=url_for("enhancements.student_dashboard"),
        show_back_button=True,
        back_url=url_for("enhancements.login"),
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


# --------------------
# VERIFY OLD PASSWORD (Step 1)
# --------------------
@enhancements_bp.route("/verify-old-password", methods=["POST"])
def verify_old_password():
    if "user_id" not in session:
        return jsonify({"success": False, "message": "Login required"})

    data = request.get_json(silent=True) or {}
    old_password = data.get("old_password", "").strip()

    if not old_password:
        return jsonify({"success": False, "message": "Old password required"})

    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("SELECT password FROM users WHERE id=?", (session["user_id"],))
    user = cur.fetchone()
    conn.close()

    if not user or not check_password_hash(user[0], old_password):
        return jsonify({"success": False, "message": "Incorrect old password"})

    return jsonify({"success": True})

# --------------------
# SEND OTP (Forgot Password)
# --------------------
@enhancements_bp.route("/send-otp", methods=["POST"])
def send_otp():
    data = request.get_json(silent=True) or {}
    email = data.get("email", "").strip()

    if not email:
        return jsonify({"success": False, "message": "Email required"})

    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE email=?", (email,))
    user = cur.fetchone()
    conn.close()

    if not user:
        return jsonify({"success": False, "message": "Email not registered"})

    otp = random.randint(100000, 999999)
    otp_store[email] = {
        "otp": str(otp),
        "expires": datetime.now() + timedelta(minutes=5),
        "attempts": 3
    }

    # optional: send email
    # msg = Message("HireHub Password Reset OTP", recipients=[email])
    # msg.body = f"Your OTP is {otp}. It is valid for 5 minutes."
    # mail.send(msg)

    return jsonify({"success": True})

# --------------------
# VERIFY OTP
# --------------------
@enhancements_bp.route("/verify-otp", methods=["POST"])
def verify_otp():
    data = request.get_json(silent=True) or {}
    email = data.get("email", "").strip()
    otp_input = data.get("otp", "").strip()

    if email not in otp_store:
        return jsonify({"success": False, "message": "OTP expired"})

    record = otp_store[email]

    if datetime.now() > record["expires"]:
        del otp_store[email]
        return jsonify({"success": False, "message": "OTP expired"})

    if record["attempts"] <= 0:
        del otp_store[email]
        return jsonify({"success": False, "message": "Too many attempts"})

    if record["otp"] != otp_input:
        record["attempts"] -= 1
        return jsonify({
            "success": False,
            "message": f"Incorrect OTP ({record['attempts']} left)"
        })

    return jsonify({"success": True})

# --------------------
# UPDATE PASSWORD (Step 2 / Step 3)
# --------------------
@enhancements_bp.route("/update-password", methods=["POST"])
def update_password():
    data = request.get_json(silent=True) or {}
    
    # If logged-in user, email can be ignored
    user_id = session.get("user_id")
    email = data.get("email", "").strip()  # for forgot password flow
    new_password = data.get("password")   # matches JS
    confirm_password = data.get("confirm_password") or new_password

    if new_password != confirm_password:
        return jsonify({"success": False, "message": "Passwords do not match"})

    # Password strength check (same as JS)
    import re
    pwd_regex = re.compile(r"^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$")
    if not pwd_regex.match(new_password):
        return jsonify({"success": False, "message": "Password too weak"})

    hashed = generate_password_hash(new_password)

    conn = get_db_conn()
    cur = conn.cursor()

    if user_id:
        # Logged-in user flow
        cur.execute("UPDATE users SET password=? WHERE id=?", (hashed, user_id))
    elif email and email in otp_store:
        # Forgot password flow
        cur.execute("UPDATE users SET password=? WHERE email=?", (hashed, email))
        del otp_store[email]
    else:
        conn.close()
        return jsonify({"success": False, "message": "Session expired"})

    conn.commit()
    conn.close()
    return jsonify({"success": True})

@enhancements_bp.route("/placements")
def placements():
    if "user_id" not in session:
        return redirect(url_for("enhancements.login"))

    user_id = session["user_id"]   # ✅ ADD THIS LINE

    conn = get_db_conn()
    cur = conn.cursor()

    q = request.args.get("q", "").strip()
    location = request.args.get("location", "").strip()
    job_type = request.args.get("job_type", "").strip()

    sql = """
        SELECT p.*,
        (
            SELECT COUNT(*)
            FROM applications a
            WHERE a.user_id = ? AND a.placement_id = p.id
        ) AS applied
        FROM placements p
        WHERE 1 = 1
    """

    params = [user_id]

    if q:
        sql += " AND (p.company LIKE ? OR p.role LIKE ?)"
        params.extend([f"%{q}%", f"%{q}%"])

    if location:
        sql += " AND p.location LIKE ?"
        params.append(f"%{location}%")

    if job_type:
        sql += " AND p.job_type LIKE ?"
        params.append(f"%{job_type}%")

    cur.execute(sql, params)
    jobs = cur.fetchall()

    return render_template(
        "placements.html",
        jobs=jobs,
        show_nav_options=True,
        is_admin=False,
        home_url=url_for("enhancements.student_dashboard"),
        show_back_button=True,
        back_url=url_for("enhancements.student_dashboard")
    )

@enhancements_bp.route("/apply/<int:placement_id>", methods=["GET", "POST"])
def apply(placement_id):
    if "user_id" not in session:
        return redirect(url_for("enhancements.login"))

    user_id = session["user_id"]
    conn = get_db_conn()
    cur = conn.cursor()

    # ✅ Verify placement exists
    cur.execute(
        "SELECT company, role FROM placements WHERE id = ?",
        (placement_id,)
    )
    placement = cur.fetchone()
    if not placement:
        abort(404, "Placement not found")

    # ✅ Verify user exists
    cur.execute("SELECT id FROM users WHERE id = ?", (user_id,))
    if not cur.fetchone():
        abort(403, "Invalid user")

    # ================= GET =================
    if request.method == "GET":
        return render_template(
            "apply.html",
            placement={
                "company": placement["company"],
                "role": placement["role"]
            },
            show_nav_options=True,
            is_admin=False,
            home_url=url_for("enhancements.student_dashboard"),
            show_back_button=True,
            back_url=url_for("enhancements.placements")
        )

    # ================= POST =================
    student_name = request.form["student_name"]
    phone = request.form["phone"]
    course = request.form["course"]

    # ✅ CLEAN SKILLS (dropdown + typing safe)
    raw_skills = request.form.get("skills", "")
    skills = ", ".join(
        [s.strip() for s in raw_skills.split(",") if s.strip()]
    )

    experience = request.form.get("experience")
    resume_file = request.files.get("resume")
    resume_filename = None

    if resume_file and resume_file.filename:
        resume_filename = secure_filename(resume_file.filename)
        resume_path = os.path.join(
            "static/uploads/resumes",
            resume_filename
        )
        resume_file.save(resume_path)

    # ✅ Prevent duplicate applications
    cur.execute("""
        SELECT id FROM applications
        WHERE user_id = ? AND placement_id = ?
    """, (user_id, placement_id))
    if cur.fetchone():
        flash("⚠️ You have already applied for this placement.")
        return redirect(request.url)

    # ✅ Safe insert
    cur.execute("""
        INSERT INTO applications (
            user_id, placement_id,
            student_name, phone, course,
            skills, experience, resume
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id, placement_id,
        student_name, phone, course,
        skills, experience, resume_filename
    ))

    conn.commit()
    conn.close()

    flash("✅ Application submitted successfully!")
    return redirect(url_for("enhancements.placements"))

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

    # -------- FOLDERS --------
    PROFILE_PIC_FOLDER = os.path.join(current_app.root_path, "static", "uploads", "profile_pics")
    RESUME_FOLDER = os.path.join(current_app.root_path, "static", "uploads", "resumes")
    os.makedirs(PROFILE_PIC_FOLDER, exist_ok=True)
    os.makedirs(RESUME_FOLDER, exist_ok=True)

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
        home_url=url_for("enhancements.student_dashboard"),
        show_back_button=True,
        back_url=url_for("enhancements.student_dashboard")
    )

# ------------------ Practice ------------------

@enhancements_bp.route("/practice")
def practice():
    return render_template("practice.html",
        show_nav_options=True,
        is_admin=False,
        home_url=url_for("enhancements.student_dashboard"),
        show_back_button=True,
        back_url=url_for("enhancements.student_dashboard")                   
    )

@enhancements_bp.route("/delete-attempt", methods=["POST"])
def delete_attempt():
    data = request.get_json()
    attempt_id = data.get("id")

    if not attempt_id:
        return jsonify({"success": False, "error": "No ID provided"})

    try:
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute("DELETE FROM attempts WHERE id = ?", (attempt_id,))
        conn.commit()
        conn.close()
        return jsonify({"success": True})
    except Exception as e:
        print(e)
        return jsonify({"success": False, "error": str(e)})
@enhancements_bp.route("/status")
def status():
    if "user_id" not in session or session.get("role") != "student":
        return redirect(url_for("enhancements.login"))

    user_id = session["user_id"]

    conn = get_db_conn()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            applications.id,
            applications.status,
            applications.applied_at,
            applications.skills,
            applications.experience,
            applications.resume,

            placements.company,
            placements.role,
            placements.location,
            placements.salary,
            placements.job_type,
            placements.duration,
            placements.eligibility,
            placements.deadline
        FROM applications
        JOIN placements ON placements.id = applications.placement_id
        WHERE applications.user_id = ?
        ORDER BY applications.applied_at DESC
    """, (user_id,))

    rows = cursor.fetchall()
    conn.close()
    applications = []
    for r in rows:
        applications.append({
            "status": r["status"],
            "applied_at": r["applied_at"],
            "skills": r["skills"],
            "experience": r["experience"],
            "resume": r["resume"],
            "placement": {
                "company": r["company"],
                "role": r["role"],
                "location": r["location"],
                "salary": r["salary"],
                "job_type": r["job_type"],
                "duration": r["duration"],
                "eligibility": r["eligibility"],
                "deadline": r["deadline"]
            }
        })

    return render_template(
        "status.html",
        applications=applications,
        show_nav_options=True,
        home_url=url_for("enhancements.student_dashboard"),
        show_back_button=True,
        back_url=url_for("enhancements.student_dashboard")
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

    # Default values (if no login)
    is_admin = False
    back_url = url_for("enhancements.student_dashboard")

    if role == "admin":
        is_admin = True
        back_url = url_for("enhancements.admin_dashboard")
    elif role == "student":
        is_admin = False
        back_url = url_for("enhancements.student_dashboard")

    return render_template(
        "about.html",
        show_nav_options=True,
        is_admin=is_admin,
        home_url=home_url,
        show_back_button=True,
        back_url=back_url

    )
@enhancements_bp.route("/rate", methods=["GET", "POST"])
def rate():
    conn = get_db_conn()
    cur = conn.cursor()
    user_id = session.get("user_id")
    role = session.get("role")

    if request.method == "POST":
        if not user_id:
            flash("You must be logged in to rate.", "warning")
            conn.close()
            return redirect(url_for("enhancements.login"))

        # ⭐ SAFE RATING FETCH (prevents crash)
        rating_value = request.form.get("rating")

        if not rating_value or not rating_value.isdigit():
            flash("Please select a rating (1–5 stars).", "warning")
            conn.close()
            return redirect(url_for("enhancements.rate"))

        rating = int(rating_value)
        comment = request.form.get("comment", "").strip()

        if not (1 <= rating <= 5):
            flash("Please select a valid rating (1–5 stars).", "warning")
            conn.close()
            return redirect(url_for("enhancements.rate"))

        # Ensure user exists (prevents foreign key error)
        user_exists = cur.execute(
            "SELECT id FROM users WHERE id = ?", (user_id,)
        ).fetchone()

        if not user_exists:
            session.clear()
            flash("Invalid session. Please login again.", "danger")
            conn.close()
            return redirect(url_for("enhancements.login"))

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

    # -------------------- GET PAGE --------------------
    existing_user_feedback = None
    if user_id:
        existing_user_feedback = cur.execute(
            "SELECT rating, comment FROM feedback WHERE user_id = ?",
            (user_id,),
        ).fetchone()

    feedbacks = cur.execute(
        """
        SELECT f.id, f.rating, f.comment, f.created_at, u.username
        FROM feedback f
        LEFT JOIN users u ON f.user_id = u.id
        ORDER BY f.created_at DESC
        """
    ).fetchall()

    conn.close()

    return render_template(
        "rate.html",
        feedbacks=feedbacks,

        # ⭐ send this to template
        user_feedback=existing_user_feedback,

        show_nav_options=True,
        is_admin=(role == "admin"),
        home_url=(
            url_for("enhancements.admin_dashboard")
            if role == "admin"
            else url_for("enhancements.student_dashboard")
        ),
        show_back_button=True,
        back_url=(
            url_for("enhancements.admin_dashboard")
            if role == "admin"
            else url_for("enhancements.student_dashboard")
        ),
    )

# ------------------ Admin Pages ------------------
@enhancements_bp.route("/admin_dashboard")
def admin_dashboard():
    # --- NAVBAR + ACCESS CONTROL LOGIC ---
    user_id = session.get("user_id")
    role = session.get("role")
    username = session.get("username", "Admin")

    # If not logged in
    if not user_id:
        flash("Please login to continue.", "warning")
        return redirect(url_for("enhancements.login"))

    # --- DATABASE QUERIES ---
    conn = get_db_conn()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM users WHERE role='student'")
    student_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM placements")
    placement_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM applications")
    application_count = cur.fetchone()[0]

    conn.close()

    counts = {
        "students": student_count,
        "placements": placement_count,
        "applications": application_count
    }

    # Pass navbar logic + data to template
    return render_template(
        "admin_dashboard.html",
        counts=counts,
        show_nav_options=True,
        username=username,
        is_logged_in=True,
        is_admin=True,
        show_back_button=True,
        back_url=url_for("enhancements.login")
    )
@enhancements_bp.route("/admin/students")
def admin_students():
    if "user_id" not in session or session.get("role") != "admin":
        return redirect(url_for("enhancements.login"))

    conn = get_db_conn()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            users.id,
            users.username,
            users.email,
            COALESCE(profiles.phone, 'Not Added') AS phone,
            COALESCE(profiles.course, 'Not Added') AS course
        FROM users
        LEFT JOIN profiles 
            ON profiles.user_id = users.id
        WHERE users.role = 'student'
        ORDER BY users.id DESC
    """)

    students = cursor.fetchall()
    conn.close()

    return render_template(
        "admin/students.html",
        students=students,
        show_nav_options=True,
        is_admin=True,
        home_url=url_for("enhancements.admin_dashboard"),
        show_back_button=True,
        back_url=url_for("enhancements.admin_dashboard")
    )

@enhancements_bp.route("/admin/student/<int:user_id>")
def view_student_profile(user_id):

    if "user_id" not in session or session.get("role") != "admin":
        return redirect(url_for("enhancements.login"))

    conn = get_db_conn()
    conn.row_factory = sqlite3.Row   # <<< IMPORTANT
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            users.id AS user_id,
            users.username,
            users.email,

            COALESCE(profiles.full_name, '') AS full_name,
            COALESCE(profiles.phone, '') AS phone,
            COALESCE(profiles.gender, '') AS gender,
            COALESCE(profiles.course, '') AS course,
            COALESCE(profiles.branch, '') AS branch,
            COALESCE(profiles.passing_year, '') AS passing_year,
            COALESCE(profiles.cgpa, '') AS cgpa,
            COALESCE(profiles.bio, '') AS bio,

            COALESCE(profiles.skills, '') AS skills,
            COALESCE(profiles.certifications, '') AS certifications,
            COALESCE(profiles.linkedin, '') AS linkedin,
            COALESCE(profiles.github, '') AS github,

            COALESCE(profiles.profile_pic, '') AS profile_pic,
            COALESCE(profiles.resume, '') AS resume

        FROM users
        LEFT JOIN profiles 
            ON profiles.user_id = users.id
        WHERE users.id = ? 
          AND users.role = 'student'
    """, (user_id,))

    student = cursor.fetchone()
    conn.close()

    if not student:
        return "Student not found", 404

    return render_template(
        "admin/view_student_profile.html",
        student=student,
        show_nav_options=True,
        is_admin=True,
        home_url=url_for("enhancements.admin_dashboard"),
        show_back_button=True,
        back_url=url_for("enhancements.students")
    )

@enhancements_bp.route("/admin/placements")
def admin_placements():
    conn = get_db_conn()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("""
        SELECT 
            id,
            company,
            role,
            location,
            salary
        FROM placements
        ORDER BY id DESC
    """)

    placements = cur.fetchall()
    conn.close()

    return render_template(
        "admin/placements.html",
        placements=placements,
        show_nav_options=True,
        is_admin=True,
        home_url=url_for("enhancements.admin_dashboard"),
        show_back_button=True,
        back_url=url_for("enhancements.admin_dashboard")
    )
@enhancements_bp.route("/admin/placement_details/<int:id>", methods=["GET","POST"])
def placement_details(id):
    conn = get_db_conn()
    cur = conn.cursor()
    if request.method == "POST":
        data = request.form

        update_fields = [
            "role","location","salary","job_type",
            "duration","eligibility","description",
            "deadline","link"
        ]

        for field in update_fields:
            value = data.get(field)
            if value is not None and value.strip() != "":
                cur.execute(f"UPDATE placements SET {field}=? WHERE id=?", (value, id))

        conn.commit()
        flash("Placement Updated Successfully", "success")

        # 🔥 FIX HERE
        return redirect(url_for("enhancements.placement_details", id=id))

    cur.execute("SELECT * FROM placements WHERE id = ?", (id,))
    placement = cur.fetchone()

    conn.close()

    return render_template(
        "admin/placement_details.html",
        placement=placement,
        show_nav_options=True,
        is_admin=True,
        home_url=url_for("enhancements.admin_dashboard"),
        show_back_button=True,
        back_url=url_for("enhancements.admin_placements")
    )


@enhancements_bp.route("/admin/applications")
def admin_applications():
    if session.get("role") != "admin":
        return redirect("/")

    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            applications.id,
            users.username,
            users.email,
            placements.company,
            placements.role,
            applications.experience,
            applications.skills,
            applications.resume,
            applications.status,
            applications.applied_at
        FROM applications
        JOIN users ON applications.user_id = users.id
        JOIN placements ON applications.placement_id = placements.id
        ORDER BY applications.applied_at DESC
    """)

    applications = cur.fetchall()
    conn.close()

    return render_template("admin/applications.html", 
                           applications=applications,
                           show_nav_options=True,
                           is_admin=True,
                           home_url=url_for("enhancements.admin_dashboard"),
                           show_back_button=True,
                           back_url=url_for("enhancements.admin_dashboard")
                          )
@enhancements_bp.route("/admin/application/status/<int:app_id>", methods=["POST"])
def update_application_status(app_id):
    if session.get("role") != "admin":
        return redirect("/")

    new_status = request.form.get("status")

    conn = get_db_conn()
    cur = conn.cursor()

    cur.execute("UPDATE applications SET status = ? WHERE id = ?", (new_status, app_id))
    conn.commit()
    conn.close()

    flash("Status updated successfully!", "success")
    return redirect("/admin/applications")


@enhancements_bp.route("/manage_students")
def manage_students():
    conn = get_db_conn()
    cur = conn.cursor()
    # 1️⃣ Fetch all students with profile data (ONLY what is NOT in applications)
    cur.execute("""
        SELECT 
            u.id,
            u.username,
            u.email,
            pr.phone,
            pr.gender,
            pr.course,
            pr.branch,
            pr.passing_year,
            pr.cgpa,
            pr.bio,
            pr.linkedin,
            pr.github
        FROM users u
        LEFT JOIN profiles pr ON pr.user_id = u.id
        WHERE u.role = 'student'
        ORDER BY u.created_at DESC
    """)
    students_raw = cur.fetchall()

    students = []

    # 2️⃣ For each student → fetch applications (skills + resume ONLY from applications)
    for s in students_raw:
        cur.execute("""
            SELECT 
                p.company,
                p.role,
                a.status,
                a.applied_at,
                a.skills,
                a.experience,
                a.resume
            FROM applications a
            JOIN placements p ON p.id = a.placement_id
            WHERE a.user_id = ?
            ORDER BY a.applied_at DESC
        """, (s["id"],))
        applications = cur.fetchall()

        # Merge student + applications
        students.append({
            "id": s["id"],
            "username": s["username"],
            "email": s["email"],

            # 🔹 Profile-only fields
            "phone": s["phone"],
            "gender": s["gender"],
            "course": s["course"],
            "branch": s["branch"],
            "passing_year": s["passing_year"],
            "cgpa": s["cgpa"],
            "bio": s["bio"],
            "linkedin": s["linkedin"],
            "github": s["github"],
            # 🔹 Applications (skills + resume from HERE ONLY)
            "applications": [
                {
                    "company": a["company"],
                    "role": a["role"],
                    "status": a["status"],
                    "applied_at": a["applied_at"],
                    "skills": a["skills"],
                    "resume": a["resume"],
                    "experience": a["experience"],
                } for a in applications
            ],

            # 🔹 Used for search matching in cards
            "skills": " ".join([a["skills"] or "" for a in applications])
        })

    conn.close()

    return render_template(
        "manage_students.html",
         students=students,
         show_nav_options=True,
         is_admin=True,
         home_url=url_for("enhancements.admin_dashboard"),
         show_back_button=True,
         back_url=url_for("enhancements.admin_dashboard")
    )
@enhancements_bp.route("/manage_placements", methods=["GET"])
def manage_placements():
    conn = get_db_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT * FROM placements
        ORDER BY created_at DESC
    """)
    placements = cur.fetchall()
    conn.close()

    return render_template(
        "manage_placements.html",
        placements=placements,
        show_nav_options=True,
        is_admin=True,
        home_url=url_for("enhancements.admin_dashboard"),
        show_back_button=True,
        back_url=url_for("enhancements.admin_dashboard")
    )

@enhancements_bp.route("/delete_placement/<int:pid>", methods=["POST"])
def delete_placement(pid):
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM placements WHERE id=?", (pid,))
    conn.commit()
    conn.close()
    flash("❌ Placement deleted.", "info")
    return redirect(url_for("enhancements.manage_placements"))


@enhancements_bp.route("/add_placement", methods=["GET", "POST"])
def add_placement():
    conn = get_db_conn()
    cur = conn.cursor()

    if request.method == "POST":
        data = (
            request.form.get("company"),
            request.form.get("role"),
            request.form.get("location"),
            request.form.get("description"),
            request.form.get("eligibility"),
            request.form.get("salary"),
            request.form.get("deadline"),
        )

        if not data[0] or not data[1] or not data[2]:
            flash("⚠️ Company, Role and Location are required.", "danger")
            return redirect(url_for("enhancements.add_placement"))

        cur.execute("""
            INSERT INTO placements
            (company, role, location, description, eligibility, salary, deadline)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, data)

        conn.commit()
        conn.close()
        flash("✅ Company added successfully!", "success")
        return redirect(url_for("enhancements.manage_placements"))

    return render_template("add_placement.html",
                           show_nav_options=True,
                           is_admin=True,
                           home_url=url_for("enhancements.admin_dashboard"),
                           show_back_button=True,
                           back_url=url_for("enhancements.manage_placements")
                          
                          )


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
        success_rate=round(success_rate, 2),
        show_nav_options=True,
        is_admin=True,
        home_url=url_for("enhancements.admin_dashboard"),
        show_back_button=True,
        back_url=url_for("enhancements.admin_dashboard")
    )

# ---------------- Chat Page ----------------
@enhancements_bp.route("/ask", methods=["GET"])
def ask():
    if "user_id" not in session:
        return redirect(url_for("enhancements.login"))

    return render_template("ask.html",
                           show_nav_options=True,
                           is_admin=False,
                           home_url=url_for("enhancements.student_dashboard"),
                           show_back_button=True,
                           back_url=url_for("enhancements.student_dashboard")
                          )
@enhancements_bp.route("/ask/message", methods=["POST"])
def ask_message():
    if "user_id" not in session:
        return jsonify({"error": "Login required"}), 401

    data = request.get_json()
    question = data.get("question")

    if not question:
        return jsonify({"error": "Empty question"}), 400

    conn = get_db_conn()
    cur = conn.cursor()

    # verify user exists
    cur.execute("SELECT id FROM users WHERE id = ?", (session["user_id"],))
    if not cur.fetchone():
        return jsonify({"error": "Invalid user"}), 401

    conversation_id = data.get("conversation_id") or str(uuid.uuid4())

    # save user message
    cur.execute("""
        INSERT INTO chat_logs (user_id, conversation_id, role, content)
        VALUES (?, ?, 'user', ?)
    """, (session["user_id"], conversation_id, question))

    answer = generate_ai_answer(question)  # your AI logic

    # save bot message
    cur.execute("""
        INSERT INTO chat_logs (user_id, conversation_id, role, content)
        VALUES (?, ?, 'bot', ?)
    """, (session["user_id"], conversation_id, answer))

    conn.commit()

    return jsonify({
        "answer": answer,
        "conversation_id": conversation_id
    })

# ---------------- Chat History ----------------
@enhancements_bp.route("/chat/history", methods=["GET"])
def chat_history():
    if "user_id" not in session:
        return jsonify([])

    conn = get_db_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT conversation_id, MAX(created_at) as last_time
        FROM chat_logs
        WHERE user_id = ?
        GROUP BY conversation_id
        ORDER BY last_time DESC
    """, (session["user_id"],))

    rows = cur.fetchall()
    conn.close()

    return jsonify([
        {
            "conversation_id": r["conversation_id"],
            "preview": "Open chat"
        }
        for r in rows
    ])

@enhancements_bp.route("/chat/history/<conversation_id>", methods=["GET"])
def chat_history_detail(conversation_id):
    if "user_id" not in session:
        return jsonify([])

    conn = get_db_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT role, content
        FROM chat_logs
        WHERE user_id = ? AND conversation_id = ?
        ORDER BY created_at
    """, (session["user_id"], conversation_id))

    rows = cur.fetchall()
    conn.close()

    return jsonify([
        {"role": r["role"], "content": r["content"]}
        for r in rows
    ])


@enhancements_bp.route("/chat/new", methods=["GET"])
def chat_new():
    if "user_id" not in session:
        flash("⚠️ Login required.", "warning")
        return redirect(url_for("enhancements.login"))

    return render_template(
        "ask.html",
        show_nav_options=True,
        is_admin=False,
        home_url=url_for("enhancements.student_dashboard"),
        new_chat=True,
        show_back_button=True,
        back_url=url_for("enhancements.student_dashboard")
    )

@enhancements_bp.route("/admin/questions1", methods=["GET"])
def admin_questions1():
    if "user_id" not in session or session.get("role") != "admin":
        return redirect(url_for("enhancements.login"))

    return render_template("admin/questions1.html",
                            show_nav_options=True,
                            is_admin=True,
                            home_url=url_for("enhancements.admin_dashboard"),
                            show_back_button=True,
                            back_url=url_for("enhancements.admin_dashboard")
                          )
@enhancements_bp.route("/admin/questions1/message", methods=["POST"])
def admin_questions1_message():
    if "user_id" not in session or session.get("role") != "admin":
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    user_message = data.get("message")
    reply = chat_with_ai(user_message, role="admin")

    return jsonify({"reply": reply})


