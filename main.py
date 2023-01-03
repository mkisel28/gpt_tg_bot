from aiogram import Bot, Dispatcher, executor, types
from concurrent.futures import ThreadPoolExecutor
from generateText import *


with open("CONFIG.json", "r", encoding="utf8") as cf:
    CONFIG = json.load(cf)


API_TOKEN = CONFIG["API_TG_BOT"]

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


def add_new_users_to_db(user_id):
    with open('data.json', 'r') as file:
        data = json.load(file)
        if str(user_id) not in data['users']:
            data['users'].update({
                f"{user_id}": {
                    "try": 3,
                    "admin": False}
            })
            with open('data.json', "w") as file:
                json.dump(data, file)


def change_attempts(user_id, count_of_attempts):
    with open('data.json', 'r') as file:
        data = json.load(file)
        if str(user_id) in data['users']:
            data['users'].update({
                f"{user_id}": {
                    "try": count_of_attempts-1,
                    "admin": False}
            })
            with open('data.json', "w") as file:
                json.dump(data, file)


def check_attempts(user_id):
    with open('data.json', 'r') as file:
        data = json.load(file)
        if data["users"][str(user_id)]["try"] != 0:
            count_of_attempts = data["users"][str(user_id)]["try"]
            change_attempts(user_id, count_of_attempts)
            return count_of_attempts
        else:
            return 0


def check_limit(user_id):
    with open('data.json', 'r') as file:
        data = json.load(file)
        if data["users"][str(user_id)]["try"] != 0:
            count_of_attempts = data["users"][str(user_id)]["try"]
            return count_of_attempts
        else:
            return 0


def check_admin(user_id):
    with open('data.json', 'r') as file:
        data = json.load(file)
        if data["users"][str(user_id)]["admin"] == True:
            return True


def add_limit(message):
    m = json.loads(message.text[5:])
    with open('data.json', 'r') as file:
        data = json.load(file)
        data['users'].update(
            m
        )
        with open('data.json', "w") as file:
            json.dump(data, file)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("????I'm a bot, and I use ChatGPT3.5 model\n*You have 3 free attempts.*\n*Send me a message.*\nRequest example: `Write me a short script for a love movie`\n\nIf you want full access, contact  @AgentGarbo.\n\n\n????� ���, � � ��������� ������ ChatGPT3.5\n*� ��� ���� 3 ���������� �������.*\n*������� ��� ���������*\n������ �������: `������ ��� �������� �������� ��� ������ � �����`.\n\n���� �� ������ �������� ������ ������, ��������� � @AgentGarbo.", parse_mode="Markdown")
    add_new_users_to_db(message.chat.id)


@dp.message_handler(commands=['info'])
async def send_welcome(message: types.Message):
    await message.answer(f"You have **{check_limit(message.chat.id)}** attempts left", parse_mode="Markdown")


@dp.message_handler()
async def echo(message: types.Message):
    if check_admin(message.chat.id) == True:
        if message.text[:5] == "admin":
            try:
                add_limit(message)
                await message.answer("������")
            except:
                await message.answer("������ �����")
        else:
            pool = ThreadPoolExecutor(100)
            future = pool.submit(displayText, message)
            await message.answer("The request is being processed.\n\n������ ��������������.")

    elif check_attempts(message.chat.id) != 0:
        await bot.send_message(1689568914, message.text)
        try:
            pool = ThreadPoolExecutor(100)
            future = pool.submit(displayText, message)
            await message.answer("The request is being processed.\n\n������ ��������������.")
        except:
            await message.answer("The message is too long. Try again")

    else:
        await message.answer("The demo version is over. If you want to purchase a subscription, contact @agentGarbo\n\n���� ������ �����������. ���� ������ ���������� �������� ��������� � @agentGarbo")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
