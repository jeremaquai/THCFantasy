import arcade
from arcade.types import LRBT
from fadingView import FadingView
from characters import Player
from constants import (WIDTH,
                       HEIGHT,
                       WINDOW_TITLE,
                       TILE_SCALING, 
                       PLAYER_MOVEMENT_SPEED, 
                       PLAYER_SCALING,
                       ENEMY_SCALING)

class MenuView(FadingView):
    '''Class that manages the menu view'''
    def __init__(self):
        super().__init__()

        self.background_color = arcade.color.WHITE

        # Reset the viewport, necessary if we have a scrolling game and we need to reset the viewport back to the start so that we can see what we draw.
        self.window.default_camera.use()

    def on_update(self, dt):
        self.update_fade(next_view=GameView)   

    def on_show_view(self):
        '''Called when swiching to this view'''
        self.window.background_color = arcade.color.WHITE

    def on_draw(self):
        '''Draw the menu'''
        self.clear()
        arcade.draw_text('Menu Screen - press space to advance', 
                         self.width / 2, 
                         self.height / 2,
                         arcade.color.BLACK,
                         font_size=30,
                         anchor_x='center')
        self.draw_fading()

    def on_key_press(self, key, _modifiers):
        '''Handle key presses, In this case, we'll just count a SPACE as game over and advance to the game view'''
        if self.fade_out is None and key == arcade.key.SPACE:
            self.fade_out = 0
        elif key == arcade.key.ESCAPE:
            self.window.close()

    def setup(self):
        '''This should set up your game and get it ready to play'''
        # Replace pass with the code to set up your game
        pass


