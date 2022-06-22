from django.test import TestCase
from games.minimax import Node, LeafGetter
import pytest

class NodeTestCase(TestCase):
    def setUp(self):
        self.my_node = Node()

    def test_get_score(self):
        """Get score"""
        expected = None
        actual = self.my_node.get_score()
        self.assertEqual(expected, actual)

    def test_set_score(self):
        """Set score"""
        self.my_node.set_score(5)
        expected = 5
        actual = self.my_node.get_score()
        self.assertEqual(expected, actual)
    
    def test_get_leaves(self):
        """"""
        expected = []
        actual = self.my_node.get_leaves()
        self.assertEqual(expected, actual)
    
    def test_add_leaf(self):
        """"""
        score = 4
        move_id = 123
        player = 'maximizer'
        self.my_node.add_leaf(move_id, player, score)
        leaves = self.my_node.get_leaves()
        expected = (move_id, player, score)
        leaf = leaves[0]
        actual = (leaf.move_id, leaf.player, leaf.score)
        self.assertEqual(expected, actual)
    
    def test_returns_max_for_maximizer(self):
        # GIVEN
        available_moves = [
            {
                "move_id": 14,
                "score": 1, 
            },
            {
                "move_id": 15,
                "score": 2
            },
            {
                "move_id": 16,
                "score": 3
            }
        ]
        player = "maximizer"

        # WHEN
        for move in available_moves:
            self.my_node.add_leaf(move_id=move['move_id'], score=move['score'], player=player)
        

        # THEN
        expected = 3
        actual = self.my_node.get_logical_move().get_score()
        self.assertEqual(expected, actual)

    def test_returns_min_for_minimizer(self):
        # GIVEN
        available_moves = [
            {
                "move_id": 14,
                "score": 1, 
            },
            {
                "move_id": 15,
                "score": 2
            },
            {
                "move_id": 16,
                "score": 3
            }
        ]
        player = "minimizer"

        # WHEN
        for move in available_moves:
            self.my_node.add_leaf(move_id=move['move_id'], score=move['score'], player=player)
        

        # THEN
        expected = 1
        actual = self.my_node.get_logical_move().get_score()
        self.assertEqual(expected, actual)
    
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
    
    @pytest.mark.skip(reason="need to make a helper work first")
    def test_leaf_getter_returns_attack_option(self):
        # GIVEN
        board_state = [
            ["●", "+", "+"],
            ["+", "+", "+"],
            ["+", "+", "+"]
        ]
        leaf_getting_object = LeafGetter()

        # WHEN

        # THEN
        expected = [[1,0]]
        actual = leaf_getting_object.get_potential_moves(board_state)
        self.assertEqual(expected, actual)
        
