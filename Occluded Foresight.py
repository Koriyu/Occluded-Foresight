import random
import math

"""------ some random math ------"""

def sqr(n):
    return n * n

def similaritems(l1,l2):
    truthvalue = False
    for i in l1:
        for j in l2:
            if i == j:
                truthvalue = True
    return truthvalue
"""-----------------------------------------------------------------------------------------"""
"""-----------------------------------------------------------------------------------------"""

# CLASSES

"""-----------------------------------------------------------------------------------------"""
"""-----------------------------------------------------------------------------------------"""
#-- CHARACTER --
class Character:

    def __init__(self,name,symbol):
        self.name = name
        self.symbol = symbol

character = Character('Character','♜',)


#-- ENTITIES -- (Rename to WallisinsideWalls later)
entity_list = []
class Entity:

    def __init__(self,name,symbol,alternate_symbols=[None]):
        self.name = name
        self.symbol = symbol
        self.alternate_symbols = alternate_symbols
        entity_list.append(self)


pillar_entity = Entity('Pillar','▥',['▥','▥','▥'])
treasure_entity = Entity('Treasure', '❉')
portal_entity = Entity('Portal', '♨')

# The lower the level the closer it is to the treasure
l1td_entity = Entity('Level 1 Treasure Detector', 'x')
l2td_entity = Entity('Level 2 Treasure Detector', 'X')

"""-----------------------------------------------------------------------------------------"""
"""-----------------------------------------------------------------------------------------"""

# GRIDMAKER

"""-----------------------------------------------------------------------------------------"""
"""-----------------------------------------------------------------------------------------"""

# FUNCTIONS:
    # generate_gridlist: takes the length and width (xx and yy respectively) of the grid to create a grid list.

def generate_gridlist(xx,yy):
    
    lengthx = xx
    lengthy = yy

    grid = []

    # -- For up and down walls
    wally = []
    for i in range(lengthx + 2):
        wally.append('■')

    grid.append(wally) # -- Upper wall appended as the first list in the list

    # -- The crypt itself

    for i in range(lengthy + 5): # print gridx if i is from 0 to lengthy-1, print start if i is from lengthy to lengthy + 2, print start 2 if i is from 

        # -- -- Make each x axis layer

        if i < lengthy:

            gridx = []

            gridx.append('■')
            for j in range(lengthx):
                gridx.append('◦')
            gridx.append('■')

            grid.append(gridx)

        # -- -- -- Starting area (closes once crypt is entered) (character zone only)

        elif i < lengthy + 2:

            start = []

            for j in range(lengthx + 2):
                if int((lengthx + 2) / 2) + 1 >= j >= int((lengthx + 2) / 2) - 1:
                    start.append('◦')
                else:
                    start.append('■')

            grid.append(start)


        elif i < lengthy + 5:

            start2 = []

            for j in range(lengthx + 2):
                if int((lengthx + 2) / 2) + 2 >= j >= int((lengthx + 2) / 2) - 2:
                    start2.append('◦')
                else:
                    start2.append('■')
            
            grid.append(start2)

    grid.append(wally) # -- -- Down wall

    return grid

"""-----------------------------------------------------------------------------------------"""
"""-----------------------------------------------------------------------------------------"""

# OBSTACLES AND TREASURE GENERATION

"""-----------------------------------------------------------------------------------------"""
"""-----------------------------------------------------------------------------------------"""
# FUNCTIONS:
    # For Treasure Generation:
        # call_all_air()


# Treasure and Pillar Generation:

def call_all_air(gridlist,lengthy):
    air_coords = []
    for i_list in range(len(gridlist)):
        for i_i_list in range(len(gridlist[i_list])):
            if gridlist[i_list][i_i_list] == '◦' and i_list <= lengthy:
                air_coords.append([i_i_list,i_list])
    return air_coords

def randomselect_aircoords(gridlist,lengthy,n):

    air_coords = call_all_air(gridlist,lengthy)
    random_aircoords = []
    while len(random_aircoords) < n:
        selected_coord = random.choice(air_coords)
        notinunavailrange = True
        if len(random_aircoords) != 0:
            for i in random_aircoords:
                if selected_coord == i or selected_coord[0]-1 == i[0] or selected_coord[0]+1 == i[0] or selected_coord[1]-1 == i[1] or selected_coord[1]+1 == i[1] or ([selected_coord[0]-1,selected_coord[1]-1] == i) or ([selected_coord[0]+1,selected_coord[1]-1] == i) or ([selected_coord[0]-1,selected_coord[1]+1] == i) or ([selected_coord[0]+1,selected_coord[1]+1] == i):
                    notinunavailrange = False
                    break
        if notinunavailrange:
            random_aircoords.append(selected_coord)
    return random_aircoords

