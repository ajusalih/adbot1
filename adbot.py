import json
import asyncio
import os
import time
from telethon import TelegramClient, events
import colorama
from termcolor import colored

colorama.init()

# Load acc.json
json_path = os.path.join(os.path.dirname(__file__), 'acc.json')
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        accounts = json.load(f)
except Exception as e:
    print(colored(f"❌ Unable to load acc.json: {e}", "red"))
    exit()

last_sent_times = {}
latest_message = {}

def is_valid_group(dialog):
    entity = dialog.entity
    return getattr(entity, 'megagroup', False) or getattr(entity, 'gigagroup', False) or dialog.is_group

async def forward_message_to_groups(client, message):
    dialogs = await client.get_dialogs()
    now = time.time()
    sent_count = 0

    for dialog in dialogs:
        if is_valid_group(dialog):
            group_id = dialog.id
            last_sent = last_sent_times.get(group_id, 0)
            if now - last_sent >= 120:  # 2 minutes
                try:
                    await client.forward_messages(group_id, message)
                    last_sent_times[group_id] = now
                    sent_count += 1
                except:
                    continue

    if sent_count >= 5:
        print(colored(f"✅ Message forwarded to {sent_count} groups", "green"))

async def listen_for_admin_messages(client, admin_ids, session_name):
    @client.on(events.NewMessage)
    async def handler(event):
        if event.sender_id not in admin_ids:
            return  # silently ignore non-admins

        latest_message[session_name] = event.message
        await forward_message_to_groups(client, event.message)

async def periodic_forwarder(client, session_name):
    while True:
        msg = latest_message.get(session_name)
        if msg:
            await forward_message_to_groups(client, msg)
        await asyncio.sleep(120)

async def main():
    for account in accounts:
        api_id = account["api_id"]
        api_hash = account["api_hash"]
        phone_number = account["phone_number"]
        session_name = account["session_name"]
        admin_ids = account.get("admin_ids")

        if not admin_ids:
            print(colored(f"❌ admin_ids missing for {phone_number}", "red"))
            continue

        client = TelegramClient(session_name, api_id, api_hash)

        try:
            await client.start(phone_number)
            await listen_for_admin_messages(client, admin_ids, session_name)
            print(colored(f"🤖 Bot is running successfully for {phone_number}", "cyan"))
            asyncio.create_task(periodic_forwarder(client, session_name))
            await client.run_until_disconnected()
        except Exception as e:
            print(colored(f"❌ Failed to run bot for {phone_number}: {e}", "red"))

if __name__ == "__main__":
    asyncio.run(main())


