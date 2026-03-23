import json
from config import db

EXPIRE_TIME = 3600

async def get_chat_history(user_id: int):
    data = await db.get(f"chat:{user_id}")
    return json.loads(data) if data else []

async def get_all_triggers():
    triggers = await db.lrange("triggers", 0, -1)
    return triggers

async def get_raw_subjects(mode: str):
    raw_subjects = list()
    for level in range(1, 6): #5 criticism levels and 5 defendant levels
        temp = await db.lrange(f"{mode}:{level}", 0, -1)
        raw_subjects.append(temp)
    return raw_subjects

async def get_all_subjects():
    criticisms = await get_raw_subjects("criticism")
    defendants = await get_raw_subjects("defendant")
    return criticisms + defendants

async def save_json(user_id: int, data):
    await db.set(f"chat:{user_id}", json.dumps(data), ex=EXPIRE_TIME)

def save_to_redis(func):
    async def wrapper(self, *args, **kwargs):
        user_id = self.user_id

        message = await func(self, *args, **kwargs)
        self.messages.append(message)

        await save_json(user_id, self.messages)

        return message

    return wrapper