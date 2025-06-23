import arcade

# Constants
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Cat-a-pult!"
clicked_buttons = {"play":False}
screen_history = []

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
        self.back_texture = arcade.load_texture("assets/button-back.png")
        self.current_screen = "none"


    def home(self):
        """Function for the home screen"""

        # Make the play button sprite
        self.background_color = arcade.csscolor.BURLYWOOD

        self.play_button = arcade.Sprite(self.play_texture)
        self.play_button.center_x = WINDOW_WIDTH/2
        self.play_button.center_y = WINDOW_HEIGHT/2


        # Spritelist (I think this reduces lag?)
        self.button_list = arcade.SpriteList()
        self.button_list.append(self.play_button)

    def level_select(self):
        self.back_button = arcade.Sprite(self.back_texture)
        self.back_button.center_x = 50
        self.back_button.center_y = WINDOW_HEIGHT-50
        self.button_list.append(self.back_button)

    # This is an IMPORTANT FUNCTION !!!!!!!!!!!!!!!!!!!!!!!!! (i made it)
    def change_scene(self, is_menu=False, screen_id=1):
        '''Call this function to change the 'level'. Switches to a different pre-programmed level.
        Arguments:
            is_menu (bool) I think this one is self-explanatory.
            screen_id (int) eg. 2 These are for me to code in. 1 is home 2 is settings 3 is pause
        '''
        if is_menu:
            pass
        else:
            pass

    
    def on_mouse_motion(self, x, y, dx, dy):
            # Check if the mouse cursor collides with the button sprite
            if self.back_button.collides_with_point((x, y)):
                 self.back_button.scale = 1.1
            else:
                self.back_button.scale = 1.1

    def on_mouse_press(self, x, y, button, modifiers):
        if self.back_button in self.button_list:
            if button == arcade.MOUSE_BUTTON_LEFT:
                if arcade.check_for_collision(self.play_button, arcade.Sprite(center_x=x, center_y=y, width=1, height=1)):
                    clicked_buttons["play"]=True
                    self.play_button.color = arcade.color.GREEN

        
    def on_mouse_release(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            if clicked_buttons["play"]:
                clicked_buttons["play"] = False
                self.level_select()
            self.play_button.color = 255, 255, 255
                

    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()
        self.button_list.draw()

    def on_update(self, delta_time):
        pass







def main():
    """Main function"""
    window = GameView()
    window.home()
    arcade.run()


if __name__ == "__main__":
    main()
