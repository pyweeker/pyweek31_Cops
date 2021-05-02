"""
Platformer Game
"""
import arcade
import random
import math
import os

#from custom_named_sprite import SpriteWithHealth, Dog, MyCustomNamedSprite, MyBirdySprite, BouncingSprite, Explosion

from arcade.experimental.camera import Camera2D

from arcade import Point, Vector
from arcade.utils import _Vec2

import time

import pyglet


print("\n\n\n     * * *   https://www.kenney.nl/    FREE ASSETS   * * *")



# Constants
SCREEN_WIDTH = 1800 #1000
SCREEN_HEIGHT = 1000 #650
SCREEN_TITLE = "Gendarmerie"

# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 1
TILE_SCALING = 0.5
COIN_SCALING = 0.5
SCALE = 0.5

SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = (SPRITE_PIXEL_SIZE * TILE_SCALING)

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 10
GRAVITY = 1
PLAYER_JUMP_SPEED = 20


LEFT_VIEWPORT_MARGIN = SCREEN_WIDTH // 2
RIGHT_VIEWPORT_MARGIN = SCREEN_WIDTH // 2
BOTTOM_VIEWPORT_MARGIN = SCREEN_HEIGHT // 2
TOP_VIEWPORT_MARGIN = SCREEN_HEIGHT // 2


MOVEMENT_SPEED = PLAYER_MOVEMENT_SPEED
MOVEMENT_SPEED_AMPHET = MOVEMENT_SPEED * 3


AMPHET_TIME_MAX = 60 * 10

BULLET_SPEED = 7
GRENADE_SPEED = 6

LACRYMO_SPEED = 4


HEALTHBAR_WIDTH = 50
HEALTHBAR_HEIGHT = 3
HEALTHBAR_OFFSET_Y = -30
LIFEBAR_Yoffset = 30

HEALTH_NUMBER_OFFSET_X = -10
HEALTH_NUMBER_OFFSET_Y = -25

ENEMY_MAX_HEALTH = 20

PLAYER_MAX_HEALTH = 141

LASER_DAMMAGE = 15
GRENADE_DAMMAGE = 150


MAX_DISTANCE_DOG_DETECTION = SCREEN_HEIGHT


LIVES_AT_START = 3


AMMO_MAX = 50
AMMO_GLOCK_START = 30

AMMO_GRENADE_START = 10

AMMO_GLOCK_PACK = 20
AMMO_GRENADE_PACK = 3

MEDIKIT_HEALTH_BOOST = PLAYER_MAX_HEALTH // 2

LEFT_MOUSE_BTN = 1
RIGHT_MOUSE_BTN = 4

SPRITE_SCALING_LASER = 0.8


ROCKET_SMOKE_TEXTURE = arcade.make_soft_circle_texture(15, arcade.color.GRAY)

CLOUD_TEXTURES = [
    arcade.make_soft_circle_texture(250, arcade.color.WHITE),
    arcade.make_soft_circle_texture(250, arcade.color.LIGHT_GRAY),
    arcade.make_soft_circle_texture(250, arcade.color.LIGHT_BLUE),
]



MUSIC_INTRO = "resources/sounds/bb_intro_8sec.wav"

MUSIC_GAMEOVER = "resources/sounds/evil_laugh.wav"

MUSIC_INGAME = "resources/sounds/bb_111_bpm.ogg"


DISPLAY_YOFFSET_SCORE = 150
DISPLAY_YOFFSET_AMMO = 175
DISPLAY_YOFFSET_GRENADE = 200










# *************************************************************

HEALTHBAR_WIDTH = 50
HEALTHBAR_HEIGHT = 3
HEALTHBAR_OFFSET_Y = -30
LIFEBAR_Yoffset = 30

HEALTH_NUMBER_OFFSET_X = -10
HEALTH_NUMBER_OFFSET_Y = -25


CROSSHAIR__RELATIVE_XOFFSET_SETUP = 0
CROSSHAIR__RELATIVE_YOFFSET_SETUP = 100

XRESPAWN = SCREEN_WIDTH // 2
YRESPAWN = SCREEN_HEIGHT // 2


RADAR_RADIUS_DETECTION = 512

ECLOSION_TIME_INTERVAL = 15.0
ECLOSION_MAX_WAVES = 3



class SpriteWithHealth(arcade.Sprite):
    """ Sprite with hit points """

    def __init__(self, image, scale, max_health):
        super().__init__(image, scale)

        # Add extra attributes for health
        self.max_health = max_health
        self.cur_health = max_health

        # Load sounds. Sounds from kenney.nl
        self.gun_sound = arcade.load_sound(":resources:sounds/hurt5.wav")
        self.hit_sound = arcade.load_sound(":resources:sounds/hit4.wav")
        self.death_sound = arcade.load_sound(":resources:sounds/hit5.wav")

        self.respawning = 0


    def respawn(self, xrespawn, yrespawn):
        """
        Called when we die and need to make a new ship.
        'respawning' is an invulnerability timer.
        """
        # If we are in the middle of respawning, this is non-zero.
        self.respawning = 1
        #self.center_x = SCREEN_WIDTH / 2
        #self.center_y = SCREEN_HEIGHT / 2

        self.center_x = xrespawn
        self.center_y = yrespawn

        self.angle = 0

        self.cur_health = self.max_health


    def draw_health_number(self):
        """ Draw how many hit points we have """

        health_string = f"{self.cur_health}/{self.max_health}"
        arcade.draw_text(health_string,
                         start_x=self.center_x + HEALTH_NUMBER_OFFSET_X,
                         start_y=self.center_y + HEALTH_NUMBER_OFFSET_Y,
                         font_size=12,
                         color=arcade.color.WHITE)

    def draw_health_bar(self):
        """ Draw the health bar """

        # Draw the 'unhealthy' background
        if self.cur_health < self.max_health:
            arcade.draw_rectangle_filled(center_x=self.center_x,
                                         center_y=self.center_y + HEALTHBAR_OFFSET_Y,
                                         width=HEALTHBAR_WIDTH,
                                         height=3,
                                         color=arcade.color.RED)

        # Calculate width based on health
        health_width = HEALTHBAR_WIDTH * (self.cur_health / self.max_health)

        arcade.draw_rectangle_filled(center_x=self.center_x - 0.5 * (HEALTHBAR_WIDTH - health_width),
                                     center_y=self.center_y - LIFEBAR_Yoffset,
                                     width=health_width,
                                     height=HEALTHBAR_HEIGHT,
                                     color=arcade.color.GREEN)







class Dog(SpriteWithHealth):


    def __init__(self, image, scale, max_health):
        super().__init__(image, scale, max_health)

        # Add extra attributes for health
        self.max_health = max_health
        self.cur_health = max_health

        self.path = None
        




    @property
    def distance_player(self, target_sprite): #target will be player in this game , property instead of attribute for fresh values

        dist = math.hypot(self.center_x - target_sprite.center_x, self.center_y - target_sprite.center_y)

        return dist




class Explosion(arcade.Sprite):
    

    def __init__(self, texture_list,x,y):
        
        super().__init__()

        self.center_x = x
        self.center_y = y
        
        self.current_texture = 0      
        self.textures = texture_list  
        self.set_texture(self.current_texture)

    def update(self):

        
        self.current_texture += 1
        if self.current_texture < len(self.textures):
            self.set_texture(self.current_texture)
        else:
            self.kill()


