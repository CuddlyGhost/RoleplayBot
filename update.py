from discord.ext import commands
from xmlhandler import XMLHandler
from globals import *



#Update a character
async def updatecharacter(ctx, name: str, health:int, current_health:int, stamina:int, current_stamina, suppressMessage=False, *scaling_pairs):
    #Find the character
    character = next((character for character in all_characters if character.name == name), None)
    if character is None:
        await ctx.send(f"Character '{name}' not found.")
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
    #Update the character
    character.health = health
    character.current_health = current_health
    character.stamina = stamina
    character.current_stamina = current_stamina
    character.stats = scaling
    #Save the character to the XML file
    XMLHandler.save_character(character_path, character)
    if (suppressMessage == False):
        await ctx.send(f"Character '{name}' updated with stats: {character.__str__()}")
    