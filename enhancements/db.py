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
      conversation_id TEXT NOT NULL,
      role TEXT CHECK(role IN ('user','bot')) NOT NULL,
      content TEXT NOT NULL,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
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
         "MCA", "₹12–18 LPA", "Full-Time", "2 Years", "2025-12-15",
         "microsoft.png", "https://careers.microsoft.com"),

        ("TCS", "System Analyst", "Mumbai",
         "Work with clients to design business solutions, analyze requirements, and implement enterprise systems.",
         "Any Graduate", "₹6–10 LPA", "Full-Time", "NA", "2025-12-10",
         "tcs.png", "https://www.tcs.com"),

        ("Infosys", "Java Developer", "Hyderabad",
         "Develop backend enterprise applications using Java, Spring Boot, and microservices architecture.",
         "BCA", "₹7–11 LPA", "Full-Time", "NA", "2025-12-18",
         "infosys.png", "https://www.infosys.com"),

        ("Accenture", "Business Technology Analyst", "Bangalore",
         "Support consulting projects involving data analysis, business process optimization, and technology solutions.",
         "MBA", "₹8–12 LPA", "Full-Time", "NA", "2025-12-22",
         "accenture.png", "https://www.accenture.com"),

        ("IBM", "Software Developer", "Pune",
         "Develop enterprise-grade software solutions using modern frameworks and cloud-native technologies.",
         "BCA", "₹9–14 LPA", "Full-Time", "NA", "2025-12-08",
         "ibm.png", "https://www.ibm.com"),

        ("Deloitte", "Technology Consultant", "Bangalore",
         "Assist clients with digital transformation, analytics, and system integration solutions.",
         "BBA", "₹10–15 LPA", "Full-Time", "NA", "2025-12-05",
         "deloitte.png", "https://www.deloitte.com"),

        ("Capgemini", "DevOps Engineer", "Kolkata",
         "Implement CI/CD pipelines, automate deployments, and manage cloud infrastructure.",
         "MCA", "₹8–13 LPA", "Part-Time", "NA", "2025-12-25",
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
         "M.Tech", "₹9–14 LPA", "Full-Time", "NA", "2025-12-22",
         "paytm.png", "https://paytm.com/careers"),

        ("Wipro", "Cybersecurity Analyst", "Noida",
         "Monitor enterprise infrastructure, detect threats, and implement security best practices.",
         "BCA", "₹7–12 LPA", "Full-Time", "NA", "2025-12-20",
         "wipro.png", "https://careers.wipro.com"),

        ("Zomato", "ML Engineer", "Gurgaon",
         "Develop recommendation engines and optimize logistics using machine learning models.",
         "MCA", "₹14–20 LPA", "Full-Time", "NA", "2025-12-12",
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
         "zoho.png", "https://www.zoho.com/careers"),

        ("Tata Consultancy Services", "Software Developer", "Bangalore",
         "Build, test, and maintain enterprise-level software applications.",
         "B.Tech / MCA", "₹6–9 LPA", "Full-Time", "NA", "2025-10-05",
         "tcs.png", "https://www.tcs.com/careers"),

        ("Infosys", "Business Analyst", "Pune",
         "Analyze business requirements and bridge the gap between clients and technical teams.",
         "BBA / MBA / Any Graduate", "₹5–8 LPA", "Full-Time", "NA", "2025-09-20",
         "infosys.png", "https://www.infosys.com/careers"),

        ("Google", "Data Scientist", "Hyderabad",
         "Work on large-scale data analysis, predictive modeling, and AI-driven insights.",
         "B.Tech / M.Tech / PhD", "₹25–35 LPA", "Full-Time", "NA", "2025-11-15",
         "google.png", "https://careers.google.com"),
  
        ("Amazon", "Operations Manager", "Delhi NCR",
         "Manage supply chain operations and optimize warehouse performance.",
         "Any Graduate / MBA", "₹10–15 LPA", "Full-Time", "NA", "2025-08-30",
         "amazon.png", "https://www.amazon.jobs"),

        ("Deloitte", "Cyber Security Analyst", "Mumbai",
          "Monitor security systems, assess risks, and implement security measures.",
          "B.Tech / M.Tech", "₹8–12 LPA", "Full-Time", "NA", "2025-10-18",
          "deloitte.png", "https://www2.deloitte.com/careers"),

         ("Byju’s", "Academic Counselor", "Bangalore",
          "Guide students and parents on learning programs and career paths.",
          "Any Graduate", "₹4–6 LPA", "Full-Time", "NA", "2025-07-25",
          "byjus.png", "https://byjus.com/careers"),

         ("Flipkart", "Product Manager", "Bangalore",
          "Define product vision, work with engineering teams, and drive product launches.",
          "B.Tech / MBA", "₹18–25 LPA", "Full-Time", "NA", "2025-12-01",
          "flipkart.png", "https://www.flipkartcareers.com"),

         ("Wipro", "HR Executive", "Chennai",
          "Handle recruitment, employee engagement, and HR operations.",
          "BBA / MBA (HR)", "₹4–7 LPA", "Full-Time", "NA", "2025-09-10",
          "wipro.png", "https://careers.wipro.com"),

        ("Microsoft", "Cloud Support Engineer", "Noida",
         "Provide technical support for Azure cloud services and enterprise clients.",
         "B.Tech / MCA", "₹12–18 LPA", "Full-Time", "Hybrid", "2025-11-05",
         "microsoft.png", "https://careers.microsoft.com"),

        ("Swiggy", "Operations Analyst", "Bangalore",
         "Analyze delivery metrics and improve operational efficiency.",
         "Any Graduate", "₹7–10 LPA", "Full-Time", "Onsite", "2025-08-12",
         "swiggy.png", "https://careers.swiggy.com"),

       ("Paytm", "UI/UX Designer", "Noida",
        "Design intuitive user interfaces and improve customer experience.",
        "Any Graduate / Design Degree", "₹6–10 LPA", "Full-Time", "Onsite", "2025-09-02",
        "paytm.png", "https://paytm.com/careers"),

       ("IBM", "AI Research Intern", "Bangalore",
        "Assist in AI research projects and build experimental ML models.",
        "B.Tech / M.Tech", "₹25,000/month", "Internship", "Onsite", "2025-07-15",
        "ibm.png", "https://www.ibm.com/careers"),

       ("Reliance Industries", "Supply Chain Coordinator", "Jamnagar",
        "Coordinate logistics, inventory, and supplier communications.",
        "Any Graduate", "₹5–8 LPA", "Full-Time", "Onsite", "2025-10-20",
        "relience.png", "https://www.ril.com/Careers"),

       ("Accenture", "Digital Marketing Executive", "Gurgaon",
        "Manage digital campaigns, SEO, and performance marketing strategies.",
        "Any Graduate / MBA", "₹4–6 LPA", "Full-Time", "Hybrid", "2025-08-05",
        "accenture.png", "https://www.accenture.com/careers"),

      ("Intel", "Embedded Systems Engineer", "Bangalore",
       "Develop firmware and low-level software for embedded platforms.",
       "B.Tech / M.Tech", "₹14–22 LPA", "Full-Time", "Onsite", "2025-12-10",
       "intel.png", "https://jobs.intel.com"),

      ("HUL", "Sales & Distribution Trainee", "Kolkata",
       "Handle distributor networks and market expansion initiatives.",
       "Any Graduate / MBA", "₹3–5 LPA", "Full-Time", "Field Work", "2025-07-30",
       "hul.png", "https://www.hul.co.in/careers"),

      ("Zoho", "Technical Support Engineer", "Chennai",
       "Assist customers with product issues and provide technical solutions.",
       "Any Graduate", "₹5–7 LPA", "Full-Time", "Onsite", "2025-09-18",
       "zoho.png", "https://www.zoho.com/careers"),

     ("Meesho", "Content Operations Associate", "Remote",
      "Manage product content quality and catalog operations.",
      "Any Graduate", "₹4–6 LPA", "Part-Time", "Remote", "2025-08-22",
      "meesho.png", "https://careers.meesho.com")
    ])
    db.commit()













