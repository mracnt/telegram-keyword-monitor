import asyncio
import json
import os
import time
from telethon import TelegramClient, events

API_ID = int(os.environ['API_ID'])
API_HASH = os.environ['API_HASH']
BOT_TOKEN = os.environ['BOT_TOKEN']
MY_ID = int(os.environ['MY_ID'])
BOT_ID = int(os.environ.get('BOT_ID', 0))

KEYWORDS_FILE = 'keywords.json'
START_TIME = None

def load_keywords():
    if os.path.exists(KEYWORDS_FILE):
        with open(KEYWORDS_FILE) as f:
            return json.load(f)
    return ['A36']

def save_keywords(kws):
    with open(KEYWORDS_FILE, 'w') as f:
        json.dump(kws, f)

keywords = load_keywords()

user_client = TelegramClient('sessione', API_ID, API_HASH)
bot_client = TelegramClient('bot', API_ID, API_HASH)

@user_client.on(events.NewMessage(incoming=True))
async def monitor(event):
    if START_TIME is None:
        return
    if event.is_private:
        return
    if event.sender_id == BOT_ID:
        return
    msg_time = event.date.timestamp()
    if msg_time < START_TIME:
        return
    text = event.message.text or ''
    for kw in keywords:
        if kw.lower() in text.lower():
            chat = await event.get_chat()
            chat_name = getattr(chat, 'title', getattr(chat, 'username', 'Sconosciuto'))
            try:
                await bot_client.send_message(MY_ID,
                    f"🔔 Keyword trovata:
