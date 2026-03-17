import os

import pyrogram
from redis.asyncio import Redis
from cerebras.cloud.sdk import AsyncCerebras
from utils.loader import load_yaml

ADMIN_ID = int(os.getenv("ADMIN_ID"))

BOT_API_ID = os.getenv("BOT_API_ID")
BOT_API_HASH = os.getenv("BOT_API_HASH")
PHONE_NUMBER = os.getenv("PHONE_NUMBER")

MODEL_NAME = os.getenv("MODEL_NAME")
LLM_API = os.getenv("LLM_API")
NEWS_API = os.getenv("NEWS_API")

bot = pyrogram.Client(
    "DebateBot",
    api_id=BOT_API_ID,
    api_hash=BOT_API_HASH,
    phone_number=PHONE_NUMBER
)
client = AsyncCerebras(api_key=LLM_API)
db = Redis(host="localhost", port=6379, decode_responses=True)

messages: str = load_yaml(os.path.join("data", "messages.yaml"))
prompts: str = load_yaml(os.path.join("data", "prompts.yaml"))