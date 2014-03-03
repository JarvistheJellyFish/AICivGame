import pygame
from pygame.locals import *
pygame.init()

import os
from random import randint

from vector2 import *

from StateMachine import *
from World import *

from GameEntity import *
from Entities import *
from Villager import *
from Farmer import *
from Building import *
from Tile import *

from datetime import datetime

from Lumberjack import *
from Builder import *

from Clips import *

from crossfade import CrossFade

from GlobRand import random_map

os.environ['SDL_VIDEO_CENTERED'] = '1'


TILE_SIZE = 32 

VILLAGER_COUNT = 0
FARMER_COUNT = 0
BUILDER_COUNT = 1

font = pygame.font.SysFont("Terminal", 20)

def me_double_size(image):
    """Function for making an image the same size but just 1/2 the quality
       Was going to be used in water path finding algorithm"""
       
    Size = image.get_size()
    SmSize = (Size[0]/2, Size[1]/2)
    SmImage = pygame.transform.scale(image, SmSize)
    NormalImage = pygame.transform.scale(SmImage, Size)
    return NormalImage
    

def run():
    pygame.display.set_caption("Villager Simulation")

    sizes = pygame.display.list_modes()
    SCREEN_SIZE = sizes[0]
    Owidth, Oheight = SCREEN_SIZE
    
    side_size = Owidth/5.0

    screen = pygame.display.set_mode(SCREEN_SIZE, FULLSCREEN | HWSURFACE, 32)
    
    fade = CrossFade(screen)
    all_sprites = pygame.sprite.Group(fade)
    
    draw = False
    held = False
    
    #Load the image the world will be based on, then set the world size proportionate to it
    
    world_img_str, mini_img_str = random_map("SmallMapPerlin")
    
    world_img = pygame.image.load(world_img_str).convert()
    
    if mini_img_str == None:
        mini_img = None
    else:
        print mini_img_str
        mini_img = pygame.image.load(mini_img_str).convert()
        
    size = world_img.get_size()
    w_size = size[0]*TILE_SIZE, size[1]*TILE_SIZE

    world = World(SCREEN_SIZE, w_size, font, world_img, mini_img)
    #world.background = me_double_size(world.background)
    

    Villager_image = pygame.image.load("Images/Entities/Villager.PNG").convert()
    Farmer_image = pygame.image.load("Images/Entities/Farmer.png").convert()
    Lumberjack_image = pygame.image.load("Images/Entities/Lumberjack.png").convert()
    Builder_image = pygame.image.load("Images/Entities/Builder.png").convert()

    placing_lumberyard_img = pygame.image.load("Images/Buildings/Dark_LumberYard.png").convert()
    placing_lumberyard_img.set_colorkey((255,0,255))
    placing_house_img = pygame.image.load("Images/Buildings/Dark_House.png").convert()
    placing_house_img.set_colorkey((255,0,255))
    placing_dock_img = pygame.image.load("Images/Buildings/Dark_Dock.png").convert()
    placing_dock_img.set_colorkey((255,0,255))
    placing_manor_img = pygame.image.load("Images/Buildings/Dark_Manor.png").convert()
    placing_manor_img.set_colorkey((255,0,255))
    
    bad_lumberyard_img = pygame.image.load("Images/Buildings/Red_LumberYard.png").convert()
    bad_lumberyard_img.set_colorkey((255,0,255))
    
    clip = Clips(world, (Owidth, Oheight))
    #pygame.image.save(world.background, "Images/BOOM.png")
    
    lumber1 = LumberYard(world, lumber_yard_img)
    lumber1.location = Vector2(4*TILE_SIZE, 4*TILE_SIZE)
    lumber1.tile_x, lumber1.tile_y = 4,4
    world.add_entity(lumber1)

    for Villager_no in xrange(VILLAGER_COUNT):    #Adds all Wood Cutters

        villager = Lumberjack(world, Lumberjack_image)
        villager.location = lumber1.location.copy()
        villager.LastLumberYard = lumber1
        villager.brain.set_state("Searching")
        world.add_entity(villager)
        world.population+=1
        
    print world.BuildingQueue
        
    for Building_no in xrange(BUILDER_COUNT):
        builder = Builder(world, Builder_image, lumber1)
        builder.location = lumber1.location.copy()
        builder.brain.set_state("Idle")
        world.add_entity(builder)
        world.population+=1
    

    for FARMER in xrange(FARMER_COUNT):     #Adds all the farmers
        farmer = Farmer(world, Farmer_image)
        farmer.location = Vector2(20,20)
        farmer.brain.set_state("Planting")
        world.add_entity(farmer)
        world.population+=1
    
    selected_building = "LumberYard"
    selected_img = pygame.image.load("Images/Buildings/Dark_LumberYard.png").convert()
    selected_img.set_colorkey((255,0,255))
    
    SCREENSHOTNUM = 12
    
    world.clock.tick()
    while True:
        
        time_passed = world.clock.tick(60)
        time_passed_seconds = time_passed/1000.
        pos = Vector2(*pygame.mouse.get_pos())
        
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
                
            if event.type == MOUSEBUTTONDOWN:
                if ( pos.x > clip.minimap_rect.x and pos.y > clip.minimap_rect.y ):
                    pass
                else:
                    if event.button == 1:
                        held = True
                        start = Vector2(*pygame.mouse.get_pos())
                        draw = True
                        if ( pos.x < clip.side.w ) and (pos.y < clip.side.top_rect.h):
                            for L in clip.side.tiles:
                                for T in L:
                                    if T == None:
                                        continue
                                    
                                    if T.rect.collidepoint((pos.x, pos.y)):
                                        if T.selected:
                                            T.selected = False
                                        else:
                                            T.selected = True
                                            
                                        selected_building = T.rep
                                        clip.side.update(T)
                                        
                        else:
                            selected_building = None
                            clip.side.update()
                            
                        
                    if event.button == 3 and selected_building != None:
                        world.add_building(selected_building, pos)
                        if world.test_buildable(selected_building, 0, pos):
                            selected_building = None
                            clip.side.update()
            
            if event.type == MOUSEBUTTONUP:
                draw = False
                held = False
                    
            if event.type == KEYDOWN:
                if event.key == K_F2:
                    str1 =  str(datetime.now())
                    str1 = str1.split(".")
                    str2 = str1[0]+str1[1]
                    str2 = str2.split(":")
                    str1 = ""
                    for i in str2:
                        str1+=i
                    pygame.image.save(screen, "Images/Screenshots/SCREENSHOT%s.png"%str1)
                    
            if event.type == VIDEORESIZE:
                Owidth, Oheight = event.size
                    
            
                
        #------------------Keys Below--------------------------------------------------
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_ESCAPE]:  #quits the game
            pygame.quit() 
            exit()
            
        if pressed_keys[K_SPACE]:   #Resets wood
            world.wood = 0
        
        if pressed_keys[K_d]:   #Fast-forward-esk functionability
            world.clock_degree+=5
            
        if pressed_keys[K_l]:   #Test to see what the first entity's state is
            print world.entities[1].brain.active_state
            
        #--------------Keys Above----------------------------------------
        #--------------Mouse Below---------------------------------------
        
        if int(pos.x) <= 15:
            pygame.mouse.set_pos((15, pos.y))
            world.background_pos.x+=500*time_passed_seconds
            #print world.background_pos.x
            if world.background_pos.x > side_size:

                world.background_pos.x = side_size

            
        elif int(pos.x) >= Owidth-16:
            pygame.mouse.set_pos((Owidth-16, pos.y))
            world.background_pos.x-=500*time_passed_seconds
            
            if world.background_pos.x < -1*(world.w-Owidth):
                world.background_pos.x = -1*(world.w-Owidth)
            
            #print world.background_pos.x
            
        if int(pos.y) <= 15:
            pygame.mouse.set_pos((pos.x, 15))
            world.background_pos.y+=500*time_passed_seconds
            
            if world.background_pos.y > 0:
                world.background_pos.y = 0
            
        elif int(pos.y) >= Oheight-16:
            pygame.mouse.set_pos((pos.x, Oheight-16))
            world.background_pos.y-=500*time_passed_seconds
            
            if world.background_pos.y < -1*(world.h-Oheight):
                world.background_pos.y = -1*(world.h-Oheight)
            
        if pygame.mouse.get_pressed()[0]:
            if pos.x > clip.minimap_rect.x and pos.y > clip.minimap_rect.y:
                draw = False
                if held != True:
                    world.background_pos.x = (-1*(pos.x-clip.minimap_rect.x)*clip.a)+(clip.rect_view_w*clip.a)/2
                    world.background_pos.y = (-1*(pos.y-clip.minimap_rect.y)*clip.b)+(clip.rect_view_h*clip.b)/2
            

            
        #--------------Mouse Above---------------------------------------
        #--------------Process below-------------------------------------
        
        world.process(time_passed_seconds)
        
        if selected_building == "House":
            selected_img = placing_house_img
        elif selected_building == "LumberYard":
            selected_img = placing_lumberyard_img
        elif selected_building == "Dock":
            selected_img = placing_dock_img
        elif selected_building == "Manor":
            selected_img = placing_manor_img
        
        #--------------Process above-------------------------------------
        #--------------Render Below------------------------
        
        screen.fill((0,0,0))
        clip.render(screen, time_passed_seconds, pos)
        
        all_sprites.clear(screen, world.background)
        all_sprites.update()
        all_sprites.draw(screen)
        
        world.grow_trees(world.Baby_TreeLocations)
        
        if fade.trans_value == 0:
            all_sprites.remove(fade)

        if selected_building!=None:
            if ( pos.x > clip.minimap_rect.x and pos.y > clip.minimap_rect.y ) or ( pos.x < clip.side.w + 32 ):
                pass
            else:
                if not world.test_buildable(selected_building, 0, pos):
                    selected_img = bad_lumberyard_img
                blit_pos = world.get_tile_pos(pos-world.background_pos)*32
                screen.blit(selected_img, ((blit_pos.x-(selected_img.get_width()-32))+world.background_pos.x, (blit_pos.y-(selected_img.get_height()-32))+world.background_pos.y))
        
        #This is for selecting-------------        
        if draw == True and selected_building == None:
            a = Vector2(*pygame.mouse.get_pos())
            lst = world.get_tile_array(start,((a.x-start.x)/32,(a.x-start.x)/32))
            for i in lst:
                for j in i:
                    j.selected = 1
            s = pygame.Surface((abs(a.x-start.x),abs(a.y-start.y)))
            s.set_alpha(25)
            s.fill((255,255,255))
            if  a.x-start.x <=0 and a.y < start.y and a.x > start.x:
                newa = (a.x-(a.x-start.x),a.y)
                screen.blit(s,(newa))
            if  a.x-start.x <= 0 and a.y > start.y and a.x < start.x :
                newa = (a.x,a.y-(a.y-start.y))
                screen.blit(s,(newa))
            if a.x-start.x > 0 and a.y-start.y > 0:
                screen.blit(s,(start))
            if a.x-start.x < 0 and a.y-start.y < 0:
                screen.blit(s,(a))
            pygame.draw.rect(screen,(255,255,255),(start, (a.x-start.x,a.y-start.y)),1)
        #Selecting Above------------------
        
        #--------------Render Above------------------------

        
        pygame.display.flip()
        #pygame.display.set_caption("%.2f"%world.clock.get_fps())

if __name__ == "__main__":
    run()
