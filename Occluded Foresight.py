import random

#-- ENTITIES -- (Rename to interactives later)

class Entity:

    def __init__(self,name,symbol):
        self.name = name
        self.symbol = symbol
    
air_entity = Entity('Air','◦')
pillar_entity = Entity('Pillar','▥')
treasure_entity = Entity('Treasure', '❉')
portal_entity = Entity('Portal', '♨')
wall_entity = Entity('Wall','■')

character_entity = Entity('Character','♜')
"""-----------------------------------------------------------------------------------------"""
# GRIDMAKER
"""-----------------------------------------------------------------------------------------"""

# -- Todo: turn a grid into a list of lists [[],[],[]]
def generate_gridlist(xx,yy):

    '''for i in range(100):
        print('') # -- no reason

    print('... the crypt opens its doors to the blind and brave ...')'''

    # -- x and y values of the crypt
    lengthx = xx
    lengthy = yy

    grid = []

    # -- For up and down walls
    wally = []
    for i in range(lengthx + 2):
        wally.append(wall_entity.symbol)

    grid.append(wally) # -- Upper wall appended as the first list in the list

    # -- The crypt itself

    for i in range(lengthy + 5): # print gridx if i is from 0 to lengthy-1, print start if i is from lengthy to lengthy + 2, print start 2 if i is from 

        # -- -- Make each x axis layer

        if i < lengthy:

            gridx = []

            gridx.append(wall_entity.symbol)
            for j in range(lengthx):
                gridx.append(air_entity.symbol)
            gridx.append(wall_entity.symbol)

            grid.append(gridx)

        # -- -- -- Starting area (closes once crypt is entered) (character zone only)

        elif i < lengthy + 2:

            start = []

            for j in range(lengthx + 2):
                if int((lengthx + 2) / 2) + 1 >= j >= int((lengthx + 2) / 2) - 1:
                    start.append(air_entity.symbol)
                else:
                    start.append(wall_entity.symbol)

            grid.append(start)


        elif i < lengthy + 5:

            start2 = []

            for j in range(lengthx + 2):
                if int((lengthx + 2) / 2) + 2 >= j >= int((lengthx + 2) / 2) - 2:
                    start2.append(air_entity.symbol)
                else:
                    start2.append(wall_entity.symbol)
            
            grid.append(start2)

    grid.append(wally) # -- -- Down wall

    return grid

generated_grid_list = generate_gridlist(55,15)


"""-----------------------------------------------------------------------------------------"""
# OBSTACLES AND TREASURE GENERATION
"""-----------------------------------------------------------------------------------------"""
# -- SOON
"""-----------------------------------------------------------------------------------------"""
# CHARACTER PRESENCE & MOVEMENT CONTROL
"""-----------------------------------------------------------------------------------------"""

# -- MANIPULATING VARIABLES
lengthx = 55
lengthy = 15
generated_grid_list = generate_gridlist(lengthx,lengthy)

character_coordinates = [int(lengthx/2)+1,lengthy+4]


def change_charactercoords(x,y,movement_key):
    character_coordinates = [x,y]
    if movement_key == 'w' or movement_key == 'W':
        character_coordinates[1] -= 1
    if movement_key == 'a' or movement_key == 'A':
        character_coordinates[0] -= 1
    if movement_key == 's' or movement_key == 'S':
        character_coordinates[1] += 1
    if movement_key == 'd' or movement_key == 'D':
        character_coordinates[0] += 1
    return character_coordinates

def isinsideWall(x,y):
    character_coordinates = [x,y]
    insidewallBool = False
    for ind_list in range(len(generated_grid_list)): # -- Iterate through the list of lists
        for ind_i in range(len(generated_grid_list[ind_list])): # -- Iterate through the characters of each list
            if generated_grid_list[ind_list][ind_i] == wall_entity.symbol and [ind_i,ind_list] == character_coordinates: # -- Character position determinant
                insidewallBool = True
    return insidewallBool


def generate_gridwithcharacter(x,y):
    character_coordinates = [x,y]

    for ind_list in range(len(generated_grid_list)): # -- Represent entire line
        gridx = ''
        for ind_i in range(len(generated_grid_list[ind_list])): # -- Represent character of each line
            if generated_grid_list[ind_list][ind_i] != wall_entity.symbol and [ind_i,ind_list] == character_coordinates: # -- Character position determinant
                gridx += character_entity.symbol
            else:
                gridx += generated_grid_list[ind_list][ind_i]
        print(gridx)


# -- CHARACTER MOVEMENT (UNCHANGEABLE POSITION)
generate_gridwithcharacter(character_coordinates[0],character_coordinates[1])

while character_coordinates != [1,1]: # -- Replace the condition of while to something (either the game ends with a win or a game over)

    for i in range(50):
        print('')
        
    generate_gridwithcharacter(character_coordinates[0],character_coordinates[1])

    print(character_coordinates)
    char_movement = input('[w/a/s/d]')
    if char_movement not in ['w','a','s','d']:
        continue

    new_character_coordinates = change_charactercoords(character_coordinates[0],character_coordinates[1],char_movement)
    if isinsideWall(new_character_coordinates[0],new_character_coordinates[1]):
        print(isinsideWall)
        continue
    else:
        generate_gridwithcharacter(new_character_coordinates[0],new_character_coordinates[1])
        character_coordinates = new_character_coordinates
    


