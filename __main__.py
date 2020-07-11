import logging
from config import config
from discord_client import client
from commands import add_commands

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    token = config["token"]
    add_commands()
    client.run(token)


@client.event
async def on_ready():
    print("Ready to start mentoring")


@client.event
async def on_message(message):
    if message.author.bot:
        return
    ctx = await client.get_context(message)
    if ctx.valid:
        await client.process_commands(message)