def addtreasuredetectors(gridlist,lengthy,treasurecoords):
    air_list = call_all_air(gridlist,lengthy)
    treasure_list = treasurecoords
    treasuredetectorcoords = [[],[]]

    for treasure in treasure_list:
        for coordinate in air_list:
            if math.sqrt(sqr(treasure[0]-coordinate[0]) + sqr(treasure[1]-coordinate[1])) <= 2 and coordinate not in treasure_list:
                treasuredetectorcoords[0].append(coordinate)
            elif math.sqrt(sqr(treasure[0]-coordinate[0]) + sqr(treasure[1]-coordinate[1])) <= 4 and coordinate not in treasure_list:
                treasuredetectorcoords[1].append(coordinate)
    
    return treasuredetectorcoords

def treasurize(gridlist,lengthy,tcl,tdl,pcl,portl):

    generatedgridlist = gridlist
    for i in tcl:
        generatedgridlist[i[1]][i[0]] = treasure_entity
    for i in tdl[1]:
        generatedgridlist[i[1]][i[0]] = l2td_entity
    for i in tdl[0]:
        generatedgridlist[i[1]][i[0]] = l1td_entity
    for i in pcl:
        generatedgridlist[i[1]][i[0]] = pillar_entity
    if portl != None:
        for i in portl:
            generatedgridlist[i[1]][i[0]] = portal_entity
    return generatedgridlist

"""-----------------------------------------------------------------------------------------"""
"""-----------------------------------------------------------------------------------------"""

# CHARACTER PRESENCE & MOVEMENT CONTROL

"""-----------------------------------------------------------------------------------------"""
"""-----------------------------------------------------------------------------------------"""
# FUNCTIONS:
    # change_charactercoords(x,y,movement_key): takes character coordinates (x,y), changes it according to the desired direction(movement_key), and returns the changed coordinates.
    # isinsideWall(x,y): Takes character coordinates (x,y) and checks if the coordinate has similar coordinates as one of the walls of the grid. Returns true if so.
    # generate_gridwithcharacter(x,y): takes character coordinates (x,y) and places the character to the grid at its respective coordinate.

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

def isinsideWall(x,y,generated_grid_list):
    character_coordinates = [x,y]
    insidewallBool = False
    for ind_list in range(len(generated_grid_list)): # -- Iterate through the list of lists
        for ind_i in range(len(generated_grid_list[ind_list])): # -- Iterate through the characters of each list
            if generated_grid_list[ind_list][ind_i] == '■' and [ind_i,ind_list] == character_coordinates: # -- Character position determinant
                insidewallBool = True
    return insidewallBool

def generate_gridwithcharacter(x,y,generated_grid_list):
    character_coordinates = [x,y]

    for ind_list in range(len(generated_grid_list)): # -- Represent entire line
        gridx = ''
        for ind_i in range(len(generated_grid_list[ind_list])): # -- Represent character of each line
            if [ind_i,ind_list] == character_coordinates: # -- Character position determinant
                gridx += character.symbol
            elif type(generated_grid_list[ind_list][ind_i]) == Entity:
                gridx += generated_grid_list[ind_list][ind_i].symbol
            else:
                gridx += generated_grid_list[ind_list][ind_i]
        print(gridx)

"""-----------------------------------------------------------------------------------------"""
"""-----------------------------------------------------------------------------------------"""

# CRYPT HEALTH SYSTEM AND GAME OVER

"""-----------------------------------------------------------------------------------------"""
"""-----------------------------------------------------------------------------------------"""

crypt_health = 1000

def crumblecrypt(health):
    if health == 0:
        return True

def game_over(bool):

    gameoverbool = False
    for i in bool:
        if i == True:
            gameoverbool = True
    return gameoverbool
        

"""-----------------------------------------------------------------------------------------"""
"""-----------------------------------------------------------------------------------------"""

# OBSTACLES AND TREASURE: INTERACTIONS WITH PLAYER AND ENVIRONMENT

"""-----------------------------------------------------------------------------------------"""
"""-----------------------------------------------------------------------------------------"""

def isinsideInteractive(x,y,generated_grid_list,Interactive): # Checks 
    character_coordinates = [x,y]
    
    insideInteractiveBool = False
    for ind_list in range(len(generated_grid_list)): # -- Iterate through the list of lists
        for ind_i in range(len(generated_grid_list[ind_list])): # -- Iterate through the characters of each list
            if generated_grid_list[ind_list][ind_i] == Interactive and [ind_i,ind_list] == character_coordinates: # -- Character position determinant
                insideInteractiveBool = True
    return insideInteractiveBool


"""-----------------------------------------------------------------------------------------"""
"""-----------------------------------------------------------------------------------------"""

# BODY

"""-----------------------------------------------------------------------------------------"""
"""-----------------------------------------------------------------------------------------"""

# FUNCTIONS:
    # initgl(): responsible for character presence and movement control; takes character coordinates [x,y] and starts the grid loop, only ending once a condition has been met.

