import pyrogram
from pyrogram import filters
from config import bot, db, messages, ADMIN_ID
from utils.parser import split_args

async def respond(message: pyrogram.types.Message, text: str):
    if message.from_user.is_self:
        return await message.edit_text(text=text)
    else:
        return await message.reply_text(text=text, quote=True)


async def save_settings(message: pyrogram.types.Message, mode: str):
    args = split_args(message.text)[1:]

    if len(args) < 3:
        return await respond(message, messages[mode])

    level = args[0]
    if not level.isdigit():
        return await respond(message, messages["invalid_level"])

    level = int(level)

    if not (1<=level<=5):
        return await respond(message, messages["invalid_level"])

    subject = args[1]
    triggers = args[2:]

    mode = {
        "set_critic": "criticism",
        "set_defender": "defendant",
    }[mode]

    await db.rpush(f"{mode}:{level}", subject)
    await db.rpush("triggers", " ".join(triggers))

    return await respond(message,
        messages["set_successful"].format(
            subject=subject,
            triggers="\n".join(triggers)
        )
    )


@bot.on_message(filters.command(["set_critic"]) & filters.user(ADMIN_ID))
async def set_critic(bot: pyrogram.Client, message: pyrogram.types.Message):
    return await save_settings(message, "set_critic")


@bot.on_message(filters.command(["set_defender"]) & filters.user(ADMIN_ID))
async def set_defender(bot: pyrogram.Client, message: pyrogram.types.Message):
    return await save_settings(message, "set_defender")
