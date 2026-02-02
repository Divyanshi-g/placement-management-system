
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
("Google", "Site Reliability Engineer", "Bangalore",
 "Ensure availability, scalability, and performance of Google production systems.",
 "B.Tech / M.Tech (CS/IT)", "₹18–30 LPA", "Full-Time", "1–3 Years", "2025-12-29",
 "google.png", "https://careers.google.com"),

("Amazon", "Supply Chain Analyst", "Chennai",
 "Analyze logistics data to optimize supply chain efficiency and reduce costs.",
 "MBA (Operations)", "₹9–14 LPA", "Full-Time", "NA", "2025-12-18",
 "amazon.png", "https://www.amazon.jobs"),

("Microsoft", "Power Platform Developer", "Hyderabad",
 "Build low-code business applications using Power Apps and Power Automate.",
 "BCA / MCA", "₹10–16 LPA", "Full-Time", "1 Year", "2025-12-16",
 "microsoft.png", "https://careers.microsoft.com"),

("TCS", "SAP Functional Consultant", "Pune",
 "Configure SAP modules and support enterprise ERP implementations.",
 "MBA / M.Com", "₹7–11 LPA", "Full-Time", "NA", "2025-12-12",
 "tcs.png", "https://www.tcs.com"),

("Infosys", "Python Automation Engineer", "Mysore",
 "Develop automation scripts to improve testing and deployment pipelines.",
 "B.Sc (IT) / B.Tech", "₹6–10 LPA", "Full-Time", "NA", "2025-12-14",
 "infosys.png", "https://www.infosys.com"),

("Accenture", "Change Management Analyst", "Gurgaon",
 "Support organizational transformation through technology adoption strategies.",
 "MBA (HR)", "₹8–12 LPA", "Full-Time", "NA", "2025-12-21",
 "accenture.png", "https://www.accenture.com"),
("Meesho", "Marketplace Quality Executive", "Remote", "Ensure seller quality standards and improve catalog accuracy.", "BA / B.Com", "₹4–6 LPA", "Part-Time", "NA", "2025-08-25", "meesho.png", "https://careers.meesho.com"),
("IBM", "Blockchain Developer", "Bangalore",
 "Design and implement blockchain-based enterprise solutions.",
 "B.Tech (CS)", "₹12–20 LPA", "Full-Time", "2 Years", "2025-12-07",
 "ibm.png", "https://www.ibm.com"),
("Adobe", "Visual Design Intern", "Remote", "Create illustrations, layouts, and marketing creatives for Adobe products.", "B.Des / BFA", "₹35k/month", "Internship", "6 Months", "2025-12-27", "adobe.png", "https://adobe.wd5.myworkdayjobs.com"),
("Deloitte", "Risk Advisory Associate", "Mumbai",
 "Assist clients in managing technology and compliance-related risks.",
 "B.Com / MBA", "₹9–13 LPA", "Part-Time", "NA", "2025-12-06",
 "deloitte.png", "https://www.deloitte.com"),

("Capgemini", "Cloud Migration Engineer", "Noida",
 "Migrate legacy systems to cloud-based architectures.",
 "M.Tech (Cloud Computing)", "₹10–15 LPA", "Full-Time", "1 Year", "2025-12-26",
 "capgemini.png", "https://www.capgemini.com"),

("Adobe", "Visual Design Intern", "Remote",
 "Create illustrations, layouts, and marketing creatives for Adobe products.",
 "B.Des / BFA", "₹35k/month", "Internship", "6 Months", "2025-12-27",
 "adobe.png", "https://adobe.wd5.myworkdayjobs.com"),

("Flipkart", "Category Growth Executive", "Bangalore",
 "Drive category expansion through analytics and vendor coordination.",
 "BBA / MBA", "₹7–12 LPA", "Full-Time", "NA", "2025-12-19",
 "flipkart.png", "https://www.flipkartcareers.com"),

