import pygame
import math
from Human import Human
#from CarePackage import PackageSystem
from Data import *
from Zombie import Zombie
from loadBackground import loadBackground
from Projectiles import *
from Wall_items import *
from Guns import *
from Gun_Data import All_gun_stuff

def reset_zombie_pos(zombie):
    zombie.reset_posistion()

#human health effects
def is_zombie_attacking(human, zombie):
    pygame.sprite.collide_rect_ratio(.5)
    if pygame.sprite.collide_rect(human, zombie):
        #zombie.update_anim("ATTACK")
        if human.remove_health(.75): #if return True (player is dead) then change to idle and kill player
            #zombie.update_anim("IDLE")
            human.kill()

def explosion_touching_human(human, explotion):
    if pygame.sprite.collide_rect(human, explotion):
        if human.remove_health(50):
            human.kill()

def stun_explosion_touching_human(human, explotion):
    if pygame.sprite.collide_rect(human, explotion):
        human.remove_speed(10)

def package_obtained(package, human):
    if pygame.sprite.groupcollide(package, human, True, False):
        pass

#zombie hit by grenade
def explosion_touching_zombie(zombie, explotion):
    if pygame.sprite.collide_rect(zombie, explotion):
        if zombie.remove_health(75):
            zombie.kill()


def stun_explosion_touching_zombie(zombie, explosion):
    if pygame.sprite.collide_rect(zombie, explosion):
        zombie.remove_speed(3)

def human_touching_item_on_wall(human,items_on_wall, screen,cameraX,cameraY):
    for item in items_on_wall:
        if pygame.sprite.collide_rect(human, item):
            return item.press_to_buy(screen,cameraX,cameraY)


