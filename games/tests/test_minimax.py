from django.test import TestCase
from games.minimax import MinimaxNode

class NodeTestCase(TestCase):
    def test_get_score(self):
        """Get score"""
        # GIVEN
        my_node_1 = MinimaxNode(
            move_id=1,
            player="maximizer",
            score=None,
            leaves=[]
        )
        expected = None
        actual = my_node_1.get_score()
        self.assertEqual(expected, actual)

    def test_set_score(self):
        """Set score"""
        # GIVEN
        my_node_2 = MinimaxNode(
            move_id=2,
            player="maximizer",
            score=None,
            leaves=[]
        )
        my_node_2.set_score(5)
        expected = 5
        actual = my_node_2.get_score()
        self.assertEqual(expected, actual)

    def test_get_leaves(self):
        """"""
        # GIVEN
        my_node_3 = MinimaxNode(
            move_id=3,
            player="maximizer",
            score=None,
            leaves=[]
        )
        expected = []
        actual = my_node_3.get_leaves()
        self.assertEqual(expected, actual)

    def test_add_leaf(self):
        """"""
        # GIVEN
        my_node_4 = MinimaxNode(
            move_id=4,
            player="maximizer",
            score=None,
            leaves=[]
        )
        score = 4
        move_id = 123
        player = 'maximizer'
        my_node_4.add_leaf(move_id, player, score)
        leaves = my_node_4.get_leaves()
        expected = (move_id, player, score)
        leaf = leaves[0]
        actual = (leaf.move_id, leaf.player, leaf.score)
        self.assertEqual(expected, actual)

    def test_returns_max_for_maximizer(self):
        # GIVEN
        my_node_5 = MinimaxNode(
            move_id=5,
            player="maximizer",
            score=None,
            leaves=[]
        )
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
            my_node_5.add_leaf(move_id=move['move_id'], score=move['score'], player=player)

        # THEN
        expected = 3
        actual = my_node_5.get_optimal_move().get_score()
        self.assertEqual(expected, actual)

    def test_returns_min_for_minimizer(self):
        # GIVEN
        my_node_6 = MinimaxNode(
            move_id=6,
            player="maximizer",
            score=None,
            leaves=[]
        )
        available_moves = [
            {
                "move_id": 17,
                "score": 4,
            },
            {
                "move_id": 18,
                "score": 5
            },
            {
                "move_id": 19,
                "score": 6
            }
        ]
        player = "minimizer"

        # WHEN
        for move in available_moves:
            my_node_6.add_leaf(
                move_id=move['move_id'],
                score=move['score'],
                player=player
            )

        # THEN
        expected = 4
        optimal_move = my_node_6.get_optimal_move()
        actual = optimal_move.get_score()
        self.assertEqual(expected, actual)

