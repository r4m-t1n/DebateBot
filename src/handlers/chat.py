import pyrogram
from pyrogram import filters
from config import bot
from services.llm import Chat, llm_check_trigger
from utils.parser import check_triggers
from utils.redis_utils import get_all_triggers

@bot.on_message(~filters.me)
async def read_messages(bot: pyrogram.Client, message: pyrogram.types.Message):
    if (replied_to := message.reply_to_message) and (not replied_to.from_user == bot.me):
        triggers = await get_all_triggers()
        triggered = check_triggers(message.text, triggers)

        if not triggered:
            return

        related_to_subjects = await llm_check_trigger(message.text)

        if not related_to_subjects:
            return

    chat = Chat(message.from_user.id)
    await chat.initialize()

    response = await chat.respond_message(message.text)

    await message.reply_text(response, quote=True)