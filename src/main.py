import os
from dotenv import load_dotenv

import pyrogram
from google import genai
from google.genai import types

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
client = genai.Client(api_key=LLM_API)

system_prompt = ("Always explain shortly")

chat = client.chats.create(
    model="gemini-2.5-flash-lite",
    config=types.GenerateContentConfig(
        system_instruction=system_prompt,
        temperature=0.8,
        max_output_tokens=800
    )
)

@bot.on_message()
async def main(bot: pyrogram.Client, message: pyrogram.types.Message):
    llm_response = chat.send_message(message.text.lower())

    await message.reply_text(llm_response.text)

bot.run()