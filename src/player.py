from random import random, choice, randint
from game_data import WEAPONS, WEAPON_EQUIPE_PROB, WEAPON_USE_PROB

class Player:

    def __init__(self, name, index):
        self._name = name
        self._index = index
        self._health = 100
        self._weapons = []

    def tick(self, other):
        text = ""
        players = [self]
        if len(self._weapons) > 0 and random() < WEAPON_USE_PROB:
            weapon = choice(self._weapons)
            damage = randint(weapon['damage_range'][0], weapon['damage_range'][1])
            text = weapon['use_message'](self._name, other.get_name())
            if 'fake' in weapon:
                self.apply_damage(damage)
                text += f'\n{self.get_name()}\'s health drops to {self.get_health()}%'
            else:
                other.apply_damage(damage)
                text += f'\n{other.get_name()}\'s health drops to {other.get_health()}%'
            self._weapons.remove(weapon)
            players.append(other)
        elif random() < WEAPON_EQUIPE_PROB:
            weapon = choice(WEAPONS)
            text = weapon['get_message'](self._name)
            self._weapons.append(weapon)
        else:
            return None
        return [text, players]

    def apply_damage(self, amount):
        self._health = max(0, self._health - amount)
    
    def get_name(self):
        return self._name
    
    def get_health(self):
        return self._health

    def get_index(self):
        return self._index
    