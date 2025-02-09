class Spell:
    def __init__(self, name, scaling, cooldown, stamina_cost):
        self.name = name
        self.scaling = scaling
        self.cooldown = cooldown
        self.stamina_cost = stamina_cost

    def __str__(self):
        return f'Spell statistics of {self.name}:\n{self.scaling}\nCooldown: {self.cooldown}\nStamina cost: {self.stamina_cost}'
    
    def calculate_damage(self, *attributes):
        damage = 0
        for attr, factor in self.scaling.items():
            for scale in attributes:
                if attr in scale:
                    damage += scale[attr] * factor
        damage -= (damage * scale['durability']) / 100
        return damage