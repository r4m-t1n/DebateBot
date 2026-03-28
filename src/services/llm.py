from config import client, prompts, messages, MODEL_NAME, TokensLimitExceeded
from utils.redis_utils import get_chat_history, get_all_subjects, save_json, save_to_redis
from utils.parser import parse_subjects, export_subjects

class Chat:
    def __init__(self, user_id):
        self.user_id = user_id
        self.messages = []

    async def initialize(self):
        all_subjects = await export_subjects()
        self.messages = await get_chat_history(self.user_id)

        if self.messages != []:
            return

        self.messages = [{
            "role": "system",
            "content": prompts["system_debate"].format(
                all_subjects="\n".join(all_subjects)
            )
        }]
        await save_json(self.user_id, self.messages)

    @save_to_redis
    async def _append_users_msg(self, message: str):
        return {
            "role": "user",
            "content": message
        }

    @save_to_redis
    async def _append_responded_msg(self, message: str):
        return {
            "role": "assistant",
            "content": message
        }

    async def respond_message(self, message: str):
        try:
            response = await client.chat.completions.create(
                model=MODEL_NAME,
                messages=self.messages,
                temperature=0,
                max_tokens=800
            )

            response = response.choices[0].message.content

            await self._append_users_msg(message)
            await self._append_responded_msg(response)
            return response
        except TokensLimitExceeded:
            return messages["default_txt_tokens_limit_exceeded"]


async def llm_check_trigger(text: str):
    subjects = await get_all_subjects()
    subjects = parse_subjects(subjects)

    try:
        response = await client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": prompts["system_check_trigger"]
                }, {
                    "role": "user",
                    "content": "user's content: {}\n our subjects: {}".format(
                        text, subjects
                    )
                }],
            temperature=0,
            max_tokens=10
        )
        result = response.choices[0].message.content.strip().lower()

        if "true" in result:
            return True
        return False
    except TokensLimitExceeded:
        return False