import arcade

# Constants
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Cat-a-pult!"
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
        
        #load home screen buttons textures
        self.play_texture = arcade.load_texture("assets/button-play.png")
        self.current_screen = "none"

        self.buttons_clicked = []



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


    # This is an IMPORTANT FUNCTION !!!!!!!!!!!!!!!!!!!!!!!!! (i made it)
    def change_scene(self, is_menu=False, screen_id=1):
        '''Call this function to change the 'level'. Switches to a different pre-programmed level.
        Arguments:
            is_menu (bool) I think this one is self-explanatory.
            screen_id (int) eg. 2 These are the screens for me to code in.
        '''
        if is_menu:
            # Menu 1 screen 1 (level select)
            if screen_id == 1:
                self.back_texture = arcade.load_texture("assets/button-back.png")
                self.l_1_texture = arcade.load_texture("assets/button-level-1.png")
                self.l_L_texture = arcade.load_texture("assets/button-level-locked.png")

                self.back_button = arcade.Sprite(self.back_texture)
                self.back_button.center_x = 50
                self.back_button.center_y = WINDOW_HEIGHT-50

                self.level1_button = arcade.Sprite(self.l_1_texture)
                self.level1_button.center_x = WINDOW_WIDTH/2
                self.level1_button.center_y = WINDOW_HEIGHT/2


                self.button_list.append(self.back_button)

        else:
            pass
    


    
    def on_mouse_motion(self, x, y, dx, dy):
            # Check if the mouse cursor collides with the button sprite
            for button in self.button_list:
                if button.collides_with_point((x, y)):
                    button.scale = 1.1
                else:
                    button.scale = 1

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.buttons_clicked = arcade.check_for_collision_with_list(arcade.Sprite(center_x=x, center_y=y, width=1, height=1), self.button_list)
            for i in self.buttons_clicked:
                i.scale = 0.8
            

        
    def on_mouse_release(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            print(self.buttons_clicked)
            try:
                if self.play_button in self.buttons_clicked:
                    self.change_scene(True, 1)
                    self.play_button.kill()
                if self.back_button in self.buttons_clicked:
                    self.home()
            except:
                pass
            self.buttons_clicked = []
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
