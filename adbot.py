from telethon.sync import TelegramClient
import json
import os

with open("acc.json", "r", encoding="utf-8") as f:
    accounts = json.load(f)

for acc in accounts:
    session_name = acc["session_name"]
    api_id = acc["api_id"]
    api_hash = acc["api_hash"]
    phone = acc["phone_number"]

    print(f"\n➡️ Logging in for {phone} (session: {session_name})")

    client = TelegramClient(session_name, api_id, api_hash)
    client.start(phone)
    client.disconnect()

    print(f"✅ Session created: {session_name}.session")
