import asyncio
import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.types import InputMediaPhoto
import time

BOT_TOKEN = "7745302518:AAGdrULCTHKDyj4S0Y9JSsQPYXpQM1n86BA"
CHAT_ID = 7386658894

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

async def fetch_json(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            if r.status == 200:
                return await r.json()
            return None

async def check_jup_ag():
    url = "https://price.jup.ag/tokens"
    data = await fetch_json(url)
    results = []

    if data:
        for token in data.get("tokens", []):
            try:
                name = token.get("name")
                symbol = token.get("symbol")
                address = token.get("address")
                price = float(token.get("price", 0))
                mcap = float(token.get("marketCap", 0))

                if mcap >= 15000:
                    msg = f"🚀 <b>{name} ({symbol})</b>\n💰 Market Cap: ${int(mcap):,}\n🧠 Contract: <code>{address}</code>\n💸 Price: ${price:.8f}"
                    results.append(msg)
            except:
                continue
    return results

async def check_pumpfun():
    url = "https://pump.fun/api/recent"
    data = await fetch_json(url)
    results = []

    if data:
        for item in data[:10]:
            try:
                name = item.get("name")
                symbol = item.get("symbol", "")
                address = item.get("address")
                image = item.get("image", "")
                mcap = float(item.get("market_cap", 0))
                launched = time.time() - int(item.get("created_at", time.time()))

                if mcap >= 15000:
                    msg = f"🚀 <b>{name} ({symbol})</b>\n💰 Market Cap: ${int(mcap):,}\n🕒 Age: {int(launched)} sec\n🧠 Contract: <code>{address}</code>"
                    results.append((msg, image))
            except:
                continue
    return results

async def send_messages():
    msgs = await check_jup_ag()
    tokens = await check_pumpfun()
    if not msgs and not tokens:
        await bot.send_message(CHAT_ID, "Sorry Mr. Rafiq, no tokens at the moment. Damn you, Basem.")
    else:
        for m in msgs:
            await bot.send_message(CHAT_ID, m)

        for text, img_url in tokens:
            if img_url:
                await bot.send_photo(CHAT_ID, photo=img_url, caption=text)
            else:
                await bot.send_message(CHAT_ID, text)

async def main_loop():
    while True:
        try:
            await send_messages()
        except Exception as e:
            print("Error:", e)
        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main_loop())
