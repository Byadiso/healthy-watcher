import sqlite3

def init_db():
    conn = sqlite3.connect("sites.db")
    c = conn.cursor()

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

    conn.commit()
    conn.close()


def add_site(chat_id, website, contact, booking):
    init_db()

    conn = sqlite3.connect("sites.db")
    c = conn.cursor()

    c.execute("""
    INSERT INTO websites (chat_id, website, contact, booking, last_status)
    VALUES (?, ?, ?, ?, ?)
    """, (chat_id, website, contact, booking, "ok"))

    conn.commit()
    conn.close()


def get_sites():
    init_db()  

    conn = sqlite3.connect("sites.db")
    c = conn.cursor()

    c.execute("SELECT * FROM websites")
    rows = c.fetchall()

    conn.close()
    return rows


def update_status(site_id, status):
    init_db()

    conn = sqlite3.connect("sites.db")
    c = conn.cursor()

    c.execute(
        "UPDATE websites SET last_status=? WHERE id=?",
        (status, site_id)
    )

    conn.commit()
    conn.close()
