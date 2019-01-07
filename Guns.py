import pygame
import math

pygame.mixer.init()
gun_shot_sound = pygame.mixer.Sound('gunAudio.wav')
gun_1_reload_audio = pygame.mixer.Sound('pistolReloadAudio.wav')
gun_1_shot_audio= pygame.mixer.Sound('gunAudio2.wav')
gun_shot_sound.set_volume(.01)
gun_1_reload_audio.set_volume(.5)
gun_1_shot_audio.set_volume(.05)

class GunControl():
    gun_in_hand = "pistol"
    all_owned_guns = ["pistol"]
    price_of_guns = {"pistol": 0, "shotgun": 1000, "assult rifle": 2000}
    def __init__(self,window,screen):
        self.window=window
        self.screen=screen
        self.gun_1=Gun1(window)
        self.gun_2=Gun2(window)

    def current_gun(self):
        return self.gun_in_hand

    def change_gun_in_hand(self): #for when users presses 1 or 2
        self.all_owned_guns.append("shotgun")
        self.gun_in_hand="shotgun"

    def owned_guns(self):
        return self.all_owned_guns

    def buy_new_gun(self,cash,new_gun):
        cash.decrease_cash(self.price_of_guns[new_gun])
        if len(self.all_owned_guns)==2:
            self.all_owned_guns.remove(self.gun_in_hand)
        self.all_owned_guns.append(new_gun)
        self.gun_in_hand=new_gun

    def shoot_gun(self,bullets_group,startX,startY,x,y):
        if self.gun_in_hand=="pistol":
            self.gun_1.try_to_shoot_bullet(bullets_group,startX,startY,x,y)
        elif self.gun_in_hand == "shotgun":
            self.gun_2.try_to_shoot_bullet(bullets_group, startX, startY, x, y)

    def update_ammo_data(self):
        if self.gun_in_hand == "pistol":
            self.gun_1.update_ammo_stuff(self.screen,self.window)
        elif self.gun_in_hand == "shotgun":
            self.gun_2.update_ammo_stuff(self.screen,self.window)

    def reload_gun(self):
        if self.gun_in_hand == "pistol":
            self.gun_1.manual_reload()
        elif self.gun_in_hand == "shotgun":
            self.gun_2.manual_reload()
def bullet_touching_zombie(zombie,bullet):
    if pygame.sprite.collide_rect(zombie, bullet):
        if zombie.remove_health(20):
            zombie.kill()
        bullet.kill_me=True
        return True
    else:
        return False

#checks to see if the bullet hits a obstacle which will kill the bullet
def bullet_touching_obstacle(self, obstacle_group):
    if pygame.sprite.collide_rect(obstacle_group, self):
        return True

