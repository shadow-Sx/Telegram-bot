import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

TOKEN = os.getenv("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("📚 Manga", callback_data="manga"),
            InlineKeyboardButton("🔥 Trending", callback_data="trending"),
        ],
        [
            InlineKeyboardButton("ℹ️ About", callback_data="about")
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Asosiy menyu 👇",
        reply_markup=reply_markup
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "manga":
        await query.edit_message_text("📚 Manga bo‘limi")
    elif query.data == "trending":
        await query.edit_message_text("🔥 Eng mashhurlari")
    elif query.data == "about":
        await query.edit_message_text("Bu manga bot 🔥")


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))

app.run_polling()
