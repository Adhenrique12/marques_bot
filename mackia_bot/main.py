import logging
from telethon import TelegramClient
from handlers.tools import load_plugins as lp
from handlers.plugins import ALL_MODULES as USER_MODULES

from config import TOKEN, ID, HASH

# Set up logging
logging.basicConfig(
    format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
    level=logging.WARNING
)

# Create TelegramClient instance
client = TelegramClient(
    "bot",
    ID,
    HASH
).start(bot_token=TOKEN)

def main():
    print("Starting...")
    try:
        with client:
            client.start()
            lp.load_plugins(USER_MODULES, client)
            print("Maquia started.")
            client.run_until_disconnected()
    except KeyboardInterrupt:
        print("Client terminated.")


if __name__ == "__main__":
    main()