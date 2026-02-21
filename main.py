from telethon import TelegramClient, events
from config import API_ID, API_HASH, KEYWORDS
import re

client = TelegramClient('sessione', API_ID, API_HASH)

def contains_keyword(text):
    if not text:
        return None
    for kw in KEYWORDS:
        if re.search(rf'\b{re.escape(kw.strip())}\b', text, re.IGNORECASE):
            return kw.strip()
    return None

@client.on(events.NewMessage)
async def handler(event):
    kw = contains_keyword(event.message.text)
    if kw:
        chat = await event.get_chat()
        chat_name = getattr(chat, 'title', getattr(chat, 'username', 'Sconosciuto'))
        await client.send_message('me', (
            f"🔔 *Keyword trovata:* `{kw}`\n"
            f"📢 *Canale:* {chat_name}\n\n"
            f"{event.message.text[:500]}"
        ), parse_mode='markdown')

print("Bot avviato, monitoraggio in corso...")
client.start()
client.run_until_disconnected()