def initgl():
    lengthx = 55
    lengthy = 15

    generated_grid_list = generate_gridlist(55,15)

    character_coordinates = [int(lengthx/2)+1,lengthy+4]

    init_crypt_health = 1000
    crypt_health = 1000

    numoftreasure = 5
    current_treasure = 0

    message_line = ''

    treasurecoordslist = randomselect_aircoords(generated_grid_list,lengthy,5)
    treasuredetectorslist = addtreasuredetectors(generated_grid_list,lengthy,treasurecoordslist)
    pillarcoordslist = randomselect_aircoords(generated_grid_list,lengthy,int(len(call_all_air(generated_grid_list,lengthy))/50))

    if similaritems(treasurecoordslist,pillarcoordslist):
        while similaritems(treasurecoordslist,pillarcoordslist):
            pillarcoordslist = randomselect_aircoords(generated_grid_list,lengthy,int(len(call_all_air(generated_grid_list,lengthy))/50))
    
    portal_coord = randomselect_aircoords(generated_grid_list,lengthy,1)
    canportalize = False

    
    if similaritems(portal_coord,pillarcoordslist):
        while similaritems(portal_coord,pillarcoordslist):
                pillarcoordslist = randomselect_aircoords(generated_grid_list,lengthy,int(len(call_all_air(generated_grid_list,lengthy))/50))

    



    while (([character_coordinates[0],character_coordinates[1]] != portal_coord[0]) and (current_treasure != numoftreasure)): # -- Replace the condition of while to something (either the game ends with a win or a game over)

        temp_grid_list = generate_gridlist(55,15)


        tcl = treasurecoordslist
        tdcl = addtreasuredetectors(temp_grid_list,lengthy,treasurecoordslist)
        pcl = pillarcoordslist
        portl = portal_coord

        if canportalize:
            treasurize(temp_grid_list,lengthy,tcl,tdcl,pcl,portl)
        else:
            treasurize(temp_grid_list,lengthy,tcl,tdcl,pcl,None)
        

        for i in range(50):
            print('')

        generate_gridwithcharacter(character_coordinates[0],character_coordinates[1],temp_grid_list)

        print(message_line)
        message_line = ''

        print('Crypt health: [{x}/{y}]              ❉ Treasure: [{a}/{b}]'.format(x=crypt_health,y=init_crypt_health,a=current_treasure,b=numoftreasure))

        char_movement = input('[w/a/s/d]')
        if char_movement not in ['w','a','s','d','W','A','S','D']:
            continue

        new_character_coordinates = change_charactercoords(character_coordinates[0],character_coordinates[1],char_movement)

        # -- Place the conditions for interacting with different objects here
        
        if isinsideWall(new_character_coordinates[0],new_character_coordinates[1],temp_grid_list): 
            # -- For if the character bumps into a wall
            message_line += 'You bumped into a wall. The crypt quivers. (-2 Crypt Health)\n'
            crypt_health -= 2
            print(crypt_health)
            continue
        elif isinsideInteractive(new_character_coordinates[0],new_character_coordinates[1],temp_grid_list,pillar_entity):
            message_line += 'You bumped into a pillar. The ceiling cracks. (-5 Crypt Health)\n'
            crypt_health -= 5
            print(crypt_health)
            continue

        elif isinsideInteractive(new_character_coordinates[0],new_character_coordinates[1],temp_grid_list,l2td_entity):
            message_line += 'You sense a treasure nearby...\n'
            character_coordinates = new_character_coordinates

        elif isinsideInteractive(new_character_coordinates[0],new_character_coordinates[1],temp_grid_list,l1td_entity):
            message_line += 'You feel the treasure\'s presence growing stronger...\n'
            character_coordinates = new_character_coordinates

        elif isinsideInteractive(new_character_coordinates[0],new_character_coordinates[1],temp_grid_list,treasure_entity):
            message_line += 'You found a treasure!\n'
            treasurecoordslist.remove([new_character_coordinates[0],new_character_coordinates[1]])
            character_coordinates = new_character_coordinates
            current_treasure += 1
            if current_treasure == numoftreasure:
                message_line += 'You have found all 5 treasures! As a result, a portal has opened, but the crypt\n'
                message_line += 'is now decaying rapidly. Find the portal as soon as possible to save yourself.\n'
                canportalize = True
                print(canportalize)
        else:
            character_coordinates = new_character_coordinates
        crypt_health -= 1

initgl()
'''generated_grid_list = generate_gridlist(55,15)
portal_coord = randomselect_aircoords(generated_grid_list,15,1)
print(portal_coord)'''
"""lengthx = 55

lengthy = 15

generated_grid_list = generate_gridlist(55,15)

character_coordinates = [int(lengthx/2)+1,lengthy+4]

init_crypt_health = 1000
crypt_health = 1000

numoftreasure = 5
current_treasure = 0

message_line = ''

treasurecoordslist = randomselect_aircoords(generated_grid_list,lengthy,5)
treasuredetectorslist = addtreasuredetectors(generated_grid_list,lengthy,treasurecoordslist)
pillarcoordslist = randomselect_aircoords(generated_grid_list,lengthy,int(len(call_all_air(generated_grid_list,lengthy))/50))

for i in pillarcoordslist:
    print(i)"""