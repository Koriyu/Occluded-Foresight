# Occluded Foresight by Koriyu / woodentechno

import random
import math
import os
import msvcrt
import time

"""------ some random math and stuff ------"""


def get_key(msg="Press any key ...", time_to_sleep=3):
    """
    msg - set to an empty string if you don't want to print anything
    time_to_sleep - default 3 seconds
    """
    global key_pressed
    if msg != None:
        print(msg)
    key_pressed = None
    start_time = time.time()
    
    while True:
        if msvcrt.kbhit():  # Check if a key has been pressed
            key_pressed = msvcrt.getch().decode('utf-8')
            break

        if time.time() - start_time >= time_to_sleep:
            break
    
    return key_pressed

def sqr(n):
    return n * n

def similaritems(l1,l2):
    truthvalue = False
    for i in l1:
        for j in l2:
            if i == j:
                truthvalue = True
    return truthvalue

def identitywindows():
    if os.name != 'nt':
        return False
    else:
        return True

def clear():
    if identitywindows():
        os.system('cls')
    else:
        os.system('clear')


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


#-- ENTITIES --
entity_list = []
class Entity:

    def __init__(self,name,alternate):
        self.name = name
        self.symbol = '◦'
        self.alternate = alternate
        entity_list.append(self)


pillar_entity = Entity('Pillar', '▥')
treasure_entity = Entity('Treasure', '❉')
portal_entity = Entity('Portal', '♨')

l1td_entity = Entity('Level 1 Treasure Detector', 'x')
l2td_entity = Entity('Level 2 Treasure Detector', 'X')

l1pd_entity = Entity('Level 1 Portal Detector', '.')
l2pd_entity = Entity('Level 2 Portal Detector', 'o')
l3pd_entity = Entity('Level 3 Portal Detector', '0')

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

    wally = []
    for i in range(lengthx + 2):
        wally.append('■')

    grid.append(wally)


    for i in range(lengthy + 5): # print gridx if i is from 0 to lengthy-1, print start if i is from lengthy to lengthy + 2, print start 2 if i is from 

        if i < lengthy:

            gridx = []

            gridx.append('■')
            for j in range(lengthx):
                gridx.append('◦')
            gridx.append('■')

            grid.append(gridx)

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

    grid.append(wally)

    return grid

class Grid:

    def __init__(self,lengthx,lengthy):
        self.lengthx = lengthx
        self.lengthy = lengthy
        self.gridlist = generate_gridlist(lengthx,lengthy)

"""-----------------------------------------------------------------------------------------"""
"""-----------------------------------------------------------------------------------------"""

# OBSTACLES AND TREASURE GENERATION

"""-----------------------------------------------------------------------------------------"""
"""-----------------------------------------------------------------------------------------"""
# FUNCTIONS:
    # For Treasure Generation:
        # call_all_air(gridlist): returns a list of coordinates with '◦' inside gridlist
        # randomselect_aircoords(gridlist,n): returns a list of n random air ('◦') coordinates
        # addtreasuredetectors(gridlist,treasurecoords): returns a list of treasure detectors that surround each treasure in [treasurecoords] (used for intuition)
        # addportaldetectors(gridlist,treasurecoords): addtreasuredetectors but portal detectors instead of treasure detectors
        # treasurize(grid_list,tcl,tdl,pcl,portl,portdl): replaces all ('◦') coordinates (except the airs at the character's spawnpoint) with the Entities/Interactives based on their corresponding coordinates


# Treasure and Pillar Generation:

def call_all_air(grid_list):
    air_coords = []

    gridlist = grid_list.gridlist
    lengthy = grid_list.lengthy

    for i_list in range(len(gridlist)):
        for i_i_list in range(len(gridlist[i_list])):
            if gridlist[i_list][i_i_list] == '◦' and i_list <= lengthy:
                air_coords.append([i_i_list,i_list])
    return air_coords

def randomselect_aircoords(grid_list,n):

    air_coords = call_all_air(grid_list)
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

def addtreasuredetectors(grid_list,treasurecoords):

    air_list = call_all_air(grid_list)
    treasure_list = treasurecoords
    treasuredetectorcoords = [[],[]]

    for treasure in treasure_list:
        for coordinate in air_list:
            if math.sqrt(sqr(treasure[0]-coordinate[0]) + sqr(treasure[1]-coordinate[1])) <= 2 and coordinate not in treasure_list:
                treasuredetectorcoords[0].append(coordinate)
            elif math.sqrt(sqr(treasure[0]-coordinate[0]) + sqr(treasure[1]-coordinate[1])) <= 4 and coordinate not in treasure_list:
                treasuredetectorcoords[1].append(coordinate)
    
    return treasuredetectorcoords

