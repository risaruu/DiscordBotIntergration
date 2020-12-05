import discord
from discord.ext import commands

file = open('token.txt')
token = file.read()

client = commands.Bot(command_prefix= '.')

@client.event
async def on_ready():
    print('Bot is ready.')

@client.event
async def on_member_join(member):
    print(F'{member} has joined a server.')

@client.event
async def on_member_remove(member):
    print(F'{member} has left a server.')

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')
    

client.run(token)
