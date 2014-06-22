
import pygame
from pygame.locals import *

from math import cos, sin, pi

from vector2 import *

from Tile import *

from Building import *
from Builder import *
from Villager import *
from Lumberjack import *
from Farmer import *

from Clips import Clips

from random import randint, seed
from VoronoiMapGen import point, mapGen

grass_img = pygame.image.load("Images/Tiles/MinecraftDarkGrass.png")
tree_img = pygame.image.load("Images/Tiles/MinecraftGrass.png")
water_img = pygame.image.load("Images/Tiles/AndrewWater2.png")
sand_img = pygame.image.load("Images/Tiles/Sand.PNG")
cobble_img = pygame.image.load("Images/Tiles/AndrewCobble2.png")
SStone_img = pygame.image.load("Images/Tiles/AndrewSmoothStone.png")
deepwater_img = pygame.image.load("Images/Tiles/AndrewDeepWater.png")
snow_img = pygame.image.load("Images/Tiles/MinecraftSnow.png")
WithTree_img = pygame.image.load("Images/Tiles/GrassWithCenterTree.png")

lumber_yard_img = pygame.image.load("Images/Buildings/LumberYard.png")
house_img = pygame.image.load("Images/Buildings/House.png")
uc_house_img = pygame.image.load("Images/Buildings/UC_House.png")
dock_img = pygame.image.load("Images/Buildings/Dock.png")
manor_img = pygame.image.load("Images/Buildings/Manor.png")
uc_img = pygame.image.load("Images/Buildings/UC.png")
ucw_img = pygame.image.load("Images/Buildings/UC_Dock.png")

lumberjack_img = pygame.image.load("Images/Entities/Lumberjack.png")
farmer_img = pygame.image.load("Images/Entities/Farmer.png")
builder_img = pygame.image.load("Images/Entities/Builder.png")

class World(object):        #Class that stores basically EVERYTHING
    
    def __init__(self, ss, WorldSize, font, rand_seed):
        self.size = WorldSize     #How big the map is
        self.TileSize = 32
        self.ssize = (self.size[0]/self.TileSize, self.size[1]/self.TileSize) 
        self.seed = rand_seed
        seed(self.seed)
        
        self.ss = ss
        self.w, self.h = self.size  #Certain functions entities need this.
        self.center = Vector2(self.w/2, self.h/2)
        
        self.building = {}
        self.entities = {}          #Stores all entities the game processes
        self.entity_id = 0          #Each entity is given a unique id so the program can find it
        self.wood = 0               #Probably will add other resources
        self.MAXwood = 50
        self.food = 0
        self.MAXfood = 0
        self.population = 0
        self.MAXpopulation = 15
        self.background_pos = Vector2(ss[0]/5.0, 0)
        self.mapGenerator = mapGen()
        
        self.background_over = pygame.Surface((1600,900), HWSURFACE)
        self.background_over.set_alpha(128)
        self.background_over.fill((0,0,20,128))
        
        self.full_surface = pygame.Surface(self.size, HWSURFACE)
        
        self.clock = pygame.time.Clock()
        
        print self.size
        self.background = pygame.Surface((self.size[0], self.size[1]), HWSURFACE)
        self.background.fill((255, 255, 255))
        
                
        self.font = font
        self.font_size = self.font.size("A")[1]
        
        self.text = self.font.render(str(self.wood), True, (0,0,0))  #World entity also stores global font for rendering to the screen.
        
        self.clock_degree = 0             #Used for the clock        
        
        self.convert_all()
        self.new_world()
        self.cliper = Clips(self, self.ss)
        
        self.BuildingQueue = []
        self.buildqueue = 0
        
    def new_world(self):
        del self.full_surface
        #seed(self.seed)
        img = self.mapGenerator.negative(self.mapGenerator.reallyCoolFull(self.ssize, num_p=23))
        #img = self.mapGenerator.whole_new(25, self.ssize, 1, -1)
        self.map_width, self.map_height = img.get_size()
        
        self.minimap_img = pygame.Surface((self.map_width, self.map_height))
        
        self.TileArray = [[0 for i in xrange(self.map_width)] for a in xrange(self.map_height)]
        
        self.TreeID = 0
        self.TreeLocations  = {}
        self.Baby_TreeID = 0
        self.Baby_TreeLocations = {}
        
        self.buildings = {"LumberYard":{},
                          "Dock":{},
                          "House":{},
                          "Manor":{},
                          "UC":{}}
        
        self.building = {}
        self.entities = {}          #Stores all entities the game processes
        self.entity_id = 0          #Each entity is given a unique id so the program can find it
        self.wood = 0               #Probably will add other resources
        self.MAXwood = 50
        self.food = 0
        self.MAXfood = 0
        self.population = 0
        self.MAXpopulation = 15
        self.background_pos = Vector2(self.ss[0]/5.0, 0)
        self.mapGenerator = mapGen()
        
        self.full_surface = pygame.Surface(self.size, HWSURFACE)
        
        self.clock_degree = 0             #Used for the clock       
    
        self.BuildingQueue = []
        self.buildqueue = 0
        
        
        for i in xrange(self.map_width):
            self.current_height = 0
            w_last = False
            for a in xrange(self.map_height):
                
                f_color = img.get_at((i,a))
                color = f_color[0]
                
                to_rotate = 1
                
                color2 = (255,0,220)
                
