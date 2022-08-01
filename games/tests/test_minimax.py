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
        child = MinimaxNode(node_id=node_id, player=player, score=score)

        # WHEN
        my_node_4.add_child(child)
        child_0 = my_node_4.get_children()[0]
        actual = (child_0.node_id, child.player, child.score)

        # THEN
        expected = (node_id, player, score)
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

    def test_alpha_initialises_to_neg_inf(self):
        # GIVEN
        node_0908_0108 = MinimaxNode()

        # WHEN
        actual = node_0908_0108.alpha

        # THEN
        expected = -INFINITY
        self.assertEqual(expected, actual)

    def test_beta_initialises_to_inf(self):
        # GIVEN
        node_1022_0108 = MinimaxNode()

        # WHEN
        actual = node_1022_0108.beta

        # THEN
        expected = INFINITY
        self.assertEqual(expected, actual)

    def test_set_alpha_beta(self):
        # GIVEN
        node_1026_0108 = MinimaxNode()
        score = 5

        # WHEN
        node_1026_0108.set_alpha_beta(alpha=score)
        actual = node_1026_0108.alpha

        # THEN
        expected = score
        self.assertEqual(expected, actual)

    def test_get_alpha_beta(self):
        # GIVEN
        node_1028_0108 = MinimaxNode()
        score = 5

        # WHEN
        node_1028_0108.set_alpha_beta(alpha=score)
        actual = node_1028_0108.get_alpha_beta()

        # THEN
        expected = score, INFINITY
        self.assertEqual(expected, actual)

    def test_set_alpha_when_next_player_is_maximizer(self):
        # GIVEN
        node_0955_0108 = MinimaxNode(player="minimizer", score=0)
        child_scores = [0, 1, -2, 5, -5, 4, 3]
        for i, child_score in enumerate(child_scores):
            new_node = MinimaxNode(
                node_id=f"child_0955_{i}_0108",
                player="maximizer",
                score=child_score
            )
            a, b  = new_node.calculate_alpha_and_beta()
            new_node.set_alpha_beta(a, b)
            node_0955_0108.add_child(new_node)


        # WHEN
        actual, x = node_0955_0108.get_optimal_move().get_alpha_beta()

        # THEN
        expected = 5
        self.assertEqual(expected, actual)

    def test_calculate_alpha_and_beta_no_update(self):
        # GIVEN
        player = "maximizer"

        game_tree_node_072915_1 = MinimaxNode(
            node_id="root_node_072915",
            player=player,
        )

        alpha = -INFINITY
        beta = INFINITY

        # WHEN
        actual = game_tree_node_072915_1.calculate_alpha_and_beta(alpha, beta)

        # THEN
        expected = alpha, beta
        self.assertEqual(expected, actual)

    def test_calculate_alpha_and_beta_update_alpha(self):
        # GIVEN
        node_score = 0
        player = "maximizer"
        node_1630_0729 = MinimaxNode(
            node_id="root_node_1629_0729", player=player, score=node_score
        )

        alpha = -INFINITY
        beta = INFINITY

        # WHEN
        actual = node_1630_0729.calculate_alpha_and_beta(alpha, beta)

        # THEN
        expected = node_score, beta
        self.assertEqual(expected, actual)

    def test_calculate_alpha_and_beta_update_beta(self):
        # GIVEN

        node_score = 0
        node_1655_0729 = MinimaxNode(
            node_id="root_node_1655_0729", player="minimizer", score=node_score
        )

        alpha = -INFINITY
        beta = INFINITY

        # WHEN
        actual = node_1655_0729.calculate_alpha_and_beta(alpha, beta)

        # THEN
        expected = alpha, node_score
        self.assertEqual(expected, actual)

    def test_calculate_alpha_and_beta_update_alpha_scores_not_inf(self):
        # GIVEN
        node_score = 1
        node_1700_0729 = MinimaxNode(
            node_id="root_node_1700_0729", player="maximizer", score=node_score
        )

        alpha = 0
        beta = 0

        # WHEN
        actual = node_1700_0729.calculate_alpha_and_beta(alpha, beta)

        # THEN
        expected = node_score, beta
        self.assertEqual(expected, actual)

    def test_calculate_alpha_and_beta_update_beta_scores_not_inf_and_score_higher(self):
        # GIVEN
        node_score = 1
        node_1702_0729 = MinimaxNode(
            node_id="root_node_1702_0729", player="minimizer", score=node_score
        )

        alpha = 0
        beta = 0

        # WHEN
        actual = node_1702_0729.calculate_alpha_and_beta(alpha, beta)

        # THEN
        expected = alpha, beta
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