def addportaldetectors(grid_list,portalcoords):

    air_list = call_all_air(grid_list)
    portal_list = portalcoords
    portaldetectorcoords = [[],[],[]]

    for portal in portal_list:
        for coordinate in air_list:
            if math.sqrt(sqr(portal[0]-coordinate[0]) + sqr(portal[1]-coordinate[1])) <= 2 and coordinate not in portal_list:
                portaldetectorcoords[0].append(coordinate)
            elif math.sqrt(sqr(portal[0]-coordinate[0]) + sqr(portal[1]-coordinate[1])) <= 5 and coordinate not in portal_list:
                portaldetectorcoords[1].append(coordinate)
            elif math.sqrt(sqr(portal[0]-coordinate[0]) + sqr(portal[1]-coordinate[1])) <= 9 and coordinate not in portal_list:
                portaldetectorcoords[2].append(coordinate)
    
    return portaldetectorcoords

def treasurize(grid_list,tcl,tdl,pcl,portl,portdl):

    generatedgridlist = grid_list.gridlist

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
        for i in portdl[2]:
            generatedgridlist[i[1]][i[0]] = l3pd_entity
        for i in portdl[1]:
            generatedgridlist[i[1]][i[0]] = l2pd_entity
        for i in portdl[0]:
            generatedgridlist[i[1]][i[0]] = l1pd_entity
    
    return generatedgridlist

"""-----------------------------------------------------------------------------------------"""
"""-----------------------------------------------------------------------------------------"""

# CHARACTER PRESENCE & MOVEMENT CONTROL

"""-----------------------------------------------------------------------------------------"""
"""-----------------------------------------------------------------------------------------"""
# FUNCTIONS:
    # change_charactercoords(x,y,movement_key): takes character coordinates (x,y), changes it according to the desired direction(movement_key), and returns the changed coordinates.
    # isinsideWall(x,y): Takes character coordinates (x,y) and checks if the coordinate has similar coordinates as one of the walls of the grid. Returns true if so.
    # generate_gridwithcharacter(x,y,generated_grid_list): takes character coordinates (x,y) and places the character to the grid at its respective coordinate.
    # generate_gridwithalternate(x,y,generated_grid_list): works similarly as the former, however Interactives (Entities) become visible
    # isinsideInteractive(x,y,generated_grid_list_, Interactive): Checks if the current character's position [x,y] in [generated_grid_list] is inside the [Interactive]

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
    for ind_list in range(len(generated_grid_list.gridlist)): # -- Iterate through the list of lists
        for ind_i in range(len(generated_grid_list.gridlist[ind_list])): # -- Iterate through the characters of each list
            if generated_grid_list.gridlist[ind_list][ind_i] == '■' and [ind_i,ind_list] == character_coordinates: # -- Character position determinant
                insidewallBool = True
    return insidewallBool

def generate_gridwithcharacter(x,y,generated_grid_list):
    character_coordinates = [x,y]

    for ind_list in range(len(generated_grid_list.gridlist)): # -- Represent entire line
        gridx = ''
        for ind_i in range(len(generated_grid_list.gridlist[ind_list])): # -- Represent character of each line
            if [ind_i,ind_list] == character_coordinates: # -- Character position determinant
                gridx += character.symbol
            elif type(generated_grid_list.gridlist[ind_list][ind_i]) == Entity:
                gridx += generated_grid_list.gridlist[ind_list][ind_i].symbol
            else:
                gridx += generated_grid_list.gridlist[ind_list][ind_i]
        print(gridx)

def generate_gridwithalternate(x,y,generated_grid_list):
    character_coordinates = [x,y]

    for ind_list in range(len(generated_grid_list.gridlist)): # -- Represent entire line
        gridx = ''
        for ind_i in range(len(generated_grid_list.gridlist[ind_list])): # -- Represent character of each line
            if [ind_i,ind_list] == character_coordinates: # -- Character position determinant
                gridx += character.symbol
            elif type(generated_grid_list.gridlist[ind_list][ind_i]) == Entity:
                gridx += generated_grid_list.gridlist[ind_list][ind_i].alternate
            else:
                gridx += generated_grid_list.gridlist[ind_list][ind_i]
        print(gridx)

def isinsideInteractive(x,y,generated_grid_list,Interactive): # Checks 
    character_coordinates = [x,y]
    
    insideInteractiveBool = False
    for ind_list in range(len(generated_grid_list.gridlist)): # -- Iterate through the list of lists
        for ind_i in range(len(generated_grid_list.gridlist[ind_list])): # -- Iterate through the characters of each list
            if generated_grid_list.gridlist[ind_list][ind_i] == Interactive and [ind_i,ind_list] == character_coordinates: # -- Character position determinant
                insideInteractiveBool = True
    return insideInteractiveBool


"""-----------------------------------------------------------------------------------------"""
"""-----------------------------------------------------------------------------------------"""

# GAME INITIALIZATION
# -- Where all previous functions are finally put together

"""-----------------------------------------------------------------------------------------"""
"""-----------------------------------------------------------------------------------------"""

# FUNCTIONS:
    # initgl: responsible for character presence and movement control; takes character coordinates [x,y] and starts the grid loop, only ending once a condition has been met.

