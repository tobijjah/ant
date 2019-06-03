"""
settings
********

:Author: tobijjah
:Date: 07.05.2019
"""
from numpy.random import RandomState

GLOBAL_RNG = RandomState(42)

# display colors
BG_COLOR = 255, 255, 255

CELL_COLOR = 255, 255, 255

HOLE_COLOR = 217, 95, 14

NUTRIENT_COLOR = 49, 163, 84

PHEROMONE_COLOR = 255, 0, 0

ANT_COLOR = 115, 115, 115

SELECTION_COLOR = 255, 0, 0

# algorithm parameter
GAMMA = 0.001
""":obj:`float`: Pheromone init value (GAMMA < 1)."""

ALPHA = 1.3
""":obj:`float`: Importance of pheromone deposit (ALPHA >= 0)

IF ALPHA = 0 AND BETA = 1 (greedy decision)
IF ALPHA = 1 AND BETA = 0 (random decision)
"""

BETA = .9
""":obj:`float`: Importance move attractiveness (BETA >= 1)"""

Q = 1.0
""":obj:`float`: Global pheromone increment (0 < Q)"""

RHO = 0.005
""":obj:`float`: Pheromone decay (0 < RHO < 1)"""
