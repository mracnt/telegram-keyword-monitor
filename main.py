import asyncio
import json
import os
import time
from telethon import TelegramClient, events

API_ID = int(os.environ['API_ID'])
API_HASH = os.environ['API_HASH']
BOT_TOKEN = os.environ['BOT_TOKEN']
MY_ID = int(os.environ['MY_ID'])

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

@user_client.on(events.NewMessage)
async def monitor(event):
    if START_TIME is None:
        return
    if event.out or event.is_private:
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
                    f"🔔 Keyword trovata: {kw}\n"
                    f"📢 Canale: {chat_name}\n\n"
                    f"{text[:500]}"
                )
            except Exception as e:
                print(f"Errore invio messaggio: {e}")

@bot_client.on(events.NewMessage(from_users=MY_ID, pattern='/add (.+)'))
async def add_keyword(event):
    kw = event.pattern_match.group(1).strip()
    if kw not in keywords:
        keywords.append(kw)
        save_keywords(keywords)
        await event.reply(f"✅ Keyword {kw} aggiunta!")
    else:
        await event.reply(f"⚠️ {kw} è già presente!")

@bot_client.on(events.NewMessage(from_users=MY_ID, pattern='/remove (.+)'))
async def remove_keyword(event):
    kw = event.pattern_match.group(1).strip()
    if kw in keywords:
        keywords.remove(kw)
        save_keywords(keywords)
        await event.reply(f"✅ Keyword {kw} rimossa!")
    else:
        await event.reply(f"⚠️ {kw} non trovata!")

@bot_client.on(events.NewMessage(from_users=MY_ID, pattern='/list'))
async def list_keywords(event):
    if keywords:
        kw_list = '\n'.join([f"• {kw}" for kw in keywords])
        await event.reply(f"📋 Keyword attive:\n{kw_list}")
    else:
        await event.reply("📋 Nessuna keyword attiva.")

async def main():
    global START_TIME
    await user_client.start()
    await bot_client.start(bot_token=BOT_TOKEN)
    START_TIME = time.time()
    print(f"Bot avviato! START_TIME: {START_TIME}")
    await asyncio.gather(
        user_client.run_until_disconnected(),
        bot_client.run_until_disconnected()
    )

asyncio.run(main())
