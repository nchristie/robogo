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


class MinimaxTreeTestCase(TestCase):
    @skip("Deliberate failing test available to check this part of the code is touched")
    def test_failing_test(self):
        expected = True
        actual = False
        self.assertEqual(expected, actual)

    def test_build_game_tree_recursive_depth(self):
        # GIVEN
        player = "maximizer"
        game_tree_node_23 = MinimaxNode(
            node_id="root_node_23",
            player=player,
        )

        node_23_depth = 3
        tree_23 = MinimaxTree(game_tree_node_23)
        # hack to get around suspected test pollution
        game_tree_node_23.children = []
        tree_23.build_game_tree_recursive(game_tree_node_23, node_23_depth, set())

        # WHEN
        actual = tree_23.root_node.children[0].children[0].children[0].children

        # THEN
        expected = []
        self.assertEqual(expected, actual)

    def test_build_game_tree_recursive_breadth(self):
        # GIVEN
        player = "maximizer"
        game_tree_node_072521 = MinimaxNode(
            node_id="root_node_072521",
            player=player,
        )

        node_072521_depth = 3
        tree_072521 = MinimaxTree(game_tree_node_072521)

        tree_072521.build_game_tree_recursive(
            game_tree_node_072521, node_072521_depth, set()
        )

        # WHEN
        actual = len(tree_072521.root_node.children)
        # THEN
        expected = 5
        self.assertEqual(expected, actual)

    def test_set_alpha_and_beta_no_update(self):
        # GIVEN
        player = "maximizer"
        game_tree_node_072915 = MinimaxNode(
            node_id="root_node_072915",
            player=player,
        )

        game_tree_node_072915_1 = MinimaxNode(
            node_id="root_node_072915",
            player=player,
        )

        tree_072922 = MinimaxTree(game_tree_node_072915)
        alpha = -INFINITY
        beta = INFINITY

        # WHEN
        actual = tree_072922.set_alpha_and_beta(game_tree_node_072915_1, alpha, beta)

        # THEN
        expected = alpha, beta
        self.assertEqual(expected, actual)

    def test_set_alpha_and_beta_update_alpha(self):
        # GIVEN
        player_1629_0729 = "maximizer"
        node_1629_0729 = MinimaxNode(
            node_id="root_node_1629_0729",
            player=player_1629_0729,
        )
        tree_1629_0729 = MinimaxTree(node_1629_0729)

        node_score = 0
        player_1629_0730 = "minimizer"
        node_1630_0729 = MinimaxNode(
            node_id="root_node_1629_0729", player=player_1629_0730, score=node_score
        )

        alpha = -INFINITY
        beta = INFINITY

        # WHEN
        actual = tree_1629_0729.set_alpha_and_beta(node_1630_0729, alpha, beta)

        # THEN
        expected = node_score, beta
        self.assertEqual(expected, actual)

    def test_set_alpha_and_beta_update_beta(self):
        # GIVEN
        player_1654_0729 = "maximizer"
        node_1654_0729 = MinimaxNode(
            node_id="root_node_1629_0729",
            player=player_1654_0729,
        )
        tree_1654_0729 = MinimaxTree(node_1654_0729)

        node_score = 0
        player_1654_0730 = "maximizer"
        node_1655_0729 = MinimaxNode(
            node_id="root_node_1655_0729", player=player_1654_0730, score=node_score
        )

        alpha = -INFINITY
        beta = INFINITY

        # WHEN
        actual = tree_1654_0729.set_alpha_and_beta(node_1655_0729, alpha, beta)

        # THEN
        expected = alpha, node_score
        self.assertEqual(expected, actual)

    def test_set_alpha_and_beta_update_alpha_scores_not_inf(self):
        # GIVEN
        player_1659_0729 = "maximizer"
        node_1659_0729 = MinimaxNode(
            node_id="root_node_1629_0729",
            player=player_1659_0729,
        )
        tree_1659_0729 = MinimaxTree(node_1659_0729)

        node_score = 1
        player_1700_0730 = "minimizer"
        node_1700_0729 = MinimaxNode(
            node_id="root_node_1700_0729", player=player_1700_0730, score=node_score
        )

        alpha = 0
        beta = 0

        # WHEN
        actual = tree_1659_0729.set_alpha_and_beta(node_1700_0729, alpha, beta)

        # THEN
        expected = node_score, beta
        self.assertEqual(expected, actual)

    def test_set_alpha_and_beta_update_alpha_scores_not_inf_and_score_higher(self):
        # GIVEN
        player_1701_0729 = "maximizer"
        node_1701_0729 = MinimaxNode(
            node_id="root_node_1701_0729",
            player=player_1701_0729,
        )
        tree_1701_0729 = MinimaxTree(node_1701_0729)

        node_score = 1
        player_1702_0730 = "maximizer"
        node_1702_0729 = MinimaxNode(
            node_id="root_node_1702_0729", player=player_1702_0730, score=node_score
        )

        alpha = 0
        beta = 0

        # WHEN
        actual = tree_1701_0729.set_alpha_and_beta(node_1702_0729, alpha, beta)

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
