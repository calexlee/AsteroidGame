'''
Created on Jul 15, 2019

TODO: implement the alien object

@author: Alex
'''

import random 
import arcade

def createAlien(self, alien_list, numOfAliens, SCREEN_HEIGHT, SCREEN_WIDTH):
    
    ''' Creates a new alien and adds it to the alien list'''
    alien_size = 1
    alien = arcade.Sprite("Resources/alien_standard.png", alien_size)
    
    # Asteroid Qualities
    alien.health = 2*alien_size
                
    # Placement
    alien.center_x = 10
    alien.center_y = SCREEN_HEIGHT-1
    
    # Movement Pattern
    alien.change_x = 3
    alien.change_y = -0.5
                
    # Adding to List
    alien_list.append(alien)
    numOfAliens = numOfAliens + 1
    
    return alien_list, numOfAliens
    