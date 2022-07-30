from cmath import inf
from django.test import TestCase
from games.minimax import *
from unittest import skip
from games.game_logic import INFINITY


class MinimaxNodeTestCase(TestCase):
    def test_get_score(self):
        """Get score"""
        # GIVEN
        my_node_1 = MinimaxNode(node_id=1, player="maximizer", score=None, children=[])
        with self.assertRaises(Exception):
            my_node_1.get_score()

    def test_set_score(self):
        """Set score"""
        # GIVEN
        my_node_2 = MinimaxNode(node_id=2, player="maximizer", score=None, children=[])
        my_node_2.set_score(5)
        expected = 5
        actual = my_node_2.get_score()
        self.assertEqual(expected, actual)

    def test_get_children(self):
        """"""
        # GIVEN
        my_node_3 = MinimaxNode(node_id=3, player="maximizer", score=None, children=[])
        expected = []
        actual = my_node_3.get_children()
        self.assertEqual(expected, actual)

    def test_add_child(self):
        """"""
        # GIVEN
        my_node_4 = MinimaxNode(node_id=4, player="maximizer", score=None, children=[])
        score = 4
        node_id = 123
        player = "maximizer"
        child = MinimaxNode(node_id, player, score)
        my_node_4.add_child(child)
        children = my_node_4.get_children()
        expected = (node_id, player, score)
        child = children[0]
        actual = (child.node_id, child.player, child.score)
        self.assertEqual(expected, actual)

    def test_returns_max_for_maximizer(self):
        # GIVEN
        my_node_5 = MinimaxNode(node_id=5, player="maximizer", score=None, children=[])
        available_moves = [
            {
                "node_id": 14,
                "score": 1,
            },
            {"node_id": 15, "score": 2},
            {"node_id": 16, "score": 3},
        ]
        player = "maximizer"

        # WHEN
        for move in available_moves:
            child = MinimaxNode(move["node_id"], player=player, score=move["score"])
            my_node_5.add_child(child)

        # THEN
        expected = 3
        actual = my_node_5.get_optimal_move().get_score()
        self.assertEqual(expected, actual)

    def test_returns_min_for_minimizer(self):
        # GIVEN
        my_node_6 = MinimaxNode(node_id=6, player="maximizer", score=None, children=[])
        available_moves = [
            {
                "node_id": 17,
                "score": 4,
            },
            {"node_id": 18, "score": 5},
            {"node_id": 19, "score": 6},
        ]
        player = "minimizer"

        # WHEN
        for move in available_moves:
            child = MinimaxNode(
                node_id=move["node_id"], player=player, score=move["score"]
            )
            my_node_6.add_child(child)

        # THEN
        expected = 4
        optimal_move = my_node_6.get_optimal_move()
        actual = optimal_move.get_score()
        self.assertEqual(expected, actual)


class HelpersTestCase(TestCase):
    def test_are_break_conditions_met(self):
        # GIVEN
        alpha = -INFINITY
        beta = INFINITY

        # WHEN
        actual = are_break_conditions_met(alpha, beta)

        # THEN
        expected = False
        self.assertEqual(expected, actual)

    def test_are_break_conditions_met_alpha_greater(self):
        # GIVEN
        alpha = 1
        beta = 0

        # WHEN
        actual = are_break_conditions_met(alpha, beta)

        # THEN
        expected = True
        self.assertEqual(expected, actual)

    def test_are_break_conditions_met_black_win(self):
        # GIVEN
        alpha = INFINITY
        beta = INFINITY

        # WHEN
        actual = are_break_conditions_met(alpha, beta)

        # THEN
        expected = True
        self.assertEqual(expected, actual)

    def test_are_break_conditions_met_white_win(self):
        # GIVEN
        alpha = -INFINITY
        beta = -INFINITY

        # WHEN
        actual = are_break_conditions_met(alpha, beta)

        # THEN
        expected = True
        self.assertEqual(expected, actual)

    def test_set_alpha_and_beta_no_update(self):
        # GIVEN
        player = "maximizer"

        game_tree_node_072915_1 = MinimaxNode(
            node_id="root_node_072915",
            player=player,
        )

        alpha = -INFINITY
        beta = INFINITY

        # WHEN
        actual = set_alpha_and_beta(game_tree_node_072915_1, alpha, beta)

        # THEN
        expected = alpha, beta
        self.assertEqual(expected, actual)

    def test_set_alpha_and_beta_update_alpha(self):
        # GIVEN
        player_1629_0729 = "maximizer"

        node_score = 0
        player_1629_0730 = "minimizer"
        node_1630_0729 = MinimaxNode(
            node_id="root_node_1629_0729", player=player_1629_0730, score=node_score
        )

        alpha = -INFINITY
        beta = INFINITY

        # WHEN
        actual = set_alpha_and_beta(node_1630_0729, alpha, beta)

        # THEN
        expected = node_score, beta
        self.assertEqual(expected, actual)

    def test_set_alpha_and_beta_update_beta(self):
        # GIVEN

        node_score = 0
        player_1654_0730 = "maximizer"
        node_1655_0729 = MinimaxNode(
            node_id="root_node_1655_0729", player=player_1654_0730, score=node_score
        )

        alpha = -INFINITY
        beta = INFINITY

        # WHEN
        actual = set_alpha_and_beta(node_1655_0729, alpha, beta)

        # THEN
        expected = alpha, node_score
        self.assertEqual(expected, actual)

    def test_set_alpha_and_beta_update_alpha_scores_not_inf(self):
        # GIVEN
        node_score = 1
        player_1700_0730 = "minimizer"
        node_1700_0729 = MinimaxNode(
            node_id="root_node_1700_0729", player=player_1700_0730, score=node_score
        )

        alpha = 0
        beta = 0

        # WHEN
        actual = set_alpha_and_beta(node_1700_0729, alpha, beta)

        # THEN
        expected = node_score, beta
        self.assertEqual(expected, actual)

    def test_set_alpha_and_beta_update_alpha_scores_not_inf_and_score_higher(self):
        # GIVEN
        node_score = 1
        player_1702_0730 = "maximizer"
        node_1702_0729 = MinimaxNode(
            node_id="root_node_1702_0729", player=player_1702_0730, score=node_score
        )

        alpha = 0
        beta = 0

        # WHEN
        actual = set_alpha_and_beta(node_1702_0729, alpha, beta)

        # THEN
        expected = alpha, beta
        self.assertEqual(expected, actual)