def game_loop():
    pygame.init()
    window = (1080, 720)
    screen = pygame.display.set_mode(window)
    screen.blit(pygame.font.Font(None, 40).render("Loading...", True, (255, 255, 255)), (100, 100))
    pygame.display.update()
    game_is_running = True
    fullscreen_flag = True

    cursor = pygame.image.load('cursor.png')
    pygame.mouse.set_visible(False)

    cameraX, cameraY = 0,0

    bck = loadBackground("background_0.jpg")

    heads_up_display=HUD(window)
    human = Human(window)
    radar = RadarScrn()
    player_cash=Cash()
    health_data = HealthBar(window)
    bullets = pygame.sprite.Group()
    grenades = pygame.sprite.Group()
    explosions=pygame.sprite.Group()
    stun_grenades=pygame.sprite.Group()
    stun_explosions=pygame.sprite.Group()
    all_grenade_data=grenade_data()
    human_group = pygame.sprite.Group(human)
    zombie_group = pygame.sprite.Group()
    item1_on_wall = GunOnWall()
    items_on_wall=pygame.sprite.Group()


    #ALL GUNS
    gun_control=GunControl(window,screen)
    gun_1 = Gun1(window)

    mouseX = pygame.mouse.get_pos()[0]
    mouseY = pygame.mouse.get_pos()[1]
    centerX = int(mouseX - (window[0] / 2.0))
    centerY = -int((mouseY - (window[1] / 2.0)))

    NUMBER_OF_ZOMBIES = 5
    for i in range(NUMBER_OF_ZOMBIES):
        zombie_group.add(Zombie(window, player_cash))

    #ammo_class=gun_1_data(window)
    press_key_x_type=""

    items_on_wall.add(item1_on_wall)

    clock = pygame.time.Clock()
    while game_is_running:
        changeX=changeY=0
        human_anim = "MOVE"

        #Fullscreen Switch
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_BACKSLASH]:
            if fullscreen_flag:
                screen = pygame.display.set_mode(window)
                fullscreen_flag = False
            else:
                screen = pygame.display.set_mode(window, pygame.FULLSCREEN)
                fullscreen_flag = True

        #Controls for moving the camera, moving 40 px per frame
        human_speed=human.get_speed()
        if human.alive():
            if pressed[pygame.K_w]:
                changeY = human_speed
            elif pressed[pygame.K_s]:
                changeY = -human_speed
            if pressed[pygame.K_a]:
                changeX = human_speed
            elif pressed[pygame.K_d]:
                changeX = -human_speed

        cameraX += changeX
        cameraY += changeY

        if cameraX>0+(window[0]/2.0):
            cameraX=0+(window[0]/2.0)
        elif cameraX < -5000+(window[0]/2.0):
            cameraX=-5000+(window[0]/2.0)
        if cameraY>0+(window[1]/2.0):
            cameraY=0+(window[1]/2.0)
        elif cameraY<-5000+(window[1]/2.0):
            cameraY=-5000+(window[1]/2.0)

        #When button is lifted up sets camera x,y change to 0
        if changeX<=0 or changeY<=0:
            human_anim = "IDLE"

        #human touching a item on the wall
        press_key_x_type= human_touching_item_on_wall(human, items_on_wall, screen,cameraX,cameraY)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                gun_control.shoot_gun(bullets,(window[0]/2.0)-cameraX, (window[1]/2.0)-cameraY, centerX, centerY)

            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_g:
                    if all_grenade_data.grenade_amount > 0:
                        grenade = Grenade((window[0] / 2.0) - cameraX, (window[1] / 2.0) - cameraY, centerX, centerY)
                        grenades.add(grenade)
                        all_grenade_data.grenade_amount -= 1
                if event.key==pygame.K_f:
                    if all_grenade_data.stun_grenade_amount>0:
                        stun_grenade = stunGrenade((window[0] / 2.0) - cameraX, (window[1] / 2.0) - cameraY, centerX, centerY)
                        stun_grenades.add(stun_grenade)
                        all_grenade_data.stun_grenade_amount-=1
                if event.key == pygame.K_r:
                    gun_control.reload_gun()
                if event.key==pygame.K_x:
                    if press_key_x_type=="shotgun":
                        All_gun_stuff.buy_new_gun(player_cash,"shotgun")
                if event.key==pygame.K_1:
                    gun_control.change_gun_in_hand()


        # Quit the game
        if pressed[pygame.K_p]:
            pygame.quit()
            quit()

        #Human
        if human_anim == "IDLE":
            human.update_anim("IDLE")
        elif human_anim == "MOVE":
            human.update_anim("MOVE")
        elif human_anim == "SHOOT":
            human.update_anim("SHOOT")


        #Controls background rendering
        image = bck.image_at((0 - cameraX, 0 - cameraY, window[0], window[1]))
        screen.blit(image, (0, 0))
        items_on_wall.update(cameraX,cameraY)
        items_on_wall.draw(screen)

        # 1. Updates zombie animation
        # 1. Checks if Zombie is attacking
        # 2. Sends zombie to Human
        # 3. Moves Zombies when camera moves
        for zombie in zombie_group:
            zombie.update_anim("MOVE")
            is_zombie_attacking(human, zombie)
            zombie.moveZombieTowardMid(cameraX,cameraY)
            zombie.health_bar(screen)
            for explosion in explosions:
                explosion_touching_zombie(zombie, explosion)
            for stun_explosion in stun_explosions:
                stun_explosion_touching_zombie(zombie, stun_explosion)
            zombie.zombie_speed_timer() #check to see if zombie is stunnded and deduct time from stun time

        #Human hit by stun or grenade
        for explosion in explosions:
            explosion_touching_human(human, explosion)
        for stun_explosion in stun_explosions:
            stun_explosion_touching_human(human, stun_explosion)
        human.human_speed_timer()


        #Mouse Controls
        mouseX = pygame.mouse.get_pos()[0]
        mouseY = pygame.mouse.get_pos()[1]
        centerX = int(mouseX - (window[0] / 2))
        centerY = -int((mouseY - (window[1] / 2)))
        rotationAngle = math.degrees(math.atan2(centerY, centerX))
        human.rot_center(rotationAngle)

        #Loads in Human and Zombie
        zombie_group.draw(screen)
        human_group.draw(screen)

        #Bullet animation
        bullets.update(cameraX, cameraY,zombie_group)
        bullets.draw(screen)

        #Grenades and explosions
        grenades.update(cameraX, cameraY, screen, explosions)
        grenades.draw(screen)
        explosions.update(cameraX, cameraY)
        explosions.draw(screen)
        stun_grenades.update(cameraX, cameraY, screen, stun_explosions)
        stun_grenades.draw(screen)
        stun_explosions.update(cameraX, cameraY)
        stun_explosions.draw(screen)

        #Draw crosshair cursor
        screen.blit(cursor, (mouseX - 23, mouseY - 22))

        #pygame.draw.rect(screen, (255, 255, 255), human.get_rect())

        #Updating radar with new data, Human and Zombies
        #radar.draw(screen, -cameraX+960, -cameraY+540)
        # for zombie in zombie_group:
        #     radar.update_zom(screen, zombie)

        #update HUD
        heads_up_display.update(screen,window)
        #Updates Health Bar
        health_data.draw(screen, human.get_health())

        #update ammo text and reload timer
        gun_control.update_ammo_data()

        #update cash amount
        player_cash.update(screen)

        screen.blit(pygame.font.Font(None, 20).render(str(clock.get_fps()), True, (255, 255, 255)), (0, 0))
        pygame.display.flip()
        clock.tick(60)

game_loop()