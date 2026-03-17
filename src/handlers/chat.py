import pyrogram
from pyrogram import filters
from config import bot, client, db, MODEL_NAME
from utils.parser import check_triggers

@bot.on_message(~filters.me)
async def read_messages(bot: pyrogram.Client, message: pyrogram.types.Message):
    triggers = await db.lrange("triggers", 0, -1)
    triggered = check_triggers(message.text, triggers)

    if not triggered:
        return

    response = await client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{
            "role": "user",
            "content": message.text
        }],
        temperature=0,
        max_tokens=800
    )

    await message.reply_text(response.choices[0].message.content, quote=True)