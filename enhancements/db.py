import os
import sqlite3
from flask import g, current_app

# -------------------------------------------------
# DB CONNECTION
# -------------------------------------------------
def get_db_conn():
    if "db_conn" not in g:
        db_path = current_app.config.get("DATABASE", "placement.db")

        # store DB inside instance folder if relative
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


# -------------------------------------------------
# INIT DATABASE
# -------------------------------------------------
def init_db():
    db = get_db_conn()
    cur = db.cursor()

    # ---------------- SCHEMA ----------------
    cur.executescript("""
    
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
    );
    CREATE TABLE IF NOT EXISTS placements (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
 
       company TEXT NOT NULL,
       logo TEXT,              -- image filename or URL
       role TEXT NOT NULL,
       location TEXT NOT NULL,
 
       description TEXT,
       eligibility TEXT,                -- NEW (confirmed)
       salary TEXT,
       job_type TEXT,                   -- Full-time / Internship / Hybrid
       duration TEXT,                   -- Optional (e.g. 6 months)

       deadline TEXT,
       link TEXT,

       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS profiles (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       user_id INTEGER NOT NULL UNIQUE,

       full_name TEXT,
       phone TEXT,
       gender TEXT,
       course TEXT,
       branch TEXT,
       passing_year TEXT,
       cgpa TEXT,
       bio TEXT,

       skills TEXT,
       certifications TEXT,
       linkedin TEXT,
       github TEXT,

       profile_pic TEXT,
       resume TEXT,

       FOREIGN KEY (user_id) REFERENCES users(id)
    );
    CREATE TABLE IF NOT EXISTS feedback (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       user_id INTEGER,
       rating INTEGER NOT NULL CHECK(rating BETWEEN 1 AND 5),
       comment TEXT,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS reports (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       user_id INTEGER NOT NULL,
       report_type TEXT,
       description TEXT,
       status TEXT DEFAULT 'pending',
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

       FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
    );
    CREATE TABLE IF NOT EXISTS applications (
       id INTEGER PRIMARY KEY AUTOINCREMENT,

       user_id INTEGER NOT NULL,
       placement_id INTEGER NOT NULL,

       student_name TEXT,
       course TEXT,
       phone TEXT,

       experience TEXT,
       skills TEXT,
       resume TEXT,

       status TEXT
           CHECK(status IN ('Applied', 'Shortlisted', 'Selected', 'Rejected'))
           NOT NULL DEFAULT 'Applied',

       applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

       FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
       FOREIGN KEY (placement_id) REFERENCES placements(id) ON DELETE CASCADE
    );


    CREATE TABLE IF NOT EXISTS resumes (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       user_id INTEGER NOT NULL,
       filename TEXT,
       storage_path TEXT,
       verdict TEXT,
       details TEXT,
       uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    );

CREATE TABLE IF NOT EXISTS chat_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);

    CREATE TABLE IF NOT EXISTS notifications (
       id INTEGER PRIMARY KEY AUTOINCREMENT,

       user_id INTEGER NOT NULL,
       role TEXT CHECK(role IN ('student','admin')) NOT NULL,

       type TEXT NOT NULL,
       message TEXT NOT NULL,
       link TEXT,

       is_read INTEGER DEFAULT 0,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    );

    """)

    # ---------------- SEED DATA ----------------
    cur.execute("SELECT COUNT(*) FROM placements")
    if cur.fetchone()[0] == 0:
        cur.executemany("""
        INSERT INTO placements
        (company, role, location, description, eligibility, salary, job_type,
         duration, deadline, logo, link)
        VALUES (?,?,?,?,?,?,?,?,?,?,?)
        """, [

        ("Google", "Software Engineer", "Bangalore",
         "Work on large-scale distributed systems, improve product reliability, and build new features used by millions of users worldwide.",
         "B.Tech CS/IT", "₹15–25 LPA", "Full-Time", "NA", "2025-12-31",
         "google.png", "https://careers.google.com"),

        ("Amazon", "Data Engineer", "Hyderabad",
         "Design, build, and maintain scalable data pipelines and analytics systems supporting business intelligence.",
         "B.Tech CS/Data", "₹14–22 LPA", "Full-Time", "NA", "2025-12-20",
         "amazon.png", "https://www.amazon.jobs"),

        ("Microsoft", "Cloud Support Engineer", "Pune",
         "Provide enterprise-level technical support for Azure cloud services and assist customers globally.",
         "B.Tech CS/IT", "₹12–18 LPA", "Full-Time", "NA", "2025-12-15",
         "microsoft.png", "https://careers.microsoft.com"),

        ("TCS", "System Analyst", "Mumbai",
         "Work with clients to design business solutions, analyze requirements, and implement enterprise systems.",
         "Any Graduate", "₹6–10 LPA", "Full-Time", "NA", "2025-12-10",
         "tcs.png", "https://www.tcs.com"),

        ("Infosys", "Java Developer", "Hyderabad",
         "Develop backend enterprise applications using Java, Spring Boot, and microservices architecture.",
         "B.Tech IT/CS", "₹7–11 LPA", "Full-Time", "NA", "2025-12-18",
         "infosys.png", "https://www.infosys.com"),

        ("Accenture", "Business Technology Analyst", "Bangalore",
         "Support consulting projects involving data analysis, business process optimization, and technology solutions.",
         "B.Tech/MBA", "₹8–12 LPA", "Full-Time", "NA", "2025-12-22",
         "accenture.png", "https://www.accenture.com"),

        ("IBM", "Software Developer", "Pune",
         "Develop enterprise-grade software solutions using modern frameworks and cloud-native technologies.",
         "B.Tech CS", "₹9–14 LPA", "Full-Time", "NA", "2025-12-08",
         "ibm.png", "https://www.ibm.com"),

        ("Deloitte", "Technology Consultant", "Bangalore",
         "Assist clients with digital transformation, analytics, and system integration solutions.",
         "B.Tech/MBA", "₹10–15 LPA", "Full-Time", "NA", "2025-12-05",
         "deloitte.png", "https://www.deloitte.com"),

        ("Capgemini", "DevOps Engineer", "Kolkata",
         "Implement CI/CD pipelines, automate deployments, and manage cloud infrastructure.",
         "B.Tech CS", "₹8–13 LPA", "Full-Time", "NA", "2025-12-25",
         "capgemini.png", "https://www.capgemini.com"),

        ("Adobe", "UX Design Intern", "Noida",
         "Design intuitive user interfaces, wireframes, and prototypes for Adobe products.",
         "Design/CS", "₹30k/month", "Internship", "6 Months", "2025-12-28",
         "adobe.png", "https://adobe.wd5.myworkdayjobs.com"),

        ("Flipkart", "Frontend Developer", "Bangalore",
         "Build responsive UI using React, improve performance, and enhance user experience.",
         "B.Tech CS", "₹10–16 LPA", "Full-Time", "NA", "2025-12-18",
         "flipkart.png", "https://www.flipkartcareers.com"),

        ("Paytm", "Mobile App Developer", "Noida",
         "Develop Android/iOS features for Paytm ecosystem using modern frameworks.",
         "B.Tech CS", "₹9–14 LPA", "Full-Time", "NA", "2025-12-22",
         "paytm.png", "https://paytm.com/careers"),

        ("Wipro", "Cybersecurity Analyst", "Noida",
         "Monitor enterprise infrastructure, detect threats, and implement security best practices.",
         "B.Tech CS", "₹7–12 LPA", "Full-Time", "NA", "2025-12-20",
         "wipro.png", "https://careers.wipro.com"),

        ("Zomato", "ML Engineer", "Gurgaon",
         "Develop recommendation engines and optimize logistics using machine learning models.",
         "B.Tech CS/Data", "₹14–20 LPA", "Full-Time", "NA", "2025-12-12",
         "zomato.png", "https://www.zomato.com/careers"),

        ("ISRO", "Research Scientist", "Ahmedabad",
         "Work on satellite systems, data analysis, and advanced space research projects.",
         "M.Tech/M.Sc", "Govt Scale", "Full-Time", "NA", "2025-12-31",
         "isro.png", "https://www.isro.gov.in"),

        ("Swiggy", "Backend Engineer", "Bangalore",
         "Build scalable backend services for order and delivery systems.",
         "B.Tech CS", "₹12–18 LPA", "Full-Time", "NA", "2025-11-29",
         "swiggy.png", "https://careers.swiggy.com"),

        ("Oracle", "Database Engineer", "Hyderabad",
         "Manage enterprise databases, optimize performance, and ensure high availability.",
         "B.Tech CS", "₹11–17 LPA", "Full-Time", "NA", "2025-12-19",
         "oracle.png", "https://www.oracle.com/careers"),

        ("SAP", "Functional Consultant", "Bangalore",
         "Support SAP implementations, business analysis, and ERP solutions.",
         "B.Tech/MBA", "₹10–15 LPA", "Full-Time", "NA", "2025-12-23",
         "sap.png", "https://jobs.sap.com"),

        ("Zoho", "Product Engineer", "Chennai",
         "Develop scalable SaaS products and collaborate with cross-functional teams.",
         "B.Tech CS", "₹8–14 LPA", "Full-Time", "NA", "2025-12-27",
         "zoho.png", "https://www.zoho.com/careers")
        ])

    db.commit()







