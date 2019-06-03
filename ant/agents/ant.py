"""
ant
***

:Author: tobijjah
:Date: 31.05.19
"""
from abc import ABCMeta
from abc import abstractmethod

from math import sqrt
from numpy import array
from pygame import Surface

from ant.settings import ALPHA
from ant.settings import ANT_WITHOUT_NUTRIENT_COLOR, ANT_WITH_NUTRIENT_COLOR
from ant.settings import BETA
from ant.settings import GAMMA
from ant.settings import GLOBAL_RNG
from ant.settings import Q


class BaseAnt(metaclass=ABCMeta):

    INSTANCES = 0

    def __init__(
            self,
            cell,
            background,
            rect,
            gamma=GAMMA,
            beta=BETA,
            alpha=ALPHA,
            q=Q
    ):

        self._rng = GLOBAL_RNG
        self._name = __class__.INSTANCES
        __class__.INSTANCES += 1

        self.pos = cell.pos
        self.background = background

        width, height = 0.2*rect.width, 0.2*rect.height

        self.surface = Surface((width, height))
        self.rect = background.get_rect(
            top=self._rng.uniform(rect.top, rect.bottom - height),
            left=self._rng.uniform(rect.left, rect.right - width),
            width=width,
            height=height
        )
        self.x_off, self.y_off = self.rect.left - rect.left, self.rect.top - rect.top

        # algorithm parameter
        self._gamma = gamma
        self._alpha = alpha
        self._beta = beta
        self._q = q

        self._mandible = 0
        self._current_cell = cell
        self._movement_cell = None

        self._visited = list()  # contains visited cells
        self._allowed = list()  # allowed movement cells

        self._trail_length = 0

    @abstractmethod
    def collide(self, cells):
        pass

    @abstractmethod
    def move(self, cells):
        pass

    def mandible_full(self):
        return self._mandible > 0

    def draw(self):
        if self.mandible_full():
            self.surface.fill(ANT_WITH_NUTRIENT_COLOR)

        else:
            self.surface.fill(ANT_WITHOUT_NUTRIENT_COLOR)

        self._update_rect()
        self.background.blit(self.surface, self.rect)

    def _update_rect(self):
        dx = (self._current_cell.rect.left + self.x_off) - self.rect.left
        dy = (self._current_cell.rect.top + self.y_off) - self.rect.top

        self.rect.move_ip(dx, dy)

    def _allowed_cells(self, cells):
        # filter for obstacles
        self._allowed = list(set(cells) - set(self._visited))
        self._allowed = list(filter(lambda cell: not cell.has_obstacle(), self._allowed))

    def _probabilities(self, target):
        probabilities = array([
            cell.pheromone.intensity ** self._alpha * (1 / __class__.euclidean(cell, target)) ** self._beta
            if cell.has_pheromone() else
            self._gamma ** self._alpha * (1 / __class__.euclidean(cell, target)) ** self._beta
            for cell in self._allowed
        ])

        return probabilities / probabilities.sum()

    @staticmethod
    def euclidean(origin, target):
        return sqrt(
            ((origin.pos.x - target.pos.x)**2 + (origin.pos.y - target.pos.y)**2) + 0.0000001
        )

    def __hash__(self):
        return hash((self.__class__.__name__, self._name))

    def __str__(self):
        return '{} {} at position {} with {} unit nutrient'.format(self.__class__.__name__,
                                                                   self._name, str(self.pos),
                                                                   self._mandible)

    def __repr__(self):
        msg = '<{}(pos={}, gamma={}, alpha={}, beta={}, q={}) at {}>'.format(
            self.__class__.__name__, str(self.pos), self._gamma, self._alpha,
            self._beta, self._q, hex(id(self))
        )
        return msg


class SimpleAnt(BaseAnt):
    def __init__(self, cell, rect, background, **kwargs):
        super().__init__(cell, rect, background, **kwargs)

    def collide(self, cells):
        pass

    def move(self, cells):
        if self.mandible_full():
            self._update_pheromone()
            self._movement_cell = self._visited.pop()

            if self._movement_cell.has_hole() and self._movement_cell.hole.home(self):
                self._movement_cell.hole.nutrients += self._mandible
                self._mandible -= 1
                self._trail_length = 0

        else:
            self._visited.append(self._current_cell)
            self._allowed_cells(cells)
            self._select()

            if self._movement_cell.has_nutrient() and not self._movement_cell.nutrient.empty():
                self._mandible += self._movement_cell.nutrient.nutrient_unit

        self._current_cell = self._movement_cell
        self.pos = self._current_cell.pos

    def _select(self):
        if self._allowed:
            self._movement_cell = self._rng.choice(
                self._allowed,
                size=1,
                p=self._probabilities(self._current_cell)
            )[0]

            self._trail_length += __class__.euclidean(self._current_cell, self._movement_cell)

        else:
            self._movement_cell = self._visited[0]
            self._visited = []
            self._trail_length = 0

    def _update_pheromone(self):
        if not self._current_cell.has_pheromone():
            self._current_cell.spawn_pheromone()

        self._current_cell.pheromone.update(self._trail_length)


