from django.test import TestCase
from games.go_minimax_joiner import GoNode, BLACK_STONE
from uuid import UUID
from types import GeneratorType
from unittest import skip, skipIf


class GoNodeTestCase(TestCase):
    def test_find_legal_move(self):
        # GIVEN
        board_state = [["+", "+", "+"], ["+", "●", "+"], ["+", "+", "+"]]
        my_node_1 = GoNode(
            player="maximizer",
            score=0,
            branches=[],
            board_state=board_state,
        )

        # WHEN
        potential_moves = my_node_1.generate_next_node_around_existing_moves()
        actual = [item.move_coordinates for item in potential_moves]

        # THEN
        expected = [(0, 1), (1, 0), (1, 2), (2, 1)]
        self.assertEqual(expected, actual)

    def test_find_legal_move_when_boundary(self):
        # GIVEN
        board_state = [["+", "+", "+"], ["+", "+", "+"], ["+", "+", "●"]]
        my_node_2 = GoNode(
            player="maximizer",
            score=0,
            branches=[],
            board_state=board_state,
        )

        # WHEN
        potential_moves = my_node_2.generate_next_node_around_existing_moves()
        actual = [item.move_coordinates for item in potential_moves]

        # THEN
        expected = [(1, 2), (2, 1)]
        self.assertEqual(expected, actual)

    def test_find_legal_move_when_neighbouring_stones(self):
        # GIVEN
        board_state = [
            ["+", "+", "+", "+"],
            ["+", "●", "+", "+"],
            ["+", "●", "+", "+"],
            ["+", "+", "+", "+"],
        ]
        my_node_3 = GoNode(
            player="maximizer",
            score=0,
            branches=[],
            board_state=board_state,
        )

        # WHEN
        potential_moves = my_node_3.generate_next_node_around_existing_moves()
        actual = [item.move_coordinates for item in potential_moves]

        # THEN
        expected = [(0, 1), (1, 0), (1, 2), (2, 0), (2, 2), (3, 1)]
        self.assertEqual(expected, actual)

    # TODO test_find_legal_move_when_surrounded

    def test_generate_next_node_returns_generator(self):
        # GIVEN
        board_state = [["●", "+", "+"], ["+", "+", "+"], ["+", "+", "+"]]
        my_node_4 = GoNode(
            player="maximizer",
            score=0,
            branches=[],
            board_state=board_state,
        )

        # WHEN

        # THEN
        expected = GeneratorType
        potential_moves = my_node_4.generate_next_node()
        actual = type(potential_moves)
        self.assertEqual(expected, actual)

    def test_branch_getter_returns_attack_options(self):
        # GIVEN
        board_state = [["●", "+", "+"], ["+", "+", "+"], ["+", "+", "+"]]
        my_node_5 = GoNode(
            player="maximizer",
            score=0,
            branches=[],
            board_state=board_state,
        )

        # WHEN

        # THEN
        expected = [(0, 1), (1, 0)]
        potential_moves = my_node_5.generate_next_node_around_existing_moves()
        actual = [item.move_coordinates for item in potential_moves]
        self.assertEqual(expected, actual)

    def test_branch_getter_returns_attack_options_2_groups(self):
        # GIVEN
        board_state = [["●", "+", "+"], ["+", "+", "+"], ["+", "+", "●"]]
        my_node_6 = GoNode(
            player="maximizer",
            score=0,
            branches=[],
            board_state=board_state,
        )

        # WHEN

        # THEN
        expected = [(0, 1), (1, 0), (1, 2), (2, 1)]
        potential_moves = my_node_6.generate_next_node_around_existing_moves()
        actual = [item.move_coordinates for item in potential_moves]
        self.assertEqual(expected, actual)

    def test_branch_getter_returns_defend_options_2_groups(self):
        # GIVEN
        board_state = [["○", "+", "+"], ["+", "+", "+"], ["+", "+", "○"]]
        my_node_7 = GoNode(
            player="maximizer",
            score=0,
            branches=[],
            board_state=board_state,
        )

        # WHEN

        # THEN
        expected = [(0, 1), (1, 0), (1, 2), (2, 1)]
        potential_moves = my_node_7.generate_next_node_around_existing_moves()
        actual = [item.move_coordinates for item in potential_moves]
        self.assertEqual(expected, actual)

    def test_branch_getter_returns_attack_and_defend_options(self):
        # GIVEN
        board_state = [["●", "+", "+"], ["+", "+", "+"], ["+", "+", "○"]]
        my_node_8 = GoNode(
            player="maximizer",
            score=0,
            branches=[],
            board_state=board_state,
        )

        # WHEN

        # THEN
        expected = [(0, 1), (1, 0), (1, 2), (2, 1)]
        potential_moves = my_node_8.generate_next_node_around_existing_moves()
        actual = [item.move_coordinates for item in potential_moves]
        self.assertEqual(expected, actual)

    def test_get_scores_one_stone(self):
        # GIVEN
        board_state = [["●", "+", "+"], ["+", "+", "+"], ["+", "+", "+"]]
        my_node_9 = GoNode(
            player="maximizer",
            score=0,
            branches=[],
            board_state=board_state,
        )

        # WHEN
        actual = my_node_9.get_utility()

        # THEN
        expected = 1
        self.assertEqual(expected, actual)

    def test_get_scores_two_groups_of_one_stone(self):
        # GIVEN
        board_state = [["●", "+", "●"], ["+", "+", "+"], ["+", "+", "+"]]
        my_node_10 = GoNode(
            player="maximizer",
            score=0,
            branches=[],
            board_state=board_state,
        )

        # WHEN
        actual = my_node_10.get_utility()

        # THEN
        expected = 1
        self.assertEqual(expected, actual)

    def test_get_scores_two_stones_horizontal(self):
        # GIVEN
        board_state = [["●", "●", "+"], ["+", "+", "+"], ["+", "+", "+"]]
        my_node_11 = GoNode(
            player="maximizer",
            score=0,
            branches=[],
            board_state=board_state,
        )

        # WHEN
        actual = my_node_11.get_utility()

        # THEN
        expected = 2
        self.assertEqual(expected, actual)

    def test_get_scores_two_stones_horizontal_other_row(self):
        # GIVEN
        board_state = [["+", "+", "+"], ["●", "●", "+"], ["+", "+", "+"]]
        my_node_12 = GoNode(
            player="maximizer",
            score=0,
            branches=[],
            board_state=board_state,
        )

        # WHEN
        actual = my_node_12.get_utility()

        # THEN
        expected = 2
        self.assertEqual(expected, actual)

    def test_get_scores_white_stones(self):
        # GIVEN
        board_state = [["+", "+", "+"], ["○", "○", "+"], ["+", "+", "+"]]
        my_node_13 = GoNode(
            player="maximizer",
            score=0,
            branches=[],
            board_state=board_state,
        )

        # WHEN
        actual = my_node_13.get_utility()

        # THEN
        expected = -2
        self.assertEqual(expected, actual)

    def test_get_scores_two_stones_vertical(self):
        # GIVEN
        board_state = [["●", "+", "+"], ["●", "+", "+"], ["+", "+", "+"]]
        my_node_14 = GoNode(
            player="maximizer",
            score=0,
            branches=[],
            board_state=board_state,
        )

        # WHEN
        actual = my_node_14.get_utility()

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
            ["+", "+", "●", "●", "●", "●", "●", "○", "+"],
            ["+", "+", "+", "+", "+", "+", "+", "+", "+"],
            ["+", "+", "○", "○", "○", "+", "+", "○", "+"],
            ["+", "+", "+", "+", "+", "+", "+", "+", "+"],
            ["+", "+", "+", "+", "+", "+", "+", "+", "+"],
        ]
        my_node_15 = GoNode(
            player="maximizer",
            score=0,
            branches=[],
            board_state=board_state,
        )

        # WHEN
        actual = my_node_15.get_utility()

        # THEN
        expected = 1
        self.assertEqual(expected, actual)

    # TODO test_find_connecting_stones

    # TODO test_build_minimax_alpha_beta_game_tree_returns_best_score(self):

    # TODO test_gets_best_move_only_one_option(self):

    def test_build_game_tree_doesnt_build_past_terminal_node(self):
        # GIVEN
        board_state = [["●", "+", "+"], ["●", "+", "+"], ["+", "+", "+"]]

        player="minimizer"
        game_tree_node_1 = GoNode(
                    player=player,
                    move_id="test_build_game_tree_doesnt_build_past_terminal_node",
                    board_state=board_state,
                )

        depth = 0

        # hack to get around suspected test pollution
        game_tree_node_1.branches = []

        # WHEN


        game_tree_node_1.build_game_tree(depth)
        actual = game_tree_node_1.get_branches()
        print()

        # THEN
        expected = []
        self.assertEqual(expected, actual)

    def test_build_game_tree_builds(self):
        # GIVEN
        player="maximizer"
        game_tree_node_2 = GoNode(
                    player=player,
                    board_state=[
                        ["●", "+", "+"],
                        ["●", "+", "+"],
                        ["+", "+", "+"]
                    ],
                )

        depth = 1
        # hack to get around suspected test pollution
        game_tree_node_2.branches = []


        # WHEN
        game_tree_node_2.build_game_tree(depth)
        actual = len(game_tree_node_2.get_branches())

        # THEN
        expected = 7
        self.assertEqual(expected, actual)

    @skip("Removing concept of terminal from nodes")
    def test_build_game_tree_sets_nodes_as_terminal(self):
        # GIVEN
        board_state = [["●", "+", "+"], ["●", "+", "+"], ["+", "+", "+"]]
        player="maximizer"

        game_tree_node_3 = GoNode(
                    player=player,
                    board_state=board_state,
                )

        depth = 1

        # hack to get around suspected test pollution
        game_tree_node_3.branches = []

        # WHEN
        game_tree_node_3.build_game_tree(depth)
        branches = game_tree_node_3.get_branches()
        actual = all([branch.is_terminal for branch in branches])

        # THEN
        expected = True
        self.assertEqual(expected, actual)

    @skip("Removing concept of terminal from nodes")
    def test_build_game_tree_doesnt_set_terminal_for_intermediary_nodes(self):
        # GIVEN
        board_state = [["●", "+", "+"], ["●", "+", "+"], ["+", "+", "+"]]
        player="maximizer"

        game_tree_node_4 = GoNode(
                    player=player,
                    board_state=board_state,
                )

        depth = 2

        # hack to get around suspected test pollution
        game_tree_node_4.branches = []

        # WHEN
        game_tree_node_4.build_game_tree(depth)
        branches = game_tree_node_4.get_branches()
        actual = all([branch.is_terminal for branch in branches])

        # THEN
        expected = False
        self.assertEqual(expected, actual)

    @skip("Removing concept of terminal from nodes")
    def test_build_game_sets_terminal_for_winning_white_nodes(self):
        # GIVEN
        game_tree_node_5 = GoNode(
                    player="maximizer",
                    board_state=[
                        ["○", "+", "+", "+", "+"],
                        ["○", "+", "+", "+", "+"],
                        ["○", "+", "+", "+", "+"],
                        ["○", "+", "+", "+", "+"],
                        ["+", "+", "+", "+", "+"]
                    ]
                )

        # hack to get around suspected test pollution
        game_tree_node_5.branches = []

        depth = 2

        # WHEN
        game_tree_node_5.build_game_tree(depth)
        branches = game_tree_node_5.get_branches()
        terminality = [branch.is_terminal for branch in branches]
        actual = sum(item == True for item in terminality)

        # THEN
        expected = 1
        self.assertEqual(expected, actual)

    @skip("Removing concept of terminal from nodes")
    def test_build_game_sets_terminal_for_black_winning_nodes(self):
        # GIVEN
        player="minimizer"
        board_state = [
            ["●", "+", "+", "+", "+"],
            ["●", "+", "+", "+", "+"],
            ["●", "+", "+", "+", "+"],
            ["●", "+", "+", "+", "+"],
            ["+", "+", "+", "+", "+"]
        ]
        game_tree_node_6 = GoNode(
                    player=player,
                    board_state=board_state,
                )

        # hack to get around suspected test pollution
        game_tree_node_6.branches = []

        depth = 2

        # WHEN
        game_tree_node_6.build_game_tree(depth)
        branches = game_tree_node_6.get_branches()
        terminality = [branch.is_terminal for branch in branches]
        actual = sum(item == True for item in terminality)

        # THEN
        expected = 1
        self.assertEqual(expected, actual)

    @skip("Working on this at the moment")
    def test_build_game_tree_builds_to_given_depth(self):
        # GIVEN
        player="maximizer"
        game_tree_node_7 = GoNode(
                    player=player,
                    board_state=[["●", "+"], ["+", "+"]],
                )

        node_7_depth = 3
        # hack to get around suspected test pollution
        game_tree_node_7.branches = []
        game_tree_node_7.build_game_tree(node_7_depth)

        # WHEN
        actual = game_tree_node_7.find_depth(0)

        # THEN
        expected = node_7_depth
        self.assertEqual(expected, actual)