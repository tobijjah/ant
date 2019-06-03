"""
Module test_nutrient
****

:Author: tobijjah
:Date: 12.05.19
"""
from unittest import TestCase
from unittest.mock import Mock

from ant.agents import Nutrient
from ant.errors import NutrientEmptyError


class TestNutrient(TestCase):
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

        self.nut = Nutrient(10, self.rect, 'foo')

    def test_nutrient_unit(self):
        actual = self.nut.nutrient_unit

        self.assertTrue(actual == 1)
        self.assertTrue(self.nut._amount == 9)

    def test_nutrient_unit_raise(self):
        self.nut._amount = 0

        with self.assertRaises(NutrientEmptyError):
            _ = self.nut.nutrient_unit

    def test_empty_false(self):
        self.assertFalse(self.nut.empty())

    def test_empty_true(self):
        tmp = Nutrient(0, self.rect, 'foo')
        self.assertTrue(tmp.empty())

    def test_str(self):
        tmp = Nutrient(0, self.rect, 'foo')
        self.assertEqual(str(tmp), 'Nutrient with 0 units')
