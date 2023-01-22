from extra import *
import pygame as pg
from appearance import *


clock = pg.time.Clock()
screen = pg.display.set_mode(WINDOW_SIZE)

playboard = Playboard(screen)

run = True
while run:
    clock.tick(FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.MOUSEBUTTONDOWN:
            playboard.button_down(event.button, event.pos)
        if event.type == pg.MOUSEBUTTONUP:
            playboard.button_up(event.button, event.pos)

pg.quit()
