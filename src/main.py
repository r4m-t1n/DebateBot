import os
from dotenv import load_dotenv

import pyrogram
from google import genai
from cerebras.cloud.sdk import AsyncCerebras

load_dotenv()

ADMIN_ID = os.getenv("ADMIN_ID")

BOT_API_ID = os.getenv("BOT_API_ID")
BOT_API_HASH = os.getenv("BOT_API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

LLM_API = os.getenv("LLM_API")

bot = pyrogram.Client(
    "DebateBot",
    api_id=BOT_API_ID,
    api_hash=BOT_API_HASH,
    bot_token=BOT_TOKEN
)
client = AsyncCerebras(api_key=LLM_API)

@bot.on_message()
async def main(bot: pyrogram.Client, message: pyrogram.types.Message):

    response = await client.chat.completions.create(
        model="llama3.1-8b",
        messages=[{
            "role": "user",
            "content": message.text
        }],
        temperature=0.4,
        max_tokens=800
    )

    await message.reply_text(response.choices[0].message.content, quote=True)

bot.run()