("Paytm", "Payments Risk Analyst", "Noida",
 "Monitor fraud patterns and implement transaction risk controls.",
 "B.Sc (Statistics)", "₹6–10 LPA", "Full-Time", "NA", "2025-12-23",
 "paytm.png", "https://paytm.com/careers"),

("Wipro", "Network Operations Engineer", "Kochi",
 "Manage enterprise networks and resolve infrastructure issues.",
 "Diploma / B.Tech (Networking)", "₹5–9 LPA", "Full-Time", "NA", "2025-12-17",
 "wipro.png", "https://careers.wipro.com"),

("Zomato", "Restaurant Growth Analyst", "Delhi",
 "Analyze restaurant data and improve partner onboarding success.",
 "BBA (Marketing)", "₹8–13 LPA", "Remote", "NA", "2025-12-11",
 "zomato.png", "https://www.zomato.com/careers"),

("ISRO", "Satellite Data Analyst", "Sriharikota",
 "Analyze remote sensing data for space research missions.",
 "M.Sc (Physics)", "Govt Scale", "Full-Time", "NA", "2025-12-31",
 "isro.png", "https://www.isro.gov.in"),

("Oracle", "ERP Implementation Consultant", "Bangalore",
 "Implement and customize Oracle ERP solutions for global clients.",
 "MBA (Finance)", "₹11–18 LPA", "Full-Time", "1 Year", "2025-12-20",
 "oracle.png", "https://www.oracle.com/careers"),

("Zoho", "Business Intelligence Analyst", "Coimbatore",
 "Build dashboards and reports to support business decisions.",
 "B.Sc (Data Science)", "₹6–11 LPA", "Full-Time", "NA", "2025-12-28",
 "zoho.png", "https://www.zoho.com/careers"),

("Intel", "VLSI Design Engineer", "Bangalore",
 "Design and validate high-performance semiconductor architectures.",
 "M.Tech (VLSI)", "₹20–30 LPA", "Full-Time", "2 Years", "2025-12-11",
 "intel.png", "https://jobs.intel.com"),

("HUL", "Brand Strategy Associate", "Mumbai",
 "Support brand positioning and national marketing campaigns.",
 "MBA (Marketing)", "₹8–12 LPA", "Full-Time", "NA", "2025-08-01",
 "hul.png", "https://www.hul.co.in/careers"),

("Meesho", "Marketplace Quality Executive", "Remote",
 "Ensure seller quality standards and improve catalog accuracy.",
 "BA / B.Com", "₹4–6 LPA", "Part-Time", "NA", "2025-08-25",
 "meesho.png", "https://careers.meesho.com"),

("Infosys BPM", "Process Executive", "Bangalore",
 "Handle business process operations and client support services.",
 "BA / B.Com / BBA", "₹3–5 LPA", "Full-Time", "NA", "2025-08-28",
 "infosys.png", "https://www.infosysbpm.com/careers"),

("Genpact", "Business Operations Analyst", "Gurgaon",
 "Analyze workflows and improve operational efficiency for global clients.",
 "BBA / MBA", "₹5–8 LPA", "Full-Time", "NA", "2025-10-10",
 "genpact.png", "https://www.genpact.com/careers"),

("Tata Capital", "Relationship Officer", "Jaipur",
 "Manage customer relationships and support financial product sales.",
 "BBA / Any Graduate", "₹4–6 LPA", "Full-Time", "NA", "2025-08-20",
 "tatacapital.png", "https://www.tatacapital.com/careers"),

("Cognizant", "Junior Software Tester", "Chennai",
 "Execute test cases and support quality assurance processes.",
 "BCA / B.Sc (IT)", "₹4–7 LPA", "Full-Time", "NA", "2025-10-05",
 "cognizant.png", "https://careers.cognizant.com"),

("Tech Mahindra", "Technical Support Associate", "Noida",
 "Provide L1 technical support for enterprise applications.",
 "BCA / Diploma (IT)", "₹3–5 LPA", "Full-Time", "NA", "2025-09-25",
 "techmahindra.png", "https://careers.techmahindra.com"),

