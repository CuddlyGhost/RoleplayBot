import sys
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# load env variables
load_dotenv()

#Get the token from the .env file
TOKEN = os.getenv('DISCORD_TOKEN')

#Create a new discord client
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.members = True
intents.messages = True
intents.message_content = True
intents.guilds = True
bot = commands.Bot(command_prefix='!', intents=intents)

#Load Cogs
from admin_commands import Admin
from combat import Combat
from utility import Utility

async def load_cogs():
    await bot.add_cog(Admin(bot))
    await bot.add_cog(Combat(bot))
    await bot.add_cog(Utility(bot))

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await load_cogs()
    print('Cogs loaded')

@bot.command(name='restart', help='This command restarts the bot.')
@commands.has_permissions(administrator=True)
async def restart(ctx):
    await ctx.send('Restarting...')
    os.execv(sys.executable, ['python'] + sys.argv)
    bot.login()

@bot.command(name='shutdown', help='This command shuts down the bot.')
@commands.has_permissions(administrator=True)
async def shutdown(ctx):
    await ctx.send('Shutting down...')
    await bot.close()

bot.run(TOKEN)