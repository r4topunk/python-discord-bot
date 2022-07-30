import discord
from config import ConfManager
from discord.ext import commands
from classes.my_view import MyView
from classes.player import Player

print("Starting program...")

# Init Discord bot
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix="!", intents=intents)

# Get configs
confs = ConfManager('config.ini')

# A channel to bot work
default_channel = int(confs.get_conf('default_channel'))

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.listen()
async def on_message(message):
    if int(message.channel.id) != int(default_channel) or \
        message.author == client.user:
        return
        

@client.command()
async def bot(ctx):
    if int(ctx.channel.id) != int(default_channel) or \
        ctx.author == client.user:
        return

    await ctx.send("<@" + str(ctx.author.id) + ">")

    author = ctx.author
    player = Player(author.id, author.nick if author.nick else author.name)
    view = MyView(ctx, player)
    # await ctx.send("You have 10 seconds to choice!", view=view)
    await ctx.send(view=view)

client.run(confs.get_conf('token'))
