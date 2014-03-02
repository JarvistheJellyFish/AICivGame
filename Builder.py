from StateMachine import *
from World import *
from GameEntity import *
from vector2 import *
from Building import *

from random import *

import pygame

LumberImg = pygame.image.load()


class Builder(GameEntity):
    
    def __init__(self, world, image):
        GameEntity.__init__(self,world,"Builder",image)
        
        self.current_build = None
        
        building_state
        walking_state
        
        
class Builder_Building(State):
    
    def __init__(self, Builder):
        State.__init__(self, "Building")
        self.Builder = Builder
        
    def check_conditions(self):
        if self.building_complete==30:
            
            self.Builder.world.add_entity()
    
    def do_actions(self):
        self.building_complete+=self.tp
    
    def entry_actions(self):
        if self.Builder.world.wood >= 50:
            self.building_complete = 0
            
class Builder_Finding(State):   #Finding a suitable place to build.
    """If:
    Lumber Yard - In the woods not near anything else
    Docks - Edge of the water, decently distanced from others
    House - Somewhere in the town area
    Manor - near top of the map or maybe replaces a house.
    """
    
    def __init__(self, Builder):
        State.__init__(self, "Finding")
        self.Builder = Builder
        
    def check_conditions(self):
        if self.Builder.location.get_distance_to(self.Builder.destination) < 2:
            if self.Builder.world.get_close_entity(self.Builder.current_build, self.Builder.destination, 30) != None:
                random_dest()
            else:
                return "Building"
            
                

    def do_actions(self):
        pass
    
    def entry_actions(self):
        self.random_dest()
    
    def random_dest(self):
        w,h = self.Farmer.worldSize
        if self.Builder.current_build == "Lumber Yard":
            self.Builder.destination = Vector2(randint(0, w/3), randint(0, h))
            self.BuildingBuilt = LumberYard()
        elif self.Builder.current_build == "Dock":
            done = False 
            while done == False:
                choice = random.randint(0, len(self.Builder.world.pond_points)-1)
                if self.Builder.world.get_close_entity("Dock",
                                                       self.Builder.world.pond_points[choice],
                                                       10)==None:
                    done = True
            self.Builder.destination = self.Builder.world.pond_points[choice]
        elif self.Builder.current_build == "House":
            self.Builder.destination = Vector2(randint(w*.333, w*.666), randint(0, h))
            
    

            

            

    