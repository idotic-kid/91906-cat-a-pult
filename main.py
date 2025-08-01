import arcade
import math
from random import randint
from arcade.particles import make_interval_emitter
from arcade.gui import UITextureButton, UIManager

# Constants
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Cat-a-pult!"
TILE_LENGTH = 40
FONT_SIZE = 30
GRAVITY = 600
LAST_LEVEL = 3
UPGRADES = []
current_level = 0
screen_history = []
file = open("save_state.txt")



def get_dist(pos1, pos2):
    '''arcade get distance but with 2 tuples instead of 4 numbers
    args
    pos1 (tuple) the first x and y coords
    pos2 (tuple the second x and y coords
    outputs the distance as a number'''
    return arcade.math.get_distance(pos1[0], pos1[1], pos2[0], pos2[1])

def particle_burst(textures,position=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2)):
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


class Button(UITextureButton):
    def __init__(self, scene, parent, x = 0, y = 0,
                 texture = None, text = "",):
        super().__init__(x=x, y=y, texture=texture, text=text)
        self.scene = scene
        self.click_status = "normal"
        self.parent = parent

        self.original_position = (x, y)
        self.original_width = self.width
        self.original_height = self.height
        self.current_scale = 1.0
        self.target_scale = 1.0

    def on_update(self, delta_time):
        self.click_status = self.get_current_state()
        
        if self.click_status == "press":
            self.target_scale = 0.9
        elif self.click_status == "hover":
            self.target_scale = 1.1
        else:  
            self.target_scale = 1.0
            
        self.current_scale += (self.target_scale - self.current_scale)/5
        self.width = self.original_width * self.current_scale
        self.height = self.original_height * self.current_scale
        self.center_x = self.original_position[0]
        self.center_y = self.original_position[1]

    def on_click(self, event):
        self.parent.disable()
        self.parent.window.show_view(self.scene)



class IntroCutscene(arcade.View):
    def __init__(self):
        ''' Initialize everything'''
        super().__init__()
        
        self.timer = 0
        self.comic_panel = 0

        self.comic = arcade.BasicSprite(
            arcade.load_texture("assets/comic.png"),
            center_x=1000,
            center_y=-420,
            scale=0.65
        )
        self.comic_spritelist = arcade.SpriteList()
        self.comic_spritelist.append(self.comic)

        self.skip_text = arcade.Text(
            "click anywhere to skip",
            color=(50, 161, 255),
            x = (WINDOW_WIDTH-30),
            y = 30,
            font_size=FONT_SIZE,
            anchor_x="right",
        )

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)
    
    def on_draw(self):
        self.clear()
        self.comic_spritelist.draw()
        #arcade.draw_rect_filled(self.skip_text_rect(0, 0, 0, 0.5))
        self.skip_text.draw()
    
    def on_mouse_release(self, x, y, button, modifiers):
        self.comic_panel = "done"
        
    
    def on_update(self, delta_time):
        self.timer += delta_time


        # isnt it supposed to be switch case
        # anyways this is my massive if else for the cutscene
        # it moves the comic to each panel
        # self.comic_panel variable refers to which panel is being shown 
        # the decimal points are just to help me make better timings
        match self.comic_panel:
            case 0:
                if self.timer >=0.5:
                    self.comic_panel = 1

            case 1:
                self.comic.scale_x += delta_time/5
                self.comic.scale_y += delta_time/5
                self.comic.center_y -= delta_time*250
                self.comic.center_x += delta_time *100            
                if self.comic.scale_x >= 0.8:
                    self.comic_panel = 1.5

            case 1.5:
                if self.timer >= 2:
                    self.comic_panel = 2
                    self.timer = 0
        
            case 2:
                # muffin walking
                self.comic.center_x -= 12

                if self.comic.center_y >= -640:
                    self.comic.center_y -= 3

                if self.comic.center_x <= -200:
                    self.comic_panel = 2.2
                    self.timer = 0
            
            case 2.2:
                if self.timer >= 0.3:
                    self.comic_panel = 2.4
            
            case 2.4:
                # cupcake walking
                self.comic.center_x -= 10
                if self.comic.center_x <= -1300:
                    self.comic_panel = 2.6
            
            case 2.6:

                # zoom out until it fits panel 3
                self.comic.scale_x -= delta_time/5
                self.comic.scale_y -= delta_time/5
                self.comic.center_y += delta_time*250
                self.comic.center_x += delta_time*500
        
                if self.comic.scale_x <= 0.6:
                    self.comic_panel = 2.8
                    self.timer = 0

            case 2.8:
                if self.timer >= 0.5:
                    self.comic_panel = 3
                    self.timer = 0

            case 3:
                # move down, zoom out
                self.comic.center_y += 8
                self.comic.center_x += 0.8

                self.comic.scale_x -= 0.0004
                self.comic.scale_y -= 0.0004
        
                if self.comic.center_y >= 900:
                    self.comic_panel = 3.5
                    self.timer = 0

            case 3.5:
                if self.timer >= 0.5:
                    self.comic_panel = 4
                    self.timer = 0

            case 4:
                self.comic.center_x += 15
                self.comic.center_y -= 2
                
                if self.comic.center_x >= 20:
                    self.comic_panel = 4.5
                    self.timer = 0
            
            case 4.5:
                if self.timer >= 0.5:
                    self.comic_panel = 5
                    self.timer = 0

            case 5:
                self.comic.center_x += 15
                self.comic.center_y += 2
                
                if self.comic.center_x >= 750:
                    self.comic_panel = 5.5
                    self.timer = 0

            case 5.5:
                if self.timer >= 0.5:
                    self.comic_panel = 6
                    self.timer = 0

            case 6:
                self.comic.center_x += 10
                self.comic.center_y += 2
                if self.comic.center_x >= 1900:
                    self.comic_panel = 6.3

            case 6.3:
                # slowly move up
                self.comic.center_y -= 3

                if self.comic.center_y <= 400:
                    self.comic_panel = 6.6

            case 6.6:
                self.comic.scale_x += delta_time/4
                self.comic.scale_y += delta_time/4
                self.comic.center_y -= delta_time*100
                self.comic.center_x += delta_time*600
                if self.comic.scale_x >= 1:
                    self.comic_panel = "done"

            case _:
                # I really could pass this as an argument into gameview 
                # but
                # I really couldn't be bothered at this point
                global current_level
                current_level = 1
                self.window.show_view(GameView())






