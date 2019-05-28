'''
Created on May 22, 2019

@author: Alex
'''
import random 

def physics(asteroid,asteroid2):
    ''' Function which determines how asteroid collisions should be handled '''     
    # General "Head on Deflection"
    asteroid.change_x = -asteroid.change_x*(1 +random.randrange(1))
    asteroid.change_y = -asteroid.change_y*(1 +random.randrange(1))
    asteroid2.change_x = -asteroid.change_x*(1 +random.randrange(1))
    asteroid2.change_y = -asteroid.change_y*(1 +random.randrange(1))
    # Random Variety
    if asteroid.center_x + asteroid.collision_radius < asteroid2.center_x - asteroid2.collision_radius:
        if random.randint(1,2) == 2:
            asteroid.change_y = -asteroid.change_y
    if asteroid.center_x - asteroid.collision_radius > asteroid2.center_x + asteroid2.collision_radius:
        if random.randint(1,2) == 2:
            asteroid.change_y = -asteroid.change_y
    if asteroid.center_y + asteroid.collision_radius < asteroid2.center_x - asteroid2.collision_radius:
        if random.randint(1,2) == 2:
            asteroid.change_x = -asteroid.change_x
    if asteroid.center_y - asteroid.collision_radius > asteroid2.center_x + asteroid2.collision_radius:
        if random.randint(1,2) == 2:
            asteroid.change_x = -asteroid.change_x
            
def isIn(asteroid,asteroid_list):
    '''Determines in an asteroid is inside the radius of another asteroid in the list'''
    for asteroid2 in asteroid_list:
        if asteroid.center_x + asteroid.collision_radius > asteroid2.center_x - asteroid2.collision_radius and \
        asteroid.center_x - asteroid.collision_radius < asteroid2.center_x + asteroid2.collision_radius and \
        asteroid.center_y + asteroid.collision_radius > asteroid2.center_y - asteroid2.collision_radius and \
        asteroid.center_y - asteroid.collision_radius < asteroid2.center_y + asteroid2.collision_radius:
            return True
    return False

def isIn2(asteroid,asteroid_list):
    '''Determines in an asteroid is inside the radius of another asteroid in the list,
    and returns the asteroid that it is stuck inside'''
    for asteroid2 in asteroid_list:
        if asteroid.center_x + asteroid.collision_radius > asteroid2.center_x - asteroid2.collision_radius and \
        asteroid.center_x - asteroid.collision_radius < asteroid2.center_x + asteroid2.collision_radius and \
        asteroid.center_y + asteroid.collision_radius > asteroid2.center_y - asteroid2.collision_radius and \
        asteroid.center_y - asteroid.collision_radius < asteroid2.center_y + asteroid2.collision_radius:
            return asteroid2
    return False
        
def unstick(asteroid, ):
    '''If Needed create a function that pushes apart asteroids that become stuck together'''
    pass