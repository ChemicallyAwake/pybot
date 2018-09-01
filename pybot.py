import discord
from discord.ext import commands
import os

BOT_PREFIX = ("pybot ", "pibot ")
client = commands.Bot(command_prefix=BOT_PREFIX)

@client.command(name='ping')
async def pingPong():
    await client.say("pong")

@client.command(name='server_count')
async def server_count():
    count = 0
    for server in client.servers:
        for member in server.members:
            count += 1
    await client.say("%s members" %(count-1))

client.run(os.getenv('TOKEN'))