class MenuView(arcade.View):
    def __init__(self, menu):
        '''Initialise the view (I don't think this is actually necessary)'''
        super().__init__()
        self.current_menu = menu


    def on_show_view(self):
        '''When first switched to this view run this code yk'''

        # Background color duh
        self.window.background_color = arcade.csscolor.BURLYWOOD

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        self.window.default_camera.use()

        # Button handling but good
        self.manager = UIManager()
        self.manager.enable()

        if self.current_menu == "title":
            self.new_run_button = Button(
                IntroCutscene(),
                self,
                WINDOW_WIDTH/2,
                WINDOW_HEIGHT/2 - 150,
                arcade.load_texture("assets/button-play.png"),
            )
            self.logo = arcade.BasicSprite(
                arcade.load_texture("assets/logo.png"),
                scale=0.3,
                center_x=WINDOW_WIDTH/2,
                center_y=WINDOW_HEIGHT/2+50,
                )
            self.logo_spritelist = arcade.SpriteList()
            self.logo_spritelist.append(self.logo)
            self.manager.add(self.new_run_button)

        elif self.current_menu == "sigma":

            self.back_texture = arcade.load_texture("assets/button-back.png")
            self.l_1_texture = arcade.load_texture("assets/button-level-1.png")
            self.l_L_texture = arcade.load_texture("assets/button-level-locked.png")
                
            self.level_1_button = Button(
                GameView(),
                self,
                WINDOW_WIDTH/2,
                WINDOW_HEIGHT/2, 
                arcade.load_texture("assets/button-level-1.png"),
            )
            self.manager.add(self.level_1_button)


    def on_draw(self):
        """ Draw this view """
        self.clear()

        if self.current_menu == "title":
            self.logo_spritelist.draw()
        
        self.manager.draw()

    def on_update(self, delta_time):
        self.manager.on_update(delta_time)




