"""
pheromone
*********

:Author: tobijjah
:Date: 31.05.19
"""
from pygame import Surface

from ant.agents.mixins import AlphaGradient
from ant.settings import GAMMA
from ant.settings import PHEROMONE_COLOR
from ant.settings import Q
from ant.settings import RHO


class Pheromone(AlphaGradient):
    """Pheromone control Ant movement.

    Pheromone are placed by Ants on cells during their movement through the environment.
    Pheromone are sigmoid functions whom intensity is between [0,1]. Pheromone provide an
    interface for decreasing and increasing their intensity.

    Args:
        rect (:obj:`Rect`): The position of the Pheromone on the display.
        surface (:obj:`Surface`): The surface to draw the Pheromone on.
        steepness (:obj:`float`, optional): The steepness of the sigmoid function.
        rel_tol (:obj:`float`, optional): Relative tolerance to 1.

    Attributes:
        intensity (:obj:`float`): Current intensity of the Pheromone.
        rect (:obj:`Rect`): The position of the Pheromone on the display.
        surface (:obj:`Surface`): The surface to draw the Pheromone on.
    """

    MIN_INTENSITY = GAMMA
    MAX_INTENSITY = GAMMA

    def __init__(self, background, width, height, gamma=GAMMA, q=Q, rho=RHO):
        self.intensity = GAMMA

        self.background = background

        dwidth, dheight = 0.8*width, 0.8*height

        self.surface = Surface((dwidth, dheight))
        self.rect = self.surface.get_rect(
            width=dwidth,
            height=dheight,
            centerx=width/2,
            centery=height/2,
        )

        self._q = q
        self._gamma = gamma
        self._rho = rho

        self._xmin = __class__.MIN_INTENSITY
        self._xmax = __class__.MAX_INTENSITY
        self._ymin = 0
        self._ymax = 255

    def draw(self):
        """Draw Pheromone on surface."""
        self.surface.fill(PHEROMONE_COLOR)

        self._xmin = __class__.MIN_INTENSITY
        self._xmax = __class__.MAX_INTENSITY

        self.surface.set_alpha(int(self.get_alpha(self.intensity)))

        self.background.blit(self.surface, self.rect)

    def update(self, length):
        """Increases the Pheromone intensity by a certain amount.

        Args:
            amount (:obj:`float`): Increase Pheromone intensity by this amount
        """
        self.intensity = (1-RHO) * self.intensity + 1/length

        if self.intensity > __class__.MAX_INTENSITY:
            __class__.MAX_INTENSITY = self.intensity

        if self.intensity < __class__.MIN_INTENSITY:
            __class__.MIN_INTENSITY = self.intensity

    def decoy(self):
        self.intensity = (1-RHO) * self.intensity

    def __str__(self):
        return '{} with {} intensity'.format(__class__.__name__, self.intensity)

    def __repr__(self):
        return '<{}(gamma={}, q={}, rho={}) at {}>'.format(
            __class__.__name__, self._gamma, self._q, self._rho, hex(id(self))
        )
