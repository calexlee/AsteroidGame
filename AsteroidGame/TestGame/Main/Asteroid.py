'''
Created on May 22, 2019
TODO: Implement GJK Algorithm as a potential physics solution
@author: Alex
'''
import random 
import arcade


def createAsteroid(self, onEdge, asteroid_list, numOfAsteroids, SCREEN_HEIGHT, SCREEN_WIDTH,
                   SPRITE_MAX_SCALING_ASTEROID, MAX_ASTEROID_SPEED):
    ''' Creates a new asteroid and adds it to the asteroid list '''
    # Asteroid Instance
    asteroid_size = SPRITE_MAX_SCALING_ASTEROID
    asteroid = arcade.Sprite("Resources/asteroid.png", asteroid_size)
    asteroid.append_texture(arcade.load_texture("Resources/asteroid_light_dmg.png"))
    asteroid.append_texture(arcade.load_texture("Resources/asteroid_med_dmg.png"))
    asteroid.append_texture(arcade.load_texture("Resources/asteroid_heavy_dmg.png"))
                
    # Asteroid Qualities
    asteroid.health = 5*asteroid_size
                
    # Placement
    if onEdge is True: 
        while True: # Ensures asteroid not on player
            if random.randint(1,2) == 1:
                asteroid.center_x = random.randrange(SCREEN_WIDTH)
                if random.randint(1,2) == 1:
                    asteroid.center_y = SCREEN_HEIGHT-1
                else:
                    asteroid.center_y = 1
            else: 
                asteroid.center_y = random.randrange(SCREEN_HEIGHT)
                if random.randint(1,2) == 1:
                    asteroid.center_x = SCREEN_WIDTH - 1
                else:
                    asteroid.center_x = 1
            
            if not isIn(asteroid, asteroid_list):
                break
    else:
        while True: # Ensures asteroid not on player
                asteroid.center_x = random.randrange(SCREEN_WIDTH)
                asteroid.center_y = random.randrange(SCREEN_HEIGHT)
                
                if (asteroid.center_x < 350 or asteroid.center_x > 450 \
                or asteroid.center_y < 250 or asteroid.center_y > 350) \
                and not isIn(asteroid, asteroid_list):
                    break
    
    # Initial direction
    asteroid.change_x = 1 + random.randrange(MAX_ASTEROID_SPEED)
    asteroid.change_y = 1 + random.randrange(MAX_ASTEROID_SPEED)
    if random.randint(1,2) == 1:
        asteroid.change_y = -asteroid.change_y
    if random.randint(1,2) == 1:
        asteroid.change_x = -asteroid.change_x
                
    # Adding to List
    asteroid_list.append(asteroid)
    numOfAsteroids = numOfAsteroids + 1
    
    return asteroid_list, numOfAsteroids

def createMiniAsteroid(self, asteroid_list, x, y, SPRITE_MAX_SCALING_ASTEROID, MAX_ASTEROID_SPEED):
    ''' Creates a small asteroid in place of the older large asteroid'''
    # Asteroid Instance
    asteroid_size = SPRITE_MAX_SCALING_ASTEROID/2
    asteroid = arcade.Sprite("Resources/asteroid.png", asteroid_size)
    asteroid.append_texture(arcade.load_texture("Resources/asteroid_light_dmg.png"))
    asteroid.append_texture(arcade.load_texture("Resources/asteroid_med_dmg.png"))
    asteroid.append_texture(arcade.load_texture("Resources/asteroid_heavy_dmg.png"))
    
    # Asteroid Qualities
    asteroid.health = 5*asteroid_size
    
    # Placement
    asteroid.center_x = x
    asteroid.center_y = y
    
    # Initial direction
    asteroid.change_x = 1 + random.randrange(MAX_ASTEROID_SPEED)
    asteroid.change_y = 1 + random.randrange(MAX_ASTEROID_SPEED)
    if random.randint(1,2) == 1:
        asteroid.change_y = -asteroid.change_y
    if random.randint(1,2) == 1:
        asteroid.change_x = -asteroid.change_x
                
    # Adding to List
    asteroid_list.append(asteroid)
    
    return asteroid_list

def physics(asteroid,asteroid2):
    ''' Function which determines how asteroid collisions should be handled
        TODO: Make the movement make actual sense '''       

    asteroid.change_x = -asteroid.change_x*(1 +random.randrange(1))
    asteroid.change_y = -asteroid.change_y*(1 +random.randrange(1))
    asteroid2.change_x = -asteroid.change_x*(1 +random.randrange(1))
    asteroid2.change_y = -asteroid.change_y*(1 +random.randrange(1))
   
def isIn(asteroid,asteroid_list):
    '''Determines if an asteroid is inside the radius of another asteroid in the list'''
    for asteroid2 in asteroid_list:
        if asteroid.center_x + asteroid.collision_radius > asteroid2.center_x - asteroid2.collision_radius and \
        asteroid.center_x - asteroid.collision_radius < asteroid2.center_x + asteroid2.collision_radius and \
        asteroid.center_y + asteroid.collision_radius > asteroid2.center_y - asteroid2.collision_radius and \
        asteroid.center_y - asteroid.collision_radius < asteroid2.center_y + asteroid2.collision_radius and asteroid2 != asteroid:
            return True
    return False
        
def unstick():
    '''If Needed create a function that pushes apart asteroids that become stuck together'''
    
    pass