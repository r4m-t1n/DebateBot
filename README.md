# DebateBot

DebateBot is a Telegram userbot designed to participate in conversations on your behalf. Based on your configuration, it acts as a "Biased Truth-Twister," either defending or criticizing specific subjects with varying levels of intensity. Since this is a userbot, it runs directly on your personal account, meaning you will need to log in with your phone number.

## Core Technologies

- Pyrogram (Telegram Framework)
- Redis (Database for triggers and history)
- Cerebras Cloud SDK (LLM Engine)

## Setup and Installation

### 1. Requirements
Ensure you have Redis installed and running on localhost:6379.

### 2. Environment Configuration
Create a .env file in the root directory. You can use example.env as a template. Fill in the following fields:

- ADMIN_ID: Your numerical Telegram User ID (only this ID can manage the bot).
- BOT_API_ID: Your API ID from my.telegram.org.
- BOT_API_HASH: Your API Hash from my.telegram.org.
- PHONE_NUMBER: Your phone number linked to the Telegram account.
- MODEL_NAME: The specific model used by the LLM provider.
- LLM_API: Your Cerebras Cloud API key.
- NEWS_API: Your NewsAPI key (Not implemented yet).

### 3. Running the Bot
Install the dependencies from the requirements file and start the project:

```bash
pip install -r requirements.txt
python src/run.py
```

On the first run, enter the code sent by Telegram into the terminal to authorize the session.

## Configuration and Commands

Only the user defined in ADMIN_ID can use these commands.

### Setting a Critic
Usage: /set_critic [level] [subject] [triggers]
- Level: 1 to 5 (1 is a mild skeptic, 5 is total destruction).
- Subject: The entity to be criticized.
- Triggers: Keywords that prompt the bot to respond.

Example:
/set_critic 5 "John Cena" "world wrestling entertainment" "john cena" WWE ""

### Setting a Defender
Usage: /set_defender [level] [subject] [triggers]
- Level: 1 to 5 (1 is a supportive fan, 5 is a fanatical zealot).

Example:
/set_defender 4 "Bitcoin" crypto btc "digital gold"

### Customizing Data
- To adjust the bot identity and response logic: src/data/prompts.yaml.
- To edit system feedback and error messages: src/data/messages.yaml.

## Project Structure

- src/run.py: Entry point.
- src/handlers/: Admin command logic and chat processing.
- src/services/: LLM integration and chat history management.
- src/utils/: Helpers for argument parsing and Redis interactions.
- src/data/: YAML storage for prompts and messages.

## Important Notes

- LLM Safety Constraints: If a user input is extremely aggressive or violates safety protocols, the LLM may pivot to defending a subject even in Critic mode to comply with its internal filters.
- Context Isolation: For optimal performance, add subjects that are contextually related. While the system uses trigger isolation, grouped subjects help minimize mixed-context errors.
- Upcoming Features: NEWS integration via newsapi.org is coming soon, allowing the bot to respond based on real-time global events.

## License

This project is licensed under the Apache License 2.0.