def initgl(lx=55, ly=15, nopillars=25, notreasure=5,crypthealth=1000):
    
    generated_grid_list = Grid(lx,ly)

    lengthx = generated_grid_list.lengthx
    lengthy = generated_grid_list.lengthy

    character_coordinates = [int(lengthx/2)+1,lengthy+4]

    init_crypt_health = crypthealth
    crypt_health = crypthealth

    numoftreasure = notreasure
    current_treasure = 0

    message_line = ''

    treasurecoordslist = randomselect_aircoords(generated_grid_list,numoftreasure)
    treasuredetectorslist = addtreasuredetectors(generated_grid_list,treasurecoordslist)
    pillarcoordslist = randomselect_aircoords(generated_grid_list,nopillars)

    if similaritems(treasurecoordslist,pillarcoordslist):
        while similaritems(treasurecoordslist,pillarcoordslist):
            pillarcoordslist = randomselect_aircoords(generated_grid_list,nopillars)
    
    portal_coord = randomselect_aircoords(generated_grid_list,1)
    
    if similaritems(portal_coord,pillarcoordslist):
        while similaritems(portal_coord,pillarcoordslist):
                portal_coord = randomselect_aircoords(generated_grid_list,1)

    

    canportalize = False
    winbool = False
    gameoverbool = False

    while True:

        if crypt_health <= 0:

            clear()

            gameoverbool = True
            
            temp_grid_list = Grid(lengthx,lengthy)


            tcl = treasurecoordslist
            tdcl = addtreasuredetectors(temp_grid_list,treasurecoordslist)
            pcl = pillarcoordslist
            portl = portal_coord
            portdl = addportaldetectors(temp_grid_list,portal_coord)

            if canportalize:
                treasurize(temp_grid_list,tcl,tdcl,pcl,portl,portdl)
            else:
                treasurize(temp_grid_list,tcl,tdcl,pcl,None,None)

            generate_gridwithalternate(character_coordinates[0],character_coordinates[1],temp_grid_list)

            break

        clear()
        
        temp_grid_list = Grid(lengthx,lengthy)


        tcl = treasurecoordslist
        tdcl = addtreasuredetectors(temp_grid_list,treasurecoordslist)
        pcl = pillarcoordslist
        portl = portal_coord
        portdl = addportaldetectors(temp_grid_list,portal_coord)

        if canportalize:
            treasurize(temp_grid_list,tcl,tdcl,pcl,portl,portdl)
        else:
            treasurize(temp_grid_list,tcl,tdcl,pcl,None,None)

        generate_gridwithcharacter(character_coordinates[0],character_coordinates[1],temp_grid_list)

        print(message_line)
        message_line = ''

        print('Crypt health: [{x}/{y}]              ❉ Treasure: [{a}/{b}]'.format(x=crypt_health,y=init_crypt_health,a=current_treasure,b=numoftreasure))

        if identitywindows():
            char_movement = get_key('''[w/a/s/d]
    > ''')

            while char_movement == None:
                char_movement = get_key(None)

        elif not identitywindows():
            char_movement = input('''[w/a/s/d]
    > ''')

        if char_movement not in ['w','a','s','d','W','A','S','D']:
            continue

        new_character_coordinates = change_charactercoords(character_coordinates[0],character_coordinates[1],char_movement)

        # -- Place the conditions for interacting with different objects here

        turnbackvalue = False
        if isinsideWall(new_character_coordinates[0],new_character_coordinates[1],temp_grid_list): 
            # -- For if the character bumps into a wall
            message_line += 'You bumped into a wall. The crypt quivers. (-2 Crypt Health)\n'
            crypt_health -= 2
            if canportalize:
                message_line += 'Dust and debris begin to fall... (-2 Crypt Health)\n'
                crypt_health -= 2
            turnbackvalue = True
            
        if isinsideInteractive(new_character_coordinates[0],new_character_coordinates[1],temp_grid_list,pillar_entity):
            message_line += 'You bumped into a pillar. The ceiling cracks. (-10 Crypt Health)\n'
            crypt_health -= 10
            if canportalize:
                message_line += 'Dust and debris begin to fall... (-10 Crypt Health)\n'
                crypt_health -= 10
            turnbackvalue = True

        if isinsideInteractive(new_character_coordinates[0],new_character_coordinates[1],temp_grid_list,l2td_entity):
            message_line += 'You sense a treasure nearby... [Intuition 1/2]\n'
            character_coordinates = new_character_coordinates

        if isinsideInteractive(new_character_coordinates[0],new_character_coordinates[1],temp_grid_list,l1td_entity):
            message_line += 'You feel the treasure\'s presence growing stronger... [Intuition 2/2]\n'
            character_coordinates = new_character_coordinates

        if isinsideInteractive(new_character_coordinates[0],new_character_coordinates[1],temp_grid_list,treasure_entity):
            message_line += 'You found a treasure!\n'
            treasurecoordslist.remove([new_character_coordinates[0],new_character_coordinates[1]])
            character_coordinates = new_character_coordinates
            current_treasure += 1
            if current_treasure == numoftreasure:
                message_line += 'You have found all 5 treasures! As a result, a portal has opened, but the crypt\n'
                message_line += 'is now decaying rapidly. Find the portal as soon as possible to save yourself.\n'
                canportalize = True

        if isinsideInteractive(new_character_coordinates[0],new_character_coordinates[1],temp_grid_list,l3pd_entity):
            message_line += 'You feel a slight tingle in your intuition. Intuition [1/3]\n'
            character_coordinates = new_character_coordinates
        
        if isinsideInteractive(new_character_coordinates[0],new_character_coordinates[1],temp_grid_list,l2pd_entity):
            message_line += 'You sense a portal nearby... Intuition [2/3]\n'
            character_coordinates = new_character_coordinates

        if isinsideInteractive(new_character_coordinates[0],new_character_coordinates[1],temp_grid_list,l1pd_entity):
            message_line += 'You feel the portal\'s presence growing stronger... Intuition [3/3]\n'
            character_coordinates = new_character_coordinates
        
        if isinsideInteractive(new_character_coordinates[0],new_character_coordinates[1],temp_grid_list,portal_entity):

            clear()
            
            winbool = True
            
            temp_grid_list = Grid(lengthx,lengthy)


            tcl = treasurecoordslist
            tdcl = addtreasuredetectors(temp_grid_list,treasurecoordslist)
            pcl = pillarcoordslist
            portl = portal_coord
            portdl = addportaldetectors(temp_grid_list,portal_coord)

            if canportalize:
                treasurize(temp_grid_list,tcl,tdcl,pcl,portl,portdl)
            else:
                treasurize(temp_grid_list,tcl,tdcl,pcl,None,None)

            generate_gridwithalternate(character_coordinates[0],character_coordinates[1],temp_grid_list)

            break

        if turnbackvalue == True:
            turnbackvalue = False
            continue

        character_coordinates = new_character_coordinates
        
        crypt_health -= 1
        if canportalize:
            crypt_health -= 1
    

    return [winbool,gameoverbool]

