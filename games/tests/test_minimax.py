from django.test import TestCase
from games.minimax import Node

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

    def test_set_leaves(self):
        actual = self.my_node.set_leaves()
        expected = None
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