#***************************************************************

def clamp(a, low, high):
    if a > high:
        return high
    elif a < low:
        return low
    else:
        return a


class AnimatedAlphaParticle(arcade.LifetimeParticle):
    """A custom particle that animates between three different alpha levels"""

    def __init__(
            self,
            filename_or_texture: arcade.FilenameOrTexture,
            change_xy: Vector,
            start_alpha: int = 0,
            duration1: float = 1.0,
            mid_alpha: int = 255,
            duration2: float = 1.0,
            end_alpha: int = 0,
            center_xy: Point = (0.0, 0.0),
            angle: float = 0,
            change_angle: float = 0,
            scale: float = 1.0,
            mutation_callback=None,
    ):
        super().__init__(filename_or_texture, change_xy, duration1 + duration2, center_xy, angle, change_angle, scale,
                         start_alpha, mutation_callback)
        self.start_alpha = start_alpha
        self.in_duration = duration1
        self.mid_alpha = mid_alpha
        self.out_duration = duration2
        self.end_alpha = end_alpha

    def update(self):
        super().update()
        if self.lifetime_elapsed <= self.in_duration:
            u = self.lifetime_elapsed / self.in_duration
            self.alpha = clamp(arcade.lerp(self.start_alpha, self.mid_alpha, u), 0, 255)
        else:
            u = (self.lifetime_elapsed - self.in_duration) / self.out_duration
            self.alpha = clamp(arcade.lerp(self.mid_alpha, self.end_alpha, u), 0, 255)






# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def make_star_field(star_count):
    """ Make a bunch of circles for stars. """

    shape_list = arcade.ShapeElementList()

    for star_no in range(star_count):
        x = random.randrange(SCREEN_WIDTH)
        y = random.randrange(SCREEN_HEIGHT)
        radius = random.randrange(1, 4)
        brightness = random.randrange(127, 256)
        color = (brightness, brightness, brightness)
        shape = arcade.create_rectangle_filled(x, y, radius, radius, color)
        shape_list.append(shape)

    return shape_list


def make_skyline(width, skyline_height, skyline_color,
                 gap_chance=0.70, window_chance=0.30, light_on_chance=0.5,
                 window_color=(255, 255, 200), window_margin=3, window_gap=2,
                 cap_chance=0.20):
    """ Make a skyline """

    shape_list = arcade.ShapeElementList()

    # Add the "base" that we build the buildings on
    shape = arcade.create_rectangle_filled(width / 2, skyline_height / 2, width, skyline_height, skyline_color)
    shape_list.append(shape)

    building_center_x = 0

    skyline_point_list = []
    color_list = []

    while building_center_x < width:

        # Is there a gap between the buildings?
        if random.random() < gap_chance:
            gap_width = random.randrange(10, 50)
        else:
            gap_width = 0

        # Figure out location and size of building
        building_width = random.randrange(20, 70)
        building_height = random.randrange(40, 150)
        building_center_x += gap_width + (building_width / 2)
        building_center_y = skyline_height + (building_height / 2)

        x1 = building_center_x - building_width / 2
        x2 = building_center_x + building_width / 2
        y1 = skyline_height
        y2 = skyline_height + building_height

        skyline_point_list.append([x1, y1])

        skyline_point_list.append([x1, y2])

        skyline_point_list.append([x2, y2])

        skyline_point_list.append([x2, y1])

        for i in range(4):
            color_list.append([skyline_color[0], skyline_color[1], skyline_color[2]])

        if random.random() < cap_chance:
            x1 = building_center_x - building_width / 2
            x2 = building_center_x + building_width / 2
            x3 = building_center_x

            y1 = y2 = building_center_y + building_height / 2
            y3 = y1 + building_width / 2

            shape = arcade.create_polygon([[x1, y1], [x2, y2], [x3, y3]], skyline_color)
            shape_list.append(shape)

        # See if we should have some windows
        if random.random() < window_chance:
            # Yes windows! How many windows?
            window_rows = random.randrange(10, 15)
            window_columns = random.randrange(1, 7)

            # Based on that, how big should they be?
            window_height = (building_height - window_margin * 2) / window_rows
            window_width = (building_width - window_margin * 2 - window_gap * (window_columns - 1)) / window_columns

            # Find the bottom left of the building so we can start adding widows
            building_base_y = building_center_y - building_height / 2
            building_left_x = building_center_x - building_width / 2

            # Loop through each window
            for row in range(window_rows):
                for column in range(window_columns):
                    if random.random() < light_on_chance:
                        x1 = building_left_x + column * (window_width + window_gap) + window_margin
                        x2 = building_left_x + column * (window_width + window_gap) + window_width + window_margin
                        y1 = building_base_y + row * window_height
                        y2 = building_base_y + row * window_height + window_height * .8

                        skyline_point_list.append([x1, y1])
                        skyline_point_list.append([x1, y2])
                        skyline_point_list.append([x2, y2])
                        skyline_point_list.append([x2, y1])

                        for i in range(4):
                            color_list.append((window_color[0], window_color[1], window_color[2]))

        building_center_x += (building_width / 2)

    shape = arcade.create_rectangles_filled_with_colors(skyline_point_list, color_list)
    shape_list.append(shape)

    return shape_list

# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////





