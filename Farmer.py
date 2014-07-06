from random import randint

import pygame
import vector2

import GameEntity
import StateMachine
import Image_funcs
import Tile
Tile_image = pygame.image.load("Images/Tiles/baby_tree.png")


class Farmer(GameEntity.GameEntity):

    def __init__(self, world, image):
        GameEntity.GameEntity.__init__(self, world, "Farmer", image)
        img_func = Image_funcs.image_funcs(18, 17)

        planting_state = Farmer_Planting(self)
#         exploring_state = Farmer_Exploring(self)

        self.brain.add_state(planting_state)
#         self.brain.add_state(exploring_state)

        self.speed = 80
        self.max_speed = self.speed

        self.planted = 0

        self.worldSize = world.size
        self.TileSize = self.world.TileSize

        self.row = 0
        self.times = 6
        self.pic = pygame.image.load("Images/Entities/map.png")
        self.cells = img_func.get_list(self.pic)
        self.ani = img_func.get_images(self.cells,
            self.times, 1, 1, 1, self.row, self.pic)
        self.start = img_func.get_image(
            self.cells, 1, 1, 0, self.row, self.pic)
        self.num = 0
        self.img = self.ani[0]
        self.num_max = len(self.ani) - 1
        self.ani_speed_init = 10
        self.ani_speed = self.ani_speed_init
        self.update()
        self.hit = 0

    def update(self):
        self.ani_speed -= 1
        if self.ani_speed == 0:
            self.image = self.ani[self.num]
            self.image.set_colorkey((255, 0, 255))
            self.ani_speed = self.ani_speed_init
            if self.num == self.num_max:
                self.num = 0
                self.hit += 1
            else:
                self.num += 1

    def render(self, surface):
        GameEntity.GameEntity.render(self, surface)


class Farmer_Planting(StateMachine.State):

    def __init__(self, Farmer):

        StateMachine.State.__init__(self, "Planting")
        self.Farmer = Farmer

    def check_conditions(self):
        if self.Farmer.location.get_distance_to(self.Farmer.destination) < 2:
            self.Farmer.destination = vector2.Vector2(self.Farmer.location)
            self.Farmer.update()

    def do_actions(self):
        if (self.Farmer.location == self.Farmer.destination
                and self.Farmer.hit == 4
                and self.Farmer.world.get_tile(self.Farmer.location).plantable
                == 1):
            self.plant_seed()
        if (self.Farmer.location == self.Farmer.destination
                and self.Farmer.hit != 4
                and self.Farmer.world.get_tile(self.Farmer.location).plantable
                != 1):
            self.random_dest()

    def plant_seed(self):
        #Function for planting trees

        #Test to see if the tile the farmer is on is a tile
        # that a tree can be planted on
        if self.Farmer.world.get_tile(self.Farmer.location).plantable == 1:
            self.Farmer.hit = 0
            self.Farmer.image = self.Farmer.start
            self.Farmer.image.set_colorkey((255, 0, 255))

            old_tile = self.Farmer.world.get_tile(
                vector2.Vector2(self.Farmer.location))

            darkness = pygame.Surface((32, 32))
            darkness.set_alpha(old_tile.darkness)

            new_tile = Tile.Baby_Tree(self.Farmer.world, Tile_image)
            new_tile.darkness = old_tile.darkness
            new_tile.location = self.Farmer.world.get_tile_pos(
                self.Farmer.destination) * 32
            new_tile.rect.topleft = new_tile.location
            new_tile.color = old_tile.color

            #Give it an ID so it can be found
            new_tile.id = self.Farmer.world.Baby_TreeID
            self.Farmer.world.Baby_TreeID += 1

            self.Farmer.world.TileArray[int(
                new_tile.location.y / 32)][int(
                new_tile.location.x / 32)] = new_tile
            self.Farmer.world.background.blit(new_tile.img, new_tile.location)
            self.Farmer.world.background.blit(darkness, new_tile.location)

            #Add the location to a dictionary so
            #villagers can see how far they are from it.
            self.Farmer.world.Baby_TreeLocations[str(
                self.Farmer.world.Baby_TreeID)] = new_tile.location

        #Goes to a random destination no matter what
        self.Farmer.hit = 0
        self.random_dest()

    def random_dest(self):
        """Function for going to a random destination,
        currently limited to top 1/12 of the map
        """
        w, h = self.Farmer.worldSize
        offset = self.Farmer.TileSize / 2
        TileSize = self.Farmer.TileSize
        random_dest = (randint(0, 25) * TileSize + offset, randint(0, 25)
            * TileSize + offset)
        self.Farmer.destination = vector2.Vector2(* random_dest)

    def entry_actions(self):
        self.random_dest()
