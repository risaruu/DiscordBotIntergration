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
from collections import Counter

# reading the Keys to the API as well as to the discord bot
file = open('Keys/bottoken.txt')
token = file.read()
apiKeyFile = open('Keys/apikey.txt')
apiKey = apiKeyFile.read()

# setting a prefix for the bot to recognize commands on discord server
client = commands.Bot(command_prefix='.')


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
    responses = ["It is certain.",
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
    await ctx.send(message)
    message = lolStats(username)
    await ctx.send(message)


# ------------------------------------
# --- Riot Games API functionality ---
# ------------------------------------

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


# Function to get most common three elements out of a list
# Parameters:
# list - a list with elements
# returns - a list containing the 3 most common items sorted from most to least
def mostCommonThree(liste):
    word_counter = {}
    for word in liste:
        if word in word_counter:
            word_counter[word] += 1
        else:
            word_counter[word] = 1

    popular_words = sorted(word_counter, key=word_counter.get, reverse=True)
    top_3 = popular_words[:3]

    return top_3

# Function to switch a given champion id into a champion name
# Parameters:
# championId - integer number of the champion
# returns - a string with the name of the champion
def championIdToText(championId):
    switcher = {
        1: "Annie",
        2: "Olaf",
        3: "Galio",
        4: "TwistedFate",
        5: "XinZhao",
        6: "Urgot",
        7: "LeBlanc",
        8: "Vladimir",
        9: "Fiddlesticks",
        10: "Kayle",
        11: "Master Yi",
        12: "Alistar",
        13: "Ryze",
        14: "Sion",
        15: "Sivir",
        16: "Soraka",
        17: "Teemo",
        18: "Tristana",
        19: "Warwick",
        20: "Nunu",
        21: "MissFortune",
        22: "Ashe",
        23: "Tryndamere",
        24: "Jax",
        25: "Morgana",
        26: "Zilean",
        27: "Singed",
        28: "Evelynn",
        29: "Twitch",
        30: "Karthus",
        31: "Cho'Gath",
        32: "Amumu",
        33: "Rammus",
        34: "Anivia",
        35: "Shaco",
        36: "Dr.Mundo",
        37: "Sona",
        38: "Kassadin",
        39: "Irelia",
        40: "Janna",
        41: "Gangplank",
        42: "Corki",
        43: "Karma",
        44: "Taric",
        45: "Veigar",
        48: "Trundle",
        50: "Swain",
        51: "Caitlyn",
        53: "Blitzcrank",
        54: "Malphite",
        55: "Katarina",
        56: "Nocturne",
        57: "Maokai",
        58: "Renekton",
        59: "JarvanIV",
        60: "Elise",
        61: "Orianna",
        62: "Wukong",
        63: "Brand",
        64: "LeeSin",
        67: "Vayne",
        68: "Rumble",
        69: "Cassiopeia",
        72: "Skarner",
        74: "Heimerdinger",
        75: "Nasus",
        76: "Nidalee",
        77: "Udyr",
        78: "Poppy",
        79: "Gragas",
        80: "Pantheon",
        81: "Ezreal",
        82: "Mordekaiser",
        83: "Yorick",
        84: "Akali",
        85: "Kennen",
        86: "Garen",
        89: "Leona",
        90: "Malzahar",
        91: "Talon",
        92: "Riven",
        96: "Kog'Maw",
        98: "Shen",
        99: "Lux",
        101: "Xerath",
        102: "Shyvana",
        103: "Ahri",
        104: "Graves",
        105: "Fizz",
        106: "Volibear",
        107: "Rengar",
        110: "Varus",
        111: "Nautilus",
        112: "Viktor",
        113: "Sejuani",
        114: "Fiora",
        115: "Ziggs",
        117: "Lulu",
        119: "Draven",
        120: "Hecarim",
        121: "Kha'Zix",
        122: "Darius",
        126: "Jayce",
        127: "Lissandra",
        131: "Diana",
        133: "Quinn",
        134: "Syndra",
        136: "AurelionSol",
        141: "Kayn",
        142: "Zoe",
        143: "Zyra",
        145: "Kai'sa",
        150: "Gnar",
        154: "Zac",
        157: "Yasuo",
        161: "Vel'Koz",
        163: "Taliyah",
        164: "Camille",
        201: "Braum",
        202: "Jhin",
        203: "Kindred",
        222: "Jinx",
        223: "TahmKench",
        235: "Senna",
        236: "Lucian",
        238: "Zed",
        240: "Kled",
        245: "Ekko",
        246: "Qiyana",
        254: "Vi",
        266: "Aatrox",
        267: "Nami",
        268: "Azir",
        350: "Yuumi",
        412: "Thresh",
        420: "Illaoi",
        421: "Rek'Sai",
        427: "Ivern",
        429: "Kalista",
        432: "Bard",
        497: "Rakan",
        498: "Xayah",
        516: "Ornn",
        517: "Sylas",
        523: "Aphelios",
        518: "Neeko",
        555: "Pyke",
        875: "Sett",
        876: "Lillia",
        777: "Yone",
        360: "Samira",
        147: "Seraphine",
    }
    return switcher.get(championId, "Invalid Champion Id")

# Function to combine all data gathering, process the data and combine it to a single message output
# Parameters:
# username - username string to search the database for
# returns - String with all the processed data
def lolStats(username):
    print("Gathering RiotGamesAPI data...")
    message = ""

    # setting the .json files
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

    # try and except to always get the solo/duo Ranked stats and catch the error that would occur if there are no
    # ranked games detected
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

    # getting the match history and creating a list of the champions played to later gather the stats of the player
    # out of all player stats in the match data json
    matchHistory = getMatchHistory(username)
    for each in matchHistory["matches"]:
        games.append(each["gameId"])
        championsPlayed.append(each["champion"])

    # gathering all specified data from our user out of the json file and putting the data into lists
    for z in range(50):
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
                if z == 25:
                    print("Halfway there...")

    top_3 = mostCommonThree(championsPlayed)

    print('Finished gathering data \nCreating text message...')

    # creating the message text
    message = message + f'**{summonerData["name"]}** ist gerade Lv. {summonerData["summonerLevel"]} \n\n'
    if noRanked == False:
        message = message + f'Stats in den letzten 50 Games für: {queue} \nRank: **{rank}** mit einer Winrate von **{winrate}%** \n\n'
    else:
        message = message + f'Dieser Spieler hat keine Ranked Games gemacht :C\n'

    # adding KDA to message
    message = message + f'Match Stats für die letzten 50 Games: \nKDA: **{"{:.2f}".format((mean(kills) + mean(assists)) / mean(deaths))}** - {mean(kills)} / {mean(deaths)} / {mean(assists)}\n'

    # adding totalDamageDealt to message
    message = message + f'DPS to Champions: **{"{:.2f}".format(mean(totalDamageDealt) / (mean(gameLength) / 60))}**\n'

    # adding VisionScore to message
    message = message + f'Vision Score: **{"{:.2f}".format(mean(visionScore))}** \n'

    # adding game length
    message = message + f'Durchschnittliche Spiellänge: **{"{:.2f}".format(mean(gameLength) / 60)} min.**\n'

    # adding most common three champions
    message = message + f'Top 3 Champions: **{championIdToText(top_3[0])}** | **{championIdToText(top_3[1])}** | **{championIdToText(top_3[2])}**\n'

    print("Finished creating text message")

    # sending message text
    return (message)

# running the bot with the given bot token
client.run(token)
