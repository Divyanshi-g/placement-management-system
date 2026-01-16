import sqlite3

def init_db():
    with open("schema.sql", "r") as f:
        schema = f.read()

    conn = sqlite3.connect("placements.db")
    cur = conn.cursor()
    cur.executescript(schema)
    conn.commit()
    conn.close()
    print("✅ Database initialized with schema.sql")

if __name__ == "__main__":
    init_db()

