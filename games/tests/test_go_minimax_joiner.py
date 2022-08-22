from django.test import TestCase
from games.go_minimax_joiner import GoNode
from games.minimax import prune_game_tree_recursive
from types import GeneratorType
from games.game_logic import *


class GoNodeTestCase(TestCase):
    def test_find_legal_move_when_boundary(self):
        # GIVEN
        board_state = [["+", "+", "+"], ["+", "+", "+"], ["+", "+", "●"]]
        my_node_2 = GoNode(score=0, board_state=board_state, player_to_move="minimizer")

        # WHEN
        potential_moves = [
            move for move in my_node_2.generate_next_child_and_rank_by_proximity()
        ]
        actual = [item.move_coordinates for item in potential_moves][:3]

        # THEN
        expected = [(1, 1), (1, 2), (2, 1)]
        self.assertEqual(expected, actual)

    def test_find_legal_move_when_neighbouring_stones(self):
        # GIVEN
        board_state = [
            ["+", "+", "+", "+"],
            ["+", "●", "+", "+"],
            ["+", "●", "+", "+"],
            ["+", "+", "+", "+"],
        ]
        my_node_3 = GoNode(score=0, board_state=board_state, player_to_move="minimizer")

        # WHEN
        potential_moves = [
            move for move in my_node_3.generate_next_child_and_rank_by_proximity()
        ]
        actual = [item.move_coordinates for item in potential_moves][:10]

        # THEN
        expected = [
            (0, 0),
            (0, 1),
            (0, 2),
            (1, 2),
            (2, 2),
            (2, 0),
            (1, 0),
            (3, 2),
            (3, 1),
            (3, 0),
        ]
        self.assertEqual(expected, actual)

    # TODO test_find_legal_move_when_surrounded

    def test_generate_next_child_and_rank_by_proximity_returns_generator(self):
        # GIVEN
        board_state = [["●", "+", "+"], ["+", "+", "+"], ["+", "+", "+"]]
        my_node_4 = GoNode(score=0, board_state=board_state, player_to_move="minimizer")
        depth = 1

        # WHEN

        # THEN
        expected = GeneratorType
        potential_moves = my_node_4.generate_next_child_and_rank_by_proximity(depth)
        actual = type(potential_moves)
        self.assertEqual(expected, actual)

    def test_generate_next_child_and_rank_by_proximity_attack_options(self):
        # GIVEN
        board_state = [["●", "+", "+"], ["+", "+", "+"], ["+", "+", "+"]]
        my_node_5 = GoNode(score=0, board_state=board_state, player_to_move="minimizer")

        # WHEN

        # THEN
        expected = [(0, 1), (1, 1), (1, 0)]
        potential_moves = [
            move for move in my_node_5.generate_next_child_and_rank_by_proximity()
        ][:3]
        actual = [item.move_coordinates for item in potential_moves]
        self.assertEqual(expected, actual)

    def test_child_getter_returns_attack_options_2_groups(self):
        # GIVEN
        board_state = [["●", "+", "+"], ["+", "+", "+"], ["+", "+", "●"]]
        my_node_6 = GoNode(score=0, board_state=board_state, player_to_move="minimizer")

        # WHEN

        # THEN
        expected = [(0, 1), (1, 1), (1, 0), (1, 2), (2, 1)]
        potential_moves = [
            move for move in my_node_6.generate_next_child_and_rank_by_proximity()
        ]
        actual = [item.move_coordinates for item in potential_moves][:5]
        self.assertEqual(expected, actual)

    def test_child_getter_returns_defend_options_2_groups(self):
        # GIVEN
        board_state = [["○", "+", "+"], ["+", "+", "+"], ["+", "+", "○"]]
        my_node_7 = GoNode(score=0, board_state=board_state, player_to_move="minimizer")

        # WHEN

        # THEN
        expected = [(0, 1), (1, 1), (1, 0), (1, 2), (2, 1)]
        potential_moves = [
            move for move in my_node_7.generate_next_child_and_rank_by_proximity()
        ]
        actual = [item.move_coordinates for item in potential_moves][:5]
        self.assertEqual(expected, actual)

    def test_generate_next_child_and_rank_by_proximity_returns_all_moves(self):
        # GIVEN
        board_state = [["●", "+", "+"], ["+", "+", "+"], ["+", "+", "+"]]
        my_node_0814_1445 = GoNode(
            score=0, board_state=board_state, player_to_move="minimizer"
        )

        # WHEN

        # THEN
        all_moves = set(list_all_moves_on_board(3))
        all_moves.remove((0, 0))
        expected = all_moves
        potential_moves = [
            move
            for move in my_node_0814_1445.generate_next_child_and_rank_by_proximity()
        ]
        actual = set([item.move_coordinates for item in potential_moves])
        self.assertEqual(expected, actual)

    def test_generate_next_child_and_rank_by_proximity_returns_attack_and_defend_options_first(
        self,
    ):
        # GIVEN
        board_state = [["●", "+", "+"], ["+", "+", "+"], ["+", "+", "○"]]
        my_node_8 = GoNode(score=0, board_state=board_state, player_to_move="minimizer")

        # WHEN
        potential_moves = [
            move for move in my_node_8.generate_next_child_and_rank_by_proximity()
        ]

        # THEN
        expected = set([(0, 1), (1, 1), (1, 0), (1, 2), (2, 1)])
        actual = set([item.move_coordinates for item in potential_moves][:5])
        self.assertEqual(expected, actual)

    def test_get_scores_one_stone(self):
        # GIVEN
        board_state = [["●", "+", "+"], ["+", "+", "+"], ["+", "+", "+"]]
        my_node_9 = GoNode(score=0, board_state=board_state, player_to_move="minimizer")

        # WHEN
        actual = my_node_9.find_utility(winning_score=5)

        # THEN
        expected = 1
        self.assertEqual(expected, actual)

    def test_get_scores_two_groups_of_one_stone(self):
        # GIVEN
        board_state = [["●", "+", "●"], ["+", "+", "+"], ["+", "+", "+"]]
        my_node_10 = GoNode(
            score=0, board_state=board_state, player_to_move="minimizer"
        )

        # WHEN
        actual = my_node_10.find_utility(winning_score=5)

        # THEN
        expected = 1
        self.assertEqual(expected, actual)

    def test_get_scores_two_stones_horizontal(self):
        # GIVEN
        board_state = [["●", "●", "+"], ["+", "+", "+"], ["+", "+", "+"]]
        my_node_11 = GoNode(
            score=0, board_state=board_state, player_to_move="minimizer"
        )

        # WHEN
        actual = my_node_11.find_utility(winning_score=5)

        # THEN
        expected = 2
        self.assertEqual(expected, actual)

    def test_get_scores_two_stones_horizontal_other_row(self):
        # GIVEN
        board_state = [["+", "+", "+"], ["●", "●", "+"], ["+", "+", "+"]]
        my_node_12 = GoNode(
            score=0, board_state=board_state, player_to_move="minimizer"
        )

        # WHEN
        actual = my_node_12.find_utility(winning_score=5)

        # THEN
        expected = 2
        self.assertEqual(expected, actual)

    def test_get_scores_white_stones(self):
        # GIVEN
        board_state = [["+", "+", "+"], ["○", "○", "+"], ["+", "+", "+"]]
        my_node_13 = GoNode(
            score=0, board_state=board_state, player_to_move="minimizer"
        )

        # WHEN
        actual = my_node_13.find_utility(winning_score=5)

        # THEN
        expected = -2
        self.assertEqual(expected, actual)

    def test_get_scores_two_stones_vertical(self):
        # GIVEN
        board_state = [["●", "+", "+"], ["●", "+", "+"], ["+", "+", "+"]]
        my_node_14 = GoNode(
            score=0, board_state=board_state, player_to_move="minimizer"
        )

        # WHEN
        actual = my_node_14.find_utility(winning_score=5)

        # THEN
        expected = 2
        self.assertEqual(expected, actual)

    def test_get_scores_big_board_lots_of_stones(self):
        # GIVEN
        board_state = [
            ["+", "●", "+", "+", "+", "+", "+", "+", "+"],
            ["+", "●", "+", "+", "+", "+", "+", "○", "+"],
            ["+", "●", "+", "●", "●", "●", "●", "○", "+"],
            ["+", "+", "+", "+", "●", "+", "+", "○", "+"],
            ["+", "+", "●", "●", "●", "●", "+", "○", "+"],
            ["+", "+", "+", "+", "+", "+", "+", "+", "+"],
            ["+", "+", "○", "○", "○", "+", "+", "○", "+"],
            ["+", "+", "+", "+", "+", "+", "+", "+", "+"],
            ["+", "+", "+", "+", "+", "+", "+", "+", "+"],
        ]
        my_node_15 = GoNode(
            score=0, board_state=board_state, player_to_move="minimizer"
        )

        # WHEN
        actual = my_node_15.find_utility(winning_score=5)

        # THEN
        expected = 0
        self.assertEqual(expected, actual)

    def test_get_scores_winner(self):
        # GIVEN
        board_state = [
            ["+", "●", "+", "+", "+", "+", "+", "+", "+"],
            ["+", "●", "+", "+", "+", "+", "+", "○", "+"],
            ["+", "●", "+", "●", "●", "●", "●", "○", "+"],
            ["+", "+", "+", "+", "●", "+", "+", "○", "+"],
            ["+", "+", "●", "●", "●", "●", "●", "○", "+"],
            ["+", "+", "+", "+", "+", "+", "+", "+", "+"],
            ["+", "+", "○", "○", "○", "+", "+", "○", "+"],
            ["+", "+", "+", "+", "+", "+", "+", "+", "+"],
            ["+", "+", "+", "+", "+", "+", "+", "+", "+"],
        ]
        my_node_15 = GoNode(
            score=0, board_state=board_state, player_to_move="minimizer"
        )

        # WHEN
        actual = my_node_15.find_utility(winning_score=5)

        # THEN
        expected = HIGHEST_SCORE
        self.assertEqual(expected, actual)

    def test_get_scores_winner_white(self):
        # GIVEN
        board_state = [
            ["+", "●", "+", "+", "+", "+", "+", "+", "+"],
            ["+", "●", "+", "+", "+", "+", "+", "○", "+"],
            ["+", "●", "+", "●", "●", "●", "●", "○", "+"],
            ["+", "+", "+", "+", "●", "+", "+", "○", "+"],
            ["+", "+", "●", "●", "●", "●", "+", "○", "+"],
            ["+", "+", "+", "+", "+", "+", "+", "○", "+"],
            ["+", "+", "○", "○", "○", "+", "+", "○", "+"],
            ["+", "+", "+", "+", "+", "+", "+", "+", "+"],
            ["+", "+", "+", "+", "+", "+", "+", "+", "+"],
        ]
        my_node_15 = GoNode(
            score=0, board_state=board_state, player_to_move="minimizer"
        )

        # WHEN
        actual = my_node_15.find_utility(winning_score=5)

        # THEN
        expected = LOWEST_SCORE
        self.assertEqual(expected, actual)

    # TODO test_find_connecting_stones

    # TODO test_build_minimax_alpha_beta_game_tree_returns_best_score(self):

    # TODO test_gets_best_move_only_one_option(self):


