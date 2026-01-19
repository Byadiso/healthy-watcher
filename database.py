import sqlite3


def init_db():
    conn = sqlite3.connect("sites.db")
    c = conn.cursor()

    # websites
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

    # history table
    c.execute("""
    CREATE TABLE IF NOT EXISTS checks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        site_id INTEGER,
        status TEXT,
        response_time REAL,
        checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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


def get_sites_by_chat(chat_id):
    init_db()
    conn = sqlite3.connect("sites.db")
    c = conn.cursor()

    c.execute(
        "SELECT id, website, last_status FROM websites WHERE chat_id=?",
        (str(chat_id),)
    )

    rows = c.fetchall()
    conn.close()
    return rows


def get_all_sites():
    init_db()
    conn = sqlite3.connect("sites.db")
    c = conn.cursor()

    c.execute("SELECT id, chat_id, website FROM websites")
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


def save_check(site_id, status, response_time):
    init_db()
    conn = sqlite3.connect("sites.db")
    c = conn.cursor()

    c.execute("""
        INSERT INTO checks (site_id, status, response_time)
        VALUES (?, ?, ?)
    """, (site_id, status, response_time))

    conn.commit()
    conn.close()

def get_uptime_stats(site_id, hours=24):
    init_db()

    conn = sqlite3.connect("sites.db")
    c = conn.cursor()

    c.execute("""
        SELECT status FROM checks
        WHERE site_id = ?
        AND checked_at >= datetime('now', ?)
    """, (site_id, f'-{hours} hours'))

    rows = c.fetchall()
    conn.close()

    total = len(rows)
    ok = len([r for r in rows if r[0] == "ok"])

    return total, ok

