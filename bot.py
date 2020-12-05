import discord
import random
from discord.ext import commands

file = open('token.txt')
token = file.read()

client = commands.Bot(command_prefix= '.')

#Event to see when the bot is online and ready to use
@client.event
async def on_ready():
    print('Bot is ready.')

#Event to print out when someone joined the server
@client.event
async def on_member_join(member):
    print(F'{member} has joined a server.')

#Event to print out when someone left the server
@client.event
async def on_member_remove(member):
    print(F'{member} has left a server.')

#Ping command to get latency of the bot
@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

#Simple 8ball command to get some responses
@client.command(aliases=['8ball'])
async def eightBall(ctx, *, question):
    responses = [ "It is certain.",
                  "It is decidedly so.",
                  "Without a doubt.",
                  "Yes - definitely.",
                  "You may rely on it.",
                  "As I see it, yes.",
                  "Most likely.",
                  "Outlook good.",
                  "Yes.",
                  "Signs point to yes.",
                  "Reply hazy, try again.",
                  "Ask again later.",
                  "Better not tell you now.",
                  "Cannot predict now.",
                  "Concentrate and ask again.",
                  "Don't count on it.",
                  "My reply is no.",
                  "My sources say no.",
                  "Outlook not so good.",
                  "Very doubtful."]
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

client.run(token)
