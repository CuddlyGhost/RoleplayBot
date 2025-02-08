import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# load env variavbles
load_dotenv()

#Get the token from the .env file
TOKEN = os.getenv('DISCORD_TOKEN')

#Create a new discord client
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.members = True
intents.messages = True
intents.guilds = True
bot = commands.Bot(command_prefix='!', intents=intents)

#Commands start here

#Test
@bot.command(name='test', help='This command returns the argument given.')
async def test(ctx, arg):
    await ctx.send('Test ' + arg)

#Run the bot with the token
bot.run(TOKEN)