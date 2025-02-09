from discord.ext import commands
from globals import *
from update import updatecharacter

class Combat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #Attack a character
    @commands.command(name='use', help='This command uses a spell with a target character. Example: !use Bob Fireball Target', aliases=['attack'])
    async def attack(self, ctx, character_name: str, spell_name: str, target_name: str):
        #Find the character
        character = next((character for character in all_characters if character.name == character_name), None)
        if character is None:
            await ctx.send(f"Character '{character_name}' not found.")
            return

        #Find the target
        target = next((target for target in all_characters if target.name == target_name), None)
        if target is None:
            await ctx.send(f"Target '{target_name}' not found.")
            return

        #Find the spell in character's usable spells
        character_spells = character.spells
        spell = next((spell for spell in character_spells if spell.name == spell_name), None)
        if spell is None:
            await ctx.send(f"Spell '{spell_name}' not found in {character_name}'s usable spells.")
            return

        #Calculate the damage
        damage = spell.calculate_damage(*[character.stats])

        #Apply stamina cost
        character.current_stamina -= spell.stamina_cost
        if character.current_stamina < 0:
            await ctx.send(f"Character '{character_name}' does not have enough stamina to cast '{spell_name}'.")
            return

        #Apply health cost
        target.current_health -= round(damage)
        if target.current_health <= 0:
            target.current_health = 0
            await ctx.send(f"Character '{target_name}' has been defeated!")

        # Update the characters stats
        await updatecharacter(ctx, character_name, character.health, character.current_health, character.stamina, character.current_stamina, True, *[f"{stat}:{value}" for stat, value in character.stats.items()])
        await updatecharacter(ctx, target_name, target.health, target.current_health, target.stamina, target.current_stamina, True,*[f"{stat}:{value}" for stat, value in target.stats.items()])


        await ctx.send(f"Character '{character_name}' attacked with spell '{spell_name}' for {round(damage)} damage! {target_name} now has {target.current_health} / {target.health} health.\n{character_name} now has {character.current_stamina} / {character.stamina} stamina.")

    #Heal a character
    @commands.command(name='heal', help='This command heals a character. Example: !heal Bob 100')
    async def heal(self, ctx, character_name: str, heal_amount: int):
        #Find the character
        character = next((character for character in all_characters if character.name == character_name), None)
        if character is None:
            await ctx.send(f"Character '{character_name}' not found.")
            return

        #Heal the character
        character.current_health += heal_amount
        if character.current_health > character.health:
            character.current_health = character.health
        updatecharacter(ctx, character_name, character.health, character.current_health, character.stamina, character.current_stamina, *[f"{stat}:{value}" for stat, value in character.stats.items()])
        await ctx.send(f"Character '{character_name}' healed for {heal_amount} health! {character_name} now has {character.health} health.")

    #Rejuvenate a character
    @commands.command(name='rejuvenate', help='This command rejuvenates a character. Example: !rejuvenate Bob 100')
    async def rejuvenate(self, ctx, character_name: str, rejuvenate_amount: int):
        #Find the character
        character = next((character for character in all_characters if character.name == character_name), None)
        if character is None:
            await ctx.send(f"Character '{character_name}' not found.")
            return

        #Rejuvenate the character
        character.current_stamina += rejuvenate_amount
        if character.current_stamina > character.stamina:
            character.current_stamina = character.stamina
        updatecharacter(ctx, character_name, character.health, character.current_health, character.stamina, character.current_stamina, *[f"{stat}:{value}" for stat, value in character.stats.items()])
        await ctx.send(f"Character '{character_name}' rejuvenated for {rejuvenate_amount} stamina! {character_name} now has {character.stamina} stamina.")

def setup(bot):
    bot.add_cog(Combat(bot))