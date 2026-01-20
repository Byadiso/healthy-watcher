import os
import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import streamlit_authenticator as stauth
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="Healthy Watcher Dash", page_icon="🌐", layout="wide")

INVITE_CODE = os.getenv("INVITE_CODE")

# --- DB INITIALIZATION (Fixes the 'No Such Table' Error) ---
def full_init():
    conn = sqlite3.connect("sites.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (email TEXT, name TEXT, username TEXT UNIQUE, password TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS logs (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, action TEXT, timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
    c.execute("CREATE TABLE IF NOT EXISTS websites (id INTEGER PRIMARY KEY AUTOINCREMENT, chat_id TEXT, website TEXT, contact TEXT, booking TEXT, last_status TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS checks (id INTEGER PRIMARY KEY AUTOINCREMENT, site_id INTEGER, status TEXT, response_time REAL, checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
    conn.commit()
    conn.close()

full_init()

# --- HELPER FUNCTIONS ---
def get_db_connection():
    return sqlite3.connect("sites.db")

def add_log(username, action):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("INSERT INTO logs (username, action) VALUES (?, ?)", (username, action))
    conn.commit()
    conn.close()

def get_auth_data():
    conn = get_db_connection()
    df = pd.read_sql("SELECT * FROM users", conn)
    conn.close()
    credentials = {"usernames": {}}
    for _, row in df.iterrows():
        credentials["usernames"][row['username']] = {
            "name": row['name'], "password": row['password'], "email": row['email']
        }
    return credentials

def load_monitor_data():
    conn = get_db_connection()
    query = """
    SELECT w.id, w.website, w.last_status, w.contact, w.booking, 
           MAX(c.checked_at) as last_check, c.response_time
    FROM websites w
    LEFT JOIN checks c ON w.id = c.site_id
    GROUP BY w.id
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# --- AUTH UI ---
credentials = get_auth_data()
authenticator = stauth.Authenticate(credentials, "watcher_session", "secret_key_123", cookie_expiry_days=30)

mode = st.sidebar.selectbox("Access Mode", ["Login", "Register New Account"])

if mode == "Register New Account":
    st.header("📝 Create Account")
    email = st.text_input("Email")
    name = st.text_input("Full Name")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    code = st.text_input("Invite Code", type="password")
    
    if st.button("Register"):
        if code == INVITE_CODE and all([email, name, username, password]):
            hashed = stauth.Hasher.hash(password)
            try:
                conn = get_db_connection()
                conn.execute("INSERT INTO users VALUES (?,?,?,?)", (email, name, username, hashed))
                conn.commit()
                conn.close()
                st.success("Success! Please log in.")
            except:
                st.error("Username already taken.")
        else:
            st.error("Missing fields or wrong code.")

else:
    # Login Logic
    authenticator.login('main')

    if st.session_state["authentication_status"]:
        # Log entry for session start
        if "session_logged" not in st.session_state:
            add_log(st.session_state["username"], "Login to Dashboard")
            st.session_state["session_logged"] = True

        st.sidebar.subheader(f"User: {st.session_state['name']}")
        if authenticator.logout('Logout', 'sidebar'):
            add_log(st.session_state["username"], "Logout from Dashboard")

        # --- DASHBOARD TABS ---
        tab1, tab2, tab3 = st.tabs(["📊 Monitor", "⚙️ Management", "📜 Audit Logs"])

        with tab1:
            st.title("🌐 Website Performance")
            df = load_monitor_data()
            if not df.empty:
                m1, m2, m3 = st.columns(3)
                m1.metric("Total", len(df))
                m2.metric("Online", len(df[df['last_status'] == 'ok']))
                m3.metric("Offline", len(df[df['last_status'] != 'ok']), delta_color="inverse")

                st.dataframe(df.style.applymap(lambda x: f'background-color: {"#90ee90" if x == "ok" else "#ffcccb"}', subset=['last_status']), use_container_width=True, hide_index=True)
                
                # Chart
                conn = get_db_connection()
                hist = pd.read_sql("SELECT w.website, c.response_time, c.checked_at FROM checks c JOIN websites w ON c.site_id = w.id ORDER BY c.checked_at DESC LIMIT 100", conn)
                conn.close()
                if not hist.empty:
                    fig = px.line(hist, x="checked_at", y="response_time", color="website", title="Response Time Trend")
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No websites monitored yet.")

        with tab2:
            st.subheader("Add/Remove Websites")
            with st.form("add_form"):
                u = st.text_input("URL (e.g., https://google.com)")
                c = st.text_input("Contact")
                b = st.text_input("Booking Link")
                if st.form_submit_button("Add Site"):
                    conn = get_db_connection()
                    conn.execute("INSERT INTO websites (chat_id, website, contact, booking, last_status) VALUES ('WEB',?,?,?,'ok')", (u, c, b))
                    conn.commit()
                    conn.close()
                    add_log(st.session_state["username"], f"Added: {u}")
                    st.rerun()

            if not df.empty:
                st.divider()
                to_del = st.selectbox("Delete site", df['website'].tolist())
                if st.button("Confirm Delete"):
                    conn = get_db_connection()
                    conn.execute("DELETE FROM websites WHERE website=?", (to_del,))
                    conn.commit()
                    conn.close()
                    add_log(st.session_state["username"], f"Deleted: {to_del}")
                    st.rerun()

        with tab3:
            st.subheader("System Activity")
            conn = get_db_connection()
            logs = pd.read_sql("SELECT * FROM logs ORDER BY timestamp DESC LIMIT 50", conn)
            conn.close()
            st.table(logs)

    elif st.session_state["authentication_status"] is False:
        st.error('Username/password incorrect')
    elif st.session_state["authentication_status"] is None:
        st.info('Please log in.')