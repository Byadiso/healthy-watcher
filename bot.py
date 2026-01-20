import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from database import (
    init_db,
    add_site,
    get_sites_by_chat,
    update_status,
    save_check
)

from database import get_uptime_stats


from checker import check_website

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


init_db()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to Healthy Watcher\n\n"
        "Commands:\n"
        "/add website contact booking\n"
        "/list — your websites\n"
        "/status url — live check"
    )


async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        website = context.args[0]
        contact = context.args[1]
        booking = context.args[2]
        chat_id = update.effective_chat.id

        add_site(chat_id, website, contact, booking)

        await update.message.reply_text(
            "✅ Monitoring activated!\n\n"
            "We check every 30 minutes."
        )
    except:
        await update.message.reply_text(
            "❌ Usage:\n/add website contact booking"
        )


async def list_sites(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    sites = get_sites_by_chat(chat_id)

    if not sites:
        await update.message.reply_text("📭 No websites added yet.")
        return

    msg = "📊 Your websites:\n\n"
    for i, (site_id, website, status) in enumerate(sites, start=1):
        icon = "✅" if status == "ok" else "🚨"
        msg += f"{i}. {icon} {website}\n"

    await update.message.reply_text(msg)


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    if not context.args:
        await update.message.reply_text(
            "❌ Usage:\n/status https://example.com"
        )
        return

    url = context.args[0]
    await update.message.reply_text("🔍 Checking website...")

    status_value, response_time = check_website(url)

    sites = get_sites_by_chat(chat_id)
    site_id = None

    for s in sites:
        if s[1] == url:
            site_id = s[0]
            break

    if site_id:
        save_check(site_id, status_value, response_time)
        update_status(site_id, status_value)

    if status_value == "ok":
        msg = (
            f"✅ Website is UP\n\n"
            f"🌐 {url}\n"
            f"⏱ Response time: {response_time}s"
        )
    else:
        msg = (
            f"🚨 Website is DOWN\n\n"
            f"🌐 {url}\n"
            f"❌ No response"
        )

    await update.message.reply_text(msg)

async def uptime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    if not context.args:
        await update.message.reply_text(
            "❌ Usage:\n/uptime https://example.com"
        )
        return

    url = context.args[0]

    sites = get_sites_by_chat(chat_id)

    site_id = None
    for s in sites:
        if s[1] == url:
            site_id = s[0]
            break

    if not site_id:
        await update.message.reply_text(
            "⚠️ Website not found.\nUse /list to see your sites."
        )
        return

    total, ok = get_uptime_stats(site_id)

    if total == 0:
        await update.message.reply_text(
            "⏳ Not enough data yet.\nWait for monitoring to collect data."
        )
        return

    uptime_percent = round((ok / total) * 100, 2)
    down_percent = round(100 - uptime_percent, 2)

    msg = (
        f"📊 <b>Uptime Report (last 24h)</b>\n\n"
        f"🌐 {url}\n"
        f"✅ Uptime: <b>{uptime_percent}%</b>\n"
        f"🚨 Downtime: {down_percent}%\n"
        f"📈 Checks: {total}"
    )

    await update.message.reply_text(msg, parse_mode="HTML")



app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("add", add))
app.add_handler(CommandHandler("list", list_sites))
app.add_handler(CommandHandler("status", status))

app.add_handler(CommandHandler("uptime", uptime))


app.run_polling()
