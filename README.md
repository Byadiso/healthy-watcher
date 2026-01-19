
---

# 🫀 Healthy Watcher

**Healthy Watcher** is a lightweight website monitoring system that checks your website health automatically and sends real-time Telegram alerts when your site goes down or comes back online.

It also tracks **response time**, **uptime percentage**, and **historical health data** — all without expensive tools or complex dashboards.

---

## Features

✅ Website uptime monitoring (every 30 minutes)
✅ Instant Telegram alerts (DOWN & BACK ONLINE)
✅ Response time tracking
✅ Uptime percentage calculation (last 24 hours)
✅ Health history storage (SQLite)
✅ Multi-website support per Telegram user
✅ Works with GitHub Actions (cloud monitoring)

---

## How It Works

1. User adds websites via Telegram bot
2. Websites are stored in a local SQLite database
3. GitHub Actions runs the monitor every 30 minutes
4. Each check is saved with:

   * status (ok / down)
   * response time
   * timestamp
5. Alerts are sent only when status changes
6. Users can request uptime reports anytime

---

## Telegram Commands

### `/start`

Start the bot and see instructions.

### `/add`

Add a website to monitor.

```
/add https://example.com https://example.com/contact https://example.com/booking
```

### `/list`

List all monitored websites.

### `/status`

Check live website status and response time.

```
/status https://example.com
```

### `/uptime`

View uptime percentage (last 24 hours).

```
/uptime https://example.com
```

---

## Uptime Calculation

Uptime is calculated using real monitoring data:

```
uptime % = (successful checks / total checks) × 100
```

Example:

* 48 checks in 24 hours
* 47 successful
* uptime = **97.91%**

---

## Tech Stack

* **Python 3.10**
* **Telegram Bot API**
* **SQLite**
* **GitHub Actions (cron monitoring)**
* **Requests library**

---

## Project Structure

```
healthy-watcher/
│
├── bot.py               # Telegram bot
├── monitor.py           # Monitoring script
├── database.py          # Database logic
├── requirements.txt
├── sites.db              # SQLite database
└── .github/workflows/
    └── monitor.yml      # GitHub Actions cron
```

---

## Monitoring Schedule

Monitoring runs automatically every **30 minutes** using GitHub Actions:

```
*/30 * * * *
```

This means:

* 48 checks per day
* Reliable uptime statistics
* Cloud-based monitoring (no server needed)

---

## Environment Variables

Set these in **GitHub Secrets**:

| Name               | Description             |
| ------------------ | ----------------------- |
| TELEGRAM_BOT_TOKEN | Your Telegram bot token |

> ⚠️ Never commit your bot token to GitHub.

---

## Local Development

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python bot.py
```

To test monitoring locally:

```bash
python monitor.py
```

---

## Use Cases

* Website uptime monitoring
* Small business websites
* Freelancers & agencies
* WordPress health checks
* Booking / contact page monitoring
* Lightweight alternative to paid tools

---

## Future Features (Planned)

* 📈 7-day & 30-day uptime reports
* 🕒 Downtime duration tracking
* 📧 Email alerts
* 🌐 Public status pages
* 💳 Paid plans & subscriptions
* 🔌 WordPress plugin integration

---

## Why Healthy Watcher?

Most uptime tools are expensive and complex.

Healthy Watcher focuses on:

✔ simplicity
✔ automation
✔ real data
✔ Telegram-first experience

Built for developers, freelancers, and small businesses.

---

## 📜 License

MIT License — free to use, modify, and extend.

---


