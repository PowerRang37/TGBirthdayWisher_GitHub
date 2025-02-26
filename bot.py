import asyncio
import random
import aiohttp
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# Replace with your actual bot token
TOKEN = "YOUR_BOT_TOKEN_HERE"
GROUP_CHAT_ID = "YOUR_GROUP_CHAT_ID_HERE"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# ✅ Dictionary of names and their birthdates (format: DD-MM)
birthdays = {
    "ExampleUser1": "27-02",
    "ExampleUser2": "05-09",
    "ExampleUser3": "18-07",
    "ExampleUser4": "25-08",
    "ExampleUser5": "13-11",
    "ExampleUser6": "15-02",
    "ExampleUser7": "13-01",
    "ExampleUser8": "16-11",
    "ExampleUser9": "14-06",
    "ExampleUser10": "26-03",
    "ExampleUser11": "01-09",
    "ExampleUser12": "16-01",
    "ExampleUser13": "03-04",
    "ExampleUser14": "10-02",
    "ExampleUser15": "17-04",
    "ExampleUser16": "08-06",
    "ExampleUser17": "16-11"
}

# Normalize username by removing '@' and converting to lowercase
def normalize_username(username):
    return username.lstrip('@').lower()

# Generate a birthday message
def generate_birthday_message(name):
    tagged_name = f"@{name}"
    messages = [
        f"🎉 Happy Birthday, {tagged_name}! 🎂🎈 May your day be filled with joy and laughter! 🥳",
        f"🥳 Wishing you a fantastic birthday, {tagged_name}! 🎁 Hope you have an amazing day ahead! 🎊",
        f"🎂 {tagged_name}, it's your special day! 🎈 Enjoy every moment and make unforgettable memories! 🥰",
        f"🌟 Happy Birthday, {tagged_name}! May this year bring you blessings, success, and happiness! 🎉",
        f"🎊 Cheers to you, {tagged_name}! 🥂 May your birthday bring joy, love, and everything your heart desires! 💖"
    ]
    return random.choice(messages)

# Fetch a joke from an external API
async def fetch_joke():
    url = "https://official-joke-api.appspot.com/jokes/random"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                joke_data = await response.json()
                return f"{joke_data['setup']} {joke_data['punchline']}"
            else:
                return "Failed to fetch a joke. Try again later."

# Command handler to send a joke
@dp.message(Command("joke"))
async def send_joke(message: types.Message):
    joke = await fetch_joke()
    await message.answer(joke)

# Check birthdays and send messages
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
        except Exception as e:
            print(f"❌ Failed to send message: {e}")

# Main function to start the bot
async def main():
    await check_birthdays()
    await dp.start_polling(bot)

# Run the bot
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot is off")
