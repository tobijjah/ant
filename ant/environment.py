"""
environment
***********

:Author: tobijjah
:Date: 07.05.2019
"""
from math import floor
from numpy import ravel
from pygame import Rect
from pygame import Surface
from pygame.draw import rect as square

from ant.agents.hole import Hole
from ant.agents.nutrient import Nutrient
from ant.agents.pheromone import Pheromone
from ant.errors import CellAgentError
from ant.errors import CellOccupiedError
from ant.errors import EnvironmentFullError
from ant.errors import EnvironmentOutOfBoundsError
from ant.settings import CELL_COLOR
from ant.settings import GLOBAL_RNG
from ant.settings import SELECTION_COLOR


# TODO add logging, add __str__, update doc, update tests


class Environment:
    """Class is the environment where the other classes/agents (Pheromone, Hole and Nutrient) lives.

    Basically it is a 2D list where each list element is a Cell object which holds
    a reference to other classes/agents. This class can be used to spawn Holes and Nutrients.
    Further it provides an interface to get the visible Cells for an Ant.
    To instantiate the class two arguments are required while three additional arguments are optional.

    Args:
        transform (:obj:`Affine`): Affine transformation matrix of the display.
        background (:obj:`Surface`): The surface to draw on.
        size (:obj:`tuple(int, int)`, optional): Defines the size of the 2D environment must
            be a tuple of two integers. First element is number of rows and second element is
            number of columns.
        neighbours (:obj:`int`, optional): Defines the number of visible neighbour cells for an
            Ant from its position. Only four or eight cells can be visible for an Ant.
        torus (:obj:`bool`, optional): If an Ant is at an edge or corner of the
            environment and torus is false the visible cells are only in bounds of the field.
            If true the Ant perceives the opposite of the field.

    Attributes:
        transform (:obj:`int`): Affine transformation matrix.
        neighbours (:obj:`int`): The total number of neighbours of a Cell.
        torus (:obj:`bool`): Environment is torus.
    """
    def __init__(self, transform, background, size=(10, 10), neighbours=4, torus=False):
        self.torus = torus
        self.transform = transform  # use this matrix (~transform) for transform of display coords to field coords
        self.inverse_transform = ~self.transform

        self._rows, self._cols = size
        self._rng = GLOBAL_RNG

        # init field with cell objects
        self._field = [
            [
                Cell(Position(x, y), background, Rect(*((x, y)*self.transform), self.transform.a, self.transform.e))
                for x in range(self._cols)
            ]
            for y in range(self._rows)
        ]

        self._field_flat = ravel(self._field)
        self._rng.shuffle(self._field_flat)

        if neighbours <= 4:  # von Neumann neighbourhood
            self.neighbours = 4
            self._rules = (Position(-1, 0), Position(0, 1), Position(1, 0), Position(0, -1))

        else:  # Moore neighbourhood
            self.neighbours = 8
            self._rules = (Position(-1, 0), Position(-1, 1), Position(0, 1), Position(1, 1),
                           Position(1, 0), Position(1, -1), Position(0, -1), Position(-1, -1))

    def draw(self):
        """Draw Environment on surface.

        Attention, this redraws the entire field.
        """
        for row in self._field:
            for cell in row:
                cell.draw()

    def spawn_hole(self, position=None):
        """Spawns a Hole on field.

        Spawns a Hole at a random position. If position is provided the Hole is spawned
        at this position.

        Args:
            position (:obj:`Position`, optional): If set the position where to spawn the Hole.
                If not set the Hole is spawned at a random position.

        Returns:
            :obj:`Cell`: A Cell with a Hole.

        Raises:
            EnvironmentFullError: If all Cells are occupied by a Hole or Nutrient.
        """
        if position:
            cell = self.get_cell(position)
            return cell.spawn_hole()

        else:
            for cell in self._field_flat:
                if not cell.occupied():
                    return cell.spawn_hole()

        raise EnvironmentFullError('No space anymore to spawn a hole')

    def spawn_nutrient(self, position=None, amount=100):
        """Spawns a Nutrient on field.

        Spawns a Nutrient at a random position. If position is provided the Nutrient is spawned
        at this position.

        Args:
            position (:obj:`Position`, optional): If set the position where to spawn the Nutrient.
                If not set the Nutrient is spawned at a random position.
            amount (:obj:`int`, optional): The amount of nutrients to spawn.

        Returns:
            :obj:`Cell`: A Cell with a Nutrient.

        Raises:
            EnvironmentFullError: If all Cells are occupied by a Hole or Nutrient.
        """
        if position:
            cell = self.get_cell(position)
            return cell.spawn_nutrient(amount)

        else:
            for cell in self._field_flat:
                if not cell.occupied():
                    return cell.spawn_nutrient(amount)

        raise EnvironmentFullError('No space anymore to spawn a hole')

    def visible(self, ant):
        """Determine neighbour cells for an Ant.

        Method returns neighbours cells for an Ant based on Neumann or Moore neighbourhood.

        Args:
            ant (:obj:`Ant`): An Ant object derived from BaseAnt.

        Returns:
            :obj:`list(Cell)`: A list of neighbour cells for the Ant.
        """
        if self.torus:
            return [self.get_torus_cell(ant.pos + rule) for rule in self._rules]

        else:
            return [self.get_cell(ant.pos + rule) for rule in self._rules if self.on_field(ant.pos + rule)]

    def get_cell(self, position):
        """Returns Cell at the position on field.

        Args:
            position (:obj:`Position`): The field position.

        Returns:
            :obj:`Cell`: Cell at the position.

        Raises:
            EnvironmentOutOfBoundsError: If position is not on field.
        """
        if self.on_field(position):
            return self._field[position.y][position.x]

        raise EnvironmentOutOfBoundsError('Position {} out of bounds'.format(position))

    def get_display_cell(self, event):
        x, y = event.pos * self.inverse_transform
        pos = Position(floor(x), floor(y))

        return self.get_cell(pos)

    def get_torus_cell(self, position):
        """Return Cell at the position from field.

        Returns a cell even if the position is not on field.

        Args:
            position (:obj:`Position`): The field position.

        Returns:
            :obj:`Cell`: Cell at the position.
        """
        try:
            return self.get_cell(position)

        except EnvironmentOutOfBoundsError:
            x, y = position.x % self._cols, position.y % self._rows
            return self.get_cell(Position(x, y))

    def on_field(self, position):
        """Determines if position is on field.

        Args:
            position (:obj:`Position`): The requested position

        Returns:
            :obj:`bool`
        """
        return 0 <= position.x < self._cols and 0 <= position.y < self._rows

    def __repr__(self):
        msg = '<{}(transform={}, surface={}, size=({},{}), visible={}, infinite={}) at {}>'.format(
            __class__.__name__, self._rows, self.transform, self._field[0][0].surface,
            self._cols, len(self._rules), self.torus, hex(id(self))
        )
        return msg

    def __len__(self):
        return self._field.__len__()

    def __getitem__(self, item):
        return self._field.__getitem__(item)

    def __iter__(self):
        return self._field.__iter__()


