"""
Module: test_cell
*****************

:Author: tobijjah
:Date: 07.05.2019
"""
from unittest import TestCase
from unittest.mock import Mock

from ant.agents.ant import SimpleAnt
from ant.agents.hole import Hole
from ant.agents.nutrient import Nutrient
from ant.agents.obstacle import Obstacle
from ant.agents.pheromone import Pheromone
from ant.environment import Cell
from ant.environment import Position
from ant.errors import CellAgentError
from ant.errors import CellOccupiedError


class TestCell(TestCase):
    def setUp(self):
        self.rect = Mock()
        self.rect.left = 1
        self.rect.right = 1
        self.rect.top = 1
        self.rect.bottom = 1
        self.rect.width = 1
        self.rect.height = 1
        self.rect.centerx = 1
        self.rect.centery = 1

        self.surface = Mock()
        self.surface.get_rect.return_value = self.rect

        self.cell1 = Cell(Position(1, 1), self.surface, self.rect)
        self.cell2 = Cell(Position(1, 1), self.surface, self.rect)
        self.cell3 = Cell(Position(1, 1), self.surface, self.rect)

    def test_construct(self):
        self.assertFalse(self.cell1.has_hole())
        self.assertFalse(self.cell1.has_nutrient())
        self.assertFalse(self.cell1.has_pheromone())

    def test_spawn_hole_with_empty_cell(self):
        actual = self.cell1.spawn_hole()

        self.assertTrue(self.cell1.has_hole())
        self.assertTrue(isinstance(actual, Cell))
        self.assertTrue(isinstance(self.cell1.hole, Hole))

    def test_spawn_hole_with_occupied_cell(self):
        self.cell1.spawn_hole()

        with self.assertRaises(CellOccupiedError):
            self.cell1.spawn_hole()

    def test_get_hole_on_empty_cell(self):
        with self.assertRaises(CellAgentError):
            _ = self.cell1.hole

    def test_delete_hole(self):
        self.cell1.spawn_hole()
        del self.cell1.hole

        self.assertFalse(self.cell1.has_hole())

    def test_spawn_nutrient_with_empty_cell(self):
        actual = self.cell1.spawn_nutrient(1)

        self.assertTrue(self.cell1.has_nutrient())
        self.assertTrue(isinstance(actual, Cell))
        self.assertTrue(isinstance(self.cell1.nutrient, Nutrient))

    def test_spawn_nutrient_with_occupied_cell(self):
        self.cell1.spawn_nutrient(1)

        with self.assertRaises(CellOccupiedError):
            self.cell1.spawn_nutrient(1)

    def test_get_nutrient_on_empty_cell(self):
        with self.assertRaises(CellAgentError):
            _ = self.cell1.nutrient

    def test_delete_nutrient(self):
        self.cell1.spawn_nutrient(1)
        del self.cell1.nutrient

        self.assertFalse(self.cell1.has_nutrient())

    def test_spawn_obstacle_with_empty_cell(self):
        actual = self.cell1.spawn_obstacle()

        self.assertTrue(self.cell1.has_obstacle())
        self.assertTrue(isinstance(actual, Cell))
        self.assertTrue(isinstance(self.cell1.obstacle, Obstacle))

    def test_spawn_obstacle_with_occupied_cell(self):
        self.cell1.spawn_obstacle()

        with self.assertRaises(CellOccupiedError):
            self.cell1.spawn_obstacle()

    def test_get_obstacle_on_empty_cell(self):
        with self.assertRaises(CellAgentError):
            _ = self.cell1.obstacle

    def test_delete_obstacle(self):
        self.cell1.spawn_obstacle()
        del self.cell1.obstacle

        self.assertFalse(self.cell1.has_obstacle())

    def test_spawn_pheromone_with_empty_cell(self):
        pheromone = self.cell1.spawn_pheromone()

        self.assertTrue(self.cell1.has_pheromone())
        self.assertTrue(isinstance(pheromone, Pheromone))

    def test_spawn_pheromone_with_occupied_cell(self):
        self.cell1.spawn_pheromone()

        with self.assertRaises(CellOccupiedError):
            self.cell1.spawn_pheromone()

    def test_get_pheromone_on_empty_cell(self):
        with self.assertRaises(CellAgentError):
            _ = self.cell1.pheromone

    def test_delete_pheromone(self):
        self.cell1.spawn_pheromone()
        del self.cell1.pheromone

        self.assertFalse(self.cell1.has_pheromone())

    def test_spawn_ant_on_holeless_cell(self):
        with self.assertRaises(CellAgentError):
            self.cell1.spawn_ant()

    def test_spawn_ant(self):
        self.cell1.spawn_hole()
        ant = self.cell1.spawn_ant()

        self.assertTrue(isinstance(ant, SimpleAnt))
        self.assertTrue(ant.pos == self.cell1.pos)

    def test_has_hole(self):
        self.assertFalse(self.cell1.has_hole())

        self.cell1.spawn_hole()

        self.assertTrue(self.cell1.has_hole())

    def test_has_nutrient(self):
        self.assertFalse(self.cell1.has_nutrient())

        self.cell1.spawn_nutrient(1)

        self.assertTrue(self.cell1.has_nutrient())

    def test_has_pheromone(self):
        self.assertFalse(self.cell1.has_pheromone())

        self.cell1.spawn_pheromone()

        self.assertTrue(self.cell1.has_pheromone())

    def test_has_obstacle(self):
        self.assertFalse(self.cell1.has_obstacle())

        self.cell1.spawn_obstacle()

        self.assertTrue(self.cell1.has_obstacle())

    def test_occupied(self):
        self.cell1.spawn_hole()
        self.cell2.spawn_nutrient(1)
        self.cell3.spawn_obstacle()

        self.assertTrue(self.cell1.occupied())
        self.assertTrue(self.cell2.occupied())
        self.assertTrue(self.cell3.occupied())
