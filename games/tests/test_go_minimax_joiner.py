from django.test import TestCase
from games.go_minimax_joiner import LeafGetter, Node

class LeafGetterTestCase(TestCase):
    def setUp(self):
        self.my_node = Node(
            move_id = "49dedb0d-5cf6-4f84-b228-efbc1dbaf06a",
            player = "white",
            score = 0,
            leaf_getter=LeafGetter
        )
    
    def test_leaf_getter_makes_array(self):
        # GIVEN
        leaf_getting_object = self.my_node.leaf_getter()
        node_array = leaf_getting_object.get_node_array()
        
        # WHEN
        actual = [node.get_move_id() for node in node_array]
        
        # THEN
        expected = [0,1,2]
        self.assertEqual(expected, actual)
    
    def test_find_intersections(self):
        # GIVEN
        leaf_getting_object = self.my_node.leaf_getter()
        x_coordinate = 1
        y_coordinate = 1
        board_size = 3

        # WHEN
        actual = leaf_getting_object.find_intersections(x_coordinate, y_coordinate, board_size)

        # THEN
        expected = [(0,1), (1,0), (1,2), (2,1)]
        self.assertEqual(expected, actual)

    def test_find_intersections_when_boundary(self):
        # GIVEN
        leaf_getting_object = self.my_node.leaf_getter()
        x_coordinate = 2
        y_coordinate = 2
        board_size = 3

        # WHEN
        actual = leaf_getting_object.find_intersections(x_coordinate, y_coordinate, board_size)

        # THEN
        expected = [(1,2), (2,1)]
        self.assertEqual(expected, actual)
    
    def test_leaf_getter_returns_attack_options(self):
        # GIVEN
        board_state = [
            ["●", "+", "+"],
            ["+", "+", "+"],
            ["+", "+", "+"]
        ]
        leaf_getting_object = LeafGetter()

        # WHEN

        # THEN
        expected = [(0,1),(1,0)]
        actual = leaf_getting_object.get_potential_moves(board_state)
        self.assertEqual(expected, actual)

    def test_leaf_getter_returns_attack_options_2_groups(self):
        # GIVEN
        board_state = [
            ["●", "+", "+"],
            ["+", "+", "+"],
            ["+", "+", "●"]
        ]
        leaf_getting_object = LeafGetter()

        # WHEN

        # THEN
        expected = [(0,1),(1,0),(1,2),(2,1)]
        actual = leaf_getting_object.get_potential_moves(board_state)
        self.assertEqual(expected, actual)

    def test_leaf_getter_returns_defend_options_2_groups(self):
        # GIVEN
        board_state = [
            ["○", "+", "+"],
            ["+", "+", "+"],
            ["+", "+", "○"]
        ]
        leaf_getting_object = LeafGetter()

        # WHEN

        # THEN
        expected = [(0,1),(1,0),(1,2),(2,1)]
        actual = leaf_getting_object.get_potential_moves(board_state)
        self.assertEqual(expected, actual)

    def test_leaf_getter_returns_attack_and_defend_options(self):
        # GIVEN
        board_state = [
            ["●", "+", "+"],
            ["+", "+", "+"],
            ["+", "+", "○"]
        ]
        leaf_getting_object = LeafGetter()

        # WHEN

        # THEN
        expected = [(0,1),(1,0),(1,2),(2,1)]
        actual = leaf_getting_object.get_potential_moves(board_state)
        self.assertEqual(expected, actual)
        
