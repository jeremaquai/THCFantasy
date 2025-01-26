import arcade
from arcade.types import LRBT
from fadingView import FadingView
from constants import WIDTH, HEIGHT

class MenuView(FadingView):
    '''Class that manages the menu view'''
    def __init__(self):
        super().__init__()

        self.background_color = arcade.color.WHITE

    def on_resize(self, width, height):
        '''This method is automatically called when the window is resized'''
        # Call the parent.  Failing to do this will mess up the coordinates, and default to 0,0 at the center and the edges being -1 to 1
        super().on_resize(width, height)

        print(f'Window resized to: {width}, {height}')

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

    def setup(self):
        '''This should set up your game and get it ready to play'''
        # Replace pass with the code to set up your game
        pass


class GameView(FadingView):
    '''Manage the Game view for our program'''

    def setup(self):
        '''This should set up ypur game and get it ready to play'''
        # Replace pass with the code to set up your game
        pass

    def on_update(self, dt):
        self.update_fade(next_view=GameOverView)

    def on_show_view(self):
        '''Called when switching to this view'''
        self.window.background_color = arcade.color.ORANGE_PEEL

    def on_draw(self):
        '''Draw everything for the game'''
        self.clear()
        arcade.draw_text('Game - press space to advance',
                         self.width / 2,
                         self.height / 2,
                         arcade.color.BLACK,
                         font_size=30,
                         anchor_x='center')
        self.draw_fading()

    def on_key_press(self, key, _modifiers):
        '''Handle key presses, In this casse, we'll just count a space as a game over and advance to the GameOver View'''
        if key == arcade.key.SPACE:
            self.fade_out = 0

class GameOverView(FadingView):
    '''Class to manage the GameOver view'''
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

    def setup(self):
        '''This should setup your game and get it ready to play'''
        # Replace pass with the code to set up your game
        pass


def main():
    '''Main function or Startup'''
    # Create a window class.  This is what actually shows up on the screen
    window = arcade.Window(WIDTH, HEIGHT, 'THC Fantasy', resizable=True)

    # Create and setup the MenuView
    menu_view = MenuView()

    # Show MenuView on screen
    window.show_view(menu_view)

    # Start the arcade game loop
    arcade.run()

if __name__ == '__main__':
    main()
                