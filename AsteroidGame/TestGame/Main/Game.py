'''
Created on May 21, 2019

@author: Alex
'''

import random
import arcade 
import Main.Asteroid
import Main.Alien



SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SPRITE_SCALING_PLAYER = 1.25
MOVEMENT_SPEED = 5
PLAYER_FLOAT = 0.1
START_ASTEROID = 4
SPRITE_MAX_SCALING_ASTEROID = 2
MAX_ASTEROID_SPEED = 1
SPRITE_SCALING_BOLT = 0.25
BOLT_SPEED = 7



class MyGame(arcade.Window):
    """ Main application class."""

    def __init__(self, width, height):
        super().__init__(width, height)

        arcade.set_background_color(arcade.color.EERIE_BLACK)

    def setup(self):
        """ Game Setup and Variable Initialization 
        TODO: Create more enemies and perhaps a menu screen beforehand"""
        
        # Create the initial object lists
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.asteroid_list = arcade.SpriteList()
        self.bolt_list = arcade.SpriteList()
        self.alien_list = arcade.SpriteList()
        
        # Initial lives, Score and More
        self.lives = 3
        self.score = 0
        self.numOfAsteroids = 0
        self.numOfAliens = 0
        
        # Sets up the player in the center
        self.player_sprite = arcade.Sprite("Resources/spaceship.png", SPRITE_SCALING_PLAYER)
        self.player_sprite.append_texture(arcade.load_texture("Resources/explosion.png"))
        self.player_sprite.center_x = 400
        self.player_sprite.center_y = 300
        self.player_sprite.movable = True
        self.player_list.append(self.player_sprite)
        
        for i in range(START_ASTEROID):
            self.asteroid_list,self.numOfAsteroids = Main.Asteroid.createAsteroid(MyGame,False, self.asteroid_list,
                self.numOfAsteroids, SCREEN_HEIGHT, SCREEN_WIDTH, SPRITE_MAX_SCALING_ASTEROID, MAX_ASTEROID_SPEED)
            
        # Physics
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.wall_list)

    def on_draw(self):
        """ Render the screen. 
        TODO: Special effects for bolt & asteroid destruction"""
        
        arcade.start_render()
        # Drawing of Moving Objects
        self.player_list.draw()
        self.asteroid_list.draw()
        self.bolt_list.draw()
        self.alien_list.draw()
        
        # Drawing of still objects
        start_x = 10
        start_y = 580
        arcade.draw_text(f"Score: {self.score}", start_x, start_y, arcade.color.WHITE)
        start_x = 10
        start_y = 565
        arcade.draw_text(f"Lives: {self.lives}",start_x,start_y, arcade.color.WHITE)
        
        # GAME OVER text
        if self.lives < 1:
            start_x = 300
            start_y = 300
            arcade.draw_text("GAME OVER",start_x, start_y, arcade.color.WHITE, 60, 1000)

    def update(self, delta_time):
        """ All the logic to move, and the game logic goes here. 
        TODO: Fix minor bugs, have ship explode each life"""
        
        # Collision Checking for Asteroid and Player, and bolt and player
        hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.asteroid_list)
        bolt_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.bolt_list)
        if hit_list or bolt_hit_list:
            if self.lives > 1:
                self.player_sprite.center_x = 400
                self.player_sprite.center_y = 300
                self.lives = self.lives - 1
                self.score = self.score - 100
            else:
                self.lives = self.lives - 1 
                self.player_sprite.set_texture(1)
                self.player_sprite.movable = False
                self.player_sprite.stop()

        # Creation of Aliens (ultimately want to put on a timer)
        spawn = random.randint(1,100)
        
        if spawn == 1:
            self.alien_list, self.numOfAliens = Main.Alien.createAlien(MyGame, self.alien_list, self.numOfAliens, SCREEN_HEIGHT, SCREEN_WIDTH)
        
        # Alien Movement
        for alien in self.alien_list:
            alien.center_x = alien.center_x + alien.change_x
            alien.center_y = alien.center_y + alien.change_y
            # Aliens collide with asteroid
            alien_hit_list = arcade.check_for_collision_with_list(alien, self.asteroid_list)
            if alien_hit_list:
                #TODO: Add result of alien death
                alien.kill()
            
            # Alien shooting
            degreeOfSpace = 3
            if alien.center_x < self.player_sprite.center_x + degreeOfSpace and alien.center_x > self.player_sprite.center_x - degreeOfSpace and alien.center_y > self.player_sprite.center_y:
                bolt = arcade.Sprite("Resources/bolt.png", SPRITE_SCALING_BOLT) # change to alien bolt
                bolt.center_x = alien.center_x 
                bolt.center_y = alien.center_y - 20
                bolt.change_x = 3
                bolt.change_y = -BOLT_SPEED*.5
                self.bolt_list.append(bolt)
            
            # Off Screen
            if alien.center_x > SCREEN_WIDTH:
                alien.center_x = 1
            
            if alien.center_x < 0:
                alien.center_x = SCREEN_WIDTH - 1
            
            if alien.center_y > SCREEN_HEIGHT:
                alien.kill()
                
            if alien.center_y < 0:
                alien.kill()
        
        # Asteroid Movement
        for asteroid in self.asteroid_list:
            asteroid.center_x = asteroid.center_x + asteroid.change_x
            asteroid.center_y = asteroid.center_y + asteroid.change_y
            asteroid_hit_list = arcade.check_for_collision_with_list(asteroid,self.asteroid_list)
                
            # Collision between asteroid physics
            for asteroid2 in asteroid_hit_list:
                if asteroid2 != asteroid:
                    Main.Asteroid.physics(asteroid,asteroid2)
                    
            # Off Screen 
            if asteroid.center_x > SCREEN_WIDTH:
                asteroid.center_x = 1
                
            if asteroid.center_x < 0: 
                asteroid.center_x = SCREEN_WIDTH - 1
            
            if asteroid.center_y > SCREEN_HEIGHT:
                asteroid.center_y = 1
                
            if asteroid.center_y < 0:
                asteroid.center_y = SCREEN_HEIGHT - 1
                
        # Bolt Movement
        for bolt in self.bolt_list:
            bolt.center_x = bolt.center_x + bolt.change_x
            bolt.center_y = bolt.center_y + bolt.change_y
            
            # Collision with alien
            bolt_hit_list = arcade.check_for_collision_with_list(bolt,self.alien_list)
            for alien_hit in bolt_hit_list:
                alien_hit.kill()
                bolt.kill()
                self.numOfAliens = self.numOfAliens - 1
                self.score = self.score + 50
            
            # Collision with asteroid
            bolt_hit_list = arcade.check_for_collision_with_list(bolt,self.asteroid_list)
            for asteroid_hit in bolt_hit_list:
                    
                if asteroid_hit.health > 1:
                    asteroid_hit.health = asteroid_hit.health - 1
                    bolt.kill()
                    self.score = self.score + 1
                    if asteroid_hit.health <= .25*(5*SPRITE_MAX_SCALING_ASTEROID):
                        asteroid_hit.set_texture(3)
                        asteroid_hit._set_scale(asteroid_hit.scale)
                    elif asteroid_hit.health <= .5*(5*SPRITE_MAX_SCALING_ASTEROID):
                        asteroid_hit.set_texture(2)
                        asteroid_hit._set_scale(asteroid_hit.scale)
                    elif asteroid_hit.health <= .75*(5*SPRITE_MAX_SCALING_ASTEROID):
                        asteroid_hit.set_texture(1)
                        asteroid_hit._set_scale(asteroid_hit.scale)
                else:
                    # Splits asteroid into two unless it is of smallest size
                    if asteroid_hit.scale > SPRITE_MAX_SCALING_ASTEROID/2:
                        x1 = asteroid_hit.center_x + asteroid_hit.collision_radius/2
                        y1 = asteroid_hit.center_y + asteroid_hit.collision_radius/2
                        x2 = asteroid_hit.center_x - asteroid_hit.collision_radius/2
                        y2 = asteroid_hit.center_y - asteroid_hit.collision_radius/2
                        
                        self.asteroid_list, self.numOfAsteroids = Main.Asteroid.createMiniAsteroid(MyGame, self.asteroid_list,
                            self.numOfAsteroids, x1, y1, SPRITE_MAX_SCALING_ASTEROID, MAX_ASTEROID_SPEED)
                            
                        self.asteroid_list, self.numOfAsteroids = Main.Asteroid.createMiniAsteroid(MyGame, self.asteroid_list,
                            self.numOfAsteroids, x2, y2, SPRITE_MAX_SCALING_ASTEROID, MAX_ASTEROID_SPEED)
                            
                    asteroid_hit.kill()
                    bolt.kill()
                    self.numOfAsteroids = self.numOfAsteroids - 1
                    self.score = self.score + 10
                
            # Off Screen Deletion of Bolts 
            if bolt.center_x > SCREEN_WIDTH or bolt.center_x < 0 \
            or bolt.center_y > SCREEN_HEIGHT or bolt.center_y < 0:
                bolt.kill()
        
        # Creation of More Asteroids When One Is Destroyed
        if self.numOfAsteroids < START_ASTEROID:
            self.asteroid_list, self.numOfAsteroids = Main.Asteroid.createAsteroid(MyGame, True, self.asteroid_list,
                self.numOfAsteroids, SCREEN_HEIGHT, SCREEN_WIDTH, SPRITE_MAX_SCALING_ASTEROID, MAX_ASTEROID_SPEED)
         
        self.physics_engine.update()
    
    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. 
        TODO: More dynamic attacks/interactions"""
        
        #Movement
        if self.player_sprite.movable:
            if key == arcade.key.UP:
                self.player_sprite.change_y = MOVEMENT_SPEED
                self.player_sprite.angle = 0
            elif key == arcade.key.DOWN:
                self.player_sprite.change_y = -MOVEMENT_SPEED
                self.player_sprite.angle = 180
            elif key == arcade.key.LEFT:
                self.player_sprite.change_x = -MOVEMENT_SPEED
                self.player_sprite.angle = 90
            elif key == arcade.key.RIGHT:
                self.player_sprite.change_x = MOVEMENT_SPEED
                self.player_sprite.angle = 270
                
            #Shooting 
            if key == arcade.key.SPACE:
                bolt = arcade.Sprite("Resources/bolt.png", SPRITE_SCALING_BOLT)
                boltDistFromPlayer = 25
                
                if self.player_sprite.angle == 0:
                    bolt.center_x = self.player_sprite.center_x
                    bolt.center_y = self.player_sprite.center_y + boltDistFromPlayer
                    bolt.change_x = 0
                    bolt.change_y = BOLT_SPEED
                elif self.player_sprite.angle == 180:
                    bolt.center_x = self.player_sprite.center_x
                    bolt.center_y = self.player_sprite.center_y - boltDistFromPlayer
                    bolt.change_x = 0
                    bolt.change_y = -BOLT_SPEED
                elif self.player_sprite.angle == 90:
                    bolt.center_x = self.player_sprite.center_x - boltDistFromPlayer
                    bolt.center_y = self.player_sprite.center_y 
                    bolt.change_x = -BOLT_SPEED
                    bolt.change_y = 0
                elif self.player_sprite.angle == 270:
                    bolt.center_x = self.player_sprite.center_x + boltDistFromPlayer
                    bolt.center_y = self.player_sprite.center_y 
                    bolt.change_x = BOLT_SPEED
                    bolt.change_y = 0
                self.bolt_list.append(bolt)
                
    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """
        if self.player_sprite.movable:
            if key == arcade.key.UP:
                self.player_sprite.change_y = PLAYER_FLOAT
            elif key == arcade.key.DOWN:
                self.player_sprite.change_y = -PLAYER_FLOAT
            elif key == arcade.key.LEFT:
                self.player_sprite.change_x = -PLAYER_FLOAT
            elif key == arcade.key.RIGHT:
                self.player_sprite.change_x = PLAYER_FLOAT
        else:
            self.player_sprite.change_x = PLAYER_FLOAT
            self.player_sprite.change_y = -PLAYER_FLOAT

def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()