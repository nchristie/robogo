from cmath import inf
from django.test import TestCase
from games.minimax import *
from unittest import skip
from games.game_logic import INFINITY


class HelpersTestCase(TestCase):
    def test_break_conditions_are_met(self):
        # GIVEN
        alpha = -INFINITY
        beta = INFINITY

        # WHEN
        actual = break_conditions_are_met(alpha, beta)

        # THEN
        expected = False
        self.assertEqual(expected, actual)

    def test_break_conditions_are_met_alpha_greater(self):
        # GIVEN
        alpha = 1
        beta = 0

        # WHEN
        actual = break_conditions_are_met(alpha, beta)

        # THEN
        expected = True
        self.assertEqual(expected, actual)

    def test_break_conditions_are_met_black_win(self):
        # GIVEN
        alpha = INFINITY
        beta = INFINITY

        # WHEN
        actual = break_conditions_are_met(alpha, beta)

        # THEN
        expected = True
        self.assertEqual(expected, actual)

    def test_break_conditions_are_met_white_win(self):
        # GIVEN
        alpha = -INFINITY
        beta = -INFINITY

        # WHEN
        actual = break_conditions_are_met(alpha, beta)

        # THEN
        expected = True
        self.assertEqual(expected, actual)
