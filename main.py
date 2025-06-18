import arcade

# Constants
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Cat-a-pult!"
clicked_buttons = {"play":False}
current_screen = "none"

class GameView(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, resizable=True)
        self.highscore = 0

        self.background_color = arcade.csscolor.BURLYWOOD
        self.muffin_texture = arcade.load_texture("assets/muffin.png")
        
        #load buttons textures
        self.play_texture = arcade.load_texture("assets/button-play.png")

    def home(self):
        """Function for the home screen"""

        # Make the play button sprite
        self.play_button = arcade.Sprite(self.play_texture)
        self.play_button.center_x = WINDOW_WIDTH/2
        self.play_button.center_y = WINDOW_HEIGHT/2


        # Spritelist (I think this reduces lag?)
        self.button_list = arcade.SpriteList()
        self.button_list.append(self.play_button)

    def level_select(self):
        self.back_button = arcade.Sprite

        
    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()
        self.button_list.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            if arcade.check_for_collision(self.play_button, arcade.Sprite(center_x=x, center_y=y, width=1, height=1)):
                self.play_button.color = arcade.color.GREEN
                clicked_buttons["play"] = True

                
        
    def on_mouse_release(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            if clicked_buttons["play"] == True:
                clicked_buttons["play"] = False
                self.play_button.color = 255, 255, 255





def main():
    """Main function"""
    window = GameView()
    window.home()
    arcade.run()


if __name__ == "__main__":
    main()
