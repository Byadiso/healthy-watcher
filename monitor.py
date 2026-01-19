import os
import requests
from datetime import datetime

from checker import check_website
from database import get_all_sites, update_status, save_check

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")




def send_telegram(chat_id, message):
    if not TELEGRAM_BOT_TOKEN:
        print("❌ TELEGRAM_BOT_TOKEN missing")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    requests.post(
        url,
        json={
            "chat_id": chat_id,
            "text": message
        },
        timeout=15
    )


def main():
    print("===================================")
    print("🫀 Healthy Watcher monitor running")
    print("⏰", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("===================================")

    sites = get_all_sites()
    print(f"🔍 Found {len(sites)} websites\n")

    for site_id, chat_id, website in sites:
        print(f"➡ Checking {website}")

        status, response_time = check_website(website)

        # save history
        save_check(site_id, status, response_time)

        # get previous status handled in DB
        update_status(site_id, status)

        if status == "down":
            send_telegram(
                chat_id,
                f"🚨 WEBSITE DOWN\n\n{website}"
            )

        else:
            print(f"   ✅ OK ({response_time}s)")

    print("\n✅ Monitor cycle finished\n")


if __name__ == "__main__":
    main()