class CreateBullet(pygame.sprite.Sprite):
    # amount bullet is changed on x axis (max will be 1px)
    bullet_change_x = 0
    # amount bullet is changed on y axis (max will be 1px)
    bullet_change_y = 0
    # amount bullet is changed on y axis per frame (unless interrupted by zombie collision)
    bullet_x_per_frame = 0
    #amount bullet is changed on y axis per frame (unless interrupted by zombie collision)
    bullet_y_per_frame = 0
    #x coord for bullet before adding the camera
    bulletX = 0
    #y coord for bullet before adding the camera
    bulletY = 0
    kill_me = False

    def __init__(self,startX, startY, x, y,bullet_speed):
        # bullet_speed how many pixel to move per frame
        pygame.sprite.Sprite.__init__(self)
        angle = math.atan2(y, x)  # find angle of shot
        self.bullet_change_x = math.cos(angle)
        self.bullet_change_y = -math.sin(angle)
        self.bullet_x_per_frame = int(bullet_speed * self.bullet_change_x)  # x change amount
        self.bullet_y_per_frame = int(bullet_speed * self.bullet_change_y)  # Y change amount
        # bullet speed / size of bullet (for checking if bullet is hitting zombie)
        self.continuous=bullet_speed/14
        self.image = pygame.image.load("bullet.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.bulletX = startX - (self.rect[0] / 2)
        self.bulletY = startY - (self.rect[1] / 2)
        gun_1_shot_audio.play()

    #will update the bullet for evey frame changing its location and checking for collisions
    def update(self, camera_x,camera_y,zombie_group):
        if not self.kill_me:
            # checks to see if bullet is touching zombie (bullet_speed / bullet size) times
            for i in range(int(self.continuous)):
                self.rect.x = self.bulletX + camera_x
                self.rect.y = self.bulletY + camera_y
                self.bulletX += (14 * self.bullet_change_x)
                self.bulletY += (14 * self.bullet_change_y)
                for zombie in zombie_group:
                    if bullet_touching_zombie(zombie,self):
                        return
        else:
            self.kill()
        # kill bullet off screen (change to hitting wall to kill bullet)
        if self.rect.x > 1000 or self.rect.x < -1000 or self.rect.y > 1000 or self.rect.y < -1000:
            self.kill_me = True
class GunActions():
    #does all the things that each guns needs to do
    #grabs variables from gun classes
    def __init__(self):
        pass
        self.gun_variables=GunVaribles()

class GunVaribles():
    #make a list for each gun and this class will return the gun varibles
    test_v=0
    def gun_1_variables(self):
        bullet_speed = 60
        clip_size = 20
        ammo_amount = 60
        reload_time = 60
        ammo_state = ""
        kill_me = False
        price = 2000
        image=pygame.image.load("pistol.png")
        sound=(gun_1_shot_audio,gun_1_reload_audio)
        return [bullet_speed,clip_size,ammo_amount,reload_time,ammo_state,kill_me,price,image,sound]
    def bluu(self):
        pass

class Gun1():
    # how many pixel to move per frame
    bullet_speed = 60
    #how many bullets each clip can hold. starts at 20.
    clip_size = 20
    #amount of ammo you have besides your clip. will start being a multiple of clip size.
    ammo_amount = 60
    #amount of frames if will take to complete 1 reload (change this to clock timer rather than fps)
    reload_time=60
    #will either be nothing, reloading, or no ammo. nothing meaning you can shoot a bullet
    ammo_state=""
    #if bullet needs to be killed but still want to load that bullet for that frame (else use self.kill())
    kill_me = False
    price=2000
    gun_image = pygame.image.load("pistol.png")
    #shoot and reload sound

    def __init__(self,window_size):
        self.window=window_size

    #checks to see if there is ammo and you are not currently reloading gun then it will create bullet
    def try_to_shoot_bullet(self,bullets_group,startX,startY,x,y):
        if self.ammo_state=="":
            new_bullet=CreateBullet(startX, startY, x, y,self.bullet_speed)
            bullets_group.add(new_bullet)
            self.bullet_fired()

    def can_shoot_bullet_now(self):
        #return true if bullet can be fired right now
        pass

    def bullet_fired(self):
        if self.clip_size >1:
            self.clip_size-=1
        elif self.clip_size ==1:
            self.clip_size-=1
            if self.ammo_amount > 0:
                self.start_reload()
        else:
            self.ammo_state = "no ammo"

    #checks to see if you are reloading or have no ammo
    def check_ammo_status(self):
        return self.ammo_state

    #started when ammo reaches 0, tries to reload gun
    def out_of_ammo_reload(self):
        pass

    #when use intiates a reload it will try to reload gun
    def manual_reload(self):
        if self.ammo_amount>0:
            self.start_reload()

    def start_reload(self):
        gun_1_reload_audio.play()
        #if clip is empty and ammo has at least 60 bullets
        if self.ammo_amount >= 60 and self.clip_size==0:
            self.ammo_amount -= 60
            self.clip_size = 20
        #if clip is empty and ammo does not have 60 bullets in it
        elif self.ammo_amount<60 and self.clip_size==0:
            self.clip_size=self.ammo_amount
            self.ammo_amount=0
        #if clip has bullets in it and ammo has enough to fill it
        elif self.clip_size!=0 and self.ammo_amount>=60-self.clip_size:
            self.ammo_amount-= 60-self.clip_size
            self.clip_size=20
        #if clip has bullets in it and ammo cant fill it
        elif self.clip_size!=0 and self.ammo_amount<60-self.clip_size:
            self.clip_size+=self.ammo_amount
            self.ammo_amount=0
        self.ammo_state="reload"

    def update_ammo_stuff(self,screen,window):
        self.update_ammo_on_screen(screen)
        self.update_gun_HUD_image(screen,window)
        if self.ammo_state=="reload":
            self.update_reload_timer(screen,window)

    def update_reload_timer(self,screen,window):
        if self.reload_time>0:
            screen.blit(pygame.font.Font(None, 30).render("Reloading", True, (255, 255, 255)),
                        ((window[0] / 2.0) - 50, 100))
            self.reload_time-=1
        else:
            #make ammo_state nothing so it knows that its not still "reloading"
            self.reload_time=60
            self.ammo_state = ""

    def update_ammo_on_screen(self, screen):
        if self.clip_size>15:
            color = (255, 255, 255)
        else:
            color=(255,0,0)
        screen.blit(pygame.font.Font(None, 55).render(str(self.clip_size), True, color), (self.window[0] - 250, self.window[1] - 105))
        screen.blit(pygame.font.Font(None, 44).render(str(self.ammo_amount), True, (255,255,255)),(self.window[0] - 170, self.window[1] - 102))

    def update_gun_HUD_image(self,screen,window):
        screen.blit(self.gun_image, (self.window[0] - 100, self.window[1] - 120))

class Gun2():
    # how many pixel to move per frame
    bullet_speed = 150
    #how many bullets each clip can hold. starts at 20
    clip_size = 60
    #amount of ammo you have besides your clip. will start being a multiple of clip size.
    ammo_amount = 120
    #amount of frames if will take to complete 1 reload (change this to clock timer rather than fps)
    reload_time=60
    #will either be nothing, reloading, or no ammo. nothing meaning you can shoot a bullet
    ammo_state=""
    #if bullet needs to be killed but still want to load that bullet for that frame (else use self.kill())
    kill_me = False
    price=2000
    gun_image=pygame.image.load("gunAK47.png")

    def __init__(self,window_size):
        self.window=window_size

    #checks to see if there is ammo and you are not currently reloading gun then it will create bullet
    def try_to_shoot_bullet(self,bullets_group,startX,startY,x,y):
        if self.ammo_state=="":
            new_bullet=CreateBullet(startX, startY, x, y,self.bullet_speed)
            bullets_group.add(new_bullet)
            self.bullet_fired()

    def can_shoot_bullet_now(self):
        #return true if bullet can be fired right now
        pass

    def bullet_fired(self):
        if self.clip_size >1:
            self.clip_size-=1
        elif self.clip_size ==1:
            self.clip_size-=1
            if self.ammo_amount > 0:
                self.start_reload()
        else:
            self.ammo_state = "no ammo"

    #checks to see if you are reloading or have no ammo
    def check_ammo_status(self):
        return self.ammo_state

    #started when ammo reaches 0, tries to reload gun
    def out_of_ammo_reload(self):
        pass

    #when use intiates a reload it will try to reload gun
    def manual_reload(self):
        if self.ammo_amount>0:
            self.start_reload()

    def start_reload(self):
        #if clip is empty and ammo has at least 60 bullets
        if self.ammo_amount >= 60 and self.clip_size==0:
            self.ammo_amount -= 60
            self.clip_size = 60
        #if clip is empty and ammo does not have 60 bullets in it
        elif self.ammo_amount<60 and self.clip_size==0:
            self.clip_size=self.ammo_amount
            self.ammo_amount=0
        #if clip has bullets in it and ammo has enough to fill it
        elif self.clip_size!=0 and self.ammo_amount>=60-self.clip_size:
            self.ammo_amount-= 60-self.clip_size
            self.clip_size=60
        #if clip has bullets in it and ammo cant fill it
        elif self.clip_size!=0 and self.ammo_amount<60-self.clip_size:
            self.clip_size+=self.ammo_amount
            self.ammo_amount=0
        self.ammo_state="reload"

    def update_ammo_stuff(self,screen,window):
        self.update_ammo_on_screen(screen)
        self.update_gun_HUD_image(screen,window)
        if self.ammo_state=="reload":
            self.update_reload_timer(screen,window)

    def update_reload_timer(self,screen,window):
        if self.reload_time>0:
            screen.blit(pygame.font.Font(None, 30).render("Reloading", True, (255, 255, 255)),
                        ((window[0] / 2.0) - 50, 100))
            self.reload_time-=1
        else:
            #make ammo_state nothing so it knows that its not still "reloading"
            self.reload_time=60
            self.ammo_state = ""

    def update_ammo_on_screen(self, screen):
        if self.clip_size>15:
            color = (255, 255, 255)
        else:
            color=(255,0,0)
        screen.blit(pygame.font.Font(None, 55).render(str(self.clip_size), True, color), (self.window[0] - 250, self.window[1] - 105))
        screen.blit(pygame.font.Font(None, 44).render(str(self.ammo_amount), True, (255,255,255)),(self.window[0] - 170, self.window[1] - 102))

    def update_gun_HUD_image(self,screen,window):
        screen.blit(self.gun_image, (self.window[0] - 125, self.window[1] - 120))
