'''
Created on Aug 8, 2019

TODO: implement powerup object

@author: Alex
'''

import random 
import arcade


def createPowerUp(self, powerup_list, powType, SCREEN_HEIGHT, SCREEN_WIDTH):
    ''' Creates a new powerup and adds it to the list (game)
        TODO: More powerups!'''
    
    pow_size = 0.75
    
    # Determines type of powerup
    powType = random.randint(1,2)
    
    if powType == 1:
        powerUp = arcade.Sprite("Resources/powerup-laser.png",pow_size)
        powerUp.type = 1
    elif powType == 2:
        powerUp = arcade.Sprite("Resources/powerup-bb.png",pow_size)
        powerUp.type = 2
    
    
    # Placement
    powerUp.center_x = random.randint(10,SCREEN_WIDTH-10)
    powerUp.center_y = random.randint(10,SCREEN_HEIGHT-10)
    
    # Adding to List
    powerup_list.append(powerUp)
    
    
    return powerup_list