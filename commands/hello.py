from discord_client import client


# Command to add roles to the author.
@client.command(help="Greetings")
async def hello(ctx):
    await ctx.message.channel.send("Hi!")
