"""
Sample tests
"""

from django.test import SimpleTestCase

from . import calc


class CalcTests(SimpleTestCase):
    """ Test cases calc module"""

    def test_add_numbers(self):
        res = calc.add(7, 4)
        self.assertEqual(res, 11)

    def test_subtract_numbers(self):
        res = calc.subtract(7, 6)
        self.assertEqual(res, 'normal')

