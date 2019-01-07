import pygame

class All_gun_stuff():
    gun_in_hand="pistol"
    all_owned_guns=["pistol"]
    price_of_guns={"pistol":0,"shotgun":1000,"assult rifle":2000}

    def current_gun(self):
        return self.gun_in_hand

    def change_gun_in_hand(self,new_gun): #for when users presses 1 or 2
        self.gun_in_hand=new_gun

    def owned_guns(self):
        return self.all_owned_guns

    def buy_new_gun(self,cash,new_gun):
        cash.decrease_cash(self.price_of_guns[new_gun])
        if len(self.all_owned_guns)==2:
            self.all_owned_guns.remove(self.gun_in_hand)
        self.all_owned_guns.append(new_gun)
        self.gun_in_hand=new_gun

    #if already owned then buy ammo not gun

class gun_2_data:
    clip_size = 60
    ammo_amount = 120
    reload_time=60
    def __init__(self,window):
        self.window=window
        self.gun_type = pygame.image.load("gunShotty.png")

    def shooting_bullet(self):
        if self.clip_size >1:
            self.clip_size-=1
        elif self.clip_size ==1:
            self.clip_size-=1
            if self.ammo_amount > 0:
                return self.reload_ammo()
        else:
            return "no ammo"

    def reload_ammo(self):
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
        return "reload"

    def manual_reload(self):
        if self.ammo_amount>0:
            return self.reload_ammo()
        elif self.clip_size==0:
            return "no ammo"

    def reloading(self,screen):
        if self.reload_time>0:
            self.reload_time-=1
            self.update_screen_ammo(screen)
            return "reload"
        else:
            #return nothing so it knows that its not still "reloading"
            self.reload_time=60
            return

    def update_screen_ammo(self,screen):
        if self.clip_size>15:
            color = (255, 255, 255)
        else:
            color=(255,0,0)
        screen.blit(pygame.font.Font(None, 55).render(str(self.clip_size), True, color), (self.window[0] - 250, self.window[1] - 105))
        screen.blit(pygame.font.Font(None, 44).render(str(self.ammo_amount), True, (255,255,255)),(self.window[0] - 170, self.window[1] - 102))
        screen.blit(self.gun_type, (self.window[0]-125, self.window[1]-120))