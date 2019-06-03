"""
Module test_hole
****

:Author: tobijjah
:Date: 12.05.19
"""
from unittest import TestCase
from unittest.mock import Mock
from unittest.mock import patch

from ant.agents import Hole


class TestHole(TestCase):
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

        self.hole = Hole(self.rect, 'foo')

    def test_instantiation(self):
        tmp = Hole(self.rect, 'foo')
        self.assertTrue(self.hole._name != tmp._name)

    def test_get_nutrients(self):
        self.assertEqual(self.hole.nutrients, 0)

    def test_set_nutrients(self):
        self.hole.nutrients = 1
        self.assertEqual(self.hole.nutrients, 1)

    def test_spawn_ant(self):
        with patch('ant.agents.ant_factory') as mock:
            mock.return_value = 'ANT'
            ant = self.hole.spawn_ant(None, None, None, None)
            self.assertTrue(ant in self.hole.ants)

    def test_home_true(self):
        with patch('ant.agents.ant_factory') as mock:
            mock.return_value = 'ANT'
            ant = self.hole.spawn_ant(None, None, None, None)
            self.assertTrue(self.hole.home(ant))

    def test_home_false(self):
        with patch('ant.agents.ant_factory') as mock:
            mock.return_value = 'ANT'
            ant = self.hole.spawn_ant(None, None, None, None)
            self.assertFalse(self.hole.home('foo'))

    def test_hash(self):
        tmp = Hole(self.rect, 'foo')
        tmp._name = self.hole._name

        self.assertEqual(hash(self.hole), hash(tmp))

    def test_str(self):
        self.assertEqual(str(self.hole), 'Hole with 0 Ants and 0 Nutrients')
