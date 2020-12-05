# DiscordBotIntergration

## By Damjan Petrovic

Creating a discord bot to utilize on private server as well to integrate future projects into it. In this project we will go step through step to create a discord bot and fuel it with features to help organize and have some fun on our discord server. You can also integrate your own private projects into this as I will later do hopefully.

Helpful ressources:

https://github.com/Rapptz/discord.py
https://discordpy.readthedocs.io/en/latest/
https://www.youtube.com/watch?v=nW8c7vT6Hl4&list=PLW3GfRiBCHOhfVoiDZpSz8SM_HybXRPzZ

## Prerequisites

- Getting the discord library:

  To begin with you will need to install the discord library to use:

```
pip install discord.py
```

- Getting a discord bot ready with a token:

  In the next step you will need to sign in at: https://discord.com/developers/applications with your discord account. There you can create a new application and set the application as a bot under the bot menu.

## Setup

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

## Events

