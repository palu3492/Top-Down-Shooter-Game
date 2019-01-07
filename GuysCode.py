
pygame.init()

window = (400,400)
screen = pygame.display.set_mode(window)

font = pygame.font.Font(None,36)

clock = pygame.time.Clock()

def draw_onto_screen():
    for i in range(0,200):
        for j in range(0,200):
            pygame.draw.rect(background,(0,255,0),(i,j,5,5))

background = pygame.Surface(window)
draw_onto_screen() #### only called once

done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    screen.blit(background,(0,0)) #### blit the background onto screen
    text = font.render(str(clock.get_fps()),1,(10,10,10))
    screen.blit(text,(0,0))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()