"""-----------------------------------------------------------------------------------------"""
"""-----------------------------------------------------------------------------------------"""

# MAIN MENU AND DIALOGS

"""-----------------------------------------------------------------------------------------"""
"""-----------------------------------------------------------------------------------------"""

# FUNCTIONS
    # Dialog: A class for Dialogs
        # .determine_input(self): returns the id of the next dialog depending on the input given
        # .update(self): updates the dialog text of the Dialog

current_mode = 'Normal' # -- Difficulty

dialog_list = []

class Dialog:

    def __init__(self,id,desc,dialog,input,inputid,formatform='{format}'):
        self.id = id
        self.desc = desc
        self.dialog = dialog
        self.input = input
        self.inputid = inputid
        self.formatform = formatform
        dialog_list.append(self)
    
    def determine_input(self):

        response = input(self.dialog)

        while response not in self.input:
            input_list_str = '' 
            for i in self.input:
                input_list_str += '['+i+']'+'\n'
            response = input('Unknown response. Please choose one of the options: \n'+input_list_str)
        
        for i in range(len(self.input)):
            if response == self.input[i]:
                return self.inputid[i]
    
    def update(self,format=None):
        if format == None:
            self.dialog = self.formatform
        else:
            self.dialog = self.formatform.format(fm=format)

