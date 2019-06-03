"""
Module test_position
****

:Author: tobijjah
:Date: 11.05.19
"""
from unittest import TestCase

from ant.environment import Position


class TestPosition(TestCase):
    def setUp(self):
        self.pos1 = Position(1, 1)
        self.pos2 = Position(2, 2)

    def test_valid_add(self):
        pos = self.pos1 + self.pos1

        self.assertTrue(pos.x == 2)
        self.assertTrue(pos.y == 2)

    def test_invalid_add(self):
        with self.assertRaises(ValueError):
            self.pos1 + 1

    def test_valid_equal(self):
        self.assertTrue(self.pos1 == Position(1, 1))

    def test_not_equal(self):
        self.assertFalse(self.pos1 == self.pos2)
        self.assertFalse(self.pos1 == 1)
