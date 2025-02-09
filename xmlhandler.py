import xml.etree.ElementTree as ET
from xml.dom import minidom
from spell import Spell
from character import Character

class XMLHandler:
    @staticmethod
    def load_spells(file_path):
    # read spells from file
        spells	= []
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()

            spells = []
            for spell in root.findall('spell'):
                name = spell.find('name').text
                cooldown = int(spell.find('cooldown').text)
                stamina_cost = int(spell.find('stamina_cost').text)
                scaling = {}
                scaling_element = spell.find('scaling')
                if scaling_element is not None:
                    for stat_element in scaling_element:
                        scaling[stat_element.tag] = float(stat_element.text)
                spell_obj = Spell(name, scaling, cooldown, stamina_cost)
                spells.append(spell_obj)
        except FileNotFoundError:
            print(f"XML file '{file_path}' not found. Starting fresh.")
        except Exception as e:
            print(f"Error loading spells from XML: {e}")
        return spells
    
    @staticmethod
    def save_spell(file_path, spell):
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
        except FileNotFoundError:
            #Create new XML where it doesn't exist yet
            root = ET.Element("spells")
            tree = ET.ElementTree(root)

        existing_spell = root.find(f"spell[name='{spell.name}']")
        if existing_spell is not None:
            root.remove(existing_spell)
            print(f"Spell '{spell.name}' already exists. Overwriting.")
        
        spell_element = ET.Element('spell')
        name_element = ET.SubElement(spell_element,'name')
        name_element.text = spell.name
        scaling_element = ET.SubElement(spell_element, "scaling")
        for stat, factor in spell.scaling.items():
            stat_elem = ET.SubElement(scaling_element, stat)
            stat_elem.text = str(factor)
        
        cooldown_element = ET.SubElement(spell_element,'cooldown')
        cooldown_element.text = str(spell.cooldown)

        stamina_cost_element = ET.SubElement(spell_element,'stamina_cost')
        stamina_cost_element.text = str(spell.stamina_cost)

        # Pretty print the XML and write it to the file
        root.append(spell_element)
        tree_str = ET.tostring(root, 'utf-8')
        parsed_str = minidom.parseString(tree_str)  # Parse the XML string to format it
        pretty_str = parsed_str.toprettyxml(indent="  ")  # Apply pretty formatting with indentation

        # Remove empty lines (lines that only contain whitespace or are completely empty)
        clean_str = '\n'.join([line for line in pretty_str.splitlines() if line.strip() != ''])

        with open(file_path, "w") as file:
            file.write(clean_str)  # Write the formatted XML to the file

    @staticmethod
    def load_characters(file_path, spell_list):
        characters = []
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            for character in root.findall('character'):
                name = character.find('name').text
                stats = {stat.tag: int(stat.text) for stat in character.find('stats')}
                spells = []
                for spell in character.findall('spell'):
                    spell = next((s for s in spell_list if s.name == spell.text), None)
                    if spell:
                        spells.append(spell)
                characters.append(Character(name, stats, spells))
        except FileNotFoundError:
            print(f"XML file '{file_path}' not found. Starting fresh.")
        except Exception as e:
            print(f"Error loading characters from XML: {e}")
        return characters
    
    @staticmethod
    def save_character(file_path, character):
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
        except FileNotFoundError:
            #Create new XML where it doesn't exist yet
            root = ET.Element("characters")
            tree = ET.ElementTree(root)
        
        # Remove existing character if it exists
        existing_character = root.find(f"character[name='{character.name}']")
        if existing_character is not None:
            root.remove(existing_character)
            print(f"Character '{character.name}' already exists. Overwriting.")
        

        character_element = ET.Element('character')
        name_element = ET.SubElement(character_element,'name')
        name_element.text = character.name
        stats_element = ET.SubElement(character_element,'stats')
        for stat, value in character.stats.items():
            stat_elem = ET.SubElement(stats_element, stat)
            stat_elem.text = str(value)
        spells_elem = ET.SubElement(character_element, 'spells')
        for spell in character.spells:
            spell_elem = ET.SubElement(spells_elem, 'spell')
            spell_elem.text = spell.name
        root.append(character_element)
        tree_str = ET.tostring(root, 'utf-8')
        parsed_str = minidom.parseString(tree_str)  # Parse the XML string to format it
        pretty_str = parsed_str.toprettyxml(indent="  ")  # Apply pretty formatting with indentation

        # Remove empty lines (lines that only contain whitespace or are completely empty)
        clean_str = '\n'.join([line for line in pretty_str.splitlines() if line.strip() != ''])
        
        with open(file_path, "w") as file:
            file.write(clean_str)  # Write the formatted XML to the file