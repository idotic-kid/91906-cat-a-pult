import arcade
import math
from random import randint
from arcade.particles import make_interval_emitter


# Constants
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Cat-a-pult!"
TILE_LENGTH = 40
GRAVITY = 600 #This is a different gravity from self.gravity
UPGRADES = []
screen_history = []



def get_dist(pos1, pos2):
    return arcade.math.get_distance(pos1[0], pos1[1], pos2[0], pos2[1])

def particle_burst(textures, position=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2)):
    return make_interval_emitter(
                    center_xy=position,
                    filenames_and_textures=textures,
                    emit_duration=0.2,
                    emit_interval=0.03,
                    particle_speed=2,
                    particle_lifetime_max=0.5,
                    particle_lifetime_min=0.3,
                    particle_scale=0.5,
                    fade_particles=True
                )

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
        self.claw_texture = arcade.load_texture("assets/slash.png")
        self.fish_texture = arcade.load_texture("tiles/fish.png")
        
        #load home screen buttons textures
        self.play_texture = arcade.load_texture("assets/button-play.png")

        self.buttons_hovered = []
        self.buttons_clicked = []

        self.car_status = "none"
        self.cars_left = 0
        self.fish_left = 999

        self.camera = None

        self.tilemap = None


        self.emitter = []

        


    def smooth_scale_to(self, sprite, scaleto):
        """Rescale sprite
        args:
        sprite = sprite to be rescaled
        scaleto = new scale"""
        sprite.scale_x += (scaleto-sprite.scale_x)/5
        sprite.scale_y += (scaleto-sprite.scale_y)/5




    def home(self):
        """Function for the home screen"""

        self.camera = arcade.camera.Camera2D()
        self.camera.position = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2)


        self.background_color = arcade.csscolor.BURLYWOOD

        # Make the play button sprite
        self.play_button = arcade.Sprite(self.play_texture)
        self.play_button.center_x = 200
        self.play_button.center_y = 200


        # Spritelist (I think this reduces lag?)
        self.button_list = arcade.SpriteList(True)
        self.button_list.append(self.play_button)
        
        self.player = arcade.SpriteList()
        self.fish = arcade.SpriteList()

        self.car_spawn_x = 300
        self.car_spawn_y = 200

        self.launch_line_dots = []

    def spawn_car(self, x, y, car_type="muffin"):
        self.car_status = "none"

        self.car = arcade.Sprite(self.muffin_texture)
        self.car.center_x = x
        self.car.center_y = y
        self.car.scale = 0.7
        self.player.append(self.car)
        self.scene.add_sprite("Player", self.car)



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

        # Clears scene
        self.scene = None
        self.fish_left = 999
        self.launch_line_dots = []


        # Kill all buttons
        for i in self.button_list:
            i.kill()
        
        for i in self.player:
            i.kill()

        self.map_length = 1280

        if is_menu:
            # Menu 1 screen 1 (level select)
            if screen_id == 1:
                self.background_color = arcade.csscolor.BURLYWOOD

                self.back_texture = arcade.load_texture("assets/button-back.png")
                self.l_1_texture = arcade.load_texture("assets/button-level-1.png")
                self.l_L_texture = arcade.load_texture("assets/button-level-locked.png")

                self.back_button = arcade.Sprite(self.back_texture)
                self.back_button.center_x = 50
                self.back_button.center_y = WINDOW_HEIGHT-50

                self.level1_button = arcade.Sprite(self.l_1_texture)
                self.level1_button.center_x = WINDOW_WIDTH/2
                self.level1_button.center_y = WINDOW_HEIGHT/2

                self.level2_button = arcade.Sprite(self.l_L_texture)
                self.level2_button.center_x = WINDOW_WIDTH/2
                self.level2_button.center_y = WINDOW_HEIGHT/2 - 150

                self.level3_button = arcade.Sprite(self.l_L_texture)
                self.level3_button.center_x = WINDOW_WIDTH/2
                self.level3_button.center_y = WINDOW_HEIGHT/2 - 300

                self.button_list.append(self.back_button)
                self.button_list.append(self.level1_button)
                self.button_list.append(self.level2_button)
                self.button_list.append(self.level3_button)

            # level win screen
            if screen_id == 5:
                pass

        else:
            self.background_color = (124, 244, 255)

            # Loading textures
            self.pause_texture = arcade.load_texture("assets/button-pause.png")
            self.pause_button = arcade.Sprite(self.pause_texture)

            self.wood_textures = []
            self.wood_textures.append(arcade.load_texture("tiles/wood.png"))
            self.wood_textures.append(arcade.load_texture("assets/wood_dmg_1.png"))
            self.wood_textures.append(arcade.load_texture("assets/wood_dmg_0.png"))


            # Loading tilemap
            self.tile_map = arcade.load_tilemap(
                f"tiles/level-{screen_id}.tmx",
                layer_options=layer_options,
            )
            
            self.map_length = self.tile_map.width*self.tile_map.tile_width

            # Load spritelists in
            self.wood = self.tile_map.sprite_lists["bits"]
            self.ground_sprlist = self.tile_map.sprite_lists["ground"]
            self.fish = self.tile_map.sprite_lists["fish"]

            for i in self.wood:
                i.hp = 3
                i.type = i.texture

            self.fish_left = len(self.fish)

            self.scene = arcade.Scene.from_tilemap(self.tile_map)


            # Adding sprites to the physics engine
            self.physics_engine = arcade.PymunkPhysicsEngine(gravity=(0, -GRAVITY))

            self.physics_engine.add_sprite_list(
                self.ground_sprlist,
                friction=0.5,
                collision_type="wall",
                body_type=arcade.PymunkPhysicsEngine.STATIC, elasticity=1
            )
            self.physics_engine.add_sprite_list(
                self.wood, collision_type="bricks", friction=3
            )
            self.physics_engine.add_sprite_list(
                self.fish, collision_type="fish"
            )


            # Spawn player
            self.spawn_car(self.car_spawn_x, self.car_spawn_y)


            # Level 1
            
            if screen_id == 1:
                self.cars_left = 5


            




    
    def on_mouse_motion(self, x, y, dx, dy):
        # Check if the mouse cursor collides with the button sprite
        self.buttons_hovered = arcade.get_sprites_at_point((x, y), self.button_list)

        if self.car_status == "clicked":
            angle_to_catapult = arcade.math.get_angle_radians(x, y, self.car_spawn_x, self.car_spawn_y)
            distance_to_catapult = arcade.math.clamp(arcade.math.get_distance(x, y, self.car_spawn_x, self.car_spawn_y), 0, 25)

            self.car.center_x = self.car_spawn_x - math.sin(angle_to_catapult)*distance_to_catapult
            self.car.center_y = self.car_spawn_y - math.cos(angle_to_catapult)*distance_to_catapult




    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            
            # Check for buttons being clicked
            self.buttons_clicked = self.buttons_hovered

            # Check for player
            if self.car_status == "none" and arcade.get_sprites_at_point((x, y), self.player):
                self.car_status = "clicked"

        else:
            pass


        
    def on_mouse_release(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            if self.car_status == "clicked":
                self.cars_left -=1
                self.car_status = "flying"
                self.car.lifetime = 5.0
                self.physics_engine.add_sprite(self.car, collision_type="player", elasticity=0.5)
                self.launch_line_dots = []
                self.physics_engine.apply_force(self.car, ((self.car_spawn_x - self.car.center_x)*2000, (self.car_spawn_y - self.car.center_y)*2000))
                
                #((self.car_spawn_x - self.car.center_x)*1000, (self.car_spawn_y - self.car.center_y)*1000)
                
            print(self.buttons_clicked)

            # Button click event scripts
            try:
                if self.play_button in self.buttons_clicked:
                    self.change_scene(True, 1)
                if self.back_button in self.buttons_clicked:
                    self.home()
                if self.level1_button in self.buttons_clicked:
                    self.level1_button.kill()
                    for i in self.button_list:
                        i.kill()
                    self.change_scene(False, 1)
            except:
                pass
            self.buttons_clicked = []
            self.play_button.color = 255, 255, 255
                

    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()

        if self.emitter:
            for i in self.emitter:
                i.draw()
        
        self.button_list.draw()

        # Draw the line indicator
        if self.car_status == "clicked":
            LINE_LENGTH = 10
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


        # Draw active trail
        for i in self.launch_line_dots:
            arcade.draw_circle_filled(i[0], i[1], 4, (255, 255, 255))

        # Draw our level scene
        try:
            self.scene.draw()
            arcade.draw_text(f"cars left {self.cars_left}", 100, 100, font_size=30)

            # debug hitbox
            #self.scene.draw_hit_boxes()

        except:
            pass

        self.camera.use()

        
            


    def on_update(self, delta_time):
        self.camera.position = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2)

        if self.emitter:
            for i in self.emitter:
                i.update()

        if self.fish_left <= 0:
            self.fish_left -= delta_time
            if self.fish_left <= -1:
                self.change_scene(True, 1)

        # Button smooth animation
        for i in self.button_list:
            if i in self.buttons_clicked:
                self.smooth_scale_to(i, 0.9)
            elif i in self.buttons_hovered:
                self.smooth_scale_to(i, 1.1)
            else:
                self.smooth_scale_to(i, 1)

        try:
            self.physics_engine.step()

            # Camera movement if past middle
            self.camera.position = (arcade.math.clamp(self.car.center_x, WINDOW_WIDTH/2, self.map_length-(WINDOW_WIDTH/2)), WINDOW_HEIGHT/2)
            
            if not self.car_status in "none clicked":
                if not self.launch_line_dots or get_dist(self.car.position, self.launch_line_dots[-1])>35:
                    self.launch_line_dots.append(self.car.position)

            # Claw attack code stuff here
            self.claw.lifetime -= delta_time
            if self.claw.lifetime <= 0:
                self.claw.kill()
                self.claw = None

            if self.car_status == "attacked":
                self.claw.position = self.car.position
                self.claw.angle += self.claw.va
                self.claw.va += self.claw.aa

        
            wood_hit = arcade.check_for_collision_with_list(self.claw, self.wood)
            
            for i in wood_hit:
                i.hp -=1

            for i in self.wood:
                if i.hp <= 0:
                    i.kill()
                    i = None
            
            fish_hit = arcade.check_for_collision_with_list(self.claw, self.fish)
            for i in fish_hit:
                i.kill()
                self.emitter.append(particle_burst((self.fish_texture, self.fish_texture), i.position))
                i = None
                self.fish_left -= 1

        except:
            pass

        if self.car_status == "flying":
            # If close to fish, use claw
            for i in self.fish:
                if arcade.get_distance_between_sprites(self.car, i) <= 250:
                    print("close")
                    self.car_status = "attacking"

        # Cat despawn and respawn
        try:
            self.car.lifetime -= delta_time
            if self.car.lifetime <= 0:
                self.emitter.append(particle_burst((self.muffin_texture, self.muffin_texture), self.car.position))
                self.car.kill()
                self.car = None
                if self.cars_left>0:
                    self.spawn_car(self.car_spawn_x, self.car_spawn_y)
        except:
            pass
                
        # Spawn attack
        if self.car_status == "attacking":
            self.car_status = "attacked"
            self.claw = arcade.Sprite(self.claw_texture)
            self.claw.lifetime = 0.6
            self.claw.position = self.car.position
            self.claw.angle = self.car.angle + 90

            # Nicely named variables for the code
            self.claw.va = 30
            self.claw.aa = -1
            self.scene.add_sprite("claw attack", self.claw)









def main():
    """Main function"""
    window = GameView()
    window.home()
    arcade.run()


if __name__ == "__main__":
    main()
