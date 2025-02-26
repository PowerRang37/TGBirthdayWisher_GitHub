import asyncio
import random
import aiohttp
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

TOKEN = '6139048926:AAGCuYYyXhjK9Tg0wlsdchaWi1zLHOXOjbA'
GROUP_CHAT_ID = '-1001380011085'
#My_GROUP_CHAT_ID = '-1001591926639'

bot = Bot(token=TOKEN)
dp = Dispatcher()

# ✅ List of people who can collect money
collectors = [
    "@Pow37Rang37", "@tupacalyps3", "@Dnkzgfx", "@ibakiyev",
    "@nurbeha", "@NurlybekTheGreat", "@ValerieT",
    "@zharenaya_kartoha", "@Pepe33333", "@vvinter999",
    "@Disagyndykov", "@zh_batyrbek", "@Elmenski", "@shulenov",
    "@moontuar", "@nargiz_nurly", "@dava1616"
]

# ✅ List of people **excluded** from money collection selection
excluded_from_collection = [
    "@Disagyndykov", "@zh_batyrbek",
    "@Elmenski", "@shulenov", "@moontuar", "@nargiz_nurly", "@dava1616"
]

# ✅ Dictionary of names and their birthdates (format: DD-MM)
birthdays = {
    "Pow37Rang37": "27-02",
    "tupacalyps3": "05-09",
    "Dnkzgfx": "18-07",
    "ibakiyev": "25-08",
    "nurbeha": "13-11",
    "NurlybekTheGreat": "15-02",
    "ValerieT": "13-01",
    "zharenaya_kartoha": "16-11",
    "Pepe33333": "14-06",
    "vvinter999": "26-03",
    "Disagyndykov": "01-09",
    "zh_batyrbek": "16-01",
    "moontuar": "03-04",
    "shulenov": "10-02",
    "Elmenski": "17-04",
    "nargiz_nurly": "08-06",
    "dava1616": "16-11"
}

def normalize_username(username):
    return username.lstrip('@').lower()

def generate_birthday_message(name):
    tagged_name = f"@{name}"
    messages = [
        f"🎉 С Днем Рождения, {tagged_name}! 🎂🎈 Пусть твой день будет наполнен счастьем и смехом! 🥳",
        f"🥳 Желаю тебе фантастического дня рождения, {tagged_name}! 🎁 Надеюсь, впереди тебя ждет удивительный день! 🎊",
        f"🎂 {tagged_name}, это твой особенный день! 🎈 Наслаждайся каждым мгновением и создай незабываемые воспоминания! 🥰",
        f"🌟 С Днем Рождения, {tagged_name}! Пусть наступающий год будет полон благословений, успеха и радости! 🎉",
        f"🎊 За твое здоровье, {tagged_name}! 🥂 Пусть твой день рождения принесет тебе счастье, любовь и все, о чем мечтает твое сердце! 💖"
    ]
    return random.choice(messages)

async def fetch_joke():
    url = "https://official-joke-api.appspot.com/jokes/random"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                joke_data = await response.json()
                return f"{joke_data['setup']} {joke_data['punchline']}"
            else:
                return "Failed to fetch a joke. Try again later."

@dp.message(Command("joke"))
async def send_joke(message: types.Message):
    joke = await fetch_joke()
    await message.answer(joke)

async def check_birthdays():
    today = datetime.today().strftime('%d-%m')
    birthdays_today = [name for name, bday in birthdays.items() if bday == today]

    if not birthdays_today:
        print("📅 No birthdays today.")
        return

    for name in birthdays_today:
        tagged_name = f"@{name}"
        birthday_message = generate_birthday_message(name)

        try:
            await bot.send_message(GROUP_CHAT_ID, birthday_message)
            print(f"✅ Birthday message sent: {birthday_message}")

            if normalize_username(name) not in [normalize_username(x) for x in excluded_from_collection]:
                available_collectors = [
                    collector for collector in collectors
                    if collector.lower() != f"@{name.lower()}" and
                       normalize_username(collector) not in [normalize_username(x) for x in excluded_from_collection]
                ]
                selected_collector = random.choice(available_collectors) if available_collectors else "No available collector"

                collection_message = (
                    f"Привет, {selected_collector}! Твоя миссия: собрать по 5000 тг с каждого участника для {tagged_name}. Прошу принять в работу.")
                
                await bot.send_message(GROUP_CHAT_ID, collection_message)
                print(f"✅ Collection request sent: {collection_message}")

        except Exception as e:
            print(f"❌ Failed to send message: {e}")

async def main():
    await check_birthdays()
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot is off")
