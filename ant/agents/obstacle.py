"""
obstacle
********

:Author: tobijjah
:Date: 03.06.19
"""
from pygame import Surface

from ant.settings import OBSTACLE_COLOR


class Obstacle:
    def __init__(self, background, width, height):
        self.background = background

        dwidth, dheight = .9*width, .9*height

        self.surface = Surface((dwidth, dheight))
        self.rect = self.surface.get_rect(
            width=dwidth,
            height=dheight,
            centerx=width/2,
            centery=height/2
        )

    def draw(self):
        self.surface.fill(OBSTACLE_COLOR)
        self.background.blit(self.surface, self.rect)