class InstructionView(arcade.View):

    def __init__(self):
        
        super().__init__()
        
        self.music_intro = arcade.load_sound(MUSIC_INTRO)

        self.looping_music = True



        print("type(self.music_intro)   : ", type(self.music_intro))


        self.player_music_intro = None


        # ////
        self.stars = make_star_field(150)
        self.skyline1 = make_skyline(SCREEN_WIDTH * 5, 250, (80, 80, 80))
        self.skyline2 = make_skyline(SCREEN_WIDTH * 5, 150, (50, 50, 50))




    
    
    def on_show(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.csscolor.DARK_SLATE_BLUE)

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)

        
        

        #self.player_music_intro.EOS_LOOP = 'loop'
        self.player_music_intro = arcade.play_sound(self.music_intro)
        

        print("type(self.player_music_intro)   : ", type(self.player_music_intro))


    def on_draw(self):
        """ Draw this view """
        arcade.start_render()
        arcade.draw_text("Instructions Screen", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("Click to advance", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2-75,
                         arcade.color.WHITE, font_size=20, anchor_x="center")


        start_time = int(round(time.time() * 1000))
        arcade.start_render()

        self.stars.draw()
        self.skyline1.draw()
        self.skyline2.draw()
        end_time = int(round(time.time() * 1000))
        total_time = end_time - start_time

        arcade.draw_text(f"G E N D A R M E R I E", -150 + SCREEN_WIDTH//2, 200 + SCREEN_HEIGHT//2, arcade.color.RED, font_size = 40)

        if self.music_intro.is_complete(self.player_music_intro) is True:
            self.player_music_intro = arcade.play_sound(self.music_intro)


        arcade.draw_text(f"Click Left laser , click Right Grenade, arrows to move", 100, 10, arcade.color.YELLOW, font_size = 10)




    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, start the game. """
        game_view = GameView()
        game_view.setup(level=1)
        arcade.set_background_color(arcade.csscolor.BLACK)


        try:
            self.music_intro.stop(self.player_music_intro)
        except ValueError:
            print("music already finished")  # ValueError: list.remove(x): x not in list   media.Source._players.remove(player)

        self.window.show_view(game_view)


    def on_update(self, delta_time):
        """ Movement and game logic """
        self.skyline1.center_x -= 0.5
        self.skyline2.center_x -= 1



#--------------------------------------------------------




class GameOverView(arcade.View):
    """ View to show when game is over """

    def __init__(self):
        """ This is run once when we switch to this view """
        super().__init__()
        #self.texture = arcade.load_texture("game_over.png")


        #self.background = arcade.load_texture("./resources/images/backgrounds/game_over.jpg")
        

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)

        self.texture = arcade.load_texture("./resources/images/backgrounds/game_over.jpg")


        self.music_gameover = arcade.load_sound(MUSIC_GAMEOVER)
        #print("type(self.music_intro)   : ", type(self.music_gameover))
        self.player_music_gameover = None


    def on_show(self):

        self.player_music_gameover = arcade.play_sound(self.music_gameover)



    def on_draw(self):
        """ Draw this view """
        arcade.start_render()
        self.texture.draw_sized(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT)


        #self.texture.draw_sized(0, 0,SCREEN_WIDTH, SCREEN_HEIGHT)


    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, re-start the game. """
        game_view = GameView()
        #game_view.setup()
        game_view.setup(level=1)

        #self.music_gameover.stop(self.player_music_gameover)


        try:
            self.music_gameover.stop(self.player_music_gameover)
        except ValueError:
            print("music already finished")

        self.window.show_view(game_view)






#class MyGame(arcade.Window):
class GameView(arcade.View):



    

    def __init__(self):
    

        # Call the parent class and set up the window
        #super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, fullscreen=True)
        super().__init__()


        self.datamusic = arcade.load_sound(MUSIC_INGAME)

        self.datamusic.get_length()

        self.player_music_ingame = None


        #self.set_exclusive_mouse(True) # capture mouse ; not in view ?

        #self.set_vsync(True)

        #self.camera = Camera2D(
        #    viewport=(0, 0, self.width, self.height),
        #    projection=(0, self.width, 0, self.height),
        #)


        self.camera = Camera2D(
            viewport=(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT),
            projection=(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT),
        )

        self.mouse_pos = 0, 0

        self.crosshair_relative_xoffset = 0
        self.crosshair_relative_yoffset = 0



        

        
        #self.set_mouse_visible(True)
        self.window.set_mouse_visible(False)

       
        self.frame_count = 0


        self.coin_list = None
        self.wall_list = None

        self.startposition_list = None
        self.early_spawn_enemy_list = None

        self.pitbull_spawn_list = None

        self.radar_spawn_list = None
        self.chrono_spawn_list = None




        
        
        #self.dont_touch_list = None
        self.player_list = None
        self.life_list = None

        self.enemy_list = None

        self.radar_list = None # FRUITS OF HIS MOTHER SPAWN
        self.chrono_list = None # FRUITS OF HIS MOTHER SPAWN


        self.punk_list = None
        self.yellowvest_list = None


        self.pitbull_list = None

        self.pitbulls_paths = None

        
        self.player_sprite = None
        self.enemy_sprite = None

        self.explosion_images = []
        self.explosion_list = None

        self.smokboy_images = []
        self.smokboy_sprite = None

        self.is_smoked = bool()


        

        self.crosshair_sprite = None

        # Our physics engine
        self.physics_engine_walls = None

        #.....................................................
        self.water_list = None
        

        # This holds the background images. If you don't want changing
        # background images, you can delete this part.
        self.background = None
        #----------------------------------------
        

        self.ammo_glock_list = None
        self.ammo_grenade_list = None
        self.ammo_medikit_list = None

        self.ammo_amphet_list = None

        self.shield_list = None


        self.stairs_list = None

        self.police_bullet_list = None
        self.police_grenade_list = None


        self.terro_bullet_list = None
        self.terro_lacrymo_list = None
        #..................

        
        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        # Keep track of the score
        self.score = 0
        self.lives = 0


        self.ammo = 0
        self.ammo_text = None # ????????????????????

        self.grenade = 0
        self.grenade_text = None

        self.amphet_excited = False
        self.amphet_time_left = 0

        # Load sounds. Sounds from kenney.nl
        self.gun_sound = arcade.sound.load_sound(":resources:sounds/laser1.wav")
        self.hit_sound = arcade.sound.load_sound(":resources:sounds/phaseJump1.wav")
        self.death_sound = arcade.load_sound(":resources:sounds/hit5.wav")

        # Where is the right edge of the map?
        self.end_of_map = 0

        # Level
        self.level = 1

        # Load sounds
        self.collect_coin_sound = arcade.load_sound("resources/sounds/coin1.wav")
        self.jump_sound = arcade.load_sound("resources/sounds/jump1.wav")
        self.game_over = arcade.load_sound("resources/sounds/gameover1.wav")


        # cloud lacrymo
        self.emitters = []


        self.thanks_list = []
        self.thanks_png = None

        



    def setup(self, level):
        """ Set up the game here. Call this function to restart the game. """

        self.eclosion_remaining_waves = ECLOSION_MAX_WAVES

        arcade.schedule(self.krontab, ECLOSION_TIME_INTERVAL)

        

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        # Keep track of the score
        self.score = 0

        if self.level == 1:
            self.lives = LIVES_AT_START
        

        self.ammo = AMMO_GLOCK_START
        self.grenade = AMMO_GRENADE_START

        self.startposition_list = arcade.SpriteList()
        self.early_spawn_enemy_list = arcade.SpriteList()   # ?????????  data tmx, not sprite it self directly ???

        self.pitbull_spawn_list = arcade.SpriteList()

        self.radar_spawn_list = arcade.SpriteList() # or just python list ?
        self.chrono_spawn_list = arcade.SpriteList() # or just python list ?

        # Create the Sprite lists
        self.player_list = arcade.SpriteList()
        self.enemy_list =  arcade.SpriteList()


        self.radar_list = arcade.SpriteList()
        self.chrono_list = arcade.SpriteList()


        self.punk_list = arcade.SpriteList()
        self.yellowvest_list = arcade.SpriteList()







        self.pitbull_list =  arcade.SpriteList()

        #self.pitbulls_paths = [] # list of list in fact        https://docs.python.org/fr/3/library/typing.html

        self.life_list = arcade.SpriteList()

        #self.is_smoked = False # native from bool()
        #self.is_smoked = True #test

        self.thanks_list = arcade.SpriteList()
        self.thanks_png = f"resources/images/backgrounds/thanks.png"

        



        



        for i in range(32):  
        
                        
            texture_name = f"resources/images/explosion/explosion{i:04d}.png"
            self.explosion_images.append(arcade.load_texture(texture_name))

        self.explosion_list = arcade.SpriteList()


        self.smokboy_images = ["resources/images/fx/smokboy_half_512.png"]
        self.smokboy_sprite = arcade.SpriteList()


        self.lacrymo_image = ["resources/images/items/lacrymo_128.png"]
        self.lacrymo_sprite = arcade.SpriteList()


        self.wall_list = arcade.SpriteList(use_spatial_hash=True, spatial_hash_cell_size=128)

        self.coin_list = arcade.SpriteList()

        self.water_list = arcade.SpriteList()
        self.macadam_list = arcade.SpriteList()
        self.pave_list = arcade.SpriteList()

        #......................................................................

        self.ammo_glock_list = arcade.SpriteList()
        self.ammo_grenade_list = arcade.SpriteList()
        self.ammo_medikit_list = arcade.SpriteList()

        self.ammo_amphet_list = arcade.SpriteList()

        #self.shield_list = arcade.SpriteList()


        self.stairs_list = arcade.SpriteList(is_static=True)

        self.police_bullet_list = arcade.SpriteList()
        self.police_grenade_list = arcade.SpriteList()

        self.terro_bullet_list = arcade.SpriteList()
        self.terro_lacrymo_list = arcade.SpriteList()

        #.................................
        # --- Load in a map from the tiled editor ---

        # Name of the layer in the file that has our platforms/walls
        startposition_layer_name = 'Startposition'

        early_spawn_enemy_layer_name = 'Early_spawns'


        pitbull_spawn_layer_name = 'Pitbulls_spawns'

        radar_spawn_layer_name = 'Radar_spawns'

        chrono_spawn_layer_name = 'Chrono_spawns'


        # Name of the layer in the file that has our platforms/walls
        platforms_layer_name = 'Platforms'
        # Name of the layer that has items for pick-up
        #coins_layer_name = 'Coins'
        # Name of the layer that has items for foreground
        #foreground_layer_name = 'Foreground'
        # Name of the layer that has items for background
        #background_layer_name = 'Background'
        # Name of the layer that has items we shouldn't touch
        #dont_touch_layer_name = "Don't Touch"

        waters_layer_name = "Waters"
        macadams_layer_name = "ground_mac"
        paves_layer_name = "ground_pav"


        amphets_layer_name = "amphets"
        glocks_layer_name = "glocks"
        grenades_layer_name = "grenades"
        medikits_layer_name = "medikits"

        thanks_layer_name = "Thanks_png"

        stairs_layer_name = "Stairs"

        # Map name
  
        map_name = f"resources/tmx_maps/easymap1_level_{level}.tmx"

        # Read in the tiled map
        my_map = arcade.tilemap.read_tmx(map_name)

        # Calculate the right edge of the my_map in pixels
        self.end_of_map = my_map.map_size.width * GRID_PIXEL_SIZE

        

        # -- startposition ------------------------------------------------------------------------------------------------------------------------------------------------
        self.startposition_list = arcade.tilemap.process_layer(map_object=my_map,
                                                      layer_name=startposition_layer_name,
                                                      scaling=TILE_SCALING,
                                                      use_spatial_hash=True)

        print("---> ", self.startposition_list[0])
        print(" X ", self.startposition_list[0].center_x)
        print(" Y ", self.startposition_list[0].center_y)

        start_XY = tuple((self.startposition_list[0].center_x,self.startposition_list[0].center_y))




        image_source = "resources/images/animated_characters/policeboy_gun_128.png"

        
        #self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite = SpriteWithHealth(image_source, CHARACTER_SCALING, max_health = PLAYER_MAX_HEALTH)


        self.player_sprite.center_x = start_XY[0]
        self.player_sprite.center_y = start_XY[1]
        self.player_list.append(self.player_sprite)

        # *******************************************************************************************
        #self.life_list.append(life)

        for i in range(self.lives):
                life = arcade.Sprite("resources/images/HUD/head_128.png", SCALE)
                self.life_list.append(life)



        #----------------------------------------------------------------------------------------

        #if self.is_smoked is true:

        self.smokboy_sprite = arcade.Sprite(self.smokboy_images[0], 1)


        # ---

        self.crosshair_list = arcade.SpriteList()

        self.crosshair_sprite = arcade.Sprite("resources/images/HUD/crosshair061.png", 0.4)


        self.crosshair_relative_xoffset = CROSSHAIR__RELATIVE_XOFFSET_SETUP
        self.crosshair_relative_yoffset = CROSSHAIR__RELATIVE_YOFFSET_SETUP
      


        self.crosshair_sprite.center_x = self.player_sprite.center_x + CROSSHAIR__RELATIVE_XOFFSET_SETUP
        self.crosshair_sprite.center_y = self.player_sprite.center_y + CROSSHAIR__RELATIVE_YOFFSET_SETUP

        self.crosshair_list.append(self.crosshair_sprite)
        # ///////////

        

        #self.mouse_pos = self.crosshair_sprite.center_x, self.crosshair_sprite.center_y

        # ///////////
        # ----------------------------------------------------------------------------------------------------------------------------------

        self.early_spawn_enemy_list = arcade.tilemap.process_layer(map_object = my_map,
                                                      layer_name = early_spawn_enemy_layer_name,
                                                      scaling=TILE_SCALING,
                                                      use_spatial_hash=True)

        soldier_image_source = "./resources/images/enemies/soldier_128.png"


        for spawn in self.early_spawn_enemy_list:

            
            new_enemy = SpriteWithHealth(soldier_image_source, 1, max_health = ENEMY_MAX_HEALTH)
            new_enemy.center_x = spawn.center_x
            new_enemy.center_y = spawn.center_y
            new_enemy.angle = 0

            #new_enemy.max_health = 75

            self.enemy_list.append(new_enemy)

        # ---------******************************************

        self.pitbull_spawn_list = arcade.tilemap.process_layer(map_object = my_map,
                                                      layer_name = pitbull_spawn_layer_name,
                                                      scaling=TILE_SCALING,
                                                      use_spatial_hash=True)

        pitbull_image_source = "./resources/images/enemies/pitbull_waiting_128.png"




        self.radar_spawn_list = arcade.tilemap.process_layer(map_object = my_map,
                                                      layer_name = radar_spawn_layer_name,
                                                      scaling=TILE_SCALING,
                                                      use_spatial_hash=True)

        #radar_spawn_image_source = "./resources/images/tiles/radar_128.png"


        

                

       
            



        self.chrono_spawn_list = arcade.tilemap.process_layer(map_object = my_map,
                                                      layer_name = chrono_spawn_layer_name,
                                                      scaling=TILE_SCALING,
                                                      use_spatial_hash=True)

        #chrono_spawn_image_source = "./resources/images/tiles/foetus128.png"


        



        for spawn in self.pitbull_spawn_list:

            new_pitbull = Dog(pitbull_image_source, 0.4, max_health = ENEMY_MAX_HEALTH)
            new_pitbull.center_x = spawn.center_x
            new_pitbull.center_y = spawn.center_y
            new_pitbull.angle = 0

            self.pitbull_list.append(new_pitbull)

        len_pitbull_list = len(self.pitbull_list)
        self.pitbulls_paths = [[tuple()] for i in range(len_pitbull_list)]




        # come back



        


  




        









        #self.radar_spawn_list = arcade.SpriteList()
        #self.chrono_spawn_list = arcade.SpriteList()

        
        #debug_setup = f"debug setup MyGame self.pitbulls_paths   {self.pitbulls_paths} "
        #print(debug_setup)


        # *********************************************************************************************************************************

        self.stairs_list = arcade.tilemap.process_layer(map_object=my_map,
                                                      layer_name=stairs_layer_name,
                                                      scaling=TILE_SCALING,
                                                      use_spatial_hash=True)


        # -- Platforms
        self.wall_list = arcade.tilemap.process_layer(map_object=my_map,
                                                      layer_name=platforms_layer_name,
                                                      scaling=TILE_SCALING,
                                                      use_spatial_hash=True)

        self.water_list = arcade.tilemap.process_layer(map_object=my_map,
                                                      layer_name=waters_layer_name,
                                                      scaling=TILE_SCALING,
                                                      use_spatial_hash=True)

        self.macadam_list = arcade.tilemap.process_layer(map_object=my_map,
                                                      layer_name=macadams_layer_name,
                                                      scaling=TILE_SCALING,
                                                      use_spatial_hash=True)

        self.pave_list = arcade.tilemap.process_layer(map_object=my_map,
                                                      layer_name=paves_layer_name,
                                                      scaling=TILE_SCALING,
                                                      use_spatial_hash=True)

        #self.coin_list = arcade.tilemap.process_layer(my_map,
        #                                              coins_layer_name,
        #                                              scaling=TILE_SCALING,
        #                                              use_spatial_hash=True)

        self.ammo_amphet_list = arcade.tilemap.process_layer(my_map,
                                                      amphets_layer_name,
                                                      scaling=TILE_SCALING,
                                                      use_spatial_hash=True)

        self.ammo_glock_list = arcade.tilemap.process_layer(my_map,
                                                      glocks_layer_name,
                                                      scaling=TILE_SCALING,
                                                      use_spatial_hash=True)

        self.ammo_grenade_list = arcade.tilemap.process_layer(my_map,
                                                      grenades_layer_name,
                                                      scaling=TILE_SCALING,
                                                      use_spatial_hash=True)

        self.ammo_medikit_list = arcade.tilemap.process_layer(my_map,
                                                      medikits_layer_name,
                                                      scaling=TILE_SCALING,
                                                      use_spatial_hash=True)



        self.thanks_list = arcade.tilemap.process_layer(map_object=my_map,
                                                      layer_name= thanks_layer_name,
                                                      scaling=1,
                                                      use_spatial_hash=True)


        # -- Don't Touch Layer
        #self.dont_touch_list = arcade.tilemap.process_layer(my_map,
                                                            #dont_touch_layer_name,
                                                            #TILE_SCALING,
                                                            #use_spatial_hash=True)

        # --- Other stuff
        # Set the background color
        if my_map.background_color:
            arcade.set_background_color(my_map.background_color)

        # Create the 'physics engine'
        self.physics_engine_walls = arcade.PhysicsEngineSimple(self.player_sprite, self.wall_list)


        if self.level == 1:
            #self.background = arcade.load_texture("./resources/images/backgrounds/abstract_1.jpg")

            self.background = arcade.load_texture("./resources/images/backgrounds/jaune_uni.jpg")

            

        if self.level == 2:
            self.background = None

        if self.level == 3:
            self.background = arcade.load_texture("./resources/images/backgrounds/abstract_2.jpg")

        if self.level == 4:
            self.background = arcade.load_texture("./resources/images/backgrounds/final_background.jpg")



        




    def krontab(self, delta_time):

        #chrono_spawn_image_source = "./resources/images/tiles/foetus128.png"
        yellowvest_image_source = "./resources/images/enemies/yellowboy_128.png"

        if self.eclosion_remaining_waves > 0:

            for chrono_spawn in self.chrono_spawn_list:

                #new_enemy = SpriteWithHealth(chrono_spawn_image_source, 1, max_health = ENEMY_MAX_HEALTH)
                new_enemy = SpriteWithHealth(yellowvest_image_source, 1, max_health = ENEMY_MAX_HEALTH)
                new_enemy.center_x = chrono_spawn.center_x
                new_enemy.center_y = chrono_spawn.center_y
                new_enemy.angle = 0


                #self.chrono_list.append(new_enemy)
                self.yellowvest_list.append(new_enemy)

            self.eclosion_remaining_waves -= 1

        else:

            arcade.unschedule(krontab)




    def on_show(self):

        self.player_music_ingame = arcade.play_sound(self.datamusic)


    def on_draw(self):
        """ Render the screen. """

        # Clear the screen to the background color

        arcade.start_render()

        self.center_on_player()

        try:

            arcade.set_background_color(arcade.csscolor.BLACK)

                
            arcade.draw_lrwh_rectangle_textured(0, 0,
                                                SCREEN_WIDTH, SCREEN_HEIGHT,
                                                self.background)
        except AttributeError: # level 2 background is None , it gives 'NoneType' object has no attribute 'draw_sized'

            arcade.set_background_color(arcade.csscolor.RED)

        #self.camera.use()
        #self.clear()

        world_pos = self.camera.mouse_coordinates_to_world(*self.mouse_pos)
        arcade.draw_circle_filled(*world_pos, 10, arcade.color.BLUE)

        # Draw our sprites

        self.startposition_list.draw()        
        
        self.wall_list.draw()
        self.stairs_list.draw()

        self.water_list.draw()
        self.macadam_list.draw()
        self.pave_list.draw()

        self.ammo_amphet_list.draw()
        self.ammo_glock_list.draw()
        self.ammo_grenade_list.draw()
        self.ammo_medikit_list.draw()
        
        #self.coin_list.draw()
        #self.dont_touch_list.draw()
        self.player_list.draw()
        self.player_sprite.draw_health_number()
        self.player_sprite.draw_health_bar()

        self.life_list.draw()
        self.crosshair_list.draw()

        self.police_bullet_list.draw()
        self.police_grenade_list.draw()

        self.terro_bullet_list.draw()
        self.terro_lacrymo_list.draw()

        self.enemy_list.draw()
        self.pitbull_list.draw()

        #self.radar_list.draw()
        self.punk_list.draw()


        #self.chrono_list.draw()
        self.yellowvest_list.draw()


        self.thanks_list.draw()


        #debug_dog = f"debug_dog  self.pitbulls_paths   {self.pitbulls_paths} "
        #print(debug_dog)


        for list_of_tuple in self.pitbulls_paths:
            arcade.draw_line_strip(list_of_tuple, arcade.color.BLUE, 2)


        self.explosion_list.draw()

        if self.is_smoked is True:
            self.smokboy_sprite.draw()

        for e in self.emitters:
            e.draw()
        


        # Draw our score on the screen, scrolling it with the viewport
        score_text = f"Score: {self.score}"
        arcade.draw_text(score_text, 10 + self.view_left, DISPLAY_YOFFSET_SCORE + self.view_bottom,
                         arcade.csscolor.WHITE, 18)



        output_ammo = f"Ammo: {self.ammo}"
        #arcade.draw_text(output_ammo, 100, 400, arcade.color.RED, 20)

        arcade.draw_text(output_ammo, 10 + self.view_left, DISPLAY_YOFFSET_AMMO + self.view_bottom,
                         arcade.csscolor.YELLOW, 18)


        output_grenade = f"Grenade: {self.grenade}"
        #arcade.draw_text(output_ammo, 100, 400, arcade.color.RED, 20)

        arcade.draw_text(output_grenade, 10 + self.view_left, DISPLAY_YOFFSET_GRENADE + self.view_bottom,
                         arcade.csscolor.RED, 18)


        #self.life_list.draw()


        




        



    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        #if self.player_sprite.amphet_excited is False:
        if self.amphet_excited is False:
            if key == arcade.key.UP:
                self.player_sprite.change_y = MOVEMENT_SPEED
                self.crosshair_sprite.change_y = MOVEMENT_SPEED
                

            elif key == arcade.key.DOWN:
                self.player_sprite.change_y = -MOVEMENT_SPEED
                self.crosshair_sprite.change_y = -MOVEMENT_SPEED
                

            elif key == arcade.key.LEFT:
                self.player_sprite.change_x = -MOVEMENT_SPEED
                self.crosshair_sprite.change_x = -MOVEMENT_SPEED
                

            elif key == arcade.key.RIGHT:
                self.player_sprite.change_x = MOVEMENT_SPEED
                self.crosshair_sprite.change_x = MOVEMENT_SPEED
                



            elif key == arcade.key.ESCAPE:
                raise Exception("\n\n      See You soon, fork it share it !")


        else:

            if key == arcade.key.UP:
                self.player_sprite.change_y = MOVEMENT_SPEED_AMPHET
            elif key == arcade.key.DOWN:
                self.player_sprite.change_y = -MOVEMENT_SPEED_AMPHET
            elif key == arcade.key.LEFT:
                self.player_sprite.change_x = -MOVEMENT_SPEED_AMPHET
            elif key == arcade.key.RIGHT:
                self.player_sprite.change_x = MOVEMENT_SPEED_AMPHET


            elif key == arcade.key.ESCAPE:
                raise Exception("\n\n      See You soon, fork it share it !")



 

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0



    @property
    def distance_crosshair_player(self):

        dist = math.hypot(self.crosshair_sprite.center_x - self.player_sprite.center_x, self.crosshair_sprite.center_y - self.player_sprite.center_y)

        return dist

    
    def manage_crosshair(self):

        #if self.distance_crosshair_player > SCREEN_HEIGHT / 2:
        if self.distance_crosshair_player > SCREEN_WIDTH:

            self.crosshair_sprite.center_x = self.player_sprite.center_x
            self.crosshair_sprite.center_y = self.player_sprite.center_y



    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """Called whenever the mouse moves. """

        print(x)
        print(y)
        print(delta_x)
        print(delta_y)


        #self.manage_crosshair()
        
        

        #self.crosshair_sprite.center_x += delta_x
        #self.crosshair_sprite.center_y += delta_y


        self.crosshair_relative_xoffset += delta_x
        self.crosshair_relative_yoffset += delta_y



    def on_mouse_press(self, x, y, button, modifiers):
        """ Called whenever the mouse button is clicked. """

        print(button)
        print(type(button))
        print(modifiers)

        if button == LEFT_MOUSE_BTN and self.ammo > 0:

            # Create a bullet
            bullet = arcade.Sprite(":resources:images/space_shooter/laserBlue01.png", SPRITE_SCALING_LASER)

            # Position the bullet at the player's current location
            start_x = self.player_sprite.center_x
            start_y = self.player_sprite.center_y
            bullet.center_x = start_x
            bullet.center_y = start_y

            # Get from the mouse the destination location for the bullet
            # IMPORTANT! If you have a scrolling screen, you will also need
            # to add in self.view_bottom and self.view_left.
            

            dest_x = self.crosshair_sprite.center_x
            dest_y = self.crosshair_sprite.center_y

            # Do math to calculate how to get the bullet to the destination.
            # Calculation the angle in radians between the start points
            # and end points. This is the angle the bullet will travel.
            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            angle = math.atan2(y_diff, x_diff)

            # Angle the bullet sprite so it doesn't look like it is flying
            # sideways.
            bullet.angle = math.degrees(angle)
            print(f"Bullet angle: {bullet.angle:.2f}")

            # Taking into account the angle, calculate our change_x
            # and change_y. Velocity is how fast the bullet travels.
            bullet.change_x = math.cos(angle) * BULLET_SPEED
            bullet.change_y = math.sin(angle) * BULLET_SPEED

            # Add the bullet to the appropriate lists
            
            self.police_bullet_list.append(bullet)

            self.ammo -= 1


        if button == RIGHT_MOUSE_BTN and self.grenade > 0:


            grenade = arcade.Sprite("./resources/images/items/grenade_128_128.png", 0.4)

            start_x = self.player_sprite.center_x
            start_y = self.player_sprite.center_y
            grenade.center_x = start_x
            grenade.center_y = start_y


            dest_x = self.crosshair_sprite.center_x
            dest_y = self.crosshair_sprite.center_y
   
            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            angle = math.atan2(y_diff, x_diff)


            grenade.angle = math.degrees(angle)
            print(f"grenade angle: {grenade.angle:.2f}")


            grenade.change_x = math.cos(angle) * GRENADE_SPEED
            grenade.change_y = math.sin(angle) * GRENADE_SPEED


            self.police_grenade_list.append(grenade)

            self.grenade -= 1




    def manage_pitbulls_paths(self):

        grid_size = 128
        playing_field_left_boundary = playing_field_right_boundary = playing_field_bottom_boundary = playing_field_top_boundary = 7 * 128

        i = 0

        for dog in self.pitbull_list:

            dog_index = self.pitbull_list.index(dog)

            dist_dog_player = math.hypot(dog.center_x - self.player_sprite.center_x, dog.center_y - self.player_sprite.center_y)

            print(f"dist_dog_player with dog {dog_index}  is  {dist_dog_player} ")

            if dist_dog_player < MAX_DISTANCE_DOG_DETECTION:

                

                #if arcade.has_line_of_sight(self.player_sprite.position, dog.position,self.wall_list):
                #    color = arcade.color.RED
                #    arcade.draw_line(self.player_sprite.center_x,
                #                 self.player_sprite.center_y,
                #                 dog.center_x,
                #                 dog.center_y,
                #                 color,
                #                 2)
                #    print("LIGNE DE MIRE+++++++++++++++++++++++++++++")
                #else:
                #    print("no sight")




                new_barrier_list = arcade.AStarBarrierList(self.player_sprite,
                                                    self.wall_list,
                                                    
                                                    grid_size,
                                                    -playing_field_left_boundary,
                                                    playing_field_right_boundary,
                                                    -playing_field_bottom_boundary,
                                                    playing_field_top_boundary)

                print(f"new_barrier_list   {new_barrier_list}")
                print(f"new_barrier_list.barrier_list   {new_barrier_list.barrier_list}")
                print(f"new_barrier_list.blocking_sprites   {new_barrier_list.blocking_sprites}")
                print(f"DIR   new_barrier_list.blocking_sprites   {dir(new_barrier_list.blocking_sprites)}")



                print(dir(new_barrier_list))


                maybePath = arcade.astar_calculate_path(self.player_sprite.position,
                                                            dog.position,
                                                            #self.barrier_list,
                                                            new_barrier_list,
                                                            #diagonal_movement=False)
                                                            diagonal_movement=True)



                print(f"maybePath   {maybePath}")

                if maybePath != None:
                    self.pitbulls_paths[i] = maybePath
                else:
                    self.pitbulls_paths[i] = [tuple()]


            i+= 1

        else:
            pass


    def update(self, delta_time):
    
        """ Movement and game logic """
        self.frame_count += 1
        self.player_list.update()

        for i in range (self.lives):
            #self.life_list[i].center_x = (self.player_sprite.center_x - SCREEN_WIDTH // 2) + i * self.life_list[i].width
            #self.life_list[i].center_y = (self.player_sprite.center_x - SCREEN_HEIGHT // 2) 


            self.life_list[i].center_x = (self.player_sprite.center_x - SCREEN_WIDTH // 2) + i * self.life_list[i].width
            self.life_list[i].center_y = (self.player_sprite.center_y - SCREEN_HEIGHT // 2) 




        #xxxxxxxxxxx

        #self.player_sprite.center_x - w_width // 2,

        #xxxxxxxxxxx


        self.crosshair_sprite.center_x = self.player_sprite.center_x + self.crosshair_relative_xoffset
        self.crosshair_sprite.center_y = self.player_sprite.center_y + self.crosshair_relative_yoffset

        



        

        

        self.enemy_list.update()
        self.pitbull_list.update()

        self.manage_pitbulls_paths()

        #for dog in self.pitbull_list:
        #    dog.update_path(self.player_sprite, self.wall_list)

        self.smokboy_sprite.center_x = self.player_sprite.center_x
        self.smokboy_sprite.center_y = self.player_sprite.center_y

        emitters_to_update = self.emitters.copy()

        for e in emitters_to_update:
            e.update()
        # remove emitters that can be reaped
        to_del = [e for e in emitters_to_update if e.can_reap()]
        for e in to_del:
            self.emitters.remove(e)

        # Move the player with the physics engine
        self.physics_engine_walls.update()
        self.stairs_list.update()


        self.ammo_glock_list.update_animation(delta_time)

        current_room_ammo_glock_list = self.ammo_glock_list

        current_room_ammo_glock_list.update()

        # Generate a list of all sprites that collided with the player.
        ammo_glock_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                              self.ammo_glock_list)

        # Loop through each colliding sprite, remove it, and add to the score.
        for glock in ammo_glock_hit_list:
            print("\n\n just hit a glock !!! ..........")
            glock.remove_from_sprite_lists()
            self.ammo += AMMO_GLOCK_PACK

        #--------------- --------------            ----------   ------------------------
        current_room_ammo_grenade_list = self.ammo_grenade_list

        #self.ammo_glock_list.update()
        current_room_ammo_grenade_list.update()

        # Generate a list of all sprites that collided with the player.
        ammo_grenade_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                              current_room_ammo_grenade_list)

        # Loop through each colliding sprite, remove it, and add to the score.
        for grenade in ammo_grenade_hit_list:
            grenade.remove_from_sprite_lists()
            self.grenade += AMMO_GRENADE_PACK


        current_room_ammo_medikit_list = self.ammo_medikit_list

        #self.ammo_glock_list.update()
        current_room_ammo_medikit_list.update()

        # Generate a list of all sprites that collided with the player.
        ammo_medikit_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                              current_room_ammo_medikit_list)

        # Loop through each colliding sprite, remove it, and add to the score.
        for medikit in ammo_medikit_hit_list:
            medikit.remove_from_sprite_lists()
            #self.health += MEDIKIT_HEALTH_BOOST
            #player.cur_health += MEDIKIT_HEALTH_BOOST
            self.player_sprite.cur_health += MEDIKIT_HEALTH_BOOST


        current_room_ammo_amphet_list = self.ammo_amphet_list

        #self.ammo_glock_list.update()
        current_room_ammo_amphet_list.update()

        # Generate a list of all sprites that collided with the player.
        ammo_amphet_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                              current_room_ammo_amphet_list)

        # Loop through each colliding sprite, remove it, and add to the score.
        for amphet in ammo_amphet_hit_list:
            amphet.remove_from_sprite_lists()
            #self.health += MEDIKIT_HEALTH_BOOST
            #player.cur_health += MEDIKIT_HEALTH_BOOST
            self.amphet_excited = True
            self.amphet_time_left  = AMPHET_TIME_MAX



        # Generate a list of all sprites that collided with the player.
        stairs_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                              self.stairs_list)

        for stairs in stairs_hit_list:
            self.level += 1
            self.is_smoked = False
            # Load the next level
            self.setup(self.level) #  .............?????????.........

            # Set the camera to the start
            self.view_left = 0
            self.view_bottom = 0
            changed_viewport = True



        self.police_bullet_list.update() # ????
        self.police_grenade_list.update() # ??????

        self.terro_bullet_list.update()
        self.terro_lacrymo_list.update()

        # /////////////////////////////////////////////////////////////////////////////////////////// COMBAT
        for bullet in self.police_bullet_list:
            if bullet.top < 0:
                bullet.remove_from_sprite_lists()


            # Check this bullet to see if it hit a coin
            hit_list = arcade.check_for_collision_with_list(bullet, self.enemy_list)

            # If it did, get rid of the bullet
            if len(hit_list) > 0:
                bullet.remove_from_sprite_lists()

            # For every coin we hit, process
            for enemy in hit_list:
                # Make sure this is the right type of class
                #if not isinstance(enemy, SpriteWithHealth): # ? ? ?
                #    raise TypeError("List contents must be all ints")

                # Remove one health point
                enemy.cur_health -= LASER_DAMMAGE

                # Check health
                if enemy.cur_health <= 0:
                    # Dead
                    enemy.remove_from_sprite_lists()
                    self.score += 1
                    arcade.play_sound(self.death_sound)
                else:
                    # Not dead
                    arcade.play_sound(self.hit_sound)


        #----

        for grenade in self.police_grenade_list:
            if grenade.top < 0:
                grenade.remove_from_sprite_lists()


            # Check this bullet to see if it hit a coin
            #hit_list = arcade.check_for_collision_with_list(grenade, self.enemy_list)
            enemy_hit_list = arcade.check_for_collision_with_list(grenade, self.enemy_list)

            # If it did, get rid of the bullet
            #if len(hit_list) > 0:
            if len(enemy_hit_list) > 0:
                grenade.remove_from_sprite_lists()

            # For every coin we hit, process
            #for enemy in hit_list:
            for enemy in enemy_hit_list:
                #e = Explosion(self.explosion_images,self.player_sprite.center_x,self.player_sprite.center_y)
                e = Explosion(self.explosion_images,enemy.center_x,enemy.center_y)
                self.explosion_list.append(e)
                e.update()



                # Make sure this is the right type of class
                if not isinstance(enemy, SpriteWithHealth):
                    raise TypeError("List contents must be all ints")

                # Remove one health point
                enemy.cur_health -= GRENADE_DAMMAGE

                # Check health
                if enemy.cur_health <= 0:
                    # Dead
                    enemy.remove_from_sprite_lists()
                    self.score += 1
                    arcade.play_sound(self.death_sound)
                else:
                    # Not dead
                    arcade.play_sound(self.hit_sound)

  
            #grenade.center_x += 0.5 * grenade.change_x
            grenade_wall_hit_list = arcade.check_for_collision_with_list(grenade, self.wall_list)

            for wall in grenade_wall_hit_list:
                #print(grenade.angle)
                #x=1/0
                if grenade.change_x > 0:
                    grenade.right = wall.left
                    grenade.change_x *= -1
                    #bullet.check_bounce_or_kill()
                elif grenade.change_x < 0:
                    grenade.left = wall.right
                    grenade.change_x *= -1
                    #bullet.check_bounce_or_kill()
            
            #if len(grenade_wall_hit_list) > 0:
            #    grenade.change_x *= -1

            #    grenade.change_y *= -1



            #grenade.center_y += grenade.change_y
            grenade_wall_hit_list = arcade.check_for_collision_with_list(grenade, self.wall_list)

            for wall in grenade_wall_hit_list:
                if grenade.change_y > 0:
                    grenade.top = wall.bottom
                    grenade.change_y *= -1
                    #bullet.check_bounce_or_kill()
                elif grenade.change_y < 0:
                    grenade.bottom = wall.top
                    grenade.change_y *= -1
                    #bullet.check_bounce_or_kill()
            
            #if len(grenade_wall_hit_list) > 0:
            #    grenade.change_y *= -1

            #    grenade.change_x *= -1

        # /////////////////////////////////////////////////

        for explosion in self.explosion_list:
            try:
                explosion.update()
            except:
                print("explosion bug ...")

        # ---------------------______________________________________________

        for bullet in self.terro_bullet_list:
            if bullet.top < 0:
                bullet.remove_from_sprite_lists()


            # Check this bullet to see if it hit a coin
            hit_list = arcade.check_for_collision_with_list(bullet, self.player_list)

            # If it did, get rid of the bullet
            if len(hit_list) > 0:
                bullet.remove_from_sprite_lists()

            # For every coin we hit, process
            for player in hit_list:
                # Make sure this is the right type of class
                if not isinstance(player, SpriteWithHealth):
                    raise TypeError("List contents must be all ints")

                # Remove one health point
                player.cur_health -= LASER_DAMMAGE


                # Check health
                if player.cur_health <= 0:
                    if self.lives > 0:
                        self.lives -= 1
                        self.player_sprite.respawn(XRESPAWN, YRESPAWN)
                        
                        self.life_list.pop().remove_from_sprite_lists()
                        print("Crash")
                    else:
                        self.game_over = True
                        

                        print("Game over")

                        #self.datamusic.stop(self.player_music_ingame)


                        try:
                            self.datamusic.stop(self.player_music_ingame)
                        except ValueError:
                            print("music already finished")


                        self.go_to_gameover_view()
        #-----------------------------------------------------------

        for lacrymo in self.terro_lacrymo_list:
            if lacrymo.top < 0:
                lacrymo.remove_from_sprite_lists()

            # Check this bullet to see if it hit a coin
            hit_list = arcade.check_for_collision_with_list(lacrymo, self.player_list)

            # If it did, get rid of the bullet
            if len(hit_list) > 0:
                lacrymo.remove_from_sprite_lists()
                self.is_smoked = True

                
                new_lacrymo_cloud = arcade.Emitter(
                    center_xy=(self.player_sprite.center_x, self.player_sprite.center_y),
                    change_xy=(0.15, 0),
                    emit_controller=arcade.EmitMaintainCount(60),
                    particle_factory=lambda emitter: AnimatedAlphaParticle(
                        filename_or_texture=random.choice(CLOUD_TEXTURES),
                        change_xy=(_Vec2(arcade.rand_in_circle((0.0, 0.0), 0.04)) + _Vec2(0.1, 0)).as_tuple(),
                        start_alpha=0,
                        duration1=random.uniform(5.0, 10.0),
                        mid_alpha=255,
                        duration2=random.uniform(5.0, 10.0),
                        end_alpha=0,
                        center_xy=arcade.rand_in_circle((0.0, 0.0), 50)
                    )
                )
                self.emitters.append(new_lacrymo_cloud)



            

        # Track if we need to change the viewport
        changed_viewport = False  # _______________________________________________




        #////////////////////////////// radar /////////////////////  spawn during play time

        
        #radar_spawn_image_source = "./resources/images/tiles/radar_128.png"
        punk_image_source = "./resources/images/enemies/fast_punk_128.png"



        for radspawn in self.radar_spawn_list:
            dist_player_radarspawn = math.hypot(radspawn.center_x - self.player_sprite.center_x, radspawn.center_y - self.player_sprite.center_y) 

            if dist_player_radarspawn < RADAR_RADIUS_DETECTION:



                #new_enemy = SpriteWithHealth(radar_spawn_image_source, 1, max_health = ENEMY_MAX_HEALTH)
                new_enemy = SpriteWithHealth(punk_image_source, 1, max_health = ENEMY_MAX_HEALTH)
                new_enemy.center_x = radspawn.center_x
                new_enemy.center_y = radspawn.center_y
                new_enemy.angle = 0

                

                #self.radar_list.append(self.radar_spawn_list.pop(radspawn)) #ATTENTION spawns are normal sprite, real enemy is SpriteWithHealth type
                
                #self.radar_list.append(new_enemy)
                self.punk_list.append(new_enemy)

                self.radar_spawn_list.remove(radspawn)



        #/////////////////////////////////////////



        # Loop through each enemy that we have
        for enemy in self.enemy_list:

            
            start_x = enemy.center_x
            start_y = enemy.center_y

            
            dest_x = self.player_sprite.center_x
            dest_y = self.player_sprite.center_y
            
            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            angle = math.atan2(y_diff, x_diff)

            # Set the enemy to face the player.
            enemy.angle = math.degrees(angle)-90

            # Shoot every 60 frames change of shooting each frame
            if self.frame_count % 60 == 0:
                bullet = arcade.Sprite(":resources:images/space_shooter/laserBlue01.png")                
                
                bullet.center_x = start_x
                bullet.center_y = start_y

                # Angle the bullet sprite
                bullet.angle = math.degrees(angle)

                # Taking into account the angle, calculate our change_x
                # and change_y. Velocity is how fast the bullet travels.
                bullet.change_x = math.cos(angle) * BULLET_SPEED
                bullet.change_y = math.sin(angle) * BULLET_SPEED

                #self.bullet_list.append(bullet) -------------------------
                self.terro_bullet_list.append(bullet)


            if self.frame_count % 300 == 0:
                lacrymo = arcade.Sprite("./resources/images/items/lacrymo_128.png")                
                
                lacrymo.center_x = start_x
                lacrymo.center_y = start_y

                # Angle the bullet sprite
                lacrymo.angle = math.degrees(angle)

                # Taking into account the angle, calculate our change_x
                # and change_y. Velocity is how fast the bullet travels.
                lacrymo.change_x = math.cos(angle) * LACRYMO_SPEED
                lacrymo.change_y = math.sin(angle) * LACRYMO_SPEED
                
                self.terro_lacrymo_list.append(lacrymo)



        # --- Manage Scrolling ---

        # Scroll left

        """
        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed_viewport = True

        # Scroll right
        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            changed_viewport = True

        # Scroll up
        top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary
            changed_viewport = True

        # Scroll down
        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_sprite.bottom
            changed_viewport = True

        if changed_viewport:
            # Only scroll to integers. Otherwise we end up with pixels that
            # don't line up on the screen
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            # Do the scrolling
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)
        """


    

    def center_on_player(self):
        w_width, w_height = self.window.get_size()
        arcade.set_viewport(
        self.player_sprite.center_x - w_width // 2,
        self.player_sprite.center_x + w_width // 2,
        self.player_sprite.center_y - w_height // 2,
        self.player_sprite.center_y + w_height // 2,
    )



    def go_to_gameover_view(self):

        view = GameOverView()
        self.window.show_view(view)



def main():

    #window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, fullscreen=True)

    

    #start_view = GameView()
    #window.show_view(start_view)
    
    #start_view.setup()
    #start_view.setup(level=1)

    start_view = InstructionView()
    window.show_view(start_view)

    
    arcade.run()


if __name__ == "__main__":
    main()

