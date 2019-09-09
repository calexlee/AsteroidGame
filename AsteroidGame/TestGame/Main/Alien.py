'''
Created on Jul 15, 2019

TODO: make aliens more interesting

@author: Alex
'''

import random 
import arcade

def createAlien(self, alien_list, numOfAliens, alienType, SCREEN_HEIGHT, SCREEN_WIDTH):
    
    ''' Creates a new alien and adds it to the alien list'''
    alien_size = 1
    
    if alienType <= 3:
        alien = arcade.Sprite("Resources/alien_standard.png", alien_size)
        alien.type = alienType
    
    # Asteroid Qualities
    alien.health = 2*alien_size
                
    # Placement
    alien.center_x = 10
    alien.center_y = SCREEN_HEIGHT-1
    
    # Movement Pattern
    if alien.type == 1:
        alien.change_x = 3
        alien.change_y = -0.5
    
    if alien.type == 2:
        alien.change_x = 1
        alien.change_y = -0.5
    
    if alien.type == 3:
        alien.change_y = -0.25
        alien.change_x = 2
        
                
    # Adding to List
    alien_list.append(alien)
    numOfAliens = numOfAliens + 1
    
    return alien_list, numOfAliens
    