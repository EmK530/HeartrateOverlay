import time
import math
from threading import Thread

width = 256
FPS = 60

HeartRate = [0,0]
running = [True]

thread = None

def write(num):
    HeartRate[0]=num
    HeartRate[1]=time.time()

def main():
    print("PyGame init...")
    height=width
    import os
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
    try:
        import pygame
    except ImportError:
        from os import system
        system("pip install pygame")
        import pygame
    import pygame.freetype
    pygame.init()
    clock = pygame.time.Clock()
    print("Begin render.")
    screen = pygame.display.set_mode((width,height))
    pygame.display.set_caption("Heart Overlay")
    surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA, 32)
    heart = pygame.image.load("heart_blur.png")
    heart.get_rect().center = (width/2,height/2)
    surface.set_colorkey([0,0,0])
    fnt = pygame.freetype.SysFont('ArialBold', width/6.73684210526)
    fnt2 = pygame.freetype.SysFont('ArialBold', width/12.8)
    timer = 0
    timer2 = 0
    hr=60
    while running[0]:
        hr2=str(HeartRate[0])
        if int(hr2) > 0:
            hr=int(hr2)
        else:
            hr=60
        inactive=False
        if hr2 == "0" or hr2 == "-3" or hr2 == "-10":
            hr2 = "?"
        elif time.time()-3 > HeartRate[1]:
            hr2 = "?"
            inactive=True
        tick=clock.tick(FPS)
        timer=(timer+((tick/1000)*(hr/60)))%1
        timer2=timer2+tick/250
        if hr2 == "?":
            scale = math.sin(timer2)/2-0.5
        else:
            scale = math.pow(1/(timer+1),10)
        screen.fill((0,0,0))
        surface.fill((0,0,0))
        t1 = fnt.get_rect(hr2)
        t1.center = screen.get_rect().center
        fnt.render_to(screen,t1.topleft,hr2,(200,200,200))
        if hr2 == "?":
            string=None
            if HeartRate[1] == 0:
                string = "Waiting for heart rate..."
            else:
                string = "Watch failed, please wait!"
            if inactive:
                string = "Heart rate sensor froze."
            t2 = fnt2.get_rect(string)
            t2.center = (width/2,t2.height/2+10)
            fnt2.render_to(screen,t2.topleft,string,(200,200,200))
        tempheart=pygame.transform.scale(heart,((width)+((width/4)*scale),(height)+((height/4)*scale)))
        surface.blit(tempheart,(-(width/8)*scale,-(height/8)*scale))
        #surface.blit(heartrate,text_rect)
        screen.blit(surface,(0,0))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running[0] = False
    print("PyGame closed.")

def start():
    print("Starting PyGame thread...")
    thread=Thread(target=main)
    thread.start()
