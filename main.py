import arcade
import math

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
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, resizable=False)
        self.highscore = 0

        self.background_color = arcade.csscolor.BURLYWOOD
        self.muffin_texture = arcade.load_texture("assets/muffin.png")
        
        #load home screen buttons textures
        self.play_texture = arcade.load_texture("assets/button-play.png")

        self.buttons_hovered = []
        self.buttons_clicked = []

        self.car_status = "none"
        self.GRAVITY = 0



    def home(self):
        """Function for the home screen"""

        self.background_color = arcade.csscolor.BURLYWOOD

        # Make the play button sprite
        self.play_button = arcade.Sprite(self.play_texture)
        self.play_button.center_x = WINDOW_WIDTH/2
        self.play_button.center_y = WINDOW_HEIGHT/2


        # Spritelist (I think this reduces lag?)
        self.button_list = arcade.SpriteList(True)
        self.button_list.append(self.play_button)
        
        self.player = arcade.SpriteList()
        self.fish = arcade.SpriteList()

        self.car_spawn_x = 100
        self.car_spawn_y = 100



    # This is an IMPORTANT FUNCTION !!!!!!!!!!!!!!!!!!!!!!!!! (i made it)
    def change_scene(self, is_menu=False, screen_id=1):
        '''Call this function to change the 'level'. Switches to a different pre-programmed level.
        Arguments:
            is_menu (bool) I think this one is self-explanatory.
            screen_id (int) eg. 2 These are the screens for me to code in.
        '''
        # Kill all buttons
        for i in self.button_list:
            i.kill()
        for i in self.player:
            i.kill()


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
                self.button_list.append(self.level1_button)

        else:
            # Level 1

            if screen_id == 1:
                self.GRAVITY = 0
                self.background_color = arcade.csscolor.AQUA
                self.car = arcade.Sprite(self.muffin_texture)
                self.car.center_x = self.car_spawn_x
                self.car.center_y = self.car_spawn_y
                self.car.scale = 0.7
                
                self.player.append(self.car)

                self.physics_engine = arcade.PhysicsEngineSimple(
                    self.car
                )




    
    def on_mouse_motion(self, x, y, dx, dy):
            # Check if the mouse cursor collides with the button sprite
            self.buttons_hovered = arcade.get_sprites_at_point((x, y), self.button_list)
            for i in self.button_list:
                if i in self.buttons_hovered:
                    i.scale = 1.1
                else:
                    i.scale = 1

            if self.car_status == "clicked":
                angle_to_catapult = arcade.math.get_angle_radians(x, y, self.car_spawn_x, self.car_spawn_y)
                distance_to_catapult = arcade.math.clamp(arcade.math.get_distance(x, y, self.car_spawn_x, self.car_spawn_y), 0, 25)

                self.car.center_x = self.car_spawn_x - math.sin(angle_to_catapult)*distance_to_catapult
                self.car.center_y = self.car_spawn_y - math.cos(angle_to_catapult)*distance_to_catapult





    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            
            # Check for buttons being clicked
            self.buttons_clicked = self.buttons_hovered
            for i in self.buttons_clicked:
                i.scale = 0.9

            # Check for player
            if arcade.get_sprites_at_point((x, y), self.player):
                self.car_status = "clicked"
                self.GRAVITY = 0.4

                

            


        
    def on_mouse_release(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            if self.car_status == "clicked":
                self.car_status = "flying"
                self.car.change_y = self.car_spawn_y - self.car.center_y
                self.car.change_x = self.car_spawn_x - self.car.center_x
            print(self.buttons_clicked)
            try:
                if self.play_button in self.buttons_clicked:
                    self.change_scene(True, 1)
                if self.back_button in self.buttons_clicked:
                    self.home()
                if self.level1_button in self.buttons_clicked:
                    self.level1_button.kill()
                    self.change_scene(False, 1)
            except:
                pass
            self.buttons_clicked = []
            self.play_button.color = 255, 255, 255
                

    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()
        arcade.draw_circle_filled(self.car_spawn_x, self.car_spawn_y, 50, arcade.color.GREEN)

        self.button_list.draw()
        self.player.draw()

        # Draw the line indicator
        if self.car_status == "clicked":
            LINE_LENGTH = 40

            line_turtle = arcade.Sprite(center_x=self.car.center_x, center_y=self.car.center_y)
            line_turtle.change_y = self.car_spawn_y - self.car.center_y
            for i in range(1, LINE_LENGTH):
                arcade.draw_circle_filled(line_turtle.center_x, line_turtle.center_y, 4, arcade.color.WHITE)
                line_turtle.center_x+= self.car_spawn_x - self.car.center_x
                line_turtle.center_y += line_turtle.change_y
                line_turtle.change_y -= self.GRAVITY
            line_turtle.kill()



    def on_update(self, delta_time):
        if self.car_status == "flying":
            self.physics_engine.update()
            self.car.change_y = self.car.change_y - self.GRAVITY
            if self.car.center_x > WINDOW_WIDTH or self.car.center_y<0:
                self.change_scene(False, 1)
        if self.car_status == "clicked":
            pass





def main():
    """Main function"""
    window = GameView()
    window.home()
    arcade.run()


if __name__ == "__main__":
    main()
