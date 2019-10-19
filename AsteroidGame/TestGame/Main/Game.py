'''
Created on May 21, 2019

@author: Alex
'''

import random
import arcade 
import Main.Asteroid
import Main.Alien
import Main.Powerup


SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SPRITE_SCALING_PLAYER = 1.25
MOVEMENT_SPEED = 5
PLAYER_FLOAT = 0.1
START_ASTEROID = 1
SPRITE_MAX_SCALING_ASTEROID = 2
MAX_ASTEROID_SPEED = 1
SPRITE_SCALING_BOLT = 0.25
BOLT_SPEED = 7
SPRITE_SCALING_LASER = 0.2
SPRITE_SCALING_BEAM = 2

# Game States
TITLE_SCREEN = 0
GAME_RUNNING = 1
GAME_OVER = 2



class MyGame(arcade.Window):
    """ Main application class."""

    def __init__(self, width, height):
        super().__init__(width, height)

        arcade.set_background_color(arcade.color.EERIE_BLACK)
        
        self.current_state = TITLE_SCREEN

    def setup(self):
        """ Game Setup and Variable Initialization 
        TODO: Create more enemies and Make the title screen nicer"""
        
        # Create the initial object lists
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.asteroid_list = arcade.SpriteList()
        self.bolt_list = arcade.SpriteList()
        self.laser_list = arcade.SpriteList()
        self.alien_list = arcade.SpriteList()
        self.powerup_list = arcade.SpriteList()
        self.boss_list = arcade.SpriteList()
        self.beam_list = arcade.SpriteList()
        
        # Initial lives, Score and More
        self.lives = 3
        self.score = 1000
        self.numOfAsteroids = 0
        self.numOfAliens = 0
        self.numOfPow = 0
        self.numOfBoss = 0
        self.laser = False
        self.bb = 0
        self.pow = False
        
        # Sets up the player in the center
        self.player_sprite = arcade.Sprite("Resources/spaceship.png", SPRITE_SCALING_PLAYER)
        self.player_sprite.append_texture(arcade.load_texture("Resources/explosion.png"))
        self.player_sprite.append_texture(arcade.load_texture("Resources/spaceship-laser.png"))
        self.player_sprite.append_texture(arcade.load_texture("Resources/spaceship-bb.png"))
        self.player_sprite.center_x = SCREEN_WIDTH/2
        self.player_sprite.center_y = SCREEN_HEIGHT/2
        self.player_sprite.movable = True
        self.player_list.append(self.player_sprite)
        
        for i in range(START_ASTEROID):
            self.asteroid_list,self.numOfAsteroids = Main.Asteroid.createAsteroid(MyGame,False, self.asteroid_list,
                self.numOfAsteroids, SCREEN_HEIGHT, SCREEN_WIDTH, SPRITE_MAX_SCALING_ASTEROID, MAX_ASTEROID_SPEED)
            
        # Physics
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.wall_list)
        
        # Gets rid of mouse cursor
        self.set_mouse_visible(False)
        
    def draw_title_page(self):
        """
        Draw Title Screen
        """
        output = "Press Space to Start!"
        start_x = SCREEN_WIDTH/2.65
        start_y = SCREEN_HEIGHT/2
        arcade.draw_text(output,start_x,start_y,arcade.color.WHITE,60,1000)

    def draw_game_over(self):
        """
        Draws the Game Over Screen
        """
        start_x = SCREEN_WIDTH/2.65
        start_y = SCREEN_HEIGHT/2
        output = "Game Over"
        arcade.draw_text(output,start_x, start_y, arcade.color.WHITE, 60, 1000)
        
        output = "Press Space to restart"
        start_y = SCREEN_HEIGHT/2.5
        arcade.draw_text(output,start_x, start_y, arcade.color.WHITE, 60, 1000)
    
    def draw_game(self):
        # Drawing of Moving Objects
        self.player_list.draw()
        self.asteroid_list.draw()
        self.bolt_list.draw()
        self.alien_list.draw()
        self.laser_list.draw()
        self.powerup_list.draw()
        self.boss_list.draw()
        self.beam_list.draw()
        
        # Drawing of still objects
        start_x = 60
        start_y = SCREEN_HEIGHT-20
        arcade.draw_text(f"Score: {self.score}", start_x, start_y, arcade.color.WHITE)
        start_x = 10
        start_y = SCREEN_HEIGHT-20
        arcade.draw_text(f"Lives: {self.lives}",start_x,start_y, arcade.color.WHITE)
    
    def on_draw(self):
        """ Render the screen. 
        TODO: Special effects for bolt & asteroid destruction"""
        
        arcade.start_render()
        
        if self.current_state == TITLE_SCREEN:
            self.draw_title_page()
        
        elif self.current_state == GAME_RUNNING:
            self.draw_game()
        
        else:
            self.draw_game()
            self.draw_game_over()

    def update(self, delta_time):
        """ All the logic to move, and the game logic goes here. 
        TODO: have ship explode each life, balance level design 
        player invulnerability on respawn"""
        
        if self.current_state == GAME_RUNNING:
            # Collision Checking for Asteroid and Player, and bolt and player, and alien and player
            hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.asteroid_list)
            bolt_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.bolt_list)
            alien_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.alien_list)
            boss_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.boss_list)
            beam_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.beam_list)
            
            # Checking player collisions
            if hit_list or bolt_hit_list or alien_hit_list or boss_hit_list or beam_hit_list:
                if self.lives > 1:
                    self.player_sprite.center_x = SCREEN_WIDTH/2
                    self.player_sprite.center_y = SCREEN_HEIGHT/2
                    self.lives = self.lives - 1
                    self.score = self.score - 10
                else:
                    self.lives = 0
                    self.player_sprite.set_texture(1)
                    self.player_sprite.movable = False
                    self.player_sprite.stop()
                    self.current_state = GAME_OVER

            
            # Creation of Powerups
            if self.numOfPow < 1 and random.randint(1,10000) < 50:
                powType = 1
                self.numOfPow = self.numOfPow + 1
                self.powerup_list = Main.Powerup.createPowerUp\
                                    (self,self.powerup_list, powType, SCREEN_HEIGHT, SCREEN_WIDTH)
            
            pow_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.powerup_list)
            
            for pow in pow_hit_list:
                # Dealing with collision with player
                if self.pow == False:
                    pow.kill()
                    self.numOfPow = 0
                    if pow.type == 1:
                        self.player_sprite.set_texture(2)
                        self.laser = True
                        self.pow = True
                    elif pow.type == 2:
                        self.player_sprite.set_texture(3)
                        self.bb = 4
                        self.pow = True
            
            # Boss summoning
            if self.score > 1000 and self.numOfBoss < 1:
                self.boss_list = Main.Alien.createBoss(MyGame, self.boss_list, SCREEN_HEIGHT, SCREEN_WIDTH)
                self.numOfBoss = 1
                if self.numOfAliens > 0:
                    for alien in self.alien_list:
                        alien.kill()
                
            for boss in self.boss_list:
                boss.center_x =  boss.center_x + boss.change_x
                boss.center_y = boss.center_y + boss.change_y
                boss.beamTimer = boss.beamTimer - 1
                
                if self.player_sprite.center_x > boss.center_x:
                            boss.change_x = 0.2
                elif self.player_sprite.center_x < boss.center_x:
                            boss.change_x = -0.2
                
                # Boss Beaming
                if boss.beamTimer < 500 and not boss.beamActive:
                    beam = arcade.Sprite("Resources/alienbolt.png", SPRITE_SCALING_BEAM) # Change to beam
                    beam.height = SCREEN_HEIGHT / 1.2          
                    beam.center_x = boss.center_x
                    beam.center_y = boss.center_y - 350
                    boss.beamActive = True
                    self.beam_list.append(beam)
                elif boss.beamTimer < 500 and boss.beamTimer > 0:
                    for beam in self.beam_list:
                        beam.center_x = boss.center_x
                        beam.center_y = boss.center_y - 350
                        boss.beamTimer = boss.beamTimer - 1 
                elif boss.beamTimer <= 0:
                    for beam in self.beam_list:
                        beam.kill()
                    boss.beamActive = False
                    boss.beamTimer = 1000
                    
                # Boss Shooting
                if boss.shootTimer <= 0:
                        for i in range(1,6):
                            bolt = arcade.Sprite("Resources/alienbolt.png", SPRITE_SCALING_BOLT) 
                            bolt.type = 0
                            bolt.center_x = boss.center_x - 100 + (30*i)
                            bolt.center_y = boss.center_y - 60
                            if i == 1:
                                bolt.change_x = -2
                            elif i == 2:
                                bolt.change_x = -1
                            elif i == 3:
                                bolt.change_x = 0
                            elif i == 4:
                                bolt.change_x = 1
                            elif i == 5:
                                bolt.change_x = 2
                                                                
                            bolt.change_y = -BOLT_SPEED*.35
                            self.bolt_list.append(bolt)
                            boss.shootTimer = 50
                else:
                    boss.shootTimer = boss.shootTimer - 1
                
            if self.numOfBoss < 1:
                # Creation of Aliens (ultimately want to put on a timer)
                if self.score < 250:
                    spawn = random.randint(1,200)
                elif self.score < 500:
                    spawn = random.randint(1,100)
                else: 
                    spawn = random.randint(1,50)
                
                if spawn == 1:
                    alienType = random.randint(1,4)
                    self.alien_list, self.numOfAliens = Main.Alien.createAlien\
                                        (MyGame, self.alien_list, self.numOfAliens, alienType, SCREEN_HEIGHT, SCREEN_WIDTH)
                
                # Alien Movement
                for alien in self.alien_list:
                    alien.center_x = alien.center_x + alien.change_x
                    alien.center_y = alien.center_y + alien.change_y
                    
                    #Alien 3 follow pattern
                    if alien.type == 3:
                        if self.player_sprite.center_x > alien.center_x:
                            alien.change_x = 2
                        elif self.player_sprite.center_x < alien.center_x:
                            alien.change_x = -2
                    
    #                 # Aliens collide with asteroid
    #                 alien_hit_list = arcade.check_for_collision_with_list(alien, self.asteroid_list)
    #                 if alien_hit_list:
    #                     #TODO: Add result of alien death
    #                     alien.kill()
                    
                    # Alien shooting
                    degreeOfSpace = 3
                    if alien.center_x < self.player_sprite.center_x + degreeOfSpace \
                    and alien.center_x > self.player_sprite.center_x - degreeOfSpace \
                    and alien.center_y > self.player_sprite.center_y:
                        if alien.type <= 3:
                            bolt = arcade.Sprite("Resources/alienbolt.png", SPRITE_SCALING_BOLT) 
                            bolt.type = 0
                            bolt.center_x = alien.center_x 
                            bolt.center_y = alien.center_y - 20
                            bolt.change_x = 0
                            bolt.change_y = -BOLT_SPEED*.65
                            self.bolt_list.append(bolt)
                        if alien.type == 4:
                            bolt = arcade.Sprite("Resources/alienbolt.png", 5*SPRITE_SCALING_BOLT) 
                            bolt.type = 1
                            bolt.center_x = alien.center_x 
                            bolt.center_y = alien.center_y - 60
                            bolt.change_x = 0
                            bolt.change_y = -BOLT_SPEED*.35
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
                if asteroid.center_x-asteroid.collision_radius > SCREEN_WIDTH:
                    asteroid.center_x = 10-asteroid.collision_radius
                    
                if asteroid.center_x + asteroid.collision_radius < 0: 
                    asteroid.center_x = SCREEN_WIDTH +asteroid.collision_radius
                
                if asteroid.center_y - asteroid.collision_radius > SCREEN_HEIGHT:
                    asteroid.center_y = 10-asteroid.collision_radius
                    
                if asteroid.center_y + asteroid.collision_radius < 0:
                    asteroid.center_y = SCREEN_HEIGHT + asteroid.collision_radius
                    
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
                
                # Collision with boss
                bolt_hit_list = arcade.check_for_collision_with_list(bolt,self.boss_list)
                for boss_hit in bolt_hit_list:
                    if boss_hit.health > 0:
                        if bolt.type == 0:
                            boss_hit.health = boss_hit.health - 1
                        elif bolt.type == 75:
                            boss_hit.health = boss_hit.health - 75
                    elif boss_hit.health <= 0:
                        boss_hit.kill()
                        self.numOfBoss = self.numOfBoss - 1
                    bolt.kill()
                
                # Collision with asteroid
                bolt_hit_list = arcade.check_for_collision_with_list(bolt,self.asteroid_list)
                for asteroid_hit in bolt_hit_list:
                        
                    if asteroid_hit.health > 1:
                        if bolt.type == 0:
                            asteroid_hit.health = asteroid_hit.health - 1
                        elif bolt.type == 1:
                            asteroid_hit.health = asteroid_hit.health - 75
                        
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
                            
                            self.asteroid_list = Main.Asteroid.createMiniAsteroid(MyGame, self.asteroid_list,
                                 x1, y1, SPRITE_MAX_SCALING_ASTEROID, MAX_ASTEROID_SPEED)
                                
                            self.asteroid_list = Main.Asteroid.createMiniAsteroid(MyGame, self.asteroid_list,
                                 x2, y2, SPRITE_MAX_SCALING_ASTEROID, MAX_ASTEROID_SPEED)
                            self.numOfAsteroids = self.numOfAsteroids + 2
                                
                        asteroid_hit.kill()
                        bolt.kill()
                        self.numOfAsteroids = self.numOfAsteroids-1
                        self.score = self.score + 10
                    
                # Off Screen Deletion of Bolts 
                if bolt.center_x > SCREEN_WIDTH or bolt.center_x < 0 \
                or bolt.center_y > SCREEN_HEIGHT or bolt.center_y < 0:
                    bolt.kill()
            
            for beam in self.beam_list:
                # Collision with asteroid
                laser_hit_list = arcade.check_for_collision_with_list(beam,self.asteroid_list)
                for asteroid_hit in laser_hit_list:
                        
                    if asteroid_hit.health > 1:
                        asteroid_hit.health = asteroid_hit.health - 1
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
                            
                            self.asteroid_list = Main.Asteroid.createMiniAsteroid(MyGame, self.asteroid_list,
                                 x1, y1, SPRITE_MAX_SCALING_ASTEROID, MAX_ASTEROID_SPEED)
                                
                            self.asteroid_list = Main.Asteroid.createMiniAsteroid(MyGame, self.asteroid_list,
                                x2, y2, SPRITE_MAX_SCALING_ASTEROID, MAX_ASTEROID_SPEED)
                            self.numOfAsteroids = self.numOfAsteroids + 2
                                
                        asteroid_hit.kill()
            
            
            for laser in self.laser_list:
                # Movement
                laserDistFromPlayer = laser.height/2 + 25
                if self.player_sprite.angle == 0:
                    laser.center_x = self.player_sprite.center_x
                    laser.center_y = self.player_sprite.center_y + laserDistFromPlayer
                    laser.angle = 0
    
                elif self.player_sprite.angle == 180:
                    laser.center_x = self.player_sprite.center_x
                    laser.center_y = self.player_sprite.center_y - laserDistFromPlayer
                    laser.angle = 180
    
                elif self.player_sprite.angle == 90:
                    laser.center_x = self.player_sprite.center_x - laserDistFromPlayer
                    laser.center_y = self.player_sprite.center_y
                    laser.angle = 90
    
                elif self.player_sprite.angle == 270:
                    laser.center_x = self.player_sprite.center_x + laserDistFromPlayer
                    laser.center_y = self.player_sprite.center_y 
                    laser.angle = 270
                
                # Collision with alien
                laser_hit_list = arcade.check_for_collision_with_list(laser,self.alien_list)
                for alien_hit in laser_hit_list:
                    alien_hit.kill()
                    laser.health = laser.health - 1
                    self.numOfAliens = self.numOfAliens - 1
                    self.score = self.score + 50
                    if laser.health <= 0:
                        laser.kill()
                
                # Collision with boss
                laser_hit_list = arcade.check_for_collision_with_list(laser,self.alien_list)
                for boss_hit in laser_hit_list:
                    if boss_hit.health > 1:
                        boss_hit.health = boss_hit.health - 1
                        laser.health = laser.health - 1
                        if laser.health <= 0:
                            laser.kill()
                    else:
                        boss_hit.kill()
                        laser.health = laser.health - 1
                        if laser.health <= 0:
                            laser.kill()
                        self.numOfBoss = self.numOfBoss - 1
                
                # Collision with asteroid
                laser_hit_list = arcade.check_for_collision_with_list(laser,self.asteroid_list)
                for asteroid_hit in laser_hit_list:
                        
                    if asteroid_hit.health > 1:
                        asteroid_hit.health = asteroid_hit.health - 1
                        laser.health = laser.health - 1
                        if laser.health <= 0:
                            laser.kill()
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
                            
                            self.asteroid_list = Main.Asteroid.createMiniAsteroid(MyGame, self.asteroid_list,
                                 x1, y1, SPRITE_MAX_SCALING_ASTEROID, MAX_ASTEROID_SPEED)
                                
                            self.asteroid_list = Main.Asteroid.createMiniAsteroid(MyGame, self.asteroid_list,
                                x2, y2, SPRITE_MAX_SCALING_ASTEROID, MAX_ASTEROID_SPEED)
                            self.numOfAsteroids = self.numOfAsteroids + 2
                                
                        asteroid_hit.kill()
                        laser.health = laser.health - 1
                        if laser.health <= 0:
                            laser.kill()
                        self.numOfAsteroids = self.numOfAsteroids - 1
                        self.score = self.score + 10
                # Laser Decay
                laser.health = laser.health - 1
                if laser.health <= 0:
                    laser.kill()
                    self.laser = False
                    self.pow = False
                    
            # Creation of More Asteroids When One Is Destroyed
            extraAsteroid = round(self.score/200)  
            
            if self.numOfAsteroids < START_ASTEROID + extraAsteroid:
                self.asteroid_list, self.numOfAsteroids = Main.Asteroid.createAsteroid(MyGame, True, self.asteroid_list,
                    self.numOfAsteroids, SCREEN_HEIGHT, SCREEN_WIDTH, SPRITE_MAX_SCALING_ASTEROID, MAX_ASTEROID_SPEED)
             
            self.physics_engine.update()
        
    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. 
        TODO: More dynamic attacks/interactions"""
        if self.current_state == TITLE_SCREEN:
            if key == arcade.key.SPACE:
            # Starts the game initially
                self.setup()
                self.current_state = GAME_RUNNING
        elif self.current_state == GAME_OVER:
            if key == arcade.key.SPACE:
            # Restarts after death
                self.setup()
                self.current_state = GAME_RUNNING
                
        if self.current_state == GAME_RUNNING:
            # Movement
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
                
                
                if key == arcade.key.SPACE and self.laser == True:
                    # Special Shooting (LASER)

                    laser = arcade.Sprite("Resources/laser.png", SPRITE_SCALING_LASER)
                    laser.health = 30
                    laser.height = SCREEN_HEIGHT / 2
                    laserDistFromPlayer = laser.height / 2 + 25
                    self.player_sprite.set_texture(0)
                    
                    if self.player_sprite.angle == 0:
                        laser.center_x = self.player_sprite.center_x
                        laser.center_y = self.player_sprite.center_y + laserDistFromPlayer
    
                    elif self.player_sprite.angle == 180:
                        laser.center_x = self.player_sprite.center_x
                        laser.center_y = self.player_sprite.center_y - laserDistFromPlayer
    
                    elif self.player_sprite.angle == 90:
                        laser.center_x = self.player_sprite.center_x - laserDistFromPlayer
                        laser.center_y = self.player_sprite.center_y
                        laser.angle = 90
    
                    elif self.player_sprite.angle == 270:
                        laser.center_x = self.player_sprite.center_x + laserDistFromPlayer
                        laser.center_y = self.player_sprite.center_y 
                        laser.angle = 270
    
                    self.laser_list.append(laser)
                #Big Bolts
                elif key == arcade.key.SPACE and self.bb > 0:
                    bolt = arcade.Sprite("Resources/bolt.png", 4*SPRITE_SCALING_BOLT)
                    boltDistFromPlayer = 50
                    bolt.type = 1
                    self.bb = self.bb -1
                    if self.bb == 0: self.player_sprite.set_texture(0); self.pow = False
                    
                    if self.player_sprite.angle == 0:
                        bolt.center_x = self.player_sprite.center_x
                        bolt.center_y = self.player_sprite.center_y + boltDistFromPlayer
                        bolt.change_x = 0
                        bolt.change_y = 0.5*BOLT_SPEED
                    elif self.player_sprite.angle == 180:
                        bolt.center_x = self.player_sprite.center_x
                        bolt.center_y = self.player_sprite.center_y - boltDistFromPlayer
                        bolt.change_x = 0
                        bolt.change_y = -0.5*BOLT_SPEED
                    elif self.player_sprite.angle == 90:
                        bolt.center_x = self.player_sprite.center_x - boltDistFromPlayer
                        bolt.center_y = self.player_sprite.center_y 
                        bolt.change_x = -0.5*BOLT_SPEED
                        bolt.change_y = 0
                    elif self.player_sprite.angle == 270:
                        bolt.center_x = self.player_sprite.center_x + boltDistFromPlayer
                        bolt.center_y = self.player_sprite.center_y 
                        bolt.change_x = 0.5*BOLT_SPEED
                        bolt.change_y = 0
                    self.bolt_list.append(bolt)
                # General Shooting 
                elif key == arcade.key.SPACE:
                    bolt = arcade.Sprite("Resources/bolt.png", SPRITE_SCALING_BOLT)
                    boltDistFromPlayer = 25
                    bolt.type = 0
                    
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
        if self.current_state == GAME_RUNNING:
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