("L&T Infotech", "Application Support Analyst", "Pune",
 "Support enterprise software systems and troubleshoot issues.",
 "BCA / MCA", "₹5–8 LPA", "Full-Time", "NA", "2025-10-12",
 "lti.png", "https://www.ltimindtree.com/careers"),

("BYJU’S", "Learning Program Advisor", "Remote",
 "Counsel students and explain learning programs to parents.",
 "BBA / BA", "₹4–6 LPA", "Full-Time", "NA", "2025-07-30",
 "byjus.png", "https://byjus.com/careers"),

("UpGrad", "Career Support Executive", "Remote",
 "Guide learners with career planning and placement support.",
 "BA / BBA / MBA", "₹4–6 LPA", "Full-Time", "NA", "2025-08-05",
 "upgrad.png", "https://www.upgrad.com/careers"),

("Delhivery", "Logistics Operations Coordinator", "Faridabad",
 "Coordinate delivery operations and track shipment performance.",
 "BBA / Any Graduate", "₹5–7 LPA", "Full-Time", "NA", "2025-09-12",
 "delhivery.png", "https://www.delhivery.com/careers"),

("Reliance Jio", "Retail Store Manager", "Indore",
 "Manage retail store operations and customer engagement.",
 "BBA / Diploma (Management)", "₹4–7 LPA", "Full-Time", "NA", "2025-08-18",
 "relience.png", "https://careers.jio.com"),

("Flipkart", "Vendor Support Executive", "Bangalore",
 "Support sellers with catalog onboarding and compliance processes.",
 "B.Com / BBA", "₹5–8 LPA", "Full-Time", "NA", "2025-09-22",
 "flipkart.png", "https://www.flipkartcareers.com"),

("Swiggy Instamart", "Inventory Planning Analyst", "Bangalore",
 "Plan inventory demand and reduce supply shortages.",
 "B.Sc (Maths/Statistics)", "₹6–9 LPA", "Full-Time", "NA", "2025-10-02",
 "swiggy.png", "https://careers.swiggy.com"),

("HCL Technologies", "IT Service Desk Analyst", "Nagpur",
 "Handle IT incidents and service requests for enterprise clients.",
 "BCA / Diploma (Computer)", "₹4–6 LPA", "Full-Time", "NA", "2025-09-05",
 "hcl.png", "https://www.hcltech.com/careers"),

("EY", "Audit Associate", "Kolkata",
 "Assist audit teams with financial reviews and compliance checks.",
 "B.Com / M.Com", "₹6–9 LPA", "Full-Time", "NA", "2025-10-15",
 "ey.png", "https://www.ey.com/en_in/careers"),

("KPMG", "Tax Compliance Executive", "Ahmedabad",
 "Prepare tax filings and support regulatory compliance tasks.",
 "B.Com / MBA (Finance)", "₹6–10 LPA", "Full-Time", "NA", "2025-10-20",
 "kpmg.png", "https://home.kpmg/in/en/home/careers.html"),

("Tata Motors", "Dealer Operations Coordinator", "Jamshedpur",
 "Coordinate dealer network operations and performance reporting.",
 "BBA / Any Graduate", "₹5–8 LPA", "Full-Time", "NA", "2025-09-28",
 "tatamotors.png", "https://careers.tatamotors.com"),

            ("HDFC Bank", "Digital Banking Executive", "Mumbai",
 "Support digital banking operations, customer onboarding, and platform analytics.",
 "BBA / B.Com", "₹4–7 LPA", "Full-Time", "NA", "2025-09-15",
 "hdfc.png", "https://www.hdfcbank.com/careers"),


 ("Tech Mahindra", "Software Support Engineer", "Nagpur",
 "Handle application support and basic development tasks.",
 "BCA", "₹3–5 LPA", "Full-Time", "NA", "2025-08-18",
 "techmahindra.png", "https://careers.techmahindra.com"),

