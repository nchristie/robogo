from cmath import inf
from django.test import TestCase
from games.minimax import *
from unittest import skip
from games.game_logic import INFINITY


class MinimaxNodeTestCase(TestCase):
    @skip("Too problematic to raise exception from this func")
    def test_get_score(self):
        """Get score"""
        # GIVEN
        my_node_1 = MinimaxNode(
            node_id=1, score=None, children=[], player_to_move="minimizer"
        )
        with self.assertRaises(Exception):
            my_node_1.get_score()

    def test_set_score(self):
        """Set score"""
        # GIVEN
        my_node_2 = MinimaxNode(
            node_id=2, score=None, children=[], player_to_move="minimizer"
        )
        my_node_2.set_score(5)
        expected = 5
        actual = my_node_2.get_score()
        self.assertEqual(expected, actual)

    def test_get_children(self):
        """"""
        # GIVEN
        my_node_3 = MinimaxNode(
            node_id=3, score=None, children=[], player_to_move="minimizer"
        )
        expected = []
        actual = my_node_3.get_children()
        self.assertEqual(expected, actual)

    def test_add_child(self):
        """"""
        # GIVEN
        my_node_4 = MinimaxNode(
            node_id=4, score=None, children=[], player_to_move="minimizer"
        )

        score = 4
        node_id = 123
        player_to_move = "minimizer"
        child = MinimaxNode(node_id=node_id, score=score, player_to_move=player_to_move)

        # WHEN
        my_node_4.add_child(child)
        child_0 = my_node_4.get_children()[0]
        actual = (child_0.get_node_id(), child.score, child.player_to_move)

        # THEN
        expected = (node_id, score, player_to_move)
        self.assertEqual(expected, actual)

    def test_returns_max_for_maximizer(self):
        # GIVEN
        my_node_5 = MinimaxNode(
            node_id=5, score=None, children=[], player_to_move="maximizer"
        )
        available_moves = [
            {
                "node_id": 14,
                "score": 1,
            },
            {"node_id": 15, "score": 2},
            {"node_id": 16, "score": 3},
        ]

        # WHEN
        for move in available_moves:
            child = MinimaxNode(
                move["node_id"], score=move["score"], player_to_move="minimizer"
            )
            my_node_5.add_child(child)

        # THEN
        expected = 3
        actual = my_node_5.get_optimal_move().get_score()
        self.assertEqual(expected, actual)

    def test_returns_min_for_minimizer(self):
        # GIVEN
        my_node_6 = MinimaxNode(
            node_id=6, score=None, children=[], player_to_move="minimizer"
        )
        available_moves = [
            {
                "node_id": 17,
                "score": 4,
            },
            {"node_id": 18, "score": 5},
            {"node_id": 19, "score": 6},
        ]

        # WHEN
        for move in available_moves:
            child = MinimaxNode(
                node_id=move["node_id"], score=move["score"], player_to_move="maximizer"
            )
            my_node_6.add_child(child)

        # THEN
        expected = 4
        optimal_move = my_node_6.get_optimal_move()
        actual = optimal_move.get_score()
        self.assertEqual(expected, actual)


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
