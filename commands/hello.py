from discord_client import client
from discord.ext.commands import Context
from discord import utils
import random


# Command to add roles to the author.
@client.command(help="Greetings")
async def hello(ctx):
    await ctx.message.channel.send("Hi!")
