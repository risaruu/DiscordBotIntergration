from statistics import mean

import discord
import requests
import re
import random
from discord.ext import commands

file = open('token.txt')
token = file.read()

apiKeyFile = open('apikey.txt')
apiKey = apiKeyFile.read()

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

#Command to clear messages
@client.command()
async def clear(ctx, amount=1):
    amount = amount + 1
    await ctx.channel.purge(limit=amount)

#Simple 8ball command to get some responses
@client.command(aliases=['frage'])
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

#------------------------------------
#--- Riot Games API functionality ---
#------------------------------------

#Function to get the basic summoner data of a given summoner
def getSummoner(summonerName):
    url = 'https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + summonerName + '?api_key=' + apiKey
    response = requests.get(url)
    return response.json()

#Function to get the specific ranked data of a given summoner
def getRankedStats(summonerName):
    customerData = getSummoner(summonerName)
    summonerId = customerData["id"]
    url = 'https://euw1.api.riotgames.com/lol/league/v4/entries/by-summoner/' + summonerId + '?api_key=' + apiKey
    response = requests.get(url)
    return response.json()

#Function to simply calculate the winrate out of the wins and losses of an Account
def calculateWinrate(x, y):
    z = x + y
    z_formatted = round(x / z * 100, 2)
    return str(z_formatted)

def getMatchHistory(summonerName):
    customerData = getSummoner(summonerName)
    accountId = customerData["accountId"]
    url = 'https://euw1.api.riotgames.com/lol/match/v4/matchlists/by-account/' + accountId + '?endIndex=10&api_key=' + apiKey
    response = requests.get(url)
    return response.json()

def getMatchStats(matchId):
    url = "https://euw1.api.riotgames.com/lol/match/v4/matches/" + str(matchId) + "?api_key=" + apiKey
    response = requests.get(url)
    return response.json()

def getMean(list):
    return mean(list)

#command to get the league stats with a summoner name as parameter
@client.command(aliases=['lolstats'])
async def lolStats(ctx, *, username):
    message = ""

    summonerData = getSummoner(username)
    summonerDataRanked = getRankedStats(username)
    queue = ""
    rank = ""
    winrate = ""
    noRanked = False

    try:
        if summonerDataRanked[0]["queueType"] == "RANKED_SOLO_5x5":
            queue = "Ranked Solo/Duo"
            rank = "Tier: " + summonerDataRanked[0]["tier"] + " " + summonerDataRanked[0]["rank"]
            winrate = calculateWinrate(summonerDataRanked[0]["wins"], summonerDataRanked[0]["losses"])
        elif summonerDataRanked[0]["queueType"] != "RANKED_SOLO_5x5":
            queue = "Ranked Solo/Duo"
            rank = "Tier: " + summonerDataRanked[1]["tier"] + " " + summonerDataRanked[1]["rank"]
            winrate = str(calculateWinrate(summonerDataRanked[1]["wins"], summonerDataRanked[1]["losses"]))
    except:
        noRanked = True

    message = message + f'{summonerData["name"]} ist gerade Lv. {summonerData["summonerLevel"]} \n\n'
    if noRanked == False:
        message = message + f'Stats in den letzten 50 Games für: {queue} \nRank: {rank} mit einer Winrate von {winrate}%'
    else:
        message = message + f'Dieser Spieler hat keine Ranked Games gemacht :C'

    await ctx.send(message)

client.run(token)
