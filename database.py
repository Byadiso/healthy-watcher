import sqlite3

def init_db():
    conn = sqlite3.connect("sites.db")
    c = conn.cursor()

    # 1. Websites Table
    c.execute("""
    CREATE TABLE IF NOT EXISTS websites (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chat_id TEXT,
        website TEXT,
        contact TEXT,
        booking TEXT,
        last_status TEXT
    )
    """)

    # 2. Checks History Table
    c.execute("""
    CREATE TABLE IF NOT EXISTS checks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        site_id INTEGER,
        status TEXT,
        response_time REAL,
        checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 3. Users Table
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        email TEXT PRIMARY KEY,
        name TEXT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    # 4. Audit Logs Table
    c.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        action TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

def add_site(chat_id, website, contact, booking):
    conn = sqlite3.connect("sites.db")
    c = conn.cursor()
    c.execute("""
    INSERT INTO websites (chat_id, website, contact, booking, last_status)
    VALUES (?, ?, ?, ?, ?)
    """, (chat_id, website, contact, booking, "ok"))
    conn.commit()
    conn.close()

def get_all_sites():
    conn = sqlite3.connect("sites.db")
    c = conn.cursor()
    c.execute("SELECT id, chat_id, website FROM websites")
    rows = c.fetchall()
    conn.close()
    return rows

def update_status(site_id, status):
    conn = sqlite3.connect("sites.db")
    c = conn.cursor()
    c.execute("UPDATE websites SET last_status=? WHERE id=?", (status, site_id))
    conn.commit()
    conn.close()

def save_check(site_id, status, response_time):
    conn = sqlite3.connect("sites.db")
    c = conn.cursor()
    c.execute("""
        INSERT INTO checks (site_id, status, response_time)
        VALUES (?, ?, ?)
    """, (site_id, status, response_time))
    conn.commit()
    conn.close()

# Run initialization
if __name__ == "__main__":
    init_db()