from xmlhandler import XMLHandler
# Defining global variables
spell_path = 'spells.xml'
character_path = 'characters.xml'
REQUIRED_SCALINGS = ['strength', 'luck', 'durability', 'speed', 'intellect']

#Load spells
all_spells = XMLHandler.load_spells(spell_path)
if all_spells is None:
    all_spells = []
spell_names = [spell.name for spell in all_spells]  # for spell name validation

#Load characters
all_characters = XMLHandler.load_characters(character_path, all_spells)
if all_characters is None:
    all_characters = []