from StateMachine import *
from World import *
from GameEntity import *
from vector2 import *
from Entities import *
from Tile import *

from random import *

import pygame

Tile_image = pygame.image.load("Images/Tiles/GrassWithCenterTree.png")

class Farmer(GameEntity):
    
    def __init__(self, world, image):
        GameEntity.__init__(self, world, "Farmer", image)
        
        planting_state = Farmer_Planting(self)
#         exploring_state = Farmer_Exploring(self)
        
        self.brain.add_state(planting_state)
#         self.brain.add_state(exploring_state)
        
        
        self.speed = 80
        self.max_speed = self.speed
        
        self.planted = 0
        
        self.worldSize = world.size
        self.TileSize = self.world.TileSize
        

    def render(self, surface):

        GameEntity.render(self, surface)
            
class Farmer_Planting(State):
    
    def __init__(self, Farmer):
        
        State.__init__(self, "Planting")
        self.Farmer = Farmer
        
    def check_conditions(self):
        pass
    
    def do_actions(self):
        if self.Farmer.location==self.Farmer.destination:
            #self.random_dest()
            self.plant_seed()
            
        if self.Farmer.location.get_distance_to(self.Farmer.destination) < 1:
            self.Farmer.destination=self.Farmer.location
            
    def plant_seed(self):
        #Function for planting trees
        
        #Test to see if the tile the farmer is on is a tile that a tree can be planted on
        if self.Farmer.world.get_tile(self.Farmer.location).plantable == 1:
            
            #Create a new tile with a tree class
            new_tile = TreePlantedTile_w(self.Farmer.world, Tile_image)
            
            #Set it's location and set up it's rect
            new_tile.location = self.Farmer.world.get_tile_pos(self.Farmer.location)*32
            new_tile.rect.topleft = new_tile.location
            
            old_tile_alpha = self.Farmer.world.get_tile(new_tile.location).darkness
            darkness = pygame.Surface((32,32))
            darkness.set_alpha(old_tile_alpha)
            
            new_tile.darkness = old_tile_alpha
            
            #Give it an ID so it can be found
            new_tile.id = self.Farmer.world.TreeID
            self.Farmer.world.TreeID += 1
            
            #Blit the tile with the tree on it directly to the background
            self.Farmer.world.background.blit(new_tile.img, new_tile.location)
            self.Farmer.world.background.blit(darkness, new_tile.location)
            
            #Add it to the TileArray so that it can be found
            self.Farmer.world.TileArray[int(new_tile.location.x/32)][int(new_tile.location.y/32)]
            
            #Add the location to a dictionary so villagers can see how far they are from it.
            self.Farmer.world.TreeLocations[str(self.Farmer.world.TreeID)] = new_tile.location

        #Goes to a random destination no matter what
        self.random_dest()
        
    def random_dest(self):
        #Function for going to a random destination, currently limited to top 1/12 of the map
        w,h = self.Farmer.worldSize
        offset = self.Farmer.TileSize/2
        TileSize = self.Farmer.TileSize
        random_dest = (randint(0,12)*TileSize+offset, randint(0,12)*TileSize+offset)
        self.Farmer.destination = Vector2(*random_dest)

    def entry_actions(self):
        self.random_dest()
        
