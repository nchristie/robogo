from django.test import TestCase
from games.go_minimax_joiner import GoNode, GoTree
from types import GeneratorType
from unittest import skip
from games.game_logic import MINUS_INF, PLUS_INF

class GoNodeTestCase(TestCase):
    def test_find_legal_move(self):
        # GIVEN
        board_state = [["+", "+", "+"], ["+", "●", "+"], ["+", "+", "+"]]
        my_node_1 = GoNode(
            player="maximizer",
            score=0,
            children=[],
            board_state=board_state,
        )

        # WHEN
        potential_moves = my_node_1.generate_next_child_around_existing_moves()
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
            children=[],
            board_state=board_state,
        )

        # WHEN
        potential_moves = my_node_2.generate_next_child_around_existing_moves()
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
            children=[],
            board_state=board_state,
        )

        # WHEN
        potential_moves = my_node_3.generate_next_child_around_existing_moves()
        actual = [item.move_coordinates for item in potential_moves]

        # THEN
        expected = [(0, 1), (1, 0), (1, 2), (2, 0), (2, 2), (3, 1)]
        self.assertEqual(expected, actual)

    # TODO test_find_legal_move_when_surrounded

    def test_generate_next_child_returns_generator(self):
        # GIVEN
        board_state = [["●", "+", "+"], ["+", "+", "+"], ["+", "+", "+"]]
        my_node_4 = GoNode(
            player="maximizer",
            score=0,
            children=[],
            board_state=board_state,
        )
        depth = 1

        # WHEN

        # THEN
        expected = GeneratorType
        potential_moves = my_node_4.generate_next_child(depth)
        actual = type(potential_moves)
        self.assertEqual(expected, actual)

    def test_child_getter_returns_attack_options(self):
        # GIVEN
        board_state = [["●", "+", "+"], ["+", "+", "+"], ["+", "+", "+"]]
        my_node_5 = GoNode(
            player="maximizer",
            score=0,
            children=[],
            board_state=board_state,
        )

        # WHEN

        # THEN
        expected = [(0, 1), (1, 0)]
        potential_moves = my_node_5.generate_next_child_around_existing_moves()
        actual = [item.move_coordinates for item in potential_moves]
        self.assertEqual(expected, actual)

    def test_child_getter_returns_attack_options_2_groups(self):
        # GIVEN
        board_state = [["●", "+", "+"], ["+", "+", "+"], ["+", "+", "●"]]
        my_node_6 = GoNode(
            player="maximizer",
            score=0,
            children=[],
            board_state=board_state,
        )

        # WHEN

        # THEN
        expected = [(0, 1), (1, 0), (1, 2), (2, 1)]
        potential_moves = my_node_6.generate_next_child_around_existing_moves()
        actual = [item.move_coordinates for item in potential_moves]
        self.assertEqual(expected, actual)

    def test_child_getter_returns_defend_options_2_groups(self):
        # GIVEN
        board_state = [["○", "+", "+"], ["+", "+", "+"], ["+", "+", "○"]]
        my_node_7 = GoNode(
            player="maximizer",
            score=0,
            children=[],
            board_state=board_state,
        )

        # WHEN

        # THEN
        expected = [(0, 1), (1, 0), (1, 2), (2, 1)]
        potential_moves = my_node_7.generate_next_child_around_existing_moves()
        actual = [item.move_coordinates for item in potential_moves]
        self.assertEqual(expected, actual)

    def test_child_getter_returns_attack_and_defend_options(self):
        # GIVEN
        board_state = [["●", "+", "+"], ["+", "+", "+"], ["+", "+", "○"]]
        my_node_8 = GoNode(
            player="maximizer",
            score=0,
            children=[],
            board_state=board_state,
        )

        # WHEN

        # THEN
        expected = [(0, 1), (1, 0), (1, 2), (2, 1)]
        potential_moves = my_node_8.generate_next_child_around_existing_moves()
        actual = [item.move_coordinates for item in potential_moves]
        self.assertEqual(expected, actual)

    def test_get_scores_one_stone(self):
        # GIVEN
        board_state = [["●", "+", "+"], ["+", "+", "+"], ["+", "+", "+"]]
        my_node_9 = GoNode(
            player="maximizer",
            score=0,
            children=[],
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
            children=[],
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
            children=[],
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
            children=[],
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
            children=[],
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
            children=[],
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
            ["+", "+", "●", "●", "●", "●", "+", "○", "+"],
            ["+", "+", "+", "+", "+", "+", "+", "+", "+"],
            ["+", "+", "○", "○", "○", "+", "+", "○", "+"],
            ["+", "+", "+", "+", "+", "+", "+", "+", "+"],
            ["+", "+", "+", "+", "+", "+", "+", "+", "+"],
        ]
        my_node_15 = GoNode(
            player="maximizer",
            score=0,
            children=[],
            board_state=board_state,
        )

        # WHEN
        actual = my_node_15.get_utility()

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
            player="maximizer",
            score=0,
            children=[],
            board_state=board_state,
        )

        # WHEN
        actual = my_node_15.get_utility()

        # THEN
        expected = float("inf")
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
            player="maximizer",
            score=0,
            children=[],
            board_state=board_state,
        )

        # WHEN
        actual = my_node_15.get_utility()

        # THEN
        expected = -float("inf")
        self.assertEqual(expected, actual)

    # TODO test_find_connecting_stones

    # TODO test_build_minimax_alpha_beta_game_tree_returns_best_score(self):

    # TODO test_gets_best_move_only_one_option(self):

    @skip("Removing concept of terminal from nodes")
    def test_build_game_tree_recursive_sets_nodes_as_terminal(self):
        # GIVEN
        board_state = [["●", "+", "+"], ["●", "+", "+"], ["+", "+", "+"]]
        player = "maximizer"

        game_tree_node_3 = GoNode(
            player=player,
            board_state=board_state,
        )

        depth = 1

        # hack to get around suspected test pollution
        game_tree_node_3.children = []

        # WHEN
        game_tree_node_3.build_game_tree_recursive(depth)
        children = game_tree_node_3.get_children()
        actual = all([child.is_terminal for child in children])

        # THEN
        expected = True
        self.assertEqual(expected, actual)

    @skip("Removing concept of terminal from nodes")
    def test_build_game_tree_recursive_doesnt_set_terminal_for_intermediary_nodes(self):
        # GIVEN
        board_state = [["●", "+", "+"], ["●", "+", "+"], ["+", "+", "+"]]
        player = "maximizer"

        game_tree_node_4 = GoNode(
            player=player,
            board_state=board_state,
        )

        depth = 2

        # hack to get around suspected test pollution
        game_tree_node_4.children = []

        # WHEN
        game_tree_node_4.build_game_tree_recursive(depth)
        children = game_tree_node_4.get_children()
        actual = all([child.is_terminal for child in children])

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
                ["+", "+", "+", "+", "+"],
            ],
        )

        # hack to get around suspected test pollution
        game_tree_node_5.children = []

        depth = 2

        # WHEN
        game_tree_node_5.build_game_tree_recursive(depth)
        children = game_tree_node_5.get_children()
        terminality = [child.is_terminal for child in children]
        actual = sum(item == True for item in terminality)

        # THEN
        expected = 1
        self.assertEqual(expected, actual)

    @skip("This functionality was removed, might return later")
    def test_build_game_sets_terminal_for_black_winning_nodes(self):
        # GIVEN
        player = "minimizer"
        board_state = [
            ["●", "+", "+", "+", "+"],
            ["●", "+", "+", "+", "+"],
            ["●", "+", "+", "+", "+"],
            ["●", "+", "+", "+", "+"],
            ["+", "+", "+", "+", "+"],
        ]
        game_tree_node_6 = GoNode(
            player=player,
            board_state=board_state,
        )

        # hack to get around suspected test pollution
        game_tree_node_6.children = []

        depth = 2

        # WHEN
        game_tree_node_6.build_game_tree_recursive(depth)
        children = game_tree_node_6.get_children()
        terminality = [child.is_leaf_node() for child in children]
        actual = sum(item == True for item in terminality)

        # THEN
        expected = 1
        self.assertEqual(expected, actual)

    @skip("WIP")
    def test_evaluate_node(self):
        # GIVEN
        board_state = [
            ["+", "○", "○", "○", "○", "+", "+", "+", "+"],
            ["+", "+", "+", "+", "+", "●", "+", "+", "+"],
            ["+", "+", "+", "+", "+", "●", "+", "+", "+"],
            ["+", "+", "+", "+", "+", "●", "+", "+", "+"],
            ["+", "+", "+", "+", "+", "●", "+", "+", "+"],
            ["+", "+", "+", "+", "+", "○", "+", "+", "+"],
            ["+", "+", "+", "+", "+", "+", "+", "+", "+"],
            ["+", "+", "+", "+", "+", "+", "+", "+", "+"],
            ["+", "+", "+", "+", "+", "+", "+", "+", "+"],
        ]
        root_node = GoNode(move_id="root_node", player="black", board_state=board_state)

        depth = 2

        build_game_tree_recursive(root_node, depth, set())

        maximizer_choice_node = GoNode(
            move_id="dummy_node_maximizer",
            player="minimizer",
            score=-float("inf"),
            children=[],
            board_state=board_state,
        )

        minimizer_choice_node = GoNode(
            move_id="dummy_node_minimizer",
            player="minimizer",
            score=float("inf"),
            children=[],
            board_state=board_state,
        )

        # WHEN
        actual = root_node.evaluate_node(
            root_node, maximizer_choice_node, minimizer_choice_node, depth
        ).move_coordinates

        # THEN
        expected = (0, 5)
        self.assertEqual(expected, actual)