class Cell:
    """Cell is a component of the Environment field.

    This class holds references to the static classes/agents (Hole, Nutrient, and Pheromone) of the model.
    Further this class provides an interface to spawn the following classes: Hole, Nutrient, and Ant.
    A Cell can have only a Hole or Nutrient both classes can not exists in parallel on a Cell.

    Args:
        position (:obj:`Position`): Cell position on Environment field.
        rect (:obj:`Rect`): The position of the cell on the display.
        surface (:obj:`Surface`): The surface to draw the Cell on.

    Attributes:
        pos (:obj:`Position`): Cell position on Environment field.
        rect (:obj:`Rect`): Pygame rect stores Cell position on display.
        surface (:obj:`Surface`): Surface to draw on.
    """
    def __init__(self, position, background, rect):
        self.pos = position
        self._selected = False
        self.background = background

        self.surface = Surface((rect.width, rect.height))
        self.rect = self.surface.get_rect(
            top=rect.top,
            left=rect.left,
            width=rect.width,
            height=rect.height
        )

        self._hole = None
        self._nutrient = None
        self._pheromone = None

    @property
    def hole(self):
        """:obj:`Hole`: The Hole, raises CellAgentError if Cell has no Hole."""
        if self.has_hole():
            return self._hole

        raise CellAgentError('Cell has no hole agents')

    @hole.deleter
    def hole(self):
        self._hole = None

    @property
    def nutrient(self):
        """:obj:`Nutrient`: The Nutrient, raises CellAgentError if Cell has no Nutrient."""
        if self.has_nutrient():
            return self._nutrient

        raise CellAgentError('Cell has no nutrient agents')

    @nutrient.deleter
    def nutrient(self):
        self._nutrient = None

    @property
    def pheromone(self):
        """:obj:`Pheromone`: The Pheromone, raises CellAgentError if Cell has no Pheromone."""
        if self.has_pheromone():
            return self._pheromone

        raise CellAgentError('Cell has no pheromone agents')

    @pheromone.deleter
    def pheromone(self):
        self._pheromone = None

    def set_selected(self):
        self._selected = not self._selected

    def draw(self):
        """Draw Cell on surface."""
        # uncomment for disco mode
        # self.surface.fill([GLOBAL_RNG.randint(0,255,1), GLOBAL_RNG.randint(0,255,1), GLOBAL_RNG.randint(0,255,1)])
        self.surface.fill(CELL_COLOR)  # clear cell content for new draw

        if self._selected:
            square(self.surface, SELECTION_COLOR, self.surface.get_rect(), 1)

        for attr in ['pheromone', 'nutrient', 'hole']:

            try:
                obj = self.__getattribute__(attr)
                obj.draw()

            except CellAgentError:
                continue

        self.background.blit(self.surface, self.rect)  # finally blit to background

    def spawn_hole(self):
        """Spawns a Hole on the Cell.

        Returns:
            :obj:`Cell`: The Cell with a reference to the spawned Hole.

        Raises:
            CellOccupiedError: If the Cell is already occupied by a Hole or Nutrient.
        """
        if not self.occupied():
            self._hole = Hole(self.surface, self.rect.width, self.rect.height)
            return self

        raise CellOccupiedError("Cell has already a Nutrient or Hole")

    def spawn_nutrient(self, amount):
        """Spawns a Nutrient on the Cell.

        Returns:
            :obj:`Cell`: The Cell with a reference to the spawned Nutrient.

        Raises:
            CellOccupiedError: If the Cell is already occupied by a Hole or Nutrient.
        """
        if not self.occupied():
            self._nutrient = Nutrient(amount, self.surface, self.rect.width, self.rect.height)
            return self

        raise CellOccupiedError("Cell has already a Nutrient or Hole")

    def spawn_pheromone(self):
        if not self.has_pheromone():
            self._pheromone = Pheromone(self.surface, self.rect.width, self.rect.height)
            return self.pheromone

        raise CellOccupiedError('Cell has already a Pheromone')

    def spawn_ant(self, **kwargs):
        """Spawns an Ant agents.

        Spawns an Ant and returns it. Ants can only be spawned on Cells with a hole.

        Args:
            atype (:obj:`str`): The Ant class type to return (one of simple or complex)
            **kwargs: Please refer to Ant factory method or Ant base class for further details

        Returns:
            :obj:`Ant`: The spawned Ant.

        Raises:
            CellAgentError: If the Cell does not have a Hole.
        """
        if self.has_hole():
            # receives the background and the cell rect
            return self._hole.spawn_ant(self, self.background, self.rect, **kwargs)

        raise CellAgentError("Ant spawn requires a hole agents")

    def has_hole(self):
        """Does the Cell have a Hole?

        Returns:
            :obj:`bool`
        """
        return self._hole is not None

    def has_nutrient(self):
        """Does the Cell have a Nutrient?

        Returns:
            :obj:`bool`
        """
        return self._nutrient is not None

    def has_pheromone(self):
        """Does the Cell have a Pheromone?

        Returns:
            :obj:`bool`
        """
        return self._pheromone is not None

    def occupied(self):
        """Is the Cell occupied?

        True if has_hole or has_nutrient evaluate to true.

        Returns:
            :obj:`bool`
        """
        return self._hole or self._nutrient

    def __eq__(self, other):
        if isinstance(other, Cell):
            return self.pos == other.pos

        return False

    def __hash__(self):
        return hash((__class__.__name__, hash(self.pos)))

    def __str__(self):
        return ''

    def __repr__(self):
        return '<{}(position={}, rect={}, surface={}) at {}>'.format(
            __class__.__name__, self.pos, self.rect, self.surface, hex(id(self))
        )


class Position:
    """Convenience class for storing Environment field coordinates.

    Provides an interface to add and compare positions by pythons dunder methods.
    Positions are hashable therefore operations like position in positions are possible.

    Args:
        x (:obj:`int`): X-coord
        y (:obj:`int`): Y-coord

    Attributes:
        x (:obj:`int`): X-coord
        y (:obj:`int`): Y-coord
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        if isinstance(other, Position):
            return Position(self.x + other.x, self.y + other.y)

        raise ValueError()

    def __hash__(self):
        return hash((__class__.__name__, self.x, self.y))

    def __eq__(self, other):
        if isinstance(other, Position):
            return self.x == other.x and self.y == other.y

        return False

    def __str__(self):
        return '{}({}, {})'.format(__class__.__name__, self.x, self.y)

    def __repr__(self):
        return '<{}(x={}, y={}) at {}>'.format(__class__.__name__, self.x, self.y, hex(id(self)))
