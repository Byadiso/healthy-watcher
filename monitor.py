import time
import requests
from datetime import datetime
from database import get_sites, update_status
import os

# TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
# TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")



TELEGRAM_BOT_TOKEN = "8188686402:AAFht6MjOzQTDutysW-_kfUZn9LVya5a7rI"
TELEGRAM_CHAT_ID = "2046825005"

def send_telegram(msg):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("❌ Telegram env variables not found")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": TELEGRAM_CHAT_ID,
        "text": msg
    })


def check_url(url):
    try:
        r = requests.get(url, timeout=15)
        return r.status_code == 200
    except:
        return False


def monitor():
    print("===================================")
    print("🫀 Healthy Watcher started")
    print("⏰", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("===================================")

    sites = get_sites()

    print(f"🔍 Monitoring {len(sites)} website(s)\n")

    for site in sites:
        site_id, chat_id, website, contact, booking, last_status = site

        print(f"➡ Checking: {website}")

        ok = check_url(website)

        if ok:
            print("   ✅ Site healthy")

            if last_status == "down":
                send_telegram(f"✅ Website back online:\n{website}")
                update_status(site_id, "ok")

        else:
            print("   ❌ Site DOWN")

            if last_status != "down":
                send_telegram(f"🚨 Website DOWN:\n{website}")
                update_status(site_id, "down")

    print("\n🕒 Monitor cycle completed")
    print("-----------------------------------\n")


if __name__ == "__main__":
    while True:
        monitor()
        print("😴 Sleeping 30 minutes...\n")
        time.sleep(1800)   # 30 minutes
