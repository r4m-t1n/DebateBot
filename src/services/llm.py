from config import client, prompts, MODEL_NAME

async def llm_check_trigger(text: str, triggers: list[str]):
    response = await client.chat.completions.with_raw_response(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": prompts.format(text, triggers)
            }, {
                "role": "user",
                "content:": "user's content: {}\n our subjects:{}".format(
                    text, triggers
                )
            }],
        temperature=0,
        max_tokens=800
    )
    return {
        "True": True,
        "False": False
    }[response]