#                 if color < 95:
#                     colorb = 0
#                     tile = DeepWaterTile(self, self.deepwater_img)

                    
                if color < 110:
                    colorb = 0
                    tile = WaterTile(self, self.water_img)
                    
                    last_image = self.sand_img
                    last_color = 0
                    
                    
                elif color >= 110 and color <120:
                    colorb = 110
                    tile = BeachTile(self, self.sand_img)
                    last_image = self.sand_img
                    #to_rotate = 0
                    last_color = 110
                    
                elif color >=120 and color < 140:
                    colorb = 120
                    tile = GrassTile(self, self.grass_img)
                    last_image = self.sand_img
                    last_color = 120
                    
                elif color >= 140 and color < 160:
                    colorb = 140
                    tile = TreePlantedTile(self, self.tree_img)
                    last_image = self.grass_img
                    last_color = 140
                    
                elif color >= 160 and color < 170:
                    colorb = 160
                    if color2[2] == 220:
                        
                        tile = TreePlantedTile_w(self, self.WithTree_img)
                        tile.location = Vector2(i<<5, a<<5)
                        tile.rect.topleft = tile.location
                        tile.id = self.TreeID
                            
                        self.TreeLocations[str(self.TreeID)] = tile.location
                        self.TreeID += 1
                        
                        to_rotate = 0
                    else:
                        tile = TreePlantedTile(self, self.tree_img)
                        
                    last_image = self.tree_img
                    last_color = 160
                    
                elif color >= 170 and color < 190:
                    colorb = 170
                    tile = TreePlantedTile(self, self.tree_img)
                    last_image = self.WithTree_img
                    last_color = 170
                    
                elif color >= 190 and color < 236:
                    colorb = 190
                    tile = SmoothStoneTile(self, self.SStone_img)
                    last_image = self.tree_img
                    to_rotate = 0
                    last_color = 190
                    
                else:
                    colorb = 236
                    tile = SnowTile(self, self.snow_img)
                    last_image = self.SStone_img
                    last_color = 236
                
                #Shadows----
                fake_color = color
                if color < 110:
                    fake_color = 110
                if fake_color > self.current_height-3:

                    dark_surface = pygame.Surface((32,32))
                    dark_surface.set_alpha(0)
                    if color >= 110:
                        self.current_height=fake_color
                        
                    else:
                        self.current_height-=3
                     
                else:
                    self.current_height-=3
                    dark_surface = pygame.Surface((1,1))
                    dark_surface.set_alpha(128)
                #-----------
                    
                #Used for determening start position
                if color2[1] == 255:
                    WORLD_START_POS = (i,a)
                #-----
				
                tile.location = Vector2(i<<5, a<<5)
                tile.rect.topleft = tile.location
                tile.color = color
                
                if to_rotate:
                    tile.img = pygame.transform.rotate(tile.img, randint(0,4)*90)
                
                self.background.blit(tile.img, tile.location)

                dark_surface2 = pygame.Surface((32, 32))

                alph = 235-color
                if color >= 190 and color < 236:
                    alph = 330-color
                
                dark_surface2.set_alpha(alph)
                
                tile.darkness = alph
                
                self.background.blit(dark_surface, tile.location)
                self.background.blit(dark_surface2, tile.location)
                """
                try:
                    percentage = (color-last_color) / float(colorb - last_color)
                    
                except ZeroDivisionError:
                    percentage = 0.0
                combined_img = self.mapGenerator.lerp_two_images(tile.img, last_image, percentage)
                """
                
                #self.minimap_img.blit(combined_img.subsurface((0,0,1,1)), (i,a))
                self.minimap_img.blit(tile.img.subsurface((0,0,1,1)), (i,a))
                self.minimap_img.blit(dark_surface.subsurface((0,0,1,1)), (i,a))
                self.minimap_img.blit(dark_surface2.subsurface((0,0,1,1)), (i,a))
                
                self.TileArray[a][i] = tile
                
        self.populate()
        self.cliper = Clips(self, self.ss)
                
    def populate(self):
        FARMER_COUNT = 4
        VILLAGER_COUNT = 5
        BUILDER_COUNT = 1
        
        
        #adds all the people and make sure they don't go all ape shit
        lumber1 = LumberYard(self, self.lumberyard_img)
        lumber1.location = Vector2(self.w/2, self.h/2)
        lumber1.tile_x, lumber1.tile_y = 4,4
        self.add_entity(lumber1)
    
        for Villager_no in xrange(VILLAGER_COUNT):    #Adds all Wood Cutters
    
            villager = Lumberjack(self, self.lumberjack_img)
            villager.location = lumber1.location.copy()
            villager.LastLumberYard = lumber1
            villager.brain.set_state("Searching")
            self.add_entity(villager)
            self.population+=1
            
        
            
        for Building_no in xrange(BUILDER_COUNT):
            builder = Builder(self, self.builder_img, lumber1)
            builder.location = lumber1.location.copy()
            builder.brain.set_state("Idle")
            self.add_entity(builder)
            self.population+=1
        
    
        for FARMER in xrange(FARMER_COUNT):     #Adds all the farmers
            farmer = Farmer(self, self.farmer_img)
            farmer.location = Vector2(20,20)
            farmer.brain.set_state("Planting")
            self.add_entity(farmer)
            self.population+=1
                
    def add_building(self, building, pos):
        
        buildable = self.test_buildable(building, 0, pos)
        print pos
        
        if buildable:
            Build = buildable[1]
            Build.location = self.get_tile_pos(pos-self.background_pos)*32
            print "LOC: ", Build.location
            self.add_entity(Build)
            self.buildings[building]=Build
            self.BuildingQueue.append(Build)
            return 1
        
    def add_built(self, building, pos):
        
        
        buildable = self.test_buildable(building, 1, pos)
        print pos
        
        if buildable:
            Build = buildable[1]
            Build.location = pos
            print "LOC2: ", Build.location
            self.add_entity(Build)
            self.buildings[building]=Build
            return 1
        
    def test_buildable(self, building, built, pos):
           
        if building == "LumberYard":
            if built:
                Build = LumberYard(self, self.lumberyard_img)
            else:
                Build = UnderConstruction(self, self.uc_img, "LumberYard")
                
        elif building == "House":
            if built:
                Build = House(self, self.house_img)
            else:
                Build = UnderConstruction(self, self.uc_house_img, "House")

        elif building == "Dock":
            if built:
                Build = Dock(self, self.dock_img)
            else:
                Build = UnderConstruction(self, self.ucw_img, "Dock")

        elif building == "Manor":
            if built:
                Build = Manor(self, self.manor_img)
            else:
                Build = UnderConstruction(self, self.uc_img, "Manor")

           
        buildable = 1
        land = 0
        water = 0
        
        Twidth, Theight = Build.image.get_size()
        for i in range(Twidth>>5):
            for j in range(Theight>>5):
                try:
                    if built:
                        test_tile = self.get_tile(Vector2((pos.x-32)+(i<<5), (pos.y-32)+(j<<5)))
                        #print "A", test_tile, test_tile.location
                    else:
                        test_tile = self.get_tile(Vector2(((pos.x-32)-self.background_pos.x)+(i<<5), ((pos.y-32)-self.background_pos.y)+(j>>5)))
                        #print "B", test_tile, test_tile.location
                    
                    if test_tile.buildable!=1 and building!="Dock":
                        buildable = 0
                        return 0
                    elif building == "Dock":
                        if test_tile.buildable_w:
                            water+=1
                        else:
                            land+=1
                except IndexError:
                    return 0
        
        if building == "Dock":
            if water >= 1 and land <= 2 and land > 0:
                buildable = 1
                return 1, Build
            else:
                buildable = 0
                return 0
            
        return 1, Build
                
    def convert_all(self):
        self.grass_img = grass_img.convert()
        self.tree_img = tree_img.convert()
        self.water_img = water_img.convert()
        self.sand_img = sand_img.convert()
        self.cobble_img = cobble_img.convert()
        self.SStone_img = SStone_img.convert()
        self.deepwater_img = deepwater_img.convert()
        self.snow_img = snow_img.convert()
        self.WithTree_img = WithTree_img.convert()
        
        self.lumberyard_img = lumber_yard_img.convert()
        self.lumberyard_img.set_colorkey((255,0,255))
        
        self.house_img = house_img.convert()
        self.house_img.set_colorkey((255,0,255))
        
        self.dock_img = dock_img.convert()
        self.dock_img.set_colorkey((255,0,255))
        
        self.manor_img = manor_img.convert()
        self.manor_img.set_colorkey((255,0,255))
        
        self.uc_img = uc_img.convert_alpha()
        self.ucw_img = ucw_img.convert()
        self.ucw_img.set_colorkey((255,0,255))
        self.uc_house_img = uc_house_img.convert()
        self.uc_house_img.set_colorkey((255,0,255))
        
        self.lumberjack_img = lumberjack_img.convert()
        self.farmer_img = farmer_img.convert()
        self.builder_img = builder_img.convert()
        

    def grow_trees(self,trees):
        for i in range(len(trees)):
            ran = randint(0,100)
            if ran == 1 and len(trees) > 0:
                try:
                    a = trees.keys()
                    old_tile = self.get_tile(trees[a[i]])
                    darkness = pygame.Surface((32,32))
                    darkness.set_alpha(old_tile.darkness)

                    new_tile = TreePlantedTile_w(self, WithTree_img)

                    new_tile.darkness = old_tile.darkness

                    new_tile.location = old_tile.location
                    new_tile.rect.topleft = new_tile.location
                    new_tile.color = old_tile.color

                    new_tile.id = self.TreeID
                    self.TreeID += 1

                    self.TileArray[int(new_tile.location.y/32)][int(new_tile.location.x/32)] = new_tile
                    self.background.blit(new_tile.img, new_tile.location)
                    self.background.blit(darkness, new_tile.location)
                    #print self.Baby_TreeLocations
                    del self.Baby_TreeLocations[str(a[i])]
                except IndexError:
                    pass

    def add_entity(self, entity):       #Used to add entities to the world

        self.entities[self.entity_id] = entity
        entity.id = self.entity_id
        self.entity_id += 1

    def remove_entity(self, entity):    #function for removing an entity
        del self.entities[entity.id]

    def remove_tree(self, tree_id):
        #print len(self.TreeLocations)
        try:
            del self.TreeLocations[str(tree_id)]
            return 0
        except KeyError:
            return None

    def get(self, entity_id):           #Return an entity

        if entity_id in self.entities:
            return self.entities[entity_id]
        else:
            return None

    def process(self, time_passed):     #Run the world through 1 cycle
         
        for entity in self.entities.values():
            entity.process(time_passed)

        self.wood_text = self.font.render("Wood: %d/%d"%(self.wood, self.MAXwood), True, (255,255,255))
        self.food_text = self.font.render("Food: %d/%d"%(self.food, self.MAXfood), True, (255,255,255))
        self.pop_text = self.font.render("Population: %d/%d"%(self.population, self.MAXpopulation), True, (255,255,255))
        self.frame_text = self.font.render("FPS: %.2f"%(self.clock.get_fps()), True, (255,255,255))

        semi_angle = abs(self.clock_degree-180.0)
        self.background_alpha = min((255-(255*(abs(semi_angle/180)))), 220.0)
        self.background_over.set_alpha(self.background_alpha)

    def render(self, surface):
        surface.blit(self.background, self.background_pos)

        #for i in self.tilearray:
         #   for tile in i:
          #      tile.render(surface)

        for entity in self.entities.itervalues():
            entity.render(surface)

        surface.blit(self.background_over, (0,0))

        #for point in self.pond_points:
        #    pygame.draw.circle(surface, (255,0,0), (int(point[0]), int(point[1])), 5)

