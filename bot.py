import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from database import init_db, add_site


TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


init_db()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to Healthy Watcher\n\n"
        "Use:\n"
        "/add website contact booking\n\n"
        "Example:\n"
        "/add https://site.com https://site.com/contact https://site.com/book"
    )

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        website = context.args[0]
        contact = context.args[1]
        booking = context.args[2]
        chat_id = update.effective_chat.id

        add_site(chat_id, website, contact, booking)

        await update.message.reply_text(
            "✅ Healthy Watcher activated!\n\n"
            "We will check your website every 30 minutes."
        )

    except:
        await update.message.reply_text(
            "❌ Usage:\n"
            "/add website contact booking"
        )

app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("add", add))

app.run_polling()
