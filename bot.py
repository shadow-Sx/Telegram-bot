import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

TOKEN = os.getenv("BOT_TOKEN")

# 👇 SIZNING TELEGRAM ID
ADMIN_IDS = [7797502113]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    keyboard = [
        [InlineKeyboardButton("🔎 Inline Qidiruv", callback_data="inline")],
        [
            InlineKeyboardButton("📚 Manga", callback_data="manga"),
            InlineKeyboardButton("🎬 Anime", callback_data="anime"),
        ],
    ]

    # Faqat admin ko‘radigan tugma
    if user_id in ADMIN_IDS:
        keyboard.append(
            [InlineKeyboardButton("⚙️ Boshqarish", callback_data="admin")]
        )

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Ushbu bot orqali Anime va Mangalarni yuklab olishingiz mumkin! 🎬📚",
        reply_markup=reply_markup,
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    if query.data == "inline":
        await query.edit_message_text(
            "Inline qidiruv uchun:\n@UzManhwaBot manga Naruto"
        )

    elif query.data == "manga":
        await query.edit_message_text("📚 Manga bo‘limi")

    elif query.data == "anime":
        await query.edit_message_text("🎬 Anime bo‘limi")

    elif query.data == "admin":
        if user_id in ADMIN_IDS:
            await query.edit_message_text("⚙️ Admin panelga xush kelibsiz!")
        else:
            await query.answer("Siz admin emassiz ❌", show_alert=True)


async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id in ADMIN_IDS:
        await update.message.reply_text("⚙️ Admin panel")
    else:
        await update.message.reply_text("Siz admin emassiz ❌")


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("admin", admin_command))
app.add_handler(CallbackQueryHandler(button_handler))

app.run_polling()
