from dotenv import load_dotenv
load_dotenv()

from config import bot
from handlers.admin import set_critic, set_defender
from handlers.chat import read_messages

if __name__ == "__main__":
    bot.run()