import discord
from discord.ext import commands

file = open('token.txt')
token = file.read()

client = commands.Bot(command_prefix= '.')

@client.event
async def on_ready():
    print('Bot is ready.')

client.run(token)