("Cognizant", "Programmer Analyst Trainee", "Coimbatore",
 "Assist in coding, debugging, and testing software modules.",
 "BCA", "₹4–6 LPA", "Full-Time", "NA", "2025-09-25",
 "cognizant.png", "https://careers.cognizant.com"),

("Mindtree", "Cloud Support Associate", "Bangalore",
 "Support cloud deployments and monitor cloud services.",
 "BCA", "₹5–7 LPA", "Full-Time", "NA", "2025-10-05",
 "mindtree.png", "https://www.ltimindtree.com/careers"),

("Infosys BPM", "Process Executive", "Bangalore",
 "Handle business process operations and client support services.",
 "BA / B.Com / BBA", "₹3–5 LPA", "Full-Time", "NA", "2025-08-28",
 "infosys.png", "https://www.infosysbpm.com/careers"),

("Genpact", "Business Operations Analyst", "Gurgaon",
 "Analyze workflows and improve operational efficiency for global clients.",
 "BBA / MBA", "₹5–8 LPA", "Full-Time", "NA", "2025-10-10",
 "genpact.png", "https://www.genpact.com/careers"),

("Tata Capital", "Relationship Officer", "Jaipur",
 "Manage customer relationships and support financial product sales.",
 "BBA / Any Graduate", "₹4–6 LPA", "Full-Time", "NA", "2025-08-20",
 "tatacapital.png", "https://www.tatacapital.com/careers"),

("Cognizant", "Junior Software Tester", "Chennai",
 "Execute test cases and support quality assurance processes.",
 "BCA / B.Sc (IT)", "₹4–7 LPA", "Full-Time", "NA", "2025-10-05",
 "cognizant.png", "https://careers.cognizant.com"),

("Tech Mahindra", "Technical Support Associate", "Noida",
 "Provide L1 technical support for enterprise applications.",
 "BCA / Diploma (IT)", "₹3–5 LPA", "Full-Time", "NA", "2025-09-25",
 "techmahindra.png", "https://careers.techmahindra.com"),
            
 ("Capgemini", "IT Analyst – Fresher", "Noida",
 "Support application deployment and basic troubleshooting.",
 "BCA", "₹4–5.5 LPA", "Full-Time", "NA", "2025-08-28",
 "capgemini.png", "https://www.capgemini.com/careers"),

("Infosys", "Associate Systems Engineer", "Mysore",
 "Work on software development and enterprise application support.",
 "BCA", "₹3.6–5 LPA", "Full-Time", "NA", "2025-10-01",
 "infosys.png", "https://www.infosys.com/careers"),

("HCLTech", "Graduate Trainee – IT", "Chennai",
 "Provide application and infrastructure support for clients.",
 "BCA", "₹3–4.5 LPA", "Full-Time", "NA", "2025-09-10",
 "hcl.png", "https://www.hcltech.com/careers"),

("L&T Infotech", "Application Support Analyst", "Pune",
 "Support enterprise software systems and troubleshoot issues.",
 "BCA / MCA", "₹5–8 LPA", "Full-Time", "NA", "2025-10-12",
 "lti.png", "https://www.ltimindtree.com/careers"),

("BYJU’S", "Learning Program Advisor", "Remote",
 "Counsel students and explain learning programs to parents.",
 "BBA / BA", "₹4–6 LPA", "Full-Time", "NA", "2025-07-30",
 "byjus.png", "https://byjus.com/careers"),

("UpGrad", "Career Support Executive", "Remote",
 "Guide learners with career planning and placement support.",
 "BA / BBA / MBA", "₹4–6 LPA", "Full-Time", "NA", "2025-08-05",
 "upgrad.png", "https://www.upgrad.com/careers"),

("Delhivery", "Logistics Operations Coordinator", "Faridabad",
 "Coordinate delivery operations and track shipment performance.",
 "BBA / Any Graduate", "₹5–7 LPA", "Full-Time", "NA", "2025-09-12",
 "delhivery.png", "https://www.delhivery.com/careers"),

