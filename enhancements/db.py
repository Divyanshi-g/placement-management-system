import os
import sqlite3
from flask import g, current_app


# --------------------------------
# DATABASE CONNECTION
# --------------------------------
def get_db_conn():
    if "db_conn" not in g:
        db_path = current_app.config.get("DATABASE", "placement.db")

        if not os.path.isabs(db_path):
            db_path = os.path.join(current_app.instance_path, db_path)

        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        conn = sqlite3.connect(db_path, timeout=30)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")

        g.db_conn = conn

    return g.db_conn


def close_db(e=None):
    db = g.pop("db_conn", None)
    if db is not None:
        db.close()


# --------------------------------
# INITIALIZE DATABASE
# --------------------------------
def init_db():
    db = get_db_conn()
    cur = db.cursor()

    # --------------------------------
    # USERS
    # --------------------------------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT CHECK(role IN ('student','admin')) NOT NULL DEFAULT 'student',
        phone TEXT,
        skills TEXT,
        profile_pic TEXT,
        resume TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # --------------------------------
    # PLACEMENTS
    # --------------------------------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS placements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company TEXT NOT NULL,
        role TEXT NOT NULL,
        location TEXT NOT NULL,
        salary TEXT,
        job_type TEXT,
        eligibility TEXT,
        description TEXT,
        deadline TEXT,
        link TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # --------------------------------
    # APPLICATIONS
    # --------------------------------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        placement_id INTEGER NOT NULL,
        status TEXT DEFAULT 'Applied',
        applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (placement_id) REFERENCES placements(id) ON DELETE CASCADE
    )
    """)

    # --------------------------------
    # RESUMES
    # --------------------------------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS resumes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        filename TEXT,
        score TEXT,
        feedback TEXT,
        uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)

    # --------------------------------
    # CHAT LOGS
    # --------------------------------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS chat_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        sender TEXT,
        message TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)

    # --------------------------------
    # FEEDBACK
    # --------------------------------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        rating INTEGER CHECK(rating BETWEEN 1 AND 5),
        comment TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)

    # --------------------------------
    # SEED DATA (15 COMPANIES)
    # --------------------------------
    cur.execute("SELECT COUNT(*) FROM placements")
    if cur.fetchone()[0] == 0:
        cur.executemany("""
        INSERT INTO placements
        (company, role, location, salary, job_type, eligibility, description, deadline, link)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, [

        ("Google", "Software Engineer", "Bangalore", "₹18–25 LPA", "Full-time",
         "B.Tech CS/IT",
         "Work on highly scalable distributed systems used by millions of users worldwide. "
         "You will design, develop, test, and maintain software solutions while collaborating "
         "with global engineering teams.",
         "2025-12-31", "https://careers.google.com"),

        ("Amazon", "Data Engineer", "Hyderabad", "₹16–22 LPA", "Full-time",
         "B.Tech / Data Science",
         "Design and maintain large-scale data pipelines, work with AWS services, optimize "
         "data workflows, and enable business decision-making through analytics.",
         "2025-11-30", "https://www.amazon.jobs"),

        ("Microsoft", "Cloud Support Engineer", "Pune", "₹14–20 LPA", "Full-time",
         "B.Tech CS/IT",
         "Provide enterprise-level cloud solutions, troubleshoot Azure environments, and "
         "support global customers with mission-critical systems.",
         "2025-12-15", "https://careers.microsoft.com"),

        ("Infosys", "Java Developer", "Mysore", "₹6–8 LPA", "Full-time",
         "Any Graduate",
         "Develop enterprise Java applications, participate in SDLC phases, and work "
         "on real-world client projects across multiple domains.",
         "2025-12-20", "https://www.infosys.com/careers"),

        ("TCS", "System Analyst", "Mumbai", "₹7–9 LPA", "Full-time",
         "Any Graduate",
         "Analyze business requirements, coordinate with development teams, and ensure "
         "successful implementation of IT solutions for clients.",
         "2025-12-10", "https://www.tcs.com/careers"),

        ("Accenture", "AI Intern", "Gurgaon", "₹40k/month", "Internship",
         "B.Tech / M.Tech",
         "Work on artificial intelligence and automation projects involving data processing, "
         "model training, and enterprise transformation initiatives.",
         "2025-11-25", "https://www.accenture.com/careers"),

        ("Deloitte", "Business Analyst", "Bangalore", "₹10–14 LPA", "Full-time",
         "B.Tech / MBA",
         "Analyze complex business problems, create data-driven insights, and support "
         "clients in strategic and operational decision-making.",
         "2025-12-05", "https://www.deloitte.com/careers"),

        ("Flipkart", "Frontend Developer", "Bangalore", "₹12–18 LPA", "Full-time",
         "React / JavaScript",
         "Build modern, high-performance user interfaces, collaborate with designers, "
         "and improve customer experience at scale.",
         "2025-12-18", "https://www.flipkartcareers.com"),

        ("Adobe", "UX Designer Intern", "Noida", "₹35k/month", "Internship",
         "UI/UX Portfolio",
         "Design intuitive user experiences, conduct usability research, and work closely "
         "with product and engineering teams.",
         "2025-12-28", "https://adobe.wd5.myworkdayjobs.com"),

        ("ISRO", "Research Scientist", "Ahmedabad", "₹15–20 LPA", "Full-time",
         "M.Tech / PhD",
         "Engage in advanced research related to satellite systems, space exploration, "
         "and national-level scientific missions.",
         "2025-12-31", "https://www.isro.gov.in"),

        ("Wipro", "Project Engineer", "Bangalore", "₹6–7 LPA", "Full-time",
         "Any Graduate",
         "Work on enterprise IT solutions, development, testing, and deployment for global "
         "clients across industries.",
         "2025-12-22", "https://careers.wipro.com"),

        ("Capgemini", "Cloud Analyst", "Chennai", "₹8–12 LPA", "Full-time",
         "B.Tech CS/IT",
         "Assist in cloud migration projects, manage infrastructure, and support digital "
         "transformation initiatives.",
         "2025-12-26", "https://www.capgemini.com/careers"),

        ("Oracle", "Database Engineer", "Bangalore", "₹14–19 LPA", "Full-time",
         "SQL / PL-SQL",
         "Design, maintain, and optimize database systems, ensure data security, and support "
         "enterprise-scale applications.",
         "2025-12-29", "https://www.oracle.com/careers"),

        ("Zoho", "Backend Developer", "Chennai", "₹8–13 LPA", "Full-time",
         "Python / Java",
         "Develop robust backend services, APIs, and scalable systems for Zoho's suite of "
         "enterprise products.",
         "2025-12-27", "https://www.zoho.com/careers"),

        ("Paytm", "Product Analyst", "Noida", "₹9–14 LPA", "Full-time",
         "Analytics / SQL",
         "Analyze product metrics, user behavior, and business data to improve fintech "
         "solutions and customer engagement.",
         "2025-12-30", "https://paytm.com/careers")
        ])

    db.commit()
