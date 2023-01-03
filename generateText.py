import openai
from pyrogram import Client, filters
import json

with open("CONFIG.json", "r", encoding="utf8") as cf:
    CONFIG = json.load(cf)

openai.api_key = CONFIG["API_OPENAI_KEY"]

api_id = CONFIG["PYROGRAM_API_ID"]
api_hash = CONFIG["PYROGRAM_API_HASH"]
bot_token = CONFIG["PYROGRAM_API_TOKEN"]
app = Client(
    "my_bo1t",
    api_id=api_id, api_hash=api_hash,
    bot_token=bot_token
)
app.start()


def generateText(text):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=text,
        temperature=0.7,
        max_tokens=3000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
    )
    data = response
    return (data["choices"][0]["text"])


def displayText(message):
    app.send_message(message.from_user.id, generateText(message.text))
    return "Done"
