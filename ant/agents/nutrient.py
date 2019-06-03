"""
Module nutrient
****

:Author: tobijjah
:Date: 31.05.19
"""
from pygame import Surface

from ant.agents.mixins import AlphaGradient
from ant.errors import NutrientEmptyError
from ant.settings import NUTRIENT_COLOR


class Nutrient(AlphaGradient):
    """Nutrient is collected by Ants.

    Ants search for Nutrients. Each Ant can collect one Nutrient unit.
    Nutrient provide an interface for collection Nutrient units.

    Args:
        amount (:obj:`int`): The amount of nutrient units.
        rect (:obj:`Rect`): The position of the Nutrient on the display.
        surface (:obj:`Surface`): The surface to draw the Nutrient on.

    Attributes:
        rect (:obj:`Rect`): The position of the Nutrient on the display.
        surface (:obj:`Surface`): The surface to draw the Nutrient on.
    """
    def __init__(self, amount, background, width, height):
        self.background = background

        width, height = width/2, height/2

        self.surface = Surface((width, height))
        self.rect = self.surface.get_rect(
            width=width,
            height=height,
            centerx=width,
            centery=height
        )

        self._amount = int(abs(amount))

        # Mixin attributes
        self._xmin = 0
        self._xmax = amount
        self._ymin = 0
        self._ymax = 255

    @property
    def nutrient_unit(self):
        """:obj:`int`: Get a Nutrient unit."""
        if not self.empty():
            self._amount -= 1
            return 1

        raise NutrientEmptyError()

    def draw(self):
        """Draw Nutrient on surface."""
        self.surface.fill(NUTRIENT_COLOR)
        self.surface.set_alpha(int(self.get_alpha(self._amount)))
        self.background.blit(self.surface, self.rect)

    def empty(self):
        """Is Nutrient empty?

        Returns:
            :obj:`bool`: Is Nutirent amount zero.
        """
        return self._amount == 0

    def __str__(self):
        return '{} with {} units'.format(__class__.__name__, self._amount)

    def __repr__(self):
        return '<{}(amount={}) at {}>'.format(__class__.__name__, self._amount, hex(id(self)))