class GoTreeTestCase(TestCase):

    def test_build_game_tree_recursive_depth(self):
        # GIVEN
        player = "maximizer"
        game_tree_node_3 = GoNode(
            move_id="root_node",
            player=player,
            board_state=[["●", "+"], ["+", "+"]],
        )

        node_3_depth = 3
        tree_3 = GoTree(game_tree_node_3)
        # hack to get around suspected test pollution
        game_tree_node_3.children = []
        tree_3.build_game_tree_recursive(game_tree_node_3, node_3_depth, set())

        # WHEN
        actual = tree_3.root_node.children[0].children[0].children[0].children

        # THEN
        expected = []
        self.assertEqual(expected, actual)


    def test_find_depth_recursive(self):
        # GIVEN
        player = "maximizer"
        game_tree_node_1 = GoNode(
            move_id="root_node",
            player=player,
            board_state=[["●", "+", "+"], ["+", "+", "+"], ["+", "+", "+"]],
        )

        node_1_depth = 4
        tree_1 = GoTree(game_tree_node_1)
        # hack to get around suspected test pollution
        game_tree_node_1.children = []
        tree_1.build_game_tree_recursive(game_tree_node_1, node_1_depth, set())

        # WHEN
        actual = tree_1.find_depth_recursive(game_tree_node_1, 0)

        # THEN
        expected = node_1_depth
        self.assertEqual(expected, actual)

    def test_evaluate_assigns_scores(self):
        # GIVEN
        player = "maximizer"
        game_tree_node_3 = GoNode(
            move_id="root_node",
            player=player,
            board_state=[["●", "●"], ["+", "+"]],
        )
        tree_3 = GoTree(game_tree_node_3)

        node_3_depth = 0
        alpha, beta = MINUS_INF, PLUS_INF
        # hack to get around suspected test pollution
        game_tree_node_3.children = []
        tree_3.evaluate(game_tree_node_3, node_3_depth, set(), alpha, beta)

        # WHEN
        actual = tree_3.root_node.get_score()

        # THEN
        expected = 2
        self.assertEqual(expected, actual)


    def test_evaluate_assigns_scores_based_on_leaves(self):
        # GIVEN
        player = "maximizer"
        game_tree_node_3 = GoNode(
            move_id="root_node",
            player=player,
            board_state=[["●", "●"], ["+", "+"]],
        )

        node_3_depth = 1
        alpha, beta = MINUS_INF, PLUS_INF
        # hack to get around suspected test pollution
        game_tree_node_3.children = []
        tree_3 = GoTree(game_tree_node_3)

        tree_3.evaluate(game_tree_node_3, node_3_depth, set(), alpha, beta)

        # WHEN
        actual = game_tree_node_3.get_score()

        # THEN
        expected = 1
        self.assertEqual(expected, actual)


    def test_evaluate_works_at_depth_of_2(self):
        # GIVEN
        player = "maximizer"
        game_tree_node_4 = GoNode(
            move_id="root_node",
            player=player,
            board_state=[["●", "●"], ["+", "+"]],
        )

        node_4_depth = 2
        alpha, beta = MINUS_INF, PLUS_INF
        # hack to get around suspected test pollution
        game_tree_node_4.children = []
        tree_4 = GoTree(game_tree_node_4)
        tree_4.evaluate(game_tree_node_4, node_4_depth, set(), alpha, beta)

        # WHEN
        actual = game_tree_node_4.get_score()

        # THEN
        expected = 1
        self.assertEqual(expected, actual)


    def test_evaluate_works_at_depth_of_3(self):
        # GIVEN
        player = "maximizer"
        game_tree_node_5 = GoNode(
            move_id="root_node",
            player=player,
            board_state=[["●", "+"], ["+", "+"]],
        )

        node_5_depth = 3
        alpha, beta = MINUS_INF, PLUS_INF
        # hack to get around suspected test pollution
        game_tree_node_5.children = []
        tree_5 = GoTree(game_tree_node_5)
        tree_5.evaluate(game_tree_node_5, node_5_depth, set(), alpha, beta)

        # WHEN
        actual = tree_5.root_node.get_score()

        # THEN
        expected = 0
        self.assertEqual(expected, actual)


    def test_evaluate_returns_correct_score(self):
        # GIVEN
        player = "maximizer"
        game_tree_node_6 = GoNode(
            move_id="root_node",
            player=player,
            board_state=[["●", "○", "+"], ["+", "○", "+"], ["+", "+", "●"]],
        )

        node_6_depth = 4
        alpha, beta = MINUS_INF, PLUS_INF
        # hack to get around suspected test pollution
        game_tree_node_6.children = []
        tree_6 = GoTree(game_tree_node_6)
        tree_6.evaluate(game_tree_node_6, node_6_depth, set(), alpha, beta)

        # WHEN
        actual = tree_6.root_node.get_score()

        # THEN
        expected = 1
        self.assertEqual(expected, actual)


    # @skip("WIP")
    def test_get_best_next_move(self):
        # GIVEN
        player = "maximizer"
        game_tree_node_7 = GoNode(
            move_id="root_node",
            player=player,
            board_state=[["●", "○", "+"], ["+", "○", "+"], ["+", "+", "●"]],
        )

        tree_7 = GoTree(game_tree_node_7)

        node_7_depth = 4
        alpha, beta = MINUS_INF, PLUS_INF
        # hack to get around suspected test pollution
        game_tree_node_7.children = []
        tree_7.evaluate(game_tree_node_7, node_7_depth, set(), alpha, beta)

        # WHEN
        best_score = game_tree_node_7.get_score()

        actual = tree_7.get_best_next_move(game_tree_node_7, best_score).move_coordinates

        # THEN
        expected = (2, 1)
        self.assertEqual(expected, actual)
