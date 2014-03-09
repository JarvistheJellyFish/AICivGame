import pygame
from pygame.locals import *

from math import cos, sin, pi

from vector2 import *

from Tile import *

from Building import *

grass_img = pygame.image.load("Images/Tiles/MinecraftDarkGrass.png")
tree_img = pygame.image.load("Images/Tiles/MinecraftGrass.PNG")
water_img = pygame.image.load("Images/Tiles/AndrewWater2.png")
sand_img = pygame.image.load("Images/Tiles/Sand.PNG")
cobble_img = pygame.image.load("Images/Tiles/AndrewCobble2.png")
SStone_img = pygame.image.load("Images/Tiles/AndrewSmoothStone2.png")
deepwater_img = pygame.image.load("Images/Tiles/AndrewDeepWater.png")
snow_img = pygame.image.load("Images/Tiles/MinecraftSnow.png")
WithTree_img = pygame.image.load("Images/Tiles/GrassWithCenterTree.png")

lumber_yard_img = pygame.image.load("Images/Buildings/LumberYard.png")
house_img = pygame.image.load("Images/Buildings/House.png")
uc_house_img = pygame.image.load("Images/Buildings/UC_House.png")
dock_img = pygame.image.load("Images/Buildings/Dock.PNG")
manor_img = pygame.image.load("Images/Buildings/Manor.png")
uc_img = pygame.image.load("Images/Buildings/UC.png")
ucw_img = pygame.image.load("Images/Buildings/UC_Dock.png")

class World(object):        #Class that stores basically EVERYTHING
    
    def __init__(self, ss, WorldSize, font, img, img2):
        self.size = WorldSize     #How big the screen is
        
        self.TileSize = 32
        
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
        
        self.background_over = pygame.Surface((1600,900), HWSURFACE)
        self.background_over.set_alpha(128)
        self.background_over.fill((0,0,20,128))
        
        self.clock = pygame.time.Clock()
        
        print self.size
        self.background = pygame.Surface((self.size[0], self.size[1]), HWSURFACE)
        self.background.fill((255, 255, 255))
        
                
        self.font = font
        self.font_size = self.font.size("A")[1]
        
        self.text = self.font.render(str(self.wood), True, (0,0,0))  #World entity also stores global font for rendering to the screen.
        
        self.clock_degree = 0             #Used for the clock        
        
        self.convert_all()
        self.new_world(img, img2)
        
        self.BuildingQueue = []
        self.buildqueue = 0
        
    def new_world(self, img, img2=None):
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
        
        
        for i in xrange(self.map_width):
            self.current_height = 0
            w_last = False
            for a in xrange(self.map_height):
                
                color = img.get_at((i,a))[0]
                
                if img2 == None: color2 = (255,0,220)
                else: color2 = img2.get_at((i,a))
                
                if color < 95:
                    colorb = 0
                    tile = DeepWaterTile(self, self.deepwater_img)
                    
                elif color >= 95 and color < 110:
                    colorb = 95
                    tile = WaterTile(self, self.water_img)
                    
                elif color >= 110 and color <120:
                    colorb = 110
                    tile = BeachTile(self, self.sand_img)
                    
                elif color >=120 and color < 140:
                    colorb = 120
                    tile = GrassTile(self, self.grass_img)
                    
                elif color >= 140 and color < 160:
                    colorb = 140
                    tile = TreePlantedTile(self, self.tree_img)
                    
                elif color >= 160 and color < 170:
                    colorb = 160
                    if color2[2] == 220:
                        
                        tile = TreePlantedTile_w(self, self.WithTree_img)
                        tile.location = Vector2(i*32, a*32)
                        tile.rect.topleft = tile.location
                        tile.id = self.TreeID
                            
                        self.TreeLocations[str(self.TreeID)] = tile.location
                        self.TreeID += 1
                    else:
                        tile = TreePlantedTile(self, self.tree_img)
                    
                elif color >= 170 and color < 190:
                    colorb = 170
                    tile = TreePlantedTile(self, self.tree_img)
                    
                elif color >= 190 and color < 236:
                    colorb = 190
                    tile = SmoothStoneTile(self, self.SStone_img)
                    
#                 elif color >= 230 and color < 235:
#                     colorb = 230
#                     tile = CobblestoneTile(self, self.cobble_img)
                    
                else:
                    colorb = 236
                    tile = SnowTile(self, self.snow_img)
                
                if color > self.current_height-4 or color < 110:

                    dark_surface = pygame.Surface((32,32))
                    dark_surface.set_alpha(0)
                    if color >= 110:
                        self.current_height=color
                        
                    else:
                        self.current_height-=4
                     
                else:
                    self.current_height-=4
                    dark_surface = pygame.Surface((32,32))
                    dark_surface.set_alpha(128)
                    
                if color2[1] == 255:
                    WORLD_START_POS = (i,a)
        
        
                tile.location = Vector2(i*32, a*32)
                tile.rect.topleft = tile.location
                tile.color = color
                self.background.blit(tile.img, tile.location)
                
                dark_surface2 = pygame.Surface((32, 32))
                if color >= 190 and color < 236:
                    alph = 260-(255*((color-100)/155.0))
                    dark_surface2.set_alpha(alph)
                    
                else:
                    try:
                        alph = 200-(255*(color/255.0))
                        dark_surface2.set_alpha(alph)

                    except ZeroDivisionError:   
                        dark_surface2.set_alpha(0)
                        
                tile.darkness = alph
                
                #self.background.blit(dark_surface, tile.location)
                self.background.blit(dark_surface2, tile.location)
                
                self.minimap_img.blit(tile.img.subsurface((0,0,1,1)), (i,a))
                self.minimap_img.blit(dark_surface.subsurface((0,0,1,1)), (i,a))
                self.minimap_img.blit(dark_surface2.subsurface((0,0,1,1)), (i,a))
                
                self.TileArray[a][i] = tile
                
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
            Build.location = pos.copy()
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
        for i in range(Twidth/32):
            for j in range(Theight/32):
                try:
                    if Built:
                        test_tile = self.get_tile(Vector2((pos.x-32)+i*32, (pos.y-32)+j*32))
                    else:
                        test_tile = self.get_tile(Vector2(((pos.x-32)-self.background_pos.x)+i*32, ((pos.y-32)-self.background_pos.y)+j*32))
                    
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
        

    def grow_trees(self,trees):
        for i in trees:
            ran = randint(0,200)
            if ran == 20:
                old_tile = self.get_tile(trees[i])
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
                try:
                    del self.Baby_TreeLocations[str(old_tile.id)]
                    return 0
                except KeyError:
                    return None    
 
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
        return Vector2(int(location.x)/32, int(location.y)/32)
    
    def get_tile_array(self, start_pos, dimensions):
        dimensions = (int(dimensions[0]), int(dimensions[1]))
        
        start_tile = self.get_tile_pos(start_pos)

        array = [[None for i in xrange((dimensions[0]*2)+1)] for a in xrange((dimensions[1]*2)+1)]
        
        for i in xrange((dimensions[0]*2)+1):
            for a in xrange((dimensions[1]*2)+1):
                if start_tile.x+i < 0 or start_tile.y+a < 0:
                    continue
                
                else:
                    array[a][i] = self.TileArray[int((start_tile.y+a)-1)][int((start_tile.x+i)-1)]

        return array
