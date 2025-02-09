from discord.ext import commands
from globals import *


class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    #List all spells
    @commands.command(name='list_spells', help='This command lists all spells.')
    async def listspells(self, ctx):
        spell_list = '\n\n'.join([str(spell) for spell in all_spells])
        await ctx.send(f'All spells:\n{spell_list}')

    #List all characters
    @commands.command(name='list_characters', help='This command lists all characters.')
    async def listcharacters(self, ctx):
        character_list = '\n\n'.join([str(character) for character in all_characters])
        await ctx.send(f'All characters:\n{character_list}')
    
    #Show specific character
    @commands.command(name='character', help='This command lists a specific character. !character <name>')
    async def listcharacter(self, ctx, character_name: str):
        character = next((character for character in all_characters if character.name == character_name), None)
        if character is None:
            await ctx.send(f"Character '{character_name}' not found.")
            return
        await ctx.send(f'{character}')
    
    #Show specific spell
    @commands.command(name='spell', help='This command lists a specific spell. !spell <name>')
    async def listspell(self, ctx, spell_name: str):
        spell = next((spell for spell in all_spells if spell.name == spell_name), None)
        if spell is None:
            await ctx.send(f"Spell '{spell_name}' not found.")
            return
        await ctx.send(f'{spell}')
    
def setup(bot):
    bot.add_cog(Utility(bot))