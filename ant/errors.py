"""
Module errors
*************

:Author: tobijjah
:Date: 07.05.2019
"""


class CellBaseException(Exception):
    """Inherit from this class for Cell Exceptions"""


class CellOccupiedError(CellBaseException):
    """Raise if a cell is already occupied by a hole or nutrient object"""


class CellAgentError(CellBaseException):
    """Raise if get agents but agents is None"""


class EnvironmentBaseException(Exception):
    """Inherit from this class for Cell Exceptions"""


class EnvironmentOutOfBoundsError(EnvironmentBaseException):
    """Raise if a position is not within field bounds"""


class EnvironmentFullError(EnvironmentBaseException):
    """Raise if field is completely occupied"""


class AgentBaseException(Exception):
    """Inherit from this class for Agent exceptions"""


class NutrientEmptyError(Exception):
    """Raise if nutrient stack is empty"""
