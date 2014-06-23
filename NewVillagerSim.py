import pygame
pygame.init()

import os
from random import randint
from datetime import datetime
from random import randint

import World
import vector2
import Builder
from Clips import Clips
from crossfade import CrossFade
from VoronoiMapGen import point, mapGen

os.environ['SDL_VIDEO_CENTERED'] = '1'

TILE_SIZE = 32

VILLAGER_COUNT = 15
FARMER_COUNT = 45
BUILDER_COUNT = 1

font = pygame.font.SysFont("Terminal", 20)

FULL_ON = 1


def me_double_size(image):
    """Function for making an image the same size but just 1/2 the quality
       Was going to be used in water path finding algorithm
    """

    Size = image.get_size()
    SmSize = (Size[0] * 10, Size[1] * 10)
    SmImage = pygame.transform.scale(image, SmSize)
    #NormalImage = pygame.transform.scale(SmImage, Size)
    return SmImage


def run():
    pygame.display.set_caption("Villager Simulation")

    sizes = pygame.display.list_modes()
    SCREEN_SIZE = sizes[0]
    Owidth, Oheight = SCREEN_SIZE

    side_size = Owidth / 5.0

    mapGenerator = mapGen()

    if FULL_ON:
        screen = pygame.display.set_mode(
            SCREEN_SIZE, Builder.FULLSCREEN | Builder.HWSURFACE, 32)
    else:
        screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)

    fade = CrossFade(screen)
    all_sprites = pygame.sprite.Group(fade)

    draw = False
    held = False

    #Load the image the world will be based on,
    #then set the world size proportionate to it

    #world_img_str, mini_img_str = random_map("SCREENSHOT", "*")
    #world_img = pygame.image.load(world_img_str).convert()

    #mini_img_str = None
    #world_img = mapGenerator.whole_new(25, (256, 256))

    size = (256, 256)
    w_size = size[0] * TILE_SIZE, size[1] * TILE_SIZE

    seed = randint(0, 100)
    #print seed

    world = World.World(SCREEN_SIZE, w_size, font, seed)
    #pygame.image.save(world.minimap_img, "Images/UBER-COOL-small.png")

    Villager_image = pygame.image.load(
        "Images/Entities/Villager.PNG").convert()
    Farmer_image = pygame.image.load(
        "Images/Entities/Farmer.png").convert()
    Lumberjack_image = pygame.image.load(
        "Images/Entities/Lumberjack.png").convert()
    Builder_image = pygame.image.load(
        "Images/Entities/Builder.png").convert()

    placing_lumberyard_img = pygame.image.load(
        "Images/Buildings/Dark_Lumberyard.png").convert()
    placing_lumberyard_img.set_colorkey((255, 0, 255))
    placing_house_img = pygame.image.load(
        "Images/Buildings/Dark_House.png").convert()
    placing_house_img.set_colorkey((255, 0, 255))
    placing_dock_img = pygame.image.load(
        "Images/Buildings/Dark_Dock.png").convert()
    placing_dock_img.set_colorkey((255, 0, 255))
    placing_manor_img = pygame.image.load(
        "Images/Buildings/Dark_Manor.png").convert()
    placing_manor_img.set_colorkey((255, 0, 255))

    bad_lumberyard_img = pygame.image.load(
        "Images/Buildings/Red_Lumberyard.png").convert()
    bad_lumberyard_img.set_colorkey((255, 0, 255))

    #pygame.image.save(me_double_size(pygame.image.load(
    #    "Images/Buildings/LumberYard_Icon.png").convert()), "LARGERLumb.png")
    #pygame.image.save(me_double_size(pygame.image.load(
    #    "Images/Buildings/Manor_Icon.png").convert()), "LARGERMan.png")

    world.clipper = Clips(world, (Owidth, Oheight))
    #pygame.image.save(world.background, "Images/VeryLargeShowingOff.png")
    #pygame.image.save(world.minimap_img, "Images/SmallAndVariety2.png")

    selected_building = "LumberYard"
    selected_img = pygame.image.load(
        "Images/Buildings/Dark_Lumberyard.png").convert()
    selected_img.set_colorkey((255, 0, 255))

    world.clock.tick()
    while True:

        time_passed = world.clock.tick(60)
        time_passed_seconds = time_passed / 1000.
        pos = vector2.Vector2(* pygame.mouse.get_pos())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if (pos.x > world.clipper.minimap_rect.x
                        and pos.y > world.clipper.minimap_rect.y):
                    pass
                else:
                    if event.button == 1:
                        held = True
                        start = vector2.Vector2(* pygame.mouse.get_pos())
                        draw = True
                        if (pos.x < world.clipper.side.w) and (
                                pos.y < world.clipper.side.top_rect.h):
                            for L in world.clipper.side.tiles:
                                for T in L:
                                    if T is None:
                                        continue

                                    if T.rect.collidepoint((pos.x, pos.y)):
                                        if T.selected:
                                            T.selected = False
                                        else:
                                            T.selected = True

                                        selected_building = T.rep
                                        world.clipper.side.update(T)

                        else:
                            selected_building = None
                            world.clipper.side.update()

                    if event.button == 3 and selected_building is not None:
                        world.add_building(selected_building, pos)
                        if world.test_buildable(selected_building, 0, pos):
                            selected_building = None
                            world.clipper.side.update()

            if event.type == pygame.MOUSEBUTTONUP:
                draw = False
                held = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F2:
                    str1 = str(datetime.now())
                    str1 = str1.split(".")
                    str2 = str1[0] + str1[1]
                    str2 = str2.split(":")
                    str1 = ""
                    for i in str2:
                        str1 += i
                    pygame.image.save(screen,
                        "Images/Screenshots/SCREENSHOT%s.png" % str1)
                if event.key == pygame.K_n:
                    world.new_world()

            if event.type == pygame.VIDEORESIZE:
                Owidth, Oheight = event.size

        #------------------Keys Below------------------------------------------
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_ESCAPE]:
            #quits the game
            pygame.quit()
            exit()

        if pressed_keys[pygame.K_SPACE]:
            #Resets wood
            world.wood = 0

        if pressed_keys[pygame.K_d]:
            #Fast-forward-esk functionability
            world.clock_degree += 5

        if pressed_keys[pygame.K_l]:
            #Test to see what the first entity's state is
            print world.entities[1].brain.active_state

        #--------------Keys Above----------------------------------------
        #--------------Mouse Below---------------------------------------

        if int(pos.x) <= 15:
            if not FULL_ON:
                pygame.mouse.set_pos((15, pos.y))
            world.background_pos.x += 500 * time_passed_seconds
            #print world.background_pos.x
            if world.background_pos.x > side_size:

                world.background_pos.x = side_size

        elif int(pos.x) >= Owidth - 16:
            if not FULL_ON:
                pygame.mouse.set_pos((Owidth - 16, pos.y))
            world.background_pos.x -= 500 * time_passed_seconds

            if world.background_pos.x < -1 * (world.w - Owidth):
                world.background_pos.x = -1 * (world.w - Owidth)
            #print world.background_pos.x

        if int(pos.y) <= 15:
            if not FULL_ON:
                pygame.mouse.set_pos((pos.x, 15))
            world.background_pos.y += 500 * time_passed_seconds

            if world.background_pos.y > 0:
                world.background_pos.y = 0

        elif int(pos.y) >= Oheight - 16:

            if not FULL_ON:
                pygame.mouse.set_pos((pos.x, Oheight - 16))

            world.background_pos.y -= 500 * time_passed_seconds

            if world.background_pos.y < -1 * (world.h - Oheight):
                world.background_pos.y = -1 * (world.h - Oheight)

        if pygame.mouse.get_pressed()[0]:
            if (pos.x > world.clipper.minimap_rect.x
                    and pos.y > world.clipper.minimap_rect.y):
                draw = False
                if held is not True:
                    world.background_pos.x = (-1 * (
                        pos.x - world.clipper.minimap_rect.x)
                        * world.clipper.a) + (
                        world.clipper.rect_view_w * world.clipper.a) / 2
                    world.background_pos.y = (-1 * (
                        pos.y - world.clipper.minimap_rect.y)
                        * world.clipper.b) + (
                        world.clipper.rect_view_h * world.clipper.b) / 2

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

        screen.fill((0, 0, 0))
        world.render_all(screen, time_passed_seconds, pos)

        all_sprites.clear(screen, world.background)
        all_sprites.update()
        all_sprites.draw(screen)

        world.grow_trees(world.Baby_TreeLocations)

        if fade.trans_value == 0:
            all_sprites.remove(fade)

        if selected_building is not None:
            if (pos.x > world.clipper.minimap_rect.x
                   and pos.y > world.clipper.minimap_rect.y) or (
                   pos.x < world.clipper.side.w + 32):
                pass
            else:
                if not world.test_buildable(selected_building, 0, pos):
                    selected_img = bad_lumberyard_img
                blit_pos = world.get_tile_pos(pos - world.background_pos) * 32
                screen.blit(selected_img, ((blit_pos.x - (
                    selected_img.get_width() - 32)) + world.background_pos.x, (
                    blit_pos.y - (selected_img.get_height() - 32))
                    + world.background_pos.y))

        #This is for selecting-------------
        if draw is True and selected_building is None:
            a = vector2.Vector2(* pygame.mouse.get_pos())
            lst = world.get_tile_array(start, ((a.x - start.x) / 32, (
                                       a.x - start.x) / 32))
            for i in lst:
                for j in i:
                    j.selected = 1
            s = pygame.Surface((abs(a.x - start.x), abs(a.y - start.y)))
            s.set_alpha(25)
            s.fill((255, 255, 255))
            if a.x - start.x <= 0 and a.y < start.y and a.x > start.x:
                newa = (a.x - (a.x - start.x), a.y)
                screen.blit(s, (newa))
            if a.x - start.x <= 0 and a.y > start.y and a.x < start.x:
                newa = (a.x, a.y - (a.y - start.y))
                screen.blit(s, (newa))
            if a.x - start.x > 0 and a.y - start.y > 0:
                screen.blit(s, (start))
            if a.x - start.x < 0 and a.y - start.y < 0:
                screen.blit(s, (a))
            pygame.draw.rect(screen, (255, 255, 255), (start, (
                a.x - start.x, a.y - start.y)), 1)
        #Selecting Above------------------

        #--------------Render Above------------------------

        pygame.display.flip()
        #pygame.display.set_caption("%.2f"%world.clock.get_fps())

if __name__ == "__main__":
    run()