("Reliance Jio", "Retail Store Manager", "Indore",
 "Manage retail store operations and customer engagement.",
 "BBA / Diploma (Management)", "₹4–7 LPA", "Full-Time", "NA", "2025-08-18",
 "relience.png", "https://careers.jio.com"),

("Flipkart", "Vendor Support Executive", "Bangalore",
 "Support sellers with catalog onboarding and compliance processes.",
 "B.Com / BBA", "₹5–8 LPA", "Full-Time", "NA", "2025-09-22",
 "flipkart.png", "https://www.flipkartcareers.com"),

("Swiggy Instamart", "Inventory Planning Analyst", "Bangalore",
 "Plan inventory demand and reduce supply shortages.",
 "B.Sc (Maths/Statistics)", "₹6–9 LPA", "Full-Time", "NA", "2025-10-02",
 "swiggy.png", "https://careers.swiggy.com"),

("Axis Bank", "Customer Experience Officer", "Lucknow",
 "Improve customer satisfaction and resolve service issues.",
 "BA / B.Com", "₹4–6 LPA", "Full-Time", "NA", "2025-08-10",
 "axis.png", "https://www.axisbank.com/careers"),

("HCL Technologies", "IT Service Desk Analyst", "Nagpur",
 "Handle IT incidents and service requests for enterprise clients.",
 "BCA / Diploma (Computer)", "₹4–6 LPA", "Full-Time", "NA", "2025-09-05",
 "hcl.png", "https://www.hcltech.com/careers"),

("EY", "Audit Associate", "Kolkata",
 "Assist audit teams with financial reviews and compliance checks.",
 "B.Com / M.Com", "₹6–9 LPA", "Full-Time", "NA", "2025-10-15",
 "ey.png", "https://www.ey.com/en_in/careers"),

("KPMG", "Tax Compliance Executive", "Ahmedabad",
 "Prepare tax filings and support regulatory compliance tasks.",
 "B.Com / MBA (Finance)", "₹6–10 LPA", "Full-Time", "NA", "2025-10-20",
 "kpmg.png", "https://home.kpmg/in/en/home/careers.html"),

("Tata Motors", "Dealer Operations Coordinator", "Jamshedpur",
 "Coordinate dealer network operations and performance reporting.",
 "BBA / Any Graduate", "₹5–8 LPA", "Full-Time", "NA", "2025-09-28",
 "tatamotors.png", "https://careers.tatamotors.com"),

("Oracle", "Associate Application Developer", "Bangalore",
 "Support development of database-driven enterprise applications.",
 "BCA", "₹7–10 LPA", "Full-Time", "NA", "2025-10-12",
 "oracle.png", "https://www.oracle.com/careers"),

("IBM", "Application Support Developer", "Kochi",
 "Maintain applications and assist in bug fixing and deployments.",
 "BCA", "₹4.5–7 LPA", "Full-Time", "NA", "2025-09-08",
 "ibm.png", "https://www.ibm.com/careers"),

("Hexaware", "Automation Testing Trainee", "Navi Mumbai",
 "Write and execute automation test scripts.",
 "BCA", "₹4–6 LPA", "Full-Time", "NA", "2025-09-18",
 "hexaware.png", "https://hexaware.com/careers"),

("Persistent Systems", "Backend Developer Trainee", "Pune",
 "Develop REST APIs and backend services using Python/Java.",
 "BCA", "₹5–8 LPA", "Full-Time", "NA", "2025-10-22",
 "persistent.png", "https://www.persistent.com/careers"),

("L&T Technology Services", "Embedded Software Trainee", "Mysore",
 "Assist in development of embedded and system software.",
 "BCA", "₹4–6 LPA", "Full-Time", "NA", "2025-10-10",
 "ltts.png", "https://www.ltts.com/careers")
    ])
    db.commit()


