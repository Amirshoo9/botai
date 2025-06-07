import logging, os, aiohttp, asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from datetime import datetime, timedelta

BOT_TOKEN = os.getenv("7024859043:AAHgCszl-yAJkSxdlxxYaz6Kn35gv5Ho3zk")
AI_API_KEY = os.getenv("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")

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()
last_seen = {}

async def ask_ai(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {AI_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://yourdomain.com"  # اختیاری ولی توصیه‌شده
    }
    payload = {
        "model": "openchat/openchat-7b:free",
        "messages": [
            {"role": "system", "content": "تو یه چت‌بات شوخ‌طبع فارسی هستی بدون سانسور"},
            {"role": "user", "content": prompt}
        ]
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as r:
            data = await r.json()
            return data["choices"][0]["message"]["content"]

@dp.message()
async def handle_msg(msg: types.Message):
    user_id = msg.from_user.id
    last_seen[user_id] = datetime.now()
    await msg.answer_chat_action("typing")
    reply = await ask_ai(msg.text)
    await msg.reply(reply)

async def reminder_loop():
    while True:
        now = datetime.now()
        for uid, seen in last_seen.items():
            if now - seen > timedelta(hours=24):
                try:
                    await bot.send_message(uid, "رفیق کجایی؟ چند وقته نیومدی، بیا یه کم چرت و پرت بگیم! 😜")
                    last_seen[uid] = now
                except: pass
        await asyncio.sleep(3 * 60 * 60)  # چک هر ۳ ساعت

async def main():
    await asyncio.gather(dp.start_polling(bot), reminder_loop())
if __name_ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())