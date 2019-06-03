"""
settings
********

:Author: tobijjah
:Date: 07.05.2019
"""
from numpy.random import RandomState

GLOBAL_RNG = RandomState(42)

# display colors
BG_COLOR = 255, 255, 255  # white

CELL_COLOR = BG_COLOR

HOLE_COLOR = 217, 95, 14  # brown-orangeish

NUTRIENT_COLOR = 49, 163, 84  # greenish

PHEROMONE_COLOR = 255, 0, 0  # red

ANT_WITHOUT_NUTRIENT_COLOR = 115, 115, 115  # greyish

ANT_WITH_NUTRIENT_COLOR = NUTRIENT_COLOR

SELECTION_COLOR = 255, 0, 0  # red

OBSTACLE_COLOR = 0, 0, 0  # black

# algorithm parameter
GAMMA = .001
""":obj:`float`: Pheromone init value (GAMMA < 1)."""

ALPHA = 1.3
""":obj:`float`: Importance of pheromone deposit (ALPHA >= 0)

IF ALPHA = 0 AND BETA = 1 (greedy decision)
IF ALPHA = 1 AND BETA = 0 (random decision)
"""

BETA = .9
""":obj:`float`: Importance move attractiveness (BETA >= 1)"""

Q = 1.
""":obj:`float`: Global pheromone increment (Q > 0)"""

RHO = .005
""":obj:`float`: Pheromone decay (0 < RHO < 1)"""
