import asyncio
import pyrogram
from pyrogram import filters
from pyrogram.enums import ChatAction
from pyrogram.errors import FloodWait
from config import bot
from services.llm import Chat, llm_check_trigger
from utils.parser import check_triggers
from utils.redis_utils import get_all_triggers

AVERAGE_TYPING_SPEED = 100

@bot.on_message(~filters.me)
async def read_messages(bot: pyrogram.Client, message: pyrogram.types.Message):
    if (replied_to := message.reply_to_message) and (replied_to.from_user == bot.me):
        return await respond_to_user(message)

    triggers = await get_all_triggers()
    triggered = check_triggers(message.text, triggers)

    if not triggered:
        return

    related_to_subjects = await llm_check_trigger(message.text)

    if not related_to_subjects:
        return

    await respond_to_user(message)


async def respond_to_user(message: pyrogram.types.Message):
    chat = Chat(message.from_user.id)
    await chat.initialize()

    response = await chat.respond_message(message.text)

    if not response:
        return

    asyncio.create_task(send_delayed_message(bot, message, response))


async def send_delayed_message(
        bot: pyrogram.Client, message: pyrogram.types.Message, response: str):

    minutes_to_delay = len(response.split())/AVERAGE_TYPING_SPEED
    seconds_to_delay = int(minutes_to_delay * 60)

    while seconds_to_delay>0:
        try:
            await bot.send_chat_action(message.chat.id, ChatAction.TYPING)
            await asyncio.sleep(5)
        except FloodWait as e:
            await asyncio.sleep(e.value)
        seconds_to_delay -= 5

    try:
        await message.reply_text(response, quote=True)
    except FloodWait as e:
        await asyncio.sleep(e.value)
        await message.reply_text(response, quote=True)