"""
hole
****

:Author: tobijjah
:Date: 31.05.19
"""
from pygame import Surface
from pygame.draw import circle

from ant.agents.ant import SimpleAnt
from ant.settings import BG_COLOR
from ant.settings import HOLE_COLOR


class Hole:
    """

    Args:
        rect (:obj:`Rect`): The position of the Hole on the display.
        surface (:obj:`Surface`): The surface to draw the Hole on.

    Attributes:
        ants (:obj:`list(Ant)`):
        rect (:obj:`Rect`): The position of the Hole on the display.
        surface (:obj:`Surface`): The surface to draw the Hole on.
    """
    INSTANCES = 0

    def __init__(self, background, width, height):
        self._name = __class__.INSTANCES
        __class__.INSTANCES += 1

        self.ants = []
        self._nutrients = 0

        self.background = background

        dwidth, dheight = .9*width, .9*height

        self.surface = Surface((dwidth, dheight))
        self.rect = self.surface.get_rect(
            height=dheight,
            width=dwidth,
            centerx=width/2,
            centery=height/2
        )

    @property
    def nutrients(self):
        return self._nutrients

    @nutrients.setter
    def nutrients(self, value):
        self._nutrients += value

    def draw(self):
        self.surface.fill(BG_COLOR)
        circle(self.surface, HOLE_COLOR, (int(self.rect.centerx), int(self.rect.centery)), int(self.rect.width/2))
        self.background.blit(self.surface, self.rect)

    def spawn_ant(self, position, rect, surface, **kwargs):
        ant = SimpleAnt(position, rect, surface, **kwargs)
        self.ants.append(ant)

        return ant

    def home(self, ant):
        return ant in self.ants

    def __hash__(self):
        return hash((__class__.__name__, self._name))

    def __str__(self):
        return '{} with {} Ants and {} Nutrients'.format(__class__.__name__, len(self.ants), self._nutrients)

    def __repr__(self):
        return '<{}(name={}) at {}>'.format(__class__.__name__, self._name, hex(id(self)))