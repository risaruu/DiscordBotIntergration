# -----------------------------------------------------------
# A simple discord bot integration with many useful commands
# this is mainly a learning tool on how to program a bot and
# use api's to get data as well as analyzing and displaying data
#
# (C) 2020 Damjan Petrovic, Vienna, Austria
# email p.damjan7999@gmail.com
# -----------------------------------------------------------

# Imports
from statistics import mean
import discord
import requests
import random
from discord.ext import commands

# reading the Keys to the API as well as to the discord bot
file = open('Keys/bottoken.txt')
token = file.read()
apiKeyFile = open('Keys/apikey.txt')
apiKey = apiKeyFile.read()

# setting a prefix for the bot to recognize commands on discord server
client = commands.Bot(command_prefix= '.')

# event to see when the bot is online and ready to use
@client.event
async def on_ready():
    print('Bot is ready.')

# event to print out when someone joined the server
@client.event
async def on_member_join(member):
    print(f'{member} has joined a server.')

# event to print out when someone left the server
@client.event
async def on_member_remove(member):
    print(f'{member} has left a server.')

# ping command,used to get latency of the bot
@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

# clear command, used to clear text messages on the discord
# Parameters:
# amount - int of how many message the command shall clear, default to 1
@client.command()
async def clear(ctx, amount=1):
    amount = amount + 1
    await ctx.channel.purge(limit=amount)

# 8ball command, you can ask a yes/no/maybe question and you will get a random answer
# Parameters:
# question - String with a question message from the user
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

# lolstats command, uses the defined lolStats function to print out a loading message and the collected data
# Parameters:
# question - String with a question message from the user
@client.command(aliases=['lolstats'])
async def messageStats(ctx, *, username):
    message = 'Fetching Data from Riot Games... \n'
    for y in range(2):
        await ctx.send(message)
        try:
            message = lolStats(username)
        except:
            message = 'There is no summoner with that name, you tricked me :C'

#------------------------------------
#--- Riot Games API functionality ---
#------------------------------------

# Function to get the basic summoner data of a given summoner
# Parameters:
# summonerName - username string to search the database for
# returns - .json-File with RiotGamesSummonerData in it
def getSummoner(summonerName):
    url = 'https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + summonerName + '?api_key=' + apiKey
    response = requests.get(url)
    return response.json()

# Function to get the specific ranked data of a given summoner
# Parameters:
# summonerName - username string to search the database for
# returns - .json-File with RiotGamesRankedData in it
def getRankedStats(summonerName):
    customerData = getSummoner(summonerName)
    summonerId = customerData["id"]
    url = 'https://euw1.api.riotgames.com/lol/league/v4/entries/by-summoner/' + summonerId + '?api_key=' + apiKey
    response = requests.get(url)
    return response.json()

# Function to simply calculate the winrate out of the wins and losses of an Account
# Parameters:
# x - first number to use (Wins)
# y - second number to use (Losses)
# returns - String with a number
def calculateWinrate(x, y):
    z = x + y
    z_formatted = round(x / z * 100, 2)
    return str(z_formatted)

# Function to get the match history of a given summoner
# Parameters:
# summonerName - username string to search the database for
# returns - .json-File with RiotGamesMatchData in it
def getMatchHistory(summonerName):
    customerData = getSummoner(summonerName)
    accountId = customerData["accountId"]
    url = 'https://euw1.api.riotgames.com/lol/match/v4/matchlists/by-account/' + accountId + '?endIndex=50&api_key=' + apiKey
    response = requests.get(url)
    return response.json()

# Function to get the stats of a given summoner out of a given match
# Parameters:
# matchId - matchId to search the database for
# returns - .json-File with RiotGamesMatchStatsData in it
def getMatchStats(matchId):
    url = "https://euw1.api.riotgames.com/lol/match/v4/matches/" + str(matchId) + "?api_key=" + apiKey
    response = requests.get(url)
    return response.json()

# Function to combine all data gavering, process the data and combine it to a single message output
# Parameters:
# username - username string to search the database for
# returns - String with all the processed data
def lolStats(username):
    message = ""

    #setting the .json files
    summonerData = getSummoner(username)
    summonerDataRanked = getRankedStats(username)

    # variables to set default values as well as to save basic data
    queue = ""
    rank = ""
    winrate = ""
    noRanked = False

    # lists to save the match data in
    games = []
    championId = []
    championsPlayed = []
    kills = []
    deaths = []
    assists = []
    totalDamageDealt = []
    visionScore = []
    gameLength = []

    # try and except to always get the solo/duo Ranked stats and catch the error that would occur if there are no ranked games detected
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

    # gettint the match history and creating a list of the champions played to later gather the stats of the player out of all playerstats in the match data json
    matchHistory = getMatchHistory(username)
    for each in matchHistory["matches"]:
        games.append(each["gameId"])
        championsPlayed.append(each["champion"])

    # gathering all specified data from our user out of the json file and putting the data into lists
    for z in range(0, 50):
        matchData = getMatchStats(games[z])
        gameLength.append(matchData["gameDuration"])
        for part in matchData["participants"]:
            if part["championId"] == championsPlayed[z]:
                championId.append(part["championId"])
                kills.append(part["stats"]["kills"])
                deaths.append(part["stats"]["deaths"])
                assists.append(part["stats"]["assists"])
                totalDamageDealt.append(part["stats"]["totalDamageDealtToChampions"])
                visionScore.append(part["stats"]["visionScore"])

    #creating the message text
    message = message + f'**{summonerData["name"]}** ist gerade Lv. {summonerData["summonerLevel"]} \n\n'
    if noRanked == False:
        message = message + f'Stats in den letzten 50 Games für: {queue} \nRank: **{rank}** mit einer Winrate von **{winrate}%** \n\n'
    else:
        message = message + f'Dieser Spieler hat keine Ranked Games gemacht :C\n'

    #adding KDA to message
    message = message + f'Match Stats für die letzten 50 Games: \nKDA: **{"{:.2f}".format((mean(kills) + mean(assists)) / mean(deaths))}** - {mean(kills)} / {mean(deaths)} / {mean(assists)}\n'

    #adding totalDamageDealt to message
    message = message + f'DPS: **{"{:.2f}".format(mean(totalDamageDealt) / (mean(gameLength) / 60)) }**\n'

    #adding VisionScore to message
    message = message + f'Vision Score: **{"{:.2f}".format(mean(visionScore))}** \n'

    message = message + f'Durchschnittliche Spiellänge: **{"{:.2f}".format(mean(gameLength) / 60)} min.**'

    #sending message text
    return(message)

# running the bot with the given bot token
client.run(token)
