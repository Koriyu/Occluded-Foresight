import random

class Player:
    def __init__(self,name,gold):
        self.name = name
        self.gold = gold

    def cue_death():
        pass

#-- ENTITIES --

class Entity:

    def __init__(self,name,symbol):
        self.name = name
        self.symbol = symbol
    
air_entity = Entity('Air','□')
pillar_entity = Entity('Pillar','▥')
treasure_entity = Entity('Treasure', '❉')
portal_entity = Entity('Portal', '♨')
wall_entity = Entity('Wall','▩')

#-- GRIDMAKER --

lengthx = 1
lengthy = 2

grid = ''

gridx = ''
for i in range(lengthx):
    gridx += air_entity.symbol
for i in range(lengthy):
    if i == 0:
        grid += gridx
    else:
        grid += '\n' + gridx
