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

@bot.command(name='remove_spell', help='This command removes a spell from the spell-list. Example: !removespell Fireball')
async def removespell(ctx, name: str):
    #Find the spell
    spell = next((spell for spell in all_spells if spell.name == name), None)
    if spell is None:
        await ctx.send(f"Spell '{name}' not found.")
        return

    #Remove the spell from the XML file
    XMLHandler.remove_spell(spell_path, spell)

    #Update in-memory spell list
    all_spells.remove(spell)
    await ctx.send(f"Spell '{name}' removed.")

@bot.command(name='give_spell', help='This command adds a spell to a character. Example: !give_spell Bob Fireball')
async def addspelltocharacter(ctx, character_name: str, spell_name: str):
    #Find the character
    character = next((character for character in all_characters if character.name == character_name), None)
    if character is None:
        await ctx.send(f"Character '{character_name}' not found.")
        return

    #Find the spell
    spell = next((spell for spell in all_spells if spell.name == spell_name), None)
    if spell is None:
        await ctx.send(f"Spell '{spell_name}' not found.")
        return

    #Add the spell to the character
    character.add_spell(spell)

    #Save the character to the XML file
    XMLHandler.save_character(character_path, character)

    await ctx.send(f"Spell '{spell_name}' added to character '{character_name}'.")

#List all spells
@bot.command(name='list_spells', help='This command lists all spells.')
async def listspells(ctx):
    spell_list = '\n\n'.join([str(spell) for spell in all_spells])
    await ctx.send(f'All spells:\n{spell_list}')

#Create a new character
@bot.command(name='create_character', help='This command creates a new character. Example: !create_character Bob intellect:10 strength:5')
async def createcharacter(ctx, name: str, health:int, stamina:int, *scaling_pairs):
    if name in [character.name for character in all_characters]:
        await ctx.send(f"Character '{name}' already exists.")
        return
    #Parsing scaling input
    scaling = {}
    for pair in scaling_pairs:
        try:
            attr, value = pair.split(":")
            scaling[attr] = int(value)
        except ValueError:
            await ctx.send('Invalid scaling format: ' + scaling)
            return

    # Ensure that the required scaling pairs are provided
    missing_scalings = [stat for stat in REQUIRED_SCALINGS if stat not in scaling]
    
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

#Remove a character
@bot.command(name='remove_character', help='This command removes a character. Example: !remove_character Bob')
async def removecharacter(ctx, name: str):
    #Find the character
    character = next((character for character in all_characters if character.name == name), None)
    if character is None:
        await ctx.send(f"Character '{name}' not found.")
        return

    #Remove the character from the XML file
    XMLHandler.remove_character(character_path, character)

    #Update in-memory character list
    all_characters.remove(character)
    await ctx.send(f"Character '{name}' removed.")

#List all characters
@bot.command(name='list_characters', help='This command lists all characters.')
async def listcharacters(ctx):
    character_list = '\n\n'.join([str(character) for character in all_characters])
    await ctx.send(f'All characters:\n{character_list}')

#Attack a character
@bot.command(name='attack', help='This command attacks a character with a spell. Example: !attack Bob Fireball Target')
async def attack(ctx, character_name: str, spell_name: str, target_name: str):
    #Find the character
    character = next((character for character in all_characters if character.name == character_name), None)
    if character is None:
        await ctx.send(f"Character '{character_name}' not found.")
        return
    if target_name not in all_characters:
        await ctx.send(f"Target '{target_name}' not found.")

    #Find the spell
    character_spells = character.spells
    spell = next((spell for spell in character_spells if spell.name == spell_name), None)
    if spell is None:
        await ctx.send(f"Spell '{spell_name}' not found in Bob's usable spells.")
        return

    #Calculate the damage
    damage = spell.calculate_damage(**character.stats)
    await ctx.send(f"Character '{character_name}' attacked with spell '{spell_name}' for {damage} damage.")
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