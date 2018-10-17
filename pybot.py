import discord
from discord.ext import commands
import os

BOT_PREFIX = ("py.")
bot.remove_command('help')

CMDS = [{'command' : 'ping',
        'description' : 'a way to see if bot is responsive.',
        },
        {'command' : 'echo',
        'description' : 'make the bot say something',
        'role': 'user++',]
        },
        {'command' : 'rm',
        'description' : 'delete message(s)',
        'permissions': ['manage_messages',]
        },
]

async def isAuth(cmd, msg):
    if cmd.get("permissions") != None or cmd.get("role") != None: # if command has a role or permission requirement : role takes priority
        if cmd.get('role'): # Checks to see if the requirment is a role
            for position in range(len(list(msg.server.role_hierarchy))): # Loops through all of the servers roles : position == int(role position in the role_hierarchy)
                if str(msg.server.role_hierarchy[position]).lower() == cmd.get('role').lower(): # if server role == command role requirment
                    break
            if msg.server.role_hierarchy.index(msg.author.top_role) <= position: # if user's int(top role position in role_hierarchy) <= int(command role requirment position)
                return True
            return False
        else:
            print("test")
            for permission in cmd.get("permissions"):
                for userPerm in msg.channel.permissions_for(msg.author):
                    if permission in userPerm:
                        if True in userPerm:
                            print(userPerm)
                            continue
                        else:
                            return False
    return True

async def runCMD(cmd, msg):
    if cmd == "ping":
        await ping(msg)
    elif cmd == "echo":
        await echo(BOT_PREFIX + cmd,msg)
    elif cmd == "rm":
        arg = msg.content[len(BOT_PREFIX + cmd + " "):]
        if arg.isdigit():
            await rm(msg, int(arg) + 1)
        else:
            await bot.send_message(msg.channel, "Invalid use of command")

async def ping(msg):
    await bot.send_message(msg.channel, "pong")

async def echo(cmd,msg):
    await bot.delete_message(msg)
    await bot.send_message(msg.channel, msg.content[len(cmd + " "):])

async def rm(msg, num = 1):
    await bot.purge_from(msg.channel, limit=num)


@bot.event
async def on_message(msg):
    if msg.author == bot.user:
        pass
    else:
        for cmd in CMDS:
            if msg.content.startswith(BOT_PREFIX + cmd.get("command")):
                break
        if msg.content.startswith(BOT_PREFIX + cmd.get("command")):
            if await isAuth(cmd, msg):
                await runCMD(cmd.get("command"), msg)
            else:
                await bot.send_message(msg.channel, "Too much power. You need to level before you can you that move.")

bot.run(os.getenv('TOKEN'))
