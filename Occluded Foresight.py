import random

class Player:
    def __init__(self,name,gold):
        self.name = name
        self.gold = gold

    def cue_death():
        pass

#-- ENTITIES -- (Rename to interactives later)

class Entity:

    def __init__(self,name,symbol):
        self.name = name
        self.symbol = symbol
    
air_entity = Entity('Air','□')
pillar_entity = Entity('Pillar','▥')
treasure_entity = Entity('Treasure', '❉')
portal_entity = Entity('Portal', '♨')
wall_entity = Entity('Wall','■')

character_entity = Entity('Character','♟')
"""-----------------------------------------------------------------------------------------"""
# GRIDMAKER
"""-----------------------------------------------------------------------------------------"""
def make_grid(xx,yy):
    for i in range(100):
        print('')

    print('... the crypt opens its doors to the blind and brave ...')

    # -- x and y values of the crypt
    lengthx = 55
    lengthy = 15

    character_coordinates = [xx,yy]

    # -- For up and down walls
    wally = ''
    for i in range(lengthx + 2):
        wally += wall_entity.symbol

    # -- The crypt itself

    print(wally) # -- -- up wall

    for i in range(lengthy + 5): # print gridx if i is from 0 to lengthy-1, print start if i is from lengthy to lengthy + 2, print start 2 if i is from 

        # -- -- Make each x axis layer
        gridx = ''
        gridx += wall_entity.symbol # - Left Wall
        if i < lengthy:
            for j in range(lengthx):
                if j == character_coordinates[0] and i == character_coordinates[1]:
                    gridx += character_entity.symbol
                else:
                    gridx += air_entity.symbol
            gridx += wall_entity.symbol # - Right Wall
            print(gridx)

        # -- -- -- Starting area (closes once crypt is entered) (character zone only)

        elif i < lengthy + 2:
            start = ''
            for j in range(lengthx + 2):
                if int((lengthx + 2) / 2) + 1 >= j >= int((lengthx + 2) / 2) - 1:
                    start += air_entity.symbol
                else:
                    start += wall_entity.symbol
            print(start)
        elif i < lengthy + 5:
            start2 = ''
            for j in range(lengthx + 2):
                if int((lengthx + 2) / 2) + 2 >= j >= int((lengthx + 2) / 2) - 2:
                    start2 += air_entity.symbol
                else:
                    start2 += wall_entity.symbol
            print(start2)

    print(wally) # -- -- Down wall

"""-----------------------------------------------------------------------------------------"""
# CHARACTER PRESENCE & MOVEMENT CONTROL
"""-----------------------------------------------------------------------------------------"""

# Air blocks with y-coordinates above the y-length of the crypt will turn into wall blocks / get deleted once the character enters the crypt itself

character_coordinates = [1,2]

make_grid(0,7)