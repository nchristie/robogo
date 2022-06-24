from django.test import TestCase
from games.minimax import Node

class NodeTestCase(TestCase):
    def test_get_score(self):
        """Get score"""
        # GIVEN
        my_node = Node()
        expected = None
        actual = my_node.get_score()
        self.assertEqual(expected, actual)

    def test_set_score(self):
        """Set score"""
        # GIVEN
        my_node = Node()
        my_node.set_score(5)
        expected = 5
        actual = my_node.get_score()
        self.assertEqual(expected, actual)
    
    def test_get_leaves(self):
        """"""
        # GIVEN
        my_node = Node()
        expected = []
        actual = my_node.get_leaves()
        self.assertEqual(expected, actual)
    
    def test_add_leaf(self):
        """"""
        # GIVEN
        my_node = Node()
        score = 4
        move_id = 123
        player = 'maximizer'
        my_node.add_leaf(move_id, player, score)
        leaves = my_node.get_leaves()
        expected = (move_id, player, score)
        leaf = leaves[0]
        actual = (leaf.move_id, leaf.player, leaf.score)
        self.assertEqual(expected, actual)
    
    def test_returns_max_for_maximizer(self):
        # GIVEN
        my_node = Node()
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
            my_node.add_leaf(move_id=move['move_id'], score=move['score'], player=player)
        

        # THEN
        expected = 3
        actual = my_node.get_optimal_move().get_score()
        self.assertEqual(expected, actual)

    def test_returns_min_for_minimizer(self):
        # GIVEN
        my_node = Node()
        available_moves = [
            {
                "move_id": 17,
                "score": 1, 
            },
            {
                "move_id": 18,
                "score": 2
            },
            {
                "move_id": 19,
                "score": 3
            }
        ]
        player = "minimizer"

        # WHEN
        for move in available_moves:
            my_node.add_leaf(
                move_id=move['move_id'], 
                score=move['score'], 
                player=player
            )
        
        # THEN
        expected = 1
        optimal_move = my_node.get_optimal_move()
        actual = optimal_move.get_score()
        self.assertEqual(expected, actual)
    
