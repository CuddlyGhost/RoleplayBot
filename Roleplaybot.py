import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from xmlhandler import XMLHandler
from spell import Spell
from character import Character

# Defining global variables
spell_path = 'spells.xml'
character_path = 'characters.xml'
REQUIRED_SCALINGS = ['strength', 'luck', 'durability', 'speed', 'intellect']

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

#Load spells
all_spells = XMLHandler.load_spells(spell_path)
if all_spells is None:
    all_spells = []

#Load characters
all_characters = XMLHandler.load_characters(character_path, all_spells)
if all_characters is None:
    all_characters = []

#Ping
@bot.command(name='ping', help='This command returns the latency.')
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')


#Add a spell to XML
@bot.command(name='add_spell', help='This command adds a spell to the spell-list. Example: !addspell Fireball 5 20 intellect:1.5 strength:0.3')
async def addspell(ctx, name: str, cooldown: int, stamina_cost: int, *scaling_pairs):
    #Parsing scaling input
    scaling = {}
    for pair in scaling_pairs:
        try:
            attr, value = pair.split(":")
            scaling[attr] = float(value)
        except ValueError:
            await ctx.send('Invalid scaling format: ' + scaling)
            return
    
    #Create a new spell object
    new_spell = Spell(name, scaling, cooldown, stamina_cost)

    #Save the spell to the XML file
    XMLHandler.save_spell(spell_path, new_spell)

    #Update in-memory spell list
    all_spells.append(new_spell)
    await ctx.send(f"Spell '{name}'; {new_spell} {scaling}") 

#List all spells
@bot.command(name='list_spells', help='This command lists all spells.')
async def listspells(ctx):
    spell_list = '\n'.join([str(spell) for spell in all_spells])
    await ctx.send(f'All spells:\n{spell_list}')

#Create a new character
@bot.command(name='create_character', help='This command creates a new character. Example: !create_character Bob intellect:10 strength:5')
async def createcharacter(ctx, name: str, health:int, stamina:int, *scaling_pairs):
    #Parsing scaling input
    scaling = {}
    for pair in scaling_pairs:
        try:
            attr, value = pair.split(":")
            scaling[attr] = float(value)
        except ValueError:
            await ctx.send('Invalid scaling format: ' + scaling)
            return

    # Ensure that the required scaling pairs are provided
    missing_scalings = [scaling for scaling in REQUIRED_SCALINGS if scaling not in scaling]
    
    if missing_scalings:
        await ctx.send(f"Error: Missing required scaling stats: {', '.join(missing_scalings)}")
        return  
    
    #Create a new character object
    new_character = Character(name, health, stamina, scaling)

    #Save the character to the XML file
    XMLHandler.save_character(character_path, new_character)

    #Update in-memory character list
    all_characters.append(new_character)
    await ctx.send(f"Character '{name}' created with stats: {scaling}")

#Special commands
#Roleplay attack recognition
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.startswith('Spell:'):
        await message.channel.send('Attack recognized!')
    await bot.process_commands(message)

#Run the bot with the token
bot.run(TOKEN)