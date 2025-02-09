from discord.ext import commands
from xmlhandler import XMLHandler
from spell import Spell
from character import Character
from update import updatecharacter

# Defining global variables
from globals import *

def is_admin():
    """Custom check for permission 'Administrator'."""
    async def predicate(ctx : commands.Context):
        return any(ctx.author._permissions.as_integer_ratio() == 'Administrator')
    return commands.check(predicate)

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    #Add a spell to XML
    @commands.command(name='add_spell', help='This command adds a spell to the spell-list. Example: !addspell Fireball 5(Cooldown) 20(Stamina cost) intellect:1.5 strength:0.3')
    async def addspell(self, ctx, name: str, cooldown: int, stamina_cost: int, *scaling_pairs):
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

    @commands.command(name='remove_spell', help='This command removes a spell from the spell-list. Example: !removespell Fireball')
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

    @commands.command(name='give_spell', help='This command adds a spell to a character. Example: !give_spell Bob Fireball')
    async def addspelltocharacter(self, ctx, character_name: str, spell_name: str):
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

    #Create a new character
    @commands.command(name='create_character', help='This command creates a new character. Example: !create_character Username Bob 1000(Health) 200(Stamina) intellect:10 strength:5 durability:10 speed:5 luck:5')
    async def createcharacter(self, ctx, author: str,name: str, health:int, stamina:int, *scaling_pairs):
        if name in [character.name for character in all_characters]:
            await ctx.send(f"Character '{name}' already exists.")
            return
        if health is None or stamina is None or health <= 0 or stamina <= 0:
            await ctx.send('Health and stamina must be greater than 0.')
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
        new_character = Character(author,name, health, stamina, scaling)

        #Save the character to the XML file
        XMLHandler.save_character(character_path, new_character)

        #Update in-memory character list
        all_characters.append(new_character)
        await ctx.send(f"Character '{name}' created with stats: \n{new_character.__str__()}")

    #Update a character
    @commands.command(name='update_character', help='This command updates a character. Example: !update_character Bob 800(Current Health) 1000(Health) 180 (Current stamina) 200(Stamina) intellect:10 strength:5 durability:10 speed:5 luck:5')
    async def updatecharacter(ctx, name: str, health:int, current_health:int, stamina:int, current_stamina:int, *scaling_pairs):
        await updatecharacter(ctx, name, health, current_health, stamina, current_stamina, False, *scaling_pairs)

    #Update stats of a character
    @commands.command(name='update_stats', help='This command updates the stats of a character. Example: !update_stats Bob intellect:10 strength:5 durability:10 speed:5 luck:5')
    async def updatestats(self, ctx, name: str, *scaling_pairs):
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
        character.stats = scaling

        #Save the character to the XML file
        XMLHandler.save_character(character_path, character)
        await ctx.send(f"Character '{name}' updated with stats: {character.__str__()}")

    #Remove a character
    @commands.command(name='remove_character', help='This command removes a character. Example: !remove_character Bob')
    async def removecharacter(self, ctx, name: str):
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


def setup(bot):
    bot.add_cog(Admin(bot))