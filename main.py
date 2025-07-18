import arcade
import math

from arcade.particles import (
    Emitter,
    LifetimeParticle,
    FadeParticle,
    EmitterIntervalWithTime,
    EmitMaintainCount,
    EmitBurst,
)


# Constants
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Cat-a-pult!"
TILE_LENGTH = 40
GRAVITY = 1500 #This is a different gravity from self.gravity
screen_history = []

TEXTURE = ":resources:images/pinball/pool_cue_ball.png" #temp


def emitter_1(pos, n=50, speed=1.0, size=0.3, a=32):
        """Burst, emit from center, particle lifetime 1.0 seconds. Copy pasted from arcade website directly lmao
        args
        pos is position
        n is number of bursts

        """
        e = Emitter(
            center_xy=pos,
            emit_controller=EmitBurst(n),
            particle_factory=lambda emitter: LifetimeParticle(
            filename_or_texture=TEXTURE,
                change_xy=arcade.rand_in_circle((0.0, 0.0), speed),
                lifetime=1.0,
                scale=size,
                alpha=a
            )   
            )
        return e

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

        self.camera = None

        self.tilemap = None
        
        self.emitter = None



    def home(self):
        """Function for the home screen"""

        self.camera = arcade.camera.Camera2D()
        self.camera.position = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2)


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
        self.car_spawn_y = 400

        self.shoots = []



    # This is an IMPORTANT FUNCTION !!!!!!!!!!!!!!!!!!!!!!!! (i made it)
    def change_scene(self, is_menu=False, screen_id=1):
        '''
        Call this function to change the 'level'. Switches to a
        different pre-programmed level.
        Arguments:
            is_menu (bool) I think this one is self-explanatory.
            screen_id (int) These are the screens for me to code in.
        '''

        layer_options = {
            "ground": {
                "use_spatial_hash": True
            }
        }

        # Kill all buttons
        for i in self.button_list:
            i.kill()
        for i in self.player:
            i.kill()

        self.map_length = 1280

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
                self.physics_engine = arcade.PymunkPhysicsEngine(gravity=(0, -GRAVITY))

                self.tile_map = arcade.load_tilemap(
                    "tiles/level-1.json",
                    layer_options=layer_options,
                )

                self.wood = self.tile_map.sprite_lists["bits"]
                self.ground_sprlist = self.tile_map.sprite_lists["ground"]
                self.fishes = self.tile_map.sprite_lists["fish"]



                self.scene = arcade.Scene.from_tilemap(self.tile_map)

                self.map_length = self.tile_map.width*self.tile_map.tile_width

                self.car_status = "none"


                self.background_color = (124, 244, 255)
                self.car = arcade.Sprite(self.muffin_texture)
                self.car.center_x = self.car_spawn_x
                self.car.center_y = self.car_spawn_y
                self.car.scale = 0.7

                self.player.append(self.car)

                self.scene.add_sprite("Player", self.car)

                self.physics_engine.add_sprite_list(
                    self.ground_sprlist,
                    friction=0.5,
                    collision_type="wall",
                    body_type=arcade.PymunkPhysicsEngine.STATIC, elasticity=1
                )

                self.physics_engine.add_sprite_list(
                    self.wood, collision_type="item", friction=3
                )
                self.physics_engine.add_sprite_list(
                    self.fishes, collision_type="item"
                )

                def test1():
                    print("hit")
                    self.emitter = emitter_1((self.car.center_x, self.car.center_y), 50, 1, 0.3, 32)

                def test2():
                    print("unhit")

                self.physics_engine.add_collision_handler("player", "ground", begin_handler=test1(), post_handler=test2())


                
    



    
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

                

            


        
    def on_mouse_release(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            if self.car_status == "clicked":
                self.car_status = "flying"
                self.car.lifetime = 5.0
                self.physics_engine.add_sprite(self.car, collision_type="player", elasticity=0.8)
                self.shoots = []
                self.physics_engine.apply_force(self.car, ((self.car_spawn_x - self.car.center_x)*3000, (self.car_spawn_y - self.car.center_y)*3000))
                
                #((self.car_spawn_x - self.car.center_x)*1000, (self.car_spawn_y - self.car.center_y)*1000)
                
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

        # Useful circle
        arcade.draw_circle_outline(self.car_spawn_x, self.car_spawn_y, 25, arcade.color.GREEN, 4)

        self.button_list.draw()

        try:
            self.scene.draw()
            
            # debug hitbox
            self.car.draw_hit_box()
        except:
            pass


        self.camera.use()

        # Draw trail
        try:
            for i in self.shoots:
                arcade.draw_circle_filled(i[0], i[1], 4, (255, 255, 255))
        except:
            pass

        # Draw the line indicator
        if self.car_status == "clicked":
            LINE_LENGTH = 40
            self.GRAVITY = 0.6
            line_turtle = arcade.Sprite(center_x=self.car.center_x, center_y=self.car.center_y)
            line_turtle.change_y = (self.car_spawn_y - self.car.center_y)
            line_turtle.change_x = (self.car_spawn_x - self.car.center_x)
            for i in range(1, LINE_LENGTH):
                arcade.draw_circle_filled(line_turtle.center_x, line_turtle.center_y, 4, arcade.color.WHITE)
                line_turtle.center_x += line_turtle.change_x
                line_turtle.center_y += line_turtle.change_y
                line_turtle.change_y -= self.GRAVITY
            line_turtle.kill()


        # Particles
        if self.emitter:
            self.emitter.draw()



    def on_update(self, delta_time):
        self.camera.position = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2)

        self.emitter=None

        try:
            self.physics_engine.step()
        except:
            pass

        if self.car_status == "flying":
            # Camera movement if past middle
            self.camera.position = (arcade.math.clamp(self.car.center_x, WINDOW_WIDTH/2, self.map_length-(WINDOW_WIDTH/2)), WINDOW_HEIGHT/2)
            self.shoots.append(self.car.position)
            
            # Despawn after 
            self.car.lifetime -= delta_time
            if self.car.lifetime <= 0:
                self.car_status = "dead"
                self.car.kill()
                self.car = None
                

        


        if self.car_status == "clicked":
            pass





def main():
    """Main function"""
    window = GameView()
    window.home()
    arcade.run()


if __name__ == "__main__":
    main()