class GameView(arcade.View):
    '''The Game'''

    def __init__(self):
        # Call the parent class and set up the window

        super().__init__()
        self.highscore = 0

        self.background_color = arcade.csscolor.BURLYWOOD
        self.muffin_texture = arcade.load_texture("assets/muffin.png")
        self.claw_texture = arcade.load_texture("assets/slash.png")
        self.fish_texture = arcade.load_texture("tiles/fish.png")

        # car and fish
        self.player = arcade.SpriteList()
        self.fish = arcade.SpriteList()
        self.car_status = "none"
        self.cars_left = 0
        self.fish_left = 999

        self.tilemap = None

        self.emitter = []

        # Setting up camera
        self.camera = arcade.camera.Camera2D()
        self.camera.position = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2)

        self.launch_line_dots = []

    def on_show_view(self):
        self.setup_level(current_level)


    def setup_car(self, x, y, car_type="muffin"):
        '''This function sets up the car
        Args:
            x (number) centre x position
            y (number) centre y position
            car_type (str) whcih cat'''
        
        self.car_status = "none"
        self.car = arcade.Sprite(
            self.muffin_texture,
            scale=0.7,
            center_x=x,
            center_y=y,
            )
        self.player.append(self.car)
        self.scene.add_sprite("Player", self.car)



    def setup_level(self, level=1):
        '''
        Call this function to change the level. Switches to a
        different pre-programmed level.
        Arguments:
            level (int) These are the screens for me to code in.
        '''

        layer_options = {
            "ground": {
                "use_spatial_hash": True
            }
        }

        # Clears scene
        self.scene = None
        self.emitter = []

        self.fish_left = 999
        self.launch_line_dots = []

        for i in self.player:
            i.kill()

        self.background_color = (124, 244, 255)

        # Loading textures
        self.pause_texture = arcade.load_texture("assets/button-pause.png")

        self.wood_textures = []
        self.wood_textures.append(arcade.load_texture("tiles/wood.png"))
        self.wood_textures.append(arcade.load_texture("assets/wood_dmg_1.png"))
        self.wood_textures.append(arcade.load_texture("assets/wood_dmg_0.png"))


        # Loading tilemap
        self.tile_map = arcade.load_tilemap(
            f"tiles/level-{level}.tmx",
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
        
        if level == 1:
            self.cars_left = 5
            self.car_spawn_x = 300
            self.car_spawn_y = 200  
        if level == 2:
            self.cars_left = 4

        if level == 3:
            self.car_spawn_x = 80
            self.car_spawn_y = 400
            self.cars_left = 6


        # Spawn player
        self.setup_car(self.car_spawn_x, self.car_spawn_y)

        # Text object
        self.cars_left_text = arcade.Text(
            f"cars left {self.cars_left}",
            100, 100, font_size=FONT_SIZE)


    def on_mouse_motion(self, x, y, dx, dy):
        '''Runs whenever the mouse moves within the window.
        I have it set to move the cat to the mouse if it's being clicked'''

        if self.car_status == "clicked":
            angle_to_catapult = arcade.math.get_angle_radians(x, y, self.car_spawn_x, self.car_spawn_y)
            distance_to_catapult = arcade.math.clamp(arcade.math.get_distance(x, y, self.car_spawn_x, self.car_spawn_y), 0, 25)
            self.car.center_x = self.car_spawn_x - math.sin(angle_to_catapult)*distance_to_catapult
            self.car.center_y = self.car_spawn_y - math.cos(angle_to_catapult)*distance_to_catapult


    def on_mouse_press(self, x, y, button, modifiers):
        '''Does stuff when the mouse pressed'''
        if button == arcade.MOUSE_BUTTON_LEFT:
            # Check for player
            if self.car_status == "none" and arcade.get_sprites_at_point((x, y), self.player):
                self.car_status = "clicked"



        
    def on_mouse_release(self, x, y, button, modifiers):
        '''Does stuff when the mouse released'''

        if button == arcade.MOUSE_BUTTON_LEFT:
            if self.car_status == "clicked":
                self.cars_left -=1
                self.car_status = "flying"
                self.car.lifetime = 5.0
                self.physics_engine.add_sprite(self.car, collision_type="player", elasticity=0.5)
                self.launch_line_dots = []
                self.physics_engine.apply_force(self.car, ((self.car_spawn_x - self.car.center_x)*2000, (self.car_spawn_y - self.car.center_y)*2000))
                
                #((self.car_spawn_x - self.car.center_x)*1000, (self.car_spawn_y - self.car.center_y)*1000)
                

    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()

        if self.emitter:
            for i in self.emitter:
                i.draw()

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
        self.scene.draw()
        self.cars_left_text.draw()

        self.camera.use()

        

    def on_update(self, delta_time):
        self.camera.position = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2)

        if self.emitter:
            for i in self.emitter:
                i.update()

        if self.fish_left <= 0:
            self.fish_left -= delta_time
            if self.fish_left <= -1:
                global current_level
                current_level +=1
                self.setup_level(current_level)

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
                if 0 <self.fish_left<999 and self.car.lifetime >= -0.1:
                    self.emitter.append(particle_burst((self.muffin_texture, self.muffin_texture), self.car.position))
                self.car.kill()
                if self.cars_left>0:
                    if self.car.lifetime <= -0.5:
                        self.car = None
                        self.setup_car(self.car_spawn_x, self.car_spawn_y)
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
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, resizable=False)
    start_view = MenuView("title")
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()
