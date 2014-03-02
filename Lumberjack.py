from GameEntity import GameEntity
from StateMachine import State
from Tile import *

from random import randint

import pygame

NoTreeImg = pygame.image.load("Images/Tiles/MinecraftGrass.png")

class Lumberjack(GameEntity):
    
    def __init__(self, world, img):
        GameEntity.__init__(self,world,"Lumberjack", img)
        
        self.speed = 100.
        self.can_see = 5,5
        
        self.searching_state = Searching(self)
        self.chopping_state = Chopping(self)
        self.delivering_state = Delivering(self)
        
        self.brain.add_state(self.searching_state)
        self.brain.add_state(self.chopping_state)
        self.brain.add_state(self.delivering_state)
        
        self.worldSize = world.size
        self.TileSize = self.world.TileSize
        
        self.ani = ["Images/Entities/Lumberjack.png","Images/Entities/Lumberjack_chop2.png","Images/Entities/Lumberjack_chop3.png","Images/Entities/Lumberjack_chop2.png","Images/Entities/Lumberjack_chop1.png"]
        self.num = 0
        self.num_max = len(self.ani)-1
        self.ani_speed_init = 10
        self.ani_speed = self.ani_speed_init
        self.img = pygame.image.load(self.ani[0])
        self.update()
        self.hit = 0
        self.img.set_colorkey((255,0,255))

        
    def update(self):
        self.ani_speed -= 1
        if self.ani_speed == 0:
            self.image = pygame.image.load(self.ani[self.num]).convert()
            self.image.set_colorkey((255,0,255))
            self.ani_speed = self.ani_speed_init
            if self.num == self.num_max:
                self.num = 0
                self.hit += 1
            else:
                self.num += 1
        

        
class Searching(State):
    """This state will be used to have the Lumberjack looking for
       trees to cut, It needs to be fast enough to have AT LEAST 20 Lumberjacks
       with little to no framerate loss.
       
       Perhaps it could be used to find a clump of trees. and then the Lumberjack
       wouldn't just wander around aimlessly searching for trees even though it
       saw some when it was just at another tree"""
    
    def __init__(self, Lumberjack):
        State.__init__(self, "Searching")
        self.Lumberjack = Lumberjack
        
    def entry_actions(self):
        self.tile_array = self.Lumberjack.world.get_tile_array((self.Lumberjack.location),
                                                               self.Lumberjack.can_see)

    def do_actions(self):
        pass
    
    def check_conditions(self):
        if self.Lumberjack.location.get_distance_to(self.Lumberjack.destination) < 2:
            self.tile_array = self.Lumberjack.world.get_tile_array((self.Lumberjack.location),
                                                               self.Lumberjack.can_see)
            self.Lumberjack.location = self.Lumberjack.destination.copy()
            """
            pygame.draw.rect(self.Lumberjack.world.background, (255,255,255), (self.Lumberjack.location.x-(self.Lumberjack.can_see[0]*32),
                                                                               self.Lumberjack.location.y+(self.Lumberjack.can_see[1]*32),
                                                                               self.Lumberjack.can_see[0]*64,
                                                                               self.Lumberjack.can_see[1]*64), 3)
            """
            for i in self.tile_array:
                for Tile in i:
                    if Tile != None:
                    
                        if Tile.name == "TreePlantedTile_W":
                            self.Lumberjack.Tree_tile = Tile
                            self.Lumberjack.destination = self.Lumberjack.Tree_tile.location.copy()
                            self.Lumberjack.tree_id = Tile.id
                            return "Chopping"
                        
            self.random_dest()
    
    def exit_actions(self):
        pass
    
    def random_dest(self):
        #Function for going to a random destination, currently limited to top 1/12 of the map
        w,h = self.Lumberjack.worldSize
        offset = self.Lumberjack.TileSize/2
        TileSize = self.Lumberjack.TileSize
        random_dest = (randint(0,12)*TileSize+offset, randint(0,12)*TileSize+offset)
        self.Lumberjack.destination = Vector2(*random_dest)
    
class Chopping(State):
    
    def __init__(self, Lumberjack):
        State.__init__(self, "Chopping")
        self.Lumberjack = Lumberjack
        
    def entry_actions(self):
        pass
    
    def do_actions(self):
        pass
    
    def check_conditions(self):
        self.Lumberjack.destination = self.Lumberjack.location.copy()
        if self.Lumberjack.Tree_tile.name != "TreePlantedTile_W":
            return "Searching"
        
        self.Lumberjack.update()
        
        if self.Lumberjack.location.get_distance_to(self.Lumberjack.destination) == 0 and self.Lumberjack.hit == 4:
            self.Lumberjack.location = self.Lumberjack.destination.copy()
            new_tile = TreePlantedTile(self.Lumberjack.world, NoTreeImg)
            new_tile.location = self.Lumberjack.world.get_tile_pos(self.Lumberjack.destination)*32
            new_tile.rect.topleft = new_tile.location

            self.Lumberjack.world.background.blit(new_tile.img, new_tile.location)
            self.Lumberjack.world.TileArray[int(new_tile.location.x/32)][int(new_tile.location.y/32)] = new_tile
            self.Lumberjack.hit = 0
            
            #del self.Lumberjack.world.TreeLocations[str(self.Lumberjack.tree_id)]
            return "Delivering"
    
    def exit_actions(self):
        pass
    
class Delivering(State):
    
    """This state will be used solely to deliver wood from wherever the Lumberjack
       got the wood to the closest Lumber yard. maybe all the lumber yards could
       be stored in a dictionary similar to trees, that would be much faster"""
    
    def __init__(self, Lumberjack):
        State.__init__(self, "Delivering")
        self.Lumberjack = Lumberjack
        
    def entry_actions(self):

        des = self.Lumberjack.world.get_close_entity("LumberYard",self.Lumberjack.location, 100)
        self.Lumberjack.LastLumberYard = des
        if des == None:
            des = self.Lumberjack.world.get_close_entity("LumberYard",self.Lumberjack.location, 300)
            self.Lumberjack.LastLumberYard = des
            if des == None:
                des = self.Lumberjack.LastLumberYard
                    
        self.Lumberjack.destination = des.location.copy()
    
    def do_actions(self):
        pass
        
    def check_conditions(self):

        #if self.Lumberjack.world.wood >= self.Lumberjack.world.MAXwood:
        #    return "IDLE"
        
        if self.Lumberjack.location.get_distance_to(self.Lumberjack.destination) < 2.0:
            self.Lumberjack.world.wood+=5
            return "Searching"

    
    def exit_actions(self):
        pass
    
class IDLE(State):
    
    def __init__(self, Lumberjack):
        State.__init__(self, "Delivering")
        self.Lumberjack = Lumberjack
        
    def entry_actions(self):
        pass
    
    def do_actions(self):
        pass
    
    def check_conditions(self):
        pass
    
    def exit_actions(self):
        pass
