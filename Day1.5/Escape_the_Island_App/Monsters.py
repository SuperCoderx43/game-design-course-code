import numpy as np

class Monsters:

    def __init__(self, state, name, hp, atk, quality, description, kill_message, loot, attacks):
        self.alive = state
        self.hp = hp
        self.maxhp = hp
        self.atk = atk
        self.name = name
        self.quality = quality
        self.description = description
        self.kill_message = kill_message
        self.loot = loot
        self.attacks = attacks


    