import json
import asyncio
import os
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

# Forward messages to all groups (silently)
async def forward_message_to_groups(client, message):
    dialogs = await client.get_dialogs()
    count = 0
    for dialog in dialogs:
        if dialog.is_group:
            try:
                await client.forward_messages(dialog.id, message)
                count += 1
            except:
                pass
    print(colored(f"✅ Message forwarded to {count} groups", "green"))

# Listen for admin messages
async def listen_for_admin_messages(client, admin_id):
    @client.on(events.NewMessage(from_users=admin_id))
    async def handler(event):
        await forward_message_to_groups(client, event.message)
    return handler

# Main logic
async def main():
    for account in accounts:
        api_id = account["api_id"]
        api_hash = account["api_hash"]
        phone_number = account["phone_number"]
        session_name = account["session_name"]
        admin_id = account.get("admin_id")

        if admin_id is None:
            print(colored(f"❌ admin_id missing for {phone_number}", "red"))
            continue

        client = TelegramClient(session_name, api_id, api_hash)

        try:
            await client.start(phone_number)
            await listen_for_admin_messages(client, admin_id)
            print(colored(f"🤖 Bot is running successfully for {phone_number}", "cyan"))
            await client.run_until_disconnected()
        except Exception as e:
            print(colored(f"❌ Failed to run bot for {phone_number}: {e}", "red"))

# Start bot
if __name__ == "__main__":
    asyncio.run(main()) 