d1 = Dialog(1,  'Main Menu', '''

    _______  _______  _______  _                 ______   _______  ______                             
    (  ___  )(  ____ \(  ____ \( \      |\     /|(  __  \ (  ____ \(  __  \                            
    | (   ) || (    \/| (    \/| (      | )   ( || (  \  )| (    \/| (  \  )                           
    | |   | || |      | |      | |      | |   | || |   ) || (__    | |   ) |                           
    | |   | || |      | |      | |      | |   | || |   | ||  __)   | |   | |                           
    | |   | || |      | |      | |      | |   | || |   ) || (      | |   ) |                           
    | (___) || (____/\| (____/\| (____/\| (___) || (__/  )| (____/\| (__/  )                           
    (_______)(_______/(_______/(_______/(_______)(______/ (_______/(______/                            
                                                                                                    
                    _______  _______  _______  _______  _______ _________ _______          _________
                    (  ____ \(  ___  )(  ____ )(  ____ \(  ____ \\__   __/(  ____ \|\     /|\__   __/
                    | (    \/| (   ) || (    )|| (    \/| (    \/   ) (   | (    \/| )   ( |   ) (   
                    | (__    | |   | || (____)|| (__    | (_____    | |   | |      | (___) |   | |   
                    |  __)   | |   | ||     __)|  __)   (_____  )   | |   | | ____ |  ___  |   | |   
                    | (      | |   | || (\ (   | (            ) |   | |   | | \_  )| (   ) |   | |   
                    | )      | (___) || ) \ \__| (____/\/\____) |___) (___| (___) || )   ( |   | |   
                    |/       (_______)|/   \__/(_______/\_______)\_______/(_______)|/     \|   )_(   

    by Koriyu / woodentechno

[Play] Difficulty: Normal
[How to Play]
[Settings]
[Exit]            

> ''', ['Play','How to Play','Settings','Exit'], [2,3,10,4], '''

    _______  _______  _______  _                 ______   _______  ______                             
    (  ___  )(  ____ \(  ____ \( \      |\     /|(  __  \ (  ____ \(  __  \                            
    | (   ) || (    \/| (    \/| (      | )   ( || (  \  )| (    \/| (  \  )                           
    | |   | || |      | |      | |      | |   | || |   ) || (__    | |   ) |                           
    | |   | || |      | |      | |      | |   | || |   | ||  __)   | |   | |                           
    | |   | || |      | |      | |      | |   | || |   ) || (      | |   ) |                           
    | (___) || (____/\| (____/\| (____/\| (___) || (__/  )| (____/\| (__/  )                           
    (_______)(_______/(_______/(_______/(_______)(______/ (_______/(______/                            
                                                                                                    
                    _______  _______  _______  _______  _______ _________ _______          _________
                    (  ____ \(  ___  )(  ____ )(  ____ \(  ____ \\__   __/(  ____ \|\     /|\__   __/
                    | (    \/| (   ) || (    )|| (    \/| (    \/   ) (   | (    \/| )   ( |   ) (   
                    | (__    | |   | || (____)|| (__    | (_____    | |   | |      | (___) |   | |   
                    |  __)   | |   | ||     __)|  __)   (_____  )   | |   | | ____ |  ___  |   | |   
                    | (      | |   | || (\ (   | (            ) |   | |   | | \_  )| (   ) |   | |   
                    | )      | (___) || ) \ \__| (____/\/\____) |___) (___| (___) || )   ( |   | |   
                    |/       (_______)|/   \__/(_______/\_______)\_______/(_______)|/     \|   )_(   

    by Koriyu / woodentechno

[Play] Difficulty: {fm}
[How to Play]
[Settings]
[Exit]            

> ''')

d3 = Dialog(3, 'How to Play 1', '''

    [1/6]


    WELCOME TO OCCLUDED FORESIGHT!

    Occluded Foresight is a terminal-based adventure game in which you
    navigate through a dark and crumbling crypt where hidden treasures
    and unforeseeable dangers lie within. You must collect all of the
    treasures before the crypt collapses.
    
    This game was created as my 'Python Terminal Game' portfolio
    project from Codecademy. Also made with love and passion :3

    Hope you enjoy!

            
    1/6 [Next]

    [Main Menu]

> ''', ['Next', 'Main Menu'], [5,1])

d4 = Dialog(4, 'Exit Game', '''

Do you want to exit the game?

[Yes]
[No]

> ''', ['Yes','No'], [0,1])

d5 = Dialog(5, 'How to Play 2', '''

    [2/6]

            
    YOUR HERO AGAINST THE CRYPT
            
    Starting the game, you will notice a grid made up of a large 15 by
    15 space and a little chamber underneath.
    
    ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
    ■◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦■
    ■◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦■
    ■◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦■
    ■◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦■
    ■◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦■
    ■◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦■
    ■◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦■
    ■◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦■
    ■◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦■
    ■◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦■
    ■◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦■
    ■◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦■
    ■◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦■
    ■◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦■
    ■◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦■
    ■■■■■■■■■■■■■■■■■■■■■■■■■■■◦◦◦■■■■■■■■■■■■■■■■■■■■■■■■■■■
    ■■■■■■■■■■■■■■■■■■■■■■■■■■■◦◦◦■■■■■■■■■■■■■■■■■■■■■■■■■■■
    ■■■■■■■■■■■■■■■■■■■■■■■■■■◦◦◦◦◦■■■■■■■■■■■■■■■■■■■■■■■■■■
    ■■■■■■■■■■■■■■■■■■■■■■■■■■◦◦♜◦◦■■■■■■■■■■■■■■■■■■■■■■■■■■
    ■■■■■■■■■■■■■■■■■■■■■■■■■■◦◦◦◦◦■■■■■■■■■■■■■■■■■■■■■■■■■■
    ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
    
    This entire grid is known as the crypt. Inside the 15 by 15 grid
    space lies 5 treasures and multiple obstructions scattered across.

    Your character is depicted as a chess rook piece (♜) located at
    the bottom center of the grid. Your character is movable through
    WASD movement (W for up, A for left, S for down, and D for right,
    not case-sensitive). Just make sure to press the [Enter] key     
    for every move though.

            
    [Previous] 2/6 [Next]

    [Main Menu]

> ''', ['Previous', 'Next', 'Main Menu'], [3,6,1], '''

    [2/6]

            
    YOUR HERO AGAINST THE CRYPT
            
    Starting the game, you will notice a grid made up of a large 15 by
    15 space and a little chamber underneath.
    
    ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
    ■◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦■
    ■◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦■
    ■◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦■
    ■◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦■
    ■◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦■
    ■◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦■
    ■◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦■
    ■◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦■
    ■◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦■
    ■◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦■
    ■◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦■
    ■◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦■
    ■◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦■
    ■◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦■
    ■◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦■
    ■■■■■■■■■■■■■■■■■■■■■■■■■■■◦◦◦■■■■■■■■■■■■■■■■■■■■■■■■■■■
    ■■■■■■■■■■■■■■■■■■■■■■■■■■■◦◦◦■■■■■■■■■■■■■■■■■■■■■■■■■■■
    ■■■■■■■■■■■■■■■■■■■■■■■■■■◦◦◦◦◦■■■■■■■■■■■■■■■■■■■■■■■■■■
    ■■■■■■■■■■■■■■■■■■■■■■■■■■◦◦♜◦◦■■■■■■■■■■■■■■■■■■■■■■■■■■
    ■■■■■■■■■■■■■■■■■■■■■■■■■■◦◦◦◦◦■■■■■■■■■■■■■■■■■■■■■■■■■■
    ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
    
    This entire grid is known as the crypt. Inside the 15 by 15 grid
    space lies 5 treasures and multiple obstructions scattered across.

    Your character is depicted as a chess rook piece (♜) located at
    the bottom center of the grid. Your character is movable through
    WASD movement (W for up, A for left, S for down, and D for right).

            
    [Previous] 2/6 [Next]

    [Main Menu]

> ''')

