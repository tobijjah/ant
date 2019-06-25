"""
Module: test_environment
****

:Author: tobijjah
:Date: 07.05.2019
"""
from collections import namedtuple
from unittest import TestCase
from unittest.mock import Mock

from affine import Affine

from ant.environment import Cell
from ant.environment import Environment
from ant.environment import Position
from ant.errors import EnvironmentFullError
from ant.errors import EnvironmentOutOfBoundsError


class TestEnvironment(TestCase):
    def setUp(self):
        self.transform = Affine(1, 0, 0, 0, 1, 0)
        self.environment = Environment(self.transform, None)
        self.mock = namedtuple('Ant', 'pos')

    def test_init(self):
        self.assertEqual(4, self.environment.neighbours)
        self.assertEqual(4, len(self.environment._rules))
        self.assertFalse(self.environment.torus)
        self.assertEqual(10, len(self.environment._field))
        self.assertEqual(10, len(self.environment._field[0]))

        change = Environment(self.transform, None, size=(12, 12))
        self.assertEqual(12, len(change._field))
        self.assertEqual(12, len(change._field[0]))

        conn1 = Environment(self.transform, None, neighbours=1)
        self.assertEqual(4, conn1.neighbours)
        self.assertEqual(4, len(conn1._rules))

        conn2 = Environment(self.transform, None, neighbours=5)
        self.assertEqual(8, conn2.neighbours)
        self.assertEqual(8, len(conn2._rules))

    def test_spawn_hole_full_field(self):
        [self.environment.spawn_hole() for i in range(100)]

        with self.assertRaises(EnvironmentFullError):
            self.environment.spawn_hole()

    def test_spawn_hole(self):
        actual = self.environment.spawn_hole()

        self.assertTrue(isinstance(actual, Cell))
        self.assertTrue(actual.has_hole())

    def test_spawn_nutrient_full_field(self):
        [self.environment.spawn_nutrient() for i in range(100)]

        with self.assertRaises(EnvironmentFullError):
            self.environment.spawn_nutrient()

    def test_spawn_nutrient(self):
        actual = self.environment.spawn_nutrient()

        self.assertTrue(isinstance(actual, Cell))
        self.assertTrue(actual.has_nutrient())

    def test_spawn_obstacle_full_field(self):
        [self.environment.spawn_obstacle() for i in range(100)]

        with self.assertRaises(EnvironmentFullError):
            self.environment.spawn_nutrient()

    def test_spawn_obstacle(self):
        actual = self.environment.spawn_obstacle()

        self.assertTrue(isinstance(actual, Cell))
        self.assertTrue(actual.has_obstacle())

    def test_visible_finite_4(self):
        expected = {Position(1, 0), Position(1, 2), Position(0, 1), Position(2, 1)}
        actual = [cell.pos for cell in self.environment.visible(self.mock(Position(1, 1)))]

        self.assertTrue(len(actual) == 4)
        self.assertTrue(len(expected ^ set(actual)) == 0)

        expected = {Position(1, 0), Position(0, 1)}
        actual = [cell.pos for cell in self.environment.visible(self.mock(Position(0, 0)))]

        self.assertTrue(len(actual) == 2)
        self.assertTrue(len(expected ^ set(actual)) == 0)

        expected = {Position(9, 0), Position(9, 2), Position(8, 1)}
        actual = [cell.pos for cell in self.environment.visible(self.mock(Position(9, 1)))]

        self.assertTrue(len(actual) == 3)
        self.assertTrue(len(expected ^ set(actual)) == 0)

    def test_visible_infinite_4(self):
        self.environment.torus = True

        expected = {Position(1, 0), Position(1, 2), Position(0, 1), Position(2, 1)}
        actual = [cell.pos for cell in self.environment.visible(self.mock(Position(1, 1)))]

        self.assertTrue(len(actual) == 4)
        self.assertTrue(len(expected ^ set(actual)) == 0)

        expected = {Position(1, 0), Position(0, 1), Position(9, 0), Position(0, 9)}
        actual = [cell.pos for cell in self.environment.visible(self.mock(Position(0, 0)))]

        self.assertTrue(len(actual) == 4)
        self.assertTrue(len(expected ^ set(actual)) == 0)

        expected = {Position(9, 0), Position(9, 2), Position(8, 1), Position(0, 1)}
        actual = [cell.pos for cell in self.environment.visible(self.mock(Position(9, 1)))]

        self.assertTrue(len(actual) == 4)
        self.assertTrue(len(expected ^ set(actual)) == 0)

    def test_visible_finite_8(self):
        self.environment = Environment(self.transform, None, neighbours=8)

        expected = {Position(0, 0), Position(1, 0), Position(2, 0),
                    Position(0, 1), Position(2, 1),
                    Position(0, 2), Position(1, 2), Position(2, 2)}
        actual = [cell.pos for cell in self.environment.visible(self.mock(Position(1, 1)))]

        self.assertTrue(len(actual) == 8)
        self.assertTrue(len(expected ^ set(actual)) == 0)

        expected = {Position(1, 0), Position(0, 1), Position(1, 1)}
        actual = [cell.pos for cell in self.environment.visible(self.mock(Position(0, 0)))]

        self.assertTrue(len(actual) == 3)
        self.assertTrue(len(expected ^ set(actual)) == 0)

        expected = {Position(9, 0), Position(8, 0),
                    Position(8, 1),
                    Position(9, 2), Position(8, 2)}
        actual = [cell.pos for cell in self.environment.visible(self.mock(Position(9, 1)))]

        self.assertTrue(len(actual) == 5)
        self.assertTrue(len(expected ^ set(actual)) == 0)

    def test_visible_infinite_8(self):
        self.environment = Environment(self.transform, None, neighbours=8, torus=True)

        expected = {Position(0, 0), Position(1, 0), Position(2, 0),
                    Position(0, 1), Position(2, 1),
                    Position(0, 2), Position(1, 2), Position(2, 2)}
        actual = [cell.pos for cell in self.environment.visible(self.mock(Position(1, 1)))]

        self.assertTrue(len(actual) == 8)
        self.assertTrue(len(expected ^ set(actual)) == 0)

        expected = {Position(9, 9), Position(0, 9), Position(1, 9),
                    Position(9, 0), Position(1, 0),
                    Position(9, 1), Position(0, 1), Position(1, 1)}
        actual = [cell.pos for cell in self.environment.visible(self.mock(Position(0, 0)))]

        self.assertTrue(len(actual) == 8)
        self.assertTrue(len(expected ^ set(actual)) == 0)

        expected = {Position(8, 0), Position(9, 0), Position(0, 0),
                    Position(8, 1), Position(0, 1),
                    Position(8, 2), Position(9, 2), Position(0, 2)}
        actual = [cell.pos for cell in self.environment.visible(self.mock(Position(9, 1)))]

        self.assertTrue(len(actual) == 8)
        self.assertTrue(len(expected ^ set(actual)) == 0)

    def test_get_cell_valid_position(self):
        actual = self.environment.get_cell(Position(9, 9))

        self.assertTrue(isinstance(actual, Cell))
        self.assertTrue(actual.pos == Position(9, 9))

    def test_get_cell_invalid_position(self):
        with self.assertRaises(EnvironmentOutOfBoundsError):
            self.environment.get_cell(Position(100, 100))
            self.environment.get_cell(Position(-1, -1))

    def test_get_infinite_cell(self):
        # b/t = bottom/top, l/r = left/right, d = diagonal
        tld = self.environment.get_torus_cell(Position(-1, -1))
        trd = self.environment.get_torus_cell(Position(10, -1))
        bld = self.environment.get_torus_cell(Position(-1, 10))
        brd = self.environment.get_torus_cell(Position(10, 10))

        self.assertTrue(tld.pos == Position(9, 9))
        self.assertTrue(trd.pos == Position(0, 9))
        self.assertTrue(bld.pos == Position(9, 0))
        self.assertTrue(brd.pos == Position(0, 0))

    def test_on_field(self):
        self.assertTrue(self.environment.on_field(Position(0, 0)))
        self.assertFalse(self.environment.on_field(Position(-1, -1)))

    def test_get_display_cell(self):
        event = Mock()
        event.pos = (0.5, 0.5)

        cell = self.environment.get_display_cell(event)
        self.assertTrue(Position(0, 0) == cell.pos)