#         surface.set_clip(0,0,self.w,self.font_size+4)
#         surface.blit(self.wood_text, (40,2))
#         surface.blit(self.food_text, (200,2))
#         surface.blit(self.pop_text, (360,2))
#         surface.set_clip(None)

    def render_all(self, surface, tp, mouse_pos):
        self.cliper.render(surface, tp, mouse_pos)


    def get_close_entity(self, name, location, range=100.):

        location = Vector2(*location)

        for entity in self.entities.itervalues():
            if entity.name == name:
                distance = location.get_distance_to(entity.location)
                if range == -1:
                    return entity
                if distance < range:
                    return entity

        return None

    def get_tile(self, location):
        tile = self.get_tile_pos(location)

        return self.TileArray[int(tile.y)][int(tile.x)]

    def get_tile_pos(self, location):
        return Vector2(int(location.x) >> 5, int(location.y) >> 5)

    def get_tile_array(self, start_pos, dimensions):
        dimensions = (int(dimensions[0]), int(dimensions[1]))

        start_tile = self.get_tile_pos(start_pos)

        array = [[None for i in xrange(
           (dimensions[0] * 2) + 1)] for a in xrange((dimensions[1] * 2) + 1)]

        for i in xrange((dimensions[0] * 2) + 1):
            for a in xrange((dimensions[1] * 2) + 1):
                if start_tile.x + i < 0 or start_tile.y + a < 0:
                    continue
                else:
                    array[a][i] = self.TileArray[int(
                       (start_tile.y + a) - 1)][int((start_tile.x + i) - 1)]

        return array