d6 = Dialog(6, 'How to Play 3', '''

    [3/6]
            

    CRYPT HEALTH
            
    Located at the left-hand side below the grid itself is a stat
    called [Crypt Health]. This refers to the integrity of the weak
    crypt. You start with 1000 [Crypt Health]. Once the [Crypt 
    Health] becomes 0, the entire crypt will fall, resulting in your
    demise.
    
    There are several factors that reduce [Crypt Health]:
        - Your steps
            Every step or movement your character makes reduces
            the [Crypt Health] by 1 point.
        - Bumping into a Wall (■)
            Walls are objects that surround the grid to prevent
            the character from going out. Bumping into a Wall 
            reduces the [Crypt Health] by 2 points.
        - Bumping into a Pillar (▥): 
            Ah yes, the main antagonists of the game: Pillars.
            Pillars are numerously scattered across the crypt.
            Since the pillars are the only source of integrity
            for this crypt, bumping into a Pillar reduces the
            [Crypt Health] by 10 points.

            
    [Previous] 3/6 [Next]

    [Main Menu]

> ''', ['Previous', 'Next', 'Main Menu'], [5,7,1])

d7 = Dialog(7,  'How to Play 4', '''

    [4/6]
    
    
    TREASURES AND PORTALS
    
    ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
    ■◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦■
    ■◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦▥◦◦◦◦◦◦◦◦◦◦◦◦◦◦▥◦◦◦❉◦◦◦◦◦◦◦◦◦■
    ■◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦■
    ■◦◦◦◦◦◦▥◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦■
    ■◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦■
    ■◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦▥◦◦◦◦◦◦◦◦◦◦▥◦◦◦◦■
    ■◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦❉◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦■
    ■◦◦◦◦◦◦◦◦▥◦◦◦◦◦◦◦◦◦◦◦◦◦▥◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦■
    ■◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦■
    ■◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦❉◦◦◦◦◦◦◦◦◦❉◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦■
    ■◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦▥◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦▥◦◦▥◦◦◦◦◦◦◦◦◦◦■
    ■◦◦◦◦◦◦◦❉◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦■
    ■◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦▥◦◦◦◦◦◦▥◦◦◦◦◦◦▥◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦■
    ■◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦■
    ■◦◦◦◦◦◦◦◦◦◦◦▥◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦▥◦◦◦◦■
    ■■■■■■■■■■■■■■■■■■■■■■■■■■■◦◦◦■■■■■■■■■■■■■■■■■■■■■■■■■■■
    ■■■■■■■■■■■■■■■■■■■■■■■■■■■◦◦◦■■■■■■■■■■■■■■■■■■■■■■■■■■■
    ■■■■■■■■■■■■■■■■■■■■■■■■■■◦◦◦◦◦■■■■■■■■■■■■■■■■■■■■■■■■■■
    ■■■■■■■■■■■■■■■■■■■■■■■■■■◦◦♜◦◦■■■■■■■■■■■■■■■■■■■■■■■■■■
    ■■■■■■■■■■■■■■■■■■■■■■■■■■◦◦◦◦◦■■■■■■■■■■■■■■■■■■■■■■■■■■
    ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
    
    As stated previously, collecting treasures is the main goal of
    the game. There are 5 treasures inside the crypt, and once all
    of the treasures are found, a portal to the exit will open.
    However, traversing through the crypt will be harder now.
    Each reduction to the crypt health will then be multiplied by
    two. This means that once you have collected all treasures, each 
    step you take costs the crypt health 2 points, and each pillar
    you bump into costs 20 points. In general, it's gonna be tough.
    
    But how will we find treasures and portals, you may ask? Well,
    let's move on to the next page.
    
            
    [Previous] 4/6 [Next]

    [Main Menu]

> ''', ['Previous', 'Next', 'Main Menu'], [6,8,1])

d8 = Dialog(8, 'How to Play 5', '''

    [5/6]
    
    
    THE INTUITION SYSTEM
    
    The [Intuition System] is another core part of the game. It allows
    you to be able to locate nearby treasure and portals. Intuition is
    depicted in number fractions. The greater the intuition, the nearer
    you are to said treasure/portal.
            
    Here are some examples of intuition messages:
    
    ''You sense a treasure nearby... [Intuition 1/2]''
    ''You feel the portal\'s presence growing stronger... Intuition [3/3]''
    
    Intuition messages pop up below the entirety of the grid:
    
    ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
    ■◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦■
    ■◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦▥◦◦◦◦◦◦◦◦◦◦◦◦◦◦▥◦◦◦❉◦◦◦◦◦◦◦◦◦■
    ■◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦■
    ■◦◦◦◦◦◦▥◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦■
    ■◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦■
    ■◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦▥◦◦◦◦◦◦◦◦◦◦▥◦◦◦◦■
    ■◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦❉◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦■
    ■◦◦◦◦◦◦◦◦▥◦◦◦◦◦◦◦◦◦◦◦◦◦▥◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦■
    ■◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦■
    ■◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦❉◦◦◦◦◦◦◦◦◦❉◦♜◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦■
    ■◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦▥◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦▥◦◦▥◦◦◦◦◦◦◦◦◦◦■
    ■◦◦◦◦◦◦◦❉◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦■
    ■◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦▥◦◦◦◦◦◦▥◦◦◦◦◦◦▥◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦■
    ■◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦■
    ■◦◦◦◦◦◦◦◦◦◦◦▥◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦▥◦◦◦◦■
    ■■■■■■■■■■■■■■■■■■■■■■■■■■■◦◦◦■■■■■■■■■■■■■■■■■■■■■■■■■■■
    ■■■■■■■■■■■■■■■■■■■■■■■■■■■◦◦◦■■■■■■■■■■■■■■■■■■■■■■■■■■■
    ■■■■■■■■■■■■■■■■■■■■■■■■■■◦◦◦◦◦■■■■■■■■■■■■■■■■■■■■■■■■■■
    ■■■■■■■■■■■■■■■■■■■■■■■■■■◦◦◦◦◦■■■■■■■■■■■■■■■■■■■■■■■■■■
    ■■■■■■■■■■■■■■■■■■■■■■■■■■◦◦◦◦◦■■■■■■■■■■■■■■■■■■■■■■■■■■
    ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
    You feel the treasure\'s presence growing stronger... Intuition [2/2] <-- Over here
    
    Oddly enough, your character doesn't have the intuition to detect
    nearby pillars D:

            
    [Previous] 5/6 [Next]

    [Main Menu]

> ''', ['Previous', 'Next', 'Main Menu'], [7,9,1])

d9 = Dialog(9, 'How to Play 6', '''

    [6/6]
    
            
    With that, you now know the basics of playing the game! You are
    now ready for the threats that lie ahead.
    
    ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
    ■◦◦◦◦◦◦◦◦◦◦◦◦◦0000ooo..♨♜.ooo0000▥◦◦◦◦◦◦◦◦◦◦◦◦◦▥◦◦◦◦◦◦◦◦■
    ■◦◦◦◦◦◦◦◦◦◦◦◦◦◦0000ooo...ooo0000◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦■
    ■◦◦◦◦◦◦◦◦◦◦◦◦◦◦0000oooo.oooo0000◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦■
    ■▥◦◦◦◦◦◦◦◦▥◦◦◦◦0000ooooooooo0000◦◦◦◦◦◦◦◦◦◦◦▥◦▥◦◦◦◦◦▥◦◦◦◦■
    ■◦◦◦◦◦◦◦◦◦◦◦◦◦◦00000ooooooo00000◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦■
    ■◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦0000000o0000000◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦■
    ■◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦0000000000000◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦■
    ■◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦00000000000◦◦▥◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦■
    ■◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦000000000◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦■
    ■◦◦◦◦▥◦◦◦◦◦◦◦◦◦▥◦◦◦◦◦◦◦0◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦■
    ■◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦■
    ■▥◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦▥◦◦◦◦◦◦◦◦◦◦◦◦◦◦▥◦◦◦◦■
    ■◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦■
    ■◦◦◦◦▥◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦■
    ■◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦■
    ■■■■■■■■■■■■■■■■■■■■■■■■■■■◦◦◦■■■■■■■■■■■■■■■■■■■■■■■■■■■
    ■■■■■■■■■■■■■■■■■■■■■■■■■■■◦◦◦■■■■■■■■■■■■■■■■■■■■■■■■■■■
    ■■■■■■■■■■■■■■■■■■■■■■■■■■◦◦◦◦◦■■■■■■■■■■■■■■■■■■■■■■■■■■
    ■■■■■■■■■■■■■■■■■■■■■■■■■■◦◦◦◦◦■■■■■■■■■■■■■■■■■■■■■■■■■■
    ■■■■■■■■■■■■■■■■■■■■■■■■■■◦◦◦◦◦■■■■■■■■■■■■■■■■■■■■■■■■■■
    ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

            
    [Previous] 6/6

    [Main Menu]

> ''', ['Previous', 'Main Menu'], [8,1])

d10 = Dialog(10, 'Settings', '''

    SETTINGS:
                
    [Set Difficulty]
    Current difficulty: Normal

    [Main Menu]
    
> ''', ['Set Difficulty', 'Main Menu'], [11,1], '''

    SETTINGS:
                
    [Set Difficulty]
    Current difficulty: {fm}

    [Main Menu]
    
> ''')

d11 = Dialog(11, 'Settings', '''

    SETTINGS:
                
    Set difficulty to:
    
    [Baby] [Easy] [Normal] [Hard] [Impossible]
        
    Your current difficulty: Normal
    Default difficulty: Normal
    
    [Main Menu]
    
> ''', ['Baby', 'Easy', 'Normal', 'Hard', 'Impossible' , 'Main Menu'], [12,13,14,15,16,1], '''

    SETTINGS:
                
    Set difficulty to:
    
    [Baby] [Easy] [Normal] [Hard] [Impossible]
        
    Your current difficulty: {fm}
    Default difficulty: Normal
    
    [Main Menu]
    
> ''')

d12 = Dialog(12, 'Settings', '''

    SETTINGS:
                
    Would you like to set difficulty to [Baby]?
    
    [Yes] [No]
    
> ''', ['Yes', 'No'], [17, 11])

d13 = Dialog(13, 'Settings', '''

    SETTINGS:
                
    Would you like to set difficulty to [Easy]?
    
    [Yes] [No]
    
> ''', ['Yes', 'No'], [18, 11])

d14 = Dialog(14, 'Settings', '''

    SETTINGS:
                
    Would you like to set difficulty to [Normal]?
    
    [Yes] [No]
    
> ''', ['Yes', 'No'], [19, 11])

d15 = Dialog(15, 'Settings', '''

    SETTINGS:
                
    Would you like to set difficulty to [Hard]?
    
    [Yes] [No]
    
> ''', ['Yes', 'No'], [20, 11])

d16 = Dialog(16, 'Settings', '''

    SETTINGS:
                
    Would you like to set difficulty to [Impossible]?
    
    [Yes] [No]
    
> ''', ['Yes', 'No'], [21, 11])

d2000 = Dialog(2000, 'You win/You lost', '[Yes] [Back to Main Menu]', ['Yes','Back to Main Menu'], [2,1])

# --- Code below interprets which dialog comes next to be called upon

dialogvalue = 1

while dialogvalue != 0:

    for i in dialog_list:
        if i.formatform != '{format}':
            i.update(current_mode)

    clear()
        
    for i in dialog_list:
        if dialogvalue == i.id:
            dialogvalue = i.determine_input()
            break
    
    if dialogvalue == 2:

        if current_mode == 'Baby':
            gat = initgl(15, 7, 0, 1, 100000)

        elif current_mode == 'Easy':
            gat = initgl(35, 15, 5, 3, 1500)

        elif current_mode == 'Normal':
            gat = initgl()

        elif current_mode == 'Hard':
            gat = initgl(105, 15, 75, 7, 750)

        elif current_mode == 'Impossible':
            gat = initgl(155, 19, 150, 10, 500)

        if gat[0]:
            print('You watch the entire crypt crumble before your eyes as you fall through the portal. [WIN]')
            print('Would you like to move forth to another dungeon or call it a day?')
        elif gat[1]:
            print('The crypt shakes, its entire integrity into shambles. The ceiling crushes you in an instant. [GAME OVER]')
            print('Would you like to try again?')
        dialogvalue = d2000.determine_input()
        continue
            
    elif dialogvalue == 17:
        current_mode = 'Baby'
        dialogvalue = 1
        continue

    elif dialogvalue == 18:
        current_mode = 'Easy'
        dialogvalue = 1
        continue

    elif dialogvalue == 19:
        current_mode = 'Normal'
        dialogvalue = 1
        continue

    elif dialogvalue == 20:
        current_mode = 'Hard'
        dialogvalue = 1
        continue

    elif dialogvalue == 21:
        current_mode = 'Impossible'
        dialogvalue = 1
        continue