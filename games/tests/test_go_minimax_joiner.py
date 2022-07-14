from django.test import TestCase
from games.go_minimax_joiner import GoNode, BLACK_STONE
from uuid import UUID
from types import GeneratorType


class GoNodeTestCase(TestCase):
    def setUp(self):
        self.my_node = GoNode(
            move_id="49dedb0d-5cf6-4f84-b228-efbc1dbaf06a",
            player="maximizer",
            score=0,
            is_terminal=False,
            leaves=[],
            board_state=None,
        )

    def test_leaf_getter_makes_array(self):
        # GIVEN
        board_state = [["●", "+", "+"], ["+", "+", "+"], ["+", "+", "+"]]
        self.my_node.board_state = board_state
        self.my_node.set_leaves()
        node_array = self.my_node.leaves

        # WHEN
        actual = type(node_array)

        # THEN
        expected = list
        self.assertEqual(expected, actual)

    def test_leaf_getter_array_has_uuid_move_ids(self):
        # GIVEN
        board_state = [["●", "+", "+"], ["+", "+", "+"], ["+", "+", "+"]]
        self.my_node.board_state = board_state

        # WHEN
        self.my_node.set_leaves()
        node_array = self.my_node.leaves

        # THEN
        for node in node_array:
            assert UUID(node.get_move_id())

    def test_find_legal_move(self):
        # GIVEN
        self.my_node.board_state = [["+", "+", "+"], ["+", "●", "+"], ["+", "+", "+"]]

        # WHEN
        potential_moves = self.my_node.get_potential_moves()
        actual = [item["move_coordinates"] for item in potential_moves]

        # THEN
        expected = [(0, 1), (1, 0), (1, 2), (2, 1)]
        self.assertEqual(expected, actual)

    def test_find_legal_move_when_boundary(self):
        # GIVEN
        self.my_node.board_state = [["+", "+", "+"], ["+", "+", "+"], ["+", "+", "●"]]

        # WHEN
        potential_moves = self.my_node.get_potential_moves()
        actual = [item["move_coordinates"] for item in potential_moves]


        # THEN
        expected = [(1, 2), (2, 1)]
        self.assertEqual(expected, actual)

    def test_find_legal_move_when_neighbouring_stones(self):
        # GIVEN
        self.my_node.board_state = [
            ["+", "+", "+", "+"],
            ["+", "●", "+", "+"],
            ["+", "●", "+", "+"],
            ["+", "+", "+", "+"],
        ]

        # WHEN
        potential_moves = self.my_node.get_potential_moves()
        actual = [item["move_coordinates"] for item in potential_moves]


        # THEN
        expected = [(0, 1), (1, 0), (1, 2), (2, 0), (2, 2), (3, 1)]
        self.assertEqual(expected, actual)

    # TODO Implement this logic in the code
    # def test_find_legal_move_when_surrounded(self):
    #     # GIVEN
    #     x_coordinate = 1
    #     y_coordinate = 1
    #     self.my_node.board_state = [
    #         ["+", "○", "○", "+"],
    #         ["○", "●", "+", "○"],
    #         ["+", "○", "○", "+"],
    #         ["+", "+", "+", "+"]
    #     ]

    #     # WHEN
    #     actual = [move for move in self.my_node.find_legal_moves_around_position(x_coordinate, y_coordinate)]

    #     # THEN
    #     expected = []
    #     self.assertEqual(expected, actual)


    def test_get_potential_moves_returns_generator(self):
        # GIVEN
        board_state = [["●", "+", "+"], ["+", "+", "+"], ["+", "+", "+"]]
        self.my_node.board_state = board_state

        # WHEN

        # THEN
        expected = GeneratorType
        potential_moves = self.my_node.get_potential_moves()
        actual = type(potential_moves)
        self.assertEqual(expected, actual)

    def test_leaf_getter_returns_attack_options(self):
        # GIVEN
        board_state = [["●", "+", "+"], ["+", "+", "+"], ["+", "+", "+"]]
        self.my_node.board_state = board_state

        # WHEN

        # THEN
        expected = [(0, 1), (1, 0)]
        potential_moves = self.my_node.get_potential_moves()
        actual = [item["move_coordinates"] for item in potential_moves]
        self.assertEqual(expected, actual)

    def test_leaf_getter_returns_attack_options_2_groups(self):
        # GIVEN
        board_state = [["●", "+", "+"], ["+", "+", "+"], ["+", "+", "●"]]
        self.my_node.board_state = board_state

        # WHEN

        # THEN
        expected = [(0, 1), (1, 0), (1, 2), (2, 1)]
        potential_moves = self.my_node.get_potential_moves()
        actual = [item["move_coordinates"] for item in potential_moves]
        self.assertEqual(expected, actual)

    def test_leaf_getter_returns_defend_options_2_groups(self):
        # GIVEN
        board_state = [["○", "+", "+"], ["+", "+", "+"], ["+", "+", "○"]]
        self.my_node.board_state = board_state

        # WHEN

        # THEN
        expected = [(0, 1), (1, 0), (1, 2), (2, 1)]
        potential_moves = self.my_node.get_potential_moves()
        actual = [item["move_coordinates"] for item in potential_moves]
        self.assertEqual(expected, actual)

    def test_leaf_getter_returns_attack_and_defend_options(self):
        # GIVEN
        board_state = [["●", "+", "+"], ["+", "+", "+"], ["+", "+", "○"]]
        self.my_node.board_state = board_state

        # WHEN

        # THEN
        expected = [(0, 1), (1, 0), (1, 2), (2, 1)]
        potential_moves = self.my_node.get_potential_moves()
        actual = [item["move_coordinates"] for item in potential_moves]
        self.assertEqual(expected, actual)

    def test_get_scores_one_stone(self):
        # GIVEN
        board_state = [["●", "+", "+"], ["+", "+", "+"], ["+", "+", "+"]]
        self.my_node.board_state = board_state

        # WHEN
        actual = self.my_node.get_utility()

        # THEN
        expected = 1
        self.assertEqual(expected, actual)

    def test_get_scores_two_groups_of_one_stone(self):
        # GIVEN
        board_state = [["●", "+", "●"], ["+", "+", "+"], ["+", "+", "+"]]
        self.my_node.board_state = board_state

        # WHEN
        actual = self.my_node.get_utility()

        # THEN
        expected = 1
        self.assertEqual(expected, actual)

    def test_get_scores_two_stones_horizontal(self):
        # GIVEN
        board_state = [["●", "●", "+"], ["+", "+", "+"], ["+", "+", "+"]]
        self.my_node.board_state = board_state

        # WHEN
        actual = self.my_node.get_utility()

        # THEN
        expected = 2
        self.assertEqual(expected, actual)

    def test_get_scores_two_stones_horizontal_other_row(self):
        # GIVEN
        board_state = [["+", "+", "+"], ["●", "●", "+"], ["+", "+", "+"]]
        self.my_node.board_state = board_state

        # WHEN
        actual = self.my_node.get_utility()

        # THEN
        expected = 2
        self.assertEqual(expected, actual)

    def test_get_scores_white_stones(self):
        # GIVEN
        board_state = [["+", "+", "+"], ["○", "○", "+"], ["+", "+", "+"]]
        self.my_node.board_state = board_state

        # WHEN
        actual = self.my_node.get_utility()

        # THEN
        expected = -2
        self.assertEqual(expected, actual)

    def test_get_scores_two_stones_vertical(self):
        # GIVEN
        board_state = [["●", "+", "+"], ["●", "+", "+"], ["+", "+", "+"]]
        self.my_node.board_state = board_state

        # WHEN
        actual = self.my_node.get_utility()

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
        self.my_node.board_state = board_state

        # WHEN
        actual = self.my_node.get_utility()

        # THEN
        expected = 1
        self.assertEqual(expected, actual)

    def test_gets_best_move_only_one_option(self):
        # GIVEN
        board_state = [["●", "+", "+"], ["●", "+", "+"], ["+", "+", "+"]]
        self.my_node.board_state = board_state

        # WHEN
        self.my_node.set_leaves(player="maximizer", is_terminal=True)
        actual = self.my_node.optimal_move_coordinates
        # THEN
        expected = (2, 0)
        self.assertEqual(expected, actual)

    def test_find_connecting_stones(self):
        # GIVEN
        board_state = [["●", "+", "+"], ["●", "+", "+"], ["+", "+", "+"]]
        # WHEN
        # THEN