class GoTreeTestCase(TestCase):
    def test_prune_game_tree_recursive_assigns_scores(self):
        # GIVEN
        node_0801_1308 = GoNode(
            node_id="root_0801_1308",
            board_state=[["●", "●"], ["+", "+"]],
            player_to_move="minimizer",
        )

        depth = 0

        # WHEN
        actual = prune_game_tree_recursive(
            parent=node_0801_1308, depth=depth, winning_score=5
        )["best_score"]

        # THEN
        expected = 2
        self.assertEqual(expected, actual)

    def test_prune_game_tree_recursive_sets_score_winning_node(self):
        # GIVEN
        node_0801_1253 = GoNode(
            node_id="root_node_0801_1253",
            board_state=[
                ["●", "●", "●", "●", "●"],
                ["+", "+", "+", "+", "+"],
                ["+", "+", "+", "+", "+"],
                ["+", "+", "+", "+", "+"],
                ["+", "+", "+", "+", "+"],
            ],
            player_to_move="minimizer",
        )

        depth = 0

        # WHEN
        actual = prune_game_tree_recursive(
            parent=node_0801_1253, depth=depth, winning_score=5
        )["best_score"]

        # THEN
        expected = HIGHEST_SCORE
        self.assertEqual(expected, actual)

    def test_prune_game_tree_recursive_sets_score_based_on_children(self):
        # GIVEN
        node_0801_1411 = GoNode(
            node_id="root_node_0801_1411",
            board_state=[
                ["●", "●", "●", "●", "+"],
                ["+", "+", "+", "+", "+"],
                ["+", "+", "+", "+", "+"],
                ["+", "+", "+", "+", "+"],
                ["+", "+", "+", "+", "+"],
            ],
            player_to_move="minimizer",
        )

        depth = 2

        # WHEN
        actual = prune_game_tree_recursive(
            parent=node_0801_1411, depth=depth, winning_score=5
        )["best_score"]

        # THEN
        expected = 3
        self.assertEqual(expected, actual)

    def test_prune_game_tree_recursive_nine_by_nine(self):
        # GIVEN
        node_0801_1547 = GoNode(
            node_id="root_node_0801_1547",
            score=None,
            board_state=[
                ["●", "●", "●", "●", "+", "+", "+", "+", "+"],
                ["○", "+", "+", "+", "+", "+", "+", "+", "+"],
                ["○", "+", "+", "+", "+", "+", "+", "+", "+"],
                ["○", "+", "+", "+", "+", "+", "+", "+", "+"],
                ["+", "+", "+", "+", "+", "+", "+", "+", "+"],
                ["+", "+", "+", "+", "+", "+", "+", "+", "+"],
                ["+", "+", "+", "+", "+", "+", "+", "+", "+"],
                ["+", "+", "+", "+", "+", "+", "+", "+", "+"],
                ["+", "+", "+", "+", "+", "+", "+", "+", "+"],
            ],
            player_to_move="minimizer",
        )
        depth = 2

        white_move_node = prune_game_tree_recursive(
            parent=node_0801_1547, depth=depth, winning_score=5
        )["move_node"]

        # WHEN
        actual = white_move_node.move_coordinates

        # THEN
        expected = (0, 4)
        self.assertEqual(expected, actual)

    def test_prune_game_tree_recursive_3_by_3(self):
        # GIVEN
        node_0805_2100 = GoNode(
            node_id="root_node_0805_2100",
            score=None,
            board_state=[
                ["●", "●", "+"],
                ["○", "+", "+"],
                ["+", "+", "+"],
            ],
            player_to_move="minimizer",
            move_coordinates=(0, 1),
        )

        depth = 4

        white_move_node = prune_game_tree_recursive(
            node_0805_2100, depth, winning_score=3
        )["move_node"]

        # WHEN
        actual = white_move_node.move_coordinates

        # THEN
        expected = (0, 2)
        self.assertEqual(expected, actual)

    def test_prune_game_tree_recursive_blocks_between_stones(self):
        # GIVEN
        winning_score = 3
        depth = 2

        board_state = [
            ["●", "○", "+", "+", "+"],
            ["+", "+", "+", "+", "+"],
            ["●", "+", "+", "+", "+"],
            ["+", "+", "+", "+", "+"],
            ["+", "+", "+", "+", "+"],
        ]
        node_0809_0414 = GoNode(
            node_id="root_node_0809_0414",
            score=None,
            board_state=board_state,
            player_to_move="minimizer",
        )

        white_move_node = prune_game_tree_recursive(
            parent=node_0809_0414, depth=depth, winning_score=winning_score
        )["move_node"]

        # WHEN
        actual = white_move_node.move_coordinates

        # THEN
        expected = (1, 0)
        self.assertEqual(expected, actual)
