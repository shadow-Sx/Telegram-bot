import asyncio
import secrets
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from config import BOT_TOKEN, OWNER_ID, ADMINS
from database import *

bot = Bot(BOT_TOKEN)
dp = Dispatcher()


# ================= USERNAME CHECK =================
def username_required(user):
    if user.id in ADMINS:
        return True
    return bool(user.username)


# ================= START HANDLER =================
@dp.message(CommandStart(deep_link=True))
async def start_with_token(message: Message, command):
    user = message.from_user

    if not username_required(user):
        await message.answer(
            f"Iltimos hurmatli {user.full_name},\n\n"
            "Username o‘rnatganingizdan so‘ng botga /start bosing."
        )
        return

    token = command.args
    channel = get_channel_by_token(token)

    if not channel:
        await message.answer("Noto‘g‘ri yoki eskirgan havola.")
        return

    channel_id = channel[0]
    channel_type = channel[2]
    channel_value = channel[3]
    required = channel[5]
    current = channel[6]

    # obuna tekshirish
    if channel_type in ["username", "id"]:
        try:
            member = await bot.get_chat_member(channel_value, user.id)
            if member.status not in ["member", "administrator", "creator"]:
                await message.answer("Siz hali kanalga obuna bo‘lmagansiz.")
                return
        except:
            await message.answer("Kanal tekshirishda xatolik.")
            return

    # obuna hisoblash
    increase_count(channel_id)

    await message.answer("✅ Obuna tasdiqlandi!")

    # limit tugaganini tekshirish
    if current + 1 >= required:
        await bot.send_message(
            OWNER_ID,
            f"🎉 {channel[4]} limiti bajarildi!"
        )


# ================= ODDIY START =================
@dp.message(CommandStart())
async def start_normal(message: Message):
    user = message.from_user

    if not username_required(user):
        await message.answer(
            f"Iltimos hurmatli {user.full_name},\n\n"
            "Username o‘rnatganingizdan so‘ng botga /start bosing."
        )
        return

    add_user(user.id, user.username, user.full_name)

    await message.answer("Bot ishlamoqda.")


# ================= RUN =================
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