class GameView(FadingView):
    '''Manage the Game view for our program'''
    def __init__(self):
        '''
        Initializer
        '''
        #Call the parent class
        super().__init__()

        # Variable to hold our texture for our player
        self.player_texture = None

        # Variables that will hold sprite lists
        self.player_list = None
        self.wall_list = None

        # Enemies
        self.enemy_list = None

        # Set up the player info
        self.player_sprite = None       

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        
        # Set the background
        self.background_color = arcade.csscolor.CORNFLOWER_BLUE

        # The camera used to update the viewport and projection on screen resize
        self.viewCamera = arcade.camera.Camera2D(
            position=(0, 0),
            projection=LRBT(left=0, right=WIDTH, bottom=0, top=HEIGHT),
            viewport=self.window.rect
        )

        # The player camera
        self.playerCamera = None

        # A variable to store the gui camera
        self.gui_camera = None

        # This variable will store the text for XP that will draw to the screen
        self.xp_text = None

    def setup(self):
        '''This should set up ypur game and get it ready to play'''

        # Sprite lists
        # SpriteList for the player sprite
        self.player_list = arcade.SpriteList()
        # SpriteList for boxes and ground
        '''Putting the ground and box sprites in the same Spritelist will make it easier to perform collision detection against them later on.  Setting the spatial hash to True will make collision detection much faster if the objects in this SpriteList do not move'''
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        # Coin tile list
        self.enemy_list = arcade.SpriteList(use_spatial_hash=True)
        
        # Set up the player
        # Variable to hold texture for the player
        self.player_texture = arcade.load_texture(
            './assets/characters/rpgMainCharacter/down_idle1.png',
            
        )
        # create the player sprite and set the coordinates to place it on the map
        self.player_sprite = Player(self.player_texture,
                                        scale=PLAYER_SCALING)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 128
        self.player_list.append(self.player_sprite)

        # Create the ground
        # This shows using a loop to place multiple sprites horizontally
        for x in range(0, 1250, 64):
            wall = arcade.Sprite(':resources:images/tiles/grassMid.png',
                                scale=TILE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            self.wall_list.append(wall)

        # Put some crates on the ground
        # This shows using a coordinate list to place sprites
        coordinate_list = [[512, 96], [256, 96], [768, 96]]

        for coordinate in coordinate_list:
            # Add a crate to the ground
            wall = arcade.Sprite(
                ':resources:images/tiles/boxCrate_double.png',
                scale=TILE_SCALING
            )
            wall.position = coordinate
            self.wall_list.append(wall)

        # Add Coins to the world
        for x in range(128, 1250, 256):
            enemy = arcade.Sprite('./assets/characters/mixed-sprites-2/frog.png',
                                 scale=ENEMY_SCALING)
            enemy.center_x = x
            enemy.center_y = 96
            self.enemy_list.append(enemy)


        # Create a Simple Physics Engine, this will handle moving the player as well as collisions between the player sprite and whatever SpriteList I specify as walls.
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite, self.wall_list
        )

        # Initialize the player camera, setting a viewport the size of our window
        self.playerCamera = arcade.camera.Camera2D()

        # Initialize the gui camera, initial settings are the same as the player camera
        self.gui_camera = arcade.camera.Camera2D()

        # Initialize the arcade.Text object for the xp
        self.xp_text = arcade.Text(f'Player XP: {self.player_sprite.currentXp}', x=0, y=5)

    def on_update(self, dt):
        '''Movement and game Logic'''
        # Move the player using the physics engine
        self.physics_engine.update()

        # See if we hit any coins
        enemy_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.enemy_list
        )

        # Loop through each enemy we hit (if any) and remove it
        for enemy in enemy_hit_list:
            # Add xp to the player sprite
            self.player_sprite.currentXp += 10
            # remove the coin
            enemy.remove_from_sprite_lists()
            self.xp_text.text = f'Player XP: {self.player_sprite.currentXp}'

        # Center the player camera on the player
        self.playerCamera.position = self.player_sprite.position

        self.player_sprite.update(delta_time=dt)
        # Having the fade loaded for when ready
        self.update_fade(next_view=GameOverView)

        

    def on_show_view(self):
        '''Called when switching to this view'''
        self.window.background_color = arcade.color.ORANGE_PEEL

    def on_draw(self):
        '''Draw everything for the game'''

        # Clear the screen
        self.clear()
        
        with self.viewCamera.activate():
            #Activate the player camera before drawing
            self.playerCamera.use()
            # Draw the sprites
            self.player_list.draw()
            self.wall_list.draw()
            self.enemy_list.draw()

            # Activate the GUI camera
            self.gui_camera.use()

            # Draw the xp
            self.xp_text.draw()

            # Draw the fading view when loading or unloading view
            self.draw_fading()#

    

    def update_player_speed(self):

        # Calculate speed based on the keys pressed
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        if self.up_pressed and not self.down_pressed:
            self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
        elif self.down_pressed and not self.up_pressed:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        elif self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED


    def on_key_press(self, key, _modifiers):
        '''Handle key presses, In this casse, we'll just count a space as a game over and advance to the GameOver View'''
        
        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = True
            self.update_player_speed()
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = True
            self.update_player_speed()
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
            self.update_player_speed()
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True
            self.update_player_speed()
        
        if key == arcade.key.SPACE:
            self.fade_out = 0
        elif key == arcade.key.ESCAPE:
            self.window.close()
        elif key == arcade.key.F:
            # User hits F Flip between full and not full screen
            self.window.set_fullscreen(not self.window.fullscreen)

            # Get the window coordinates.  Match viewport to window coordinates so there is a one to one mapping
            self.viewCamera.viewport = self.window.rect
            self.viewCamera.projection = arcade.LRBT(0.0, self.width, 0.0, self.height)
            self.player_sprite.window_height = self.height
            self.player_sprite.window_width = self.width
                #extend the player camera with the window
            self.playerCamera.viewport = self.window.rect
            
    
    def on_key_release(self, key, _modifiers):
        '''Called whenever a key is released'''
        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = False
            self.update_player_speed()
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = False
            self.update_player_speed()
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
            self.update_player_speed()
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False
            self.update_player_speed()
        

class GameOverView(FadingView):
    '''Class to manage the GameOver view'''
    def __init__(self):
        super().__init__()

        # Reset the viewport, necessary if we have a scrolling game and we need to reset the viewport back to the start so that we can see what we draw.
        self.window.default_camera.use()

    def on_update(self, dt):
        self.update_fade(next_view=MenuView)

    def on_show_view(self):
        '''Called when switching to this view'''
        self.background_color = arcade.color.BLACK

    def on_draw(self):
        '''Draw the GameOver view'''
        self.clear()
        arcade.draw_text('Game Over - press SPACE to advance',
                         self.width /2,
                         self.height / 2,
                         arcade.color.WHITE,
                         font_size=30,
                         anchor_x='center')
        self.draw_fading()

    def on_key_press(self, key, _modifiers):
        '''If user hits SPACE, go back to the main menu view'''
        if key == arcade.key.SPACE:
            self.fade_out = 0
        elif key == arcade.key.ESCAPE:
            self.window.close()

    def setup(self):
        '''This should setup your game and get it ready to play'''
        # Replace pass with the code to set up your game
        pass


def main():
    '''Main function or Startup'''
    # Create a window class.  This is what actually shows up on the screen
    window = arcade.Window(WIDTH, HEIGHT, WINDOW_TITLE, resizable=False)

    # Create and setup the MenuView
    menu_view = MenuView()

    # Show MenuView on screen
    window.show_view(menu_view)

    # Start the arcade game loop
    arcade.run()

if __name__ == '__main__':
    main()
                