class Ant:
    # we shoud limit the stored path traveled

    INSTANCES = 0

    def __init__(
            self,
            cell,
            rect,
            surface,
            gamma=GAMMA,
            beta=BETA,
            alpha=ALPHA,
            q=Q
    ):

        self._name = __class__.INSTANCES
        __class__.INSTANCES += 1
        self._rng = GLOBAL_RNG

        self.pos = cell.pos
        self.rect = Rect(rect.centerx, rect.centery, rect.width/2, rect.height/2)
        self.surface = surface

        # algorithm parameter
        self._gamma = gamma
        self._alpha = alpha
        self._beta = beta
        self._q = q

        self._mandible = 0
        self._current_cell = cell
        self._movement_cell = None

        self._idx = -1  # traverse index
        self._dead_end = False  # Ant can get stuck within its own path, if this happen we traverse till Ant is unstuck

        self._visited = []  # contains visited cells
        self._allowed = []  # allowed movement cells

        self.radius = 8
        self.goal = None
        self.length = 0

    def draw(self):
        square(self.surface, ANT_WITHOUT_NUTRIENT_COLOR, self.rect)

    def mandible_full(self):
        return self._mandible > 0

    def collide(self, cells):
        # select goal by nearest neighbor
        if not self.goal:
            for cell in cells:
                if cell.has_nutrient() and self._circle_collide(cell):
                    self.goal = cell
                    print('bam')

    def move(self, cells):
        if self.mandible_full():
            self.update()
            self.back()

        else:
            self._allowed_cells(cells)

            if self._dead_end:
                self._traverse()

            else:
                self._visited.append(self._current_cell)
                self._select()

        self._move()

    def update(self):
        if self._current_cell.has_pheromone():
            self._current_cell.pheromone.update(self.length)

        else:
            self._current_cell.pheromone = Pheromone(self._current_cell.rect, self._current_cell.surface)
            self._current_cell.pheromone.update(self.length)

    def back(self):
        self._movement_cell = self._visited.pop()

    def _move(self):
        previous = self._current_cell
        self._current_cell = self._movement_cell
        self.pos = self._current_cell.pos
        self.rect = Rect(self._current_cell.rect.centerx, self._current_cell.rect.centery,
                         self._current_cell.rect.width/2, self._current_cell.rect.height/2)

        if not self.mandible_full() and self._current_cell.has_nutrient() and not self._current_cell.nutrient.empty():
            self._mandible += self._current_cell.nutrient.nutrient_unit

        if self.mandible_full() and self._current_cell.has_hole():
            self._current_cell.hole.nutrients += self._mandible
            self._mandible -= 1
            self._length = 0
            self.update()

        else:
            self.length += __class__.euclidean(previous, self._current_cell)

    def _allowed_cells(self, cells):
        # filter for obstacles
        self._allowed = list(set(cells) - set(self._visited))

    def _traverse(self):
        self._movement_cell = self._visited[0]
        self._visited = []
        self.length = 0
        # if self._allowed:
        #     self._visited = self._visited[:self._idx + 1]
        #     self._dead_end = False
        #     self._select()
        #
        # else:
        #     self._idx -= 1
        #     self._movement_cell = self._visited[self._idx]

    def _select(self):
        if self._allowed and self.goal:
            self._movement_cell = self._rng.choice(
                self._allowed,
                size=1,
                p=self._probabilities(self.goal)
            )[0]

        elif self._allowed:
            self._movement_cell = self._rng.choice(
                self._allowed,
                size=1,
                p=self._probabilities(self._current_cell)
            )[0]

        else:
            self._idx = -1
            #self._dead_end = True
            self._traverse()

    def _probabilities(self, target):
        probabilities = array([
            cell.pheromone.intensity ** self._alpha * (1 / __class__.euclidean(target, cell)) ** self._beta
            if cell.has_pheromone() else
            self._gamma ** self._alpha * (1 / __class__.euclidean(target, cell)) ** self._beta
            for cell in self._allowed
        ])

        return probabilities / probabilities.sum()

    @staticmethod
    def euclidean(origin, target):
        return sqrt(
            ((origin.pos.x - target.pos.x)**2 + (origin.pos.y - target.pos.y)**2) + 0.0000001
        )

    def _circle_collide(self, cell):
        return (cell.pos.x - self.pos.x)**2 + (cell.pos.y - self.pos.y)**2 <= self.radius**2

    def __hash__(self):
        return hash((self.__class__.__name__, self._name))

    def __str__(self):
        return '{} {} at position {} with {} unit nutrient'.format(self.__class__.__name__,
                                                                   self._name, str(self.pos),
                                                                   self._mandible)

    def __repr__(self):
        msg = '<{}(pos={}, gamma={}, alpha={}, beta={}, q={}) at {}>'.format(self.__class__.__name__, str(self.pos),
                                                                             self._gamma, self._alpha,
                                                                             self._beta, self._q,
                                                                             hex(id(self)))
        return msg
