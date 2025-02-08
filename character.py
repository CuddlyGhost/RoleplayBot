class Character:
    def __init__(self, name, health, stamina, stats, spells=None):
        self.name = name
        self.health = health
        self.stamina = stamina
        self.stats = stats
        self.spells = spells if spells is not None else []

    def add_spell(self, spell):
        self.spells.append(spell)
    
    def __str__(self):
        spells_str = ', '.join([spell.name for spell in self.spells])
        return f'Character name: {self.name}\nStats: {self.stats}\nSpells: {spells_str}'