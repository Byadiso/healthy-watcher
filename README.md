## ⚙️ Automation Status
![Monitor Status](https://github.com/Byadiso/healthy-watcher/actions/workflows/healthy-watcher.yml/badge.svg)
# Healthy Watcher

**Healthy Watcher** is a lightweight, all-in-one website monitoring system. It automatically checks website health, calculates uptime, and sends real-time Telegram alerts, all managed through a professional web-based dashboard.

### 🔗 [Access the Live Dashboard](https://healthy-watcher.streamlit.app/)

*(Note: Registration requires a secret Invite Code)*

---

## 🚀 Key Features

* **Automated Monitoring:** Checks website status and response times every 30 minutes.
* **Real-time Alerts:** Instant Telegram notifications for `DOWN` and `BACK ONLINE` events.
* **Web Dashboard:** Interactive UI for non-technical users to visualize health data.
* **Secure Access:** Multi-user support with hashed password security and invite-only registration.
* **Site Management:** Add or remove monitored URLs directly via the web interface or Telegram.
* **Audit Logging:** Complete transparency with logs of user logins and administrative actions.
* **Zero-Server Cost:** Designed to run entirely on GitHub Actions and Streamlit Cloud.

---

## 🛠 Tech Stack

* **Frontend:** [Streamlit](https://streamlit.io/) (Data-focused Web Framework)
* **Backend:** Python 3.10
* **Database:** SQLite (Relational storage for sites, history, users, and logs)
* **Automation:** GitHub Actions (Scheduled monitoring cron-job)
* **Visuals:** Plotly & Pandas

---

## 📊 How It Works

1. **Management:** Users add websites via the **Telegram Bot** or the **Web Dashboard**.
2. **Monitoring:** A GitHub Action triggers `monitor.py` every 30 mins to ping each URL.
3. **Alerting:** If a site status changes (e.g., OK → DOWN), a Telegram alert is dispatched.
4. **Reporting:** All data is saved to `sites.db`. The dashboard pulls this data to generate real-time metrics and response-time charts.

---

## 🤖 Telegram Commands

| Command | Description |
| --- | --- |
| `/start` | Welcome message and setup instructions |
| `/add <url> <contact> <booking>` | Register a new site for monitoring |
| `/list` | List all websites you are currently watching |
| `/status <url>` | Get an instant health check and response time |
| `/uptime <url>` | View the 24-hour uptime percentage |

---

## 🔐 Configuration (Secrets)

To run this project, add the following to your **GitHub Secrets** and **Streamlit Secrets**:

* `TELEGRAM_BOT_TOKEN`: Your bot's API token from BotFather.
* `INVITE_CODE`: A secret string used to gatekeep the dashboard registration.

---

## 📂 Project Structure

```text
healthy-watcher/
├── dashboard.py         # Streamlit Web UI & Site Management
├── monitor.py           # The "Engine" - runs the pings
├── bot.py               # Telegram Bot interface
├── database.py          # Unified SQLite CRUD operations
├── requirements.txt     # Python dependencies
├── sites.db             # SQLite database file (Auto-initialized)
└── .github/workflows/
    └── monitor.yml      # Cron-job config (runs every 30m)

```

---

## 🛠 Local Development

1. **Clone the Repository:**
```bash
git clone https://github.com/your-username/healthy-watcher.git
cd healthy-watcher

```


2. **Install Requirements:**
```bash
pip install -r requirements.txt

```


3. **Run the UI:**
```bash
streamlit run dashboard.py

```



---

## 👨‍💻 Author

**BYAMUNGU Desire** *Lead Developer & Project Architect*

---

## 📜 License

MIT License — Feel free to fork and use for your own services.

---