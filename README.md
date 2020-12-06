# DiscordBotIntergration - learning to code a Discord Bot

## By Damjan Petrovic

Creating a discord bot to utilize on private server as well as to integrate future projects into it. In this project ill go and create a Discord Bot with different functionalitys to use on any discord server. The main feature will be a algorithm that analyzes your data from the game League of Legends and grades your permance as well as giving helpful tips to help you get better at the game.

This is mainly a project to learn how to code a Discord bot as well as how to use the RiotGames API.

## To-do List 

- [x] get the Bot up and running on a Server
- [x] create some basic events and commands
- [x] create 8ball to answer simple questions randomly
- [x] create connection to RiotGamesAPI
- [x] grab data out of the RiotGamesAPI
- [x] process data out of the RiotGamesAPI
- [x] display processed data
- [ ] further process the data in a algorithm to give users a school grade on their performance
- [ ] create music bot functionality
- [ ] create a news ticker to display news in a specific channel
- [ ] create automatic role distribution
- [ ] ...

## Prerequisites

- Getting the discord library:

  To begin with you will need to install the discord library to use:

```
pip install discord.py
```

- Getting a discord bot ready with a token:

  In the next step you will need to sign in at: https://discord.com/developers/applications with your discord account. There you can create a new application and set the application as a bot under the bot menu.

## Example

At first we will create a simple bot that just works, we will later go into the full details of how everything works:

```python
import discord
from discord.ext import commands

#sets a prefix for bot commands that can be entered on discord
client = commands.Bot(command_prefix = '.')

#defines a function to do when the bot starts up
@client.event
async def on_ready():
    print('Bot is ready.')
    
#Runs the bot with your token taken from the discord site
client.run('token')
```

#### Helpful Ressources

https://github.com/Rapptz/discord.py
https://discordpy.readthedocs.io/en/latest/
https://www.youtube.com/watch?v=nW8c7vT6Hl4&list=PLW3GfRiBCHOhfVoiDZpSz8SM_HybXRPzZ