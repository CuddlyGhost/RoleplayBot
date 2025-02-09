class Character:
    def __init__(self, author, name, health, stamina, stats, current_health = -1, current_stamina = -1, spells=None):
        self.author = author
        self.name = name
        self.health = health
        self.stamina = stamina
        self.stats = stats
        self.spells = spells if spells is not None else []
        if (current_health == -1):
            self.current_health = health
        else:
            self.current_health = current_health
        if (current_stamina == -1):
            self.current_stamina = stamina
        else:
            self.current_stamina = current_stamina

    def add_spell(self, spell):
        self.spells.append(spell)
    
    def __str__(self):
        spells_str = '\n'.join([spell.name for spell in self.spells])
        stats_str = '\n'.join([f'{stat}: {value}' for stat, value in self.stats.items()])
        return f'-------------------\nAuthor: {self.author}\nCharacter name: {self.name}\nHP: {self.current_health} / {self.health}\nStamina: {self.current_stamina} / {self.stamina}\nStats\n{stats_str}\n\nSpells:\n{spells_str}\n-------------------'