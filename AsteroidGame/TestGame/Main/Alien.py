'''
Created on Jul 15, 2019

TODO: make aliens more interesting

@author: Alex
'''

import random 
import arcade

def createAlien(self, alien_list, numOfAliens, alienType, screen_height, screen_width):
    
    ''' Creates a new alien and adds it to the alien list'''
    
    alien_size = 1
    
    if alienType <= 3:
        alien = arcade.Sprite("Resources/alien_standard.png", alien_size)
        alien.type = alienType
    elif alienType == 4:
        alien = arcade.Sprite("Resources/alien_standard.png", 2*alien_size)
        alien.type = alienType
    # Alien Qualities
    alien.health = 2*alien_size
    alien.timer = 0
                
    # Placement
    spawn = random.randint(1,4)
    
    if spawn == 1:
        alien.center_x = 10
        alien.center_y = screen_height - 1
    elif spawn == 2:
        alien.center_x = screen_width-10
        alien.center_y = screen_height - 1
    elif spawn == 3:
        alien.center_x = screen_width/2
        alien.center_y = screen_height - 1
    
    # Movement Pattern
    if alien.type == 1:
        if random.randint(1,2) == 1:
            alien.change_x = 3
        else: 
            alien.change_x = -3
        alien.change_y = -0.5
    
    if alien.type == 2:
        if random.randint(1,2) == 1:
            alien.change_x = 1
        else: 
            alien.change_x = -1
        alien.change_y = -0.5
    
    if alien.type == 3:
        if random.randint(1,2) == 1:
            alien.change_x = 2
        else: 
            alien.change_x = -2
        alien.change_y = -0.25
        
    if alien.type == 4:
        if random.randint(1,2) == 1:
            alien.change_x = 0.5
        else: 
            alien.change_x = -0.5
        alien.change_y = -0.1
                
    # Adding to List
    alien_list.append(alien)
    numOfAliens = numOfAliens + 1
    
    return alien_list, numOfAliens

def createBoss(self,boss_list,screen_height,screen_width):
    ''' Creates a boss alien '''
    
    boss_size = 5
    boss = arcade.Sprite("Resources/boss.png",boss_size)
    boss.health = 400
    boss.beamTimer = 1000
    boss.beamActive = False
    boss.shootTimer = 50
    
    boss.center_x = screen_width/2
    boss.center_y = screen_height - 80
    
    boss.change_x = 0
    boss.change_y = 0
    
    boss.height = boss.height/1.5
    boss.width = boss.width*1.5
    
    boss_list.append(boss)
    
    return boss_list
    