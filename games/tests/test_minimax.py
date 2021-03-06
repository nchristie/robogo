from django.test import TestCase
from games.minimax import MinimaxNode


class MinimaxNodeTestCase(TestCase):
    def test_get_score(self):
        """Get score"""
        # GIVEN
        my_node_1 = MinimaxNode(move_id=1, player="maximizer", score=None, children=[])
        with self.assertRaises(Exception):
            my_node_1.get_score()

    def test_set_score(self):
        """Set score"""
        # GIVEN
        my_node_2 = MinimaxNode(move_id=2, player="maximizer", score=None, children=[])
        my_node_2.set_score(5)
        expected = 5
        actual = my_node_2.get_score()
        self.assertEqual(expected, actual)

    def test_get_children(self):
        """"""
        # GIVEN
        my_node_3 = MinimaxNode(move_id=3, player="maximizer", score=None, children=[])
        expected = []
        actual = my_node_3.get_children()
        self.assertEqual(expected, actual)

    def test_add_child(self):
        """"""
        # GIVEN
        my_node_4 = MinimaxNode(move_id=4, player="maximizer", score=None, children=[])
        score = 4
        move_id = 123
        player = "maximizer"
        my_node_4.add_child(move_id, player, score)
        children = my_node_4.get_children()
        expected = (move_id, player, score)
        child = children[0]
        actual = (child.move_id, child.player, child.score)
        self.assertEqual(expected, actual)

    def test_returns_max_for_maximizer(self):
        # GIVEN
        my_node_5 = MinimaxNode(move_id=5, player="maximizer", score=None, children=[])
        available_moves = [
            {
                "move_id": 14,
                "score": 1,
            },
            {"move_id": 15, "score": 2},
            {"move_id": 16, "score": 3},
        ]
        player = "maximizer"

        # WHEN
        for move in available_moves:
            my_node_5.add_child(
                move_id=move["move_id"], score=move["score"], player=player
            )

        # THEN
        expected = 3
        actual = my_node_5.get_optimal_move().get_score()
        self.assertEqual(expected, actual)

    def test_returns_min_for_minimizer(self):
        # GIVEN
        my_node_6 = MinimaxNode(move_id=6, player="maximizer", score=None, children=[])
        available_moves = [
            {
                "move_id": 17,
                "score": 4,
            },
            {"move_id": 18, "score": 5},
            {"move_id": 19, "score": 6},
        ]
        player = "minimizer"

        # WHEN
        for move in available_moves:
            my_node_6.add_child(
                move_id=move["move_id"], score=move["score"], player=player
            )

        # THEN
        expected = 4
        optimal_move = my_node_6.get_optimal_move()
        actual = optimal_move.get_score()
        self.assertEqual(expected, actual)

    def test_node_min(self):
        # GIVEN
        my_node_none = MinimaxNode(
            move_id=1, player="maximizer", score=None, children=[]
        )
        my_node_low = MinimaxNode(move_id=1, player="maximizer", score=-5, children=[])
        my_node_high = MinimaxNode(move_id=1, player="maximizer", score=5, children=[])

        # WHEN
        actual = my_node_none.node_min(my_node_low, my_node_high)

        # THEN
        expected = my_node_low
        self.assertEqual(expected, actual)

    def test_node_max(self):
        # GIVEN
        my_node_none = MinimaxNode(
            move_id=1, player="maximizer", score=None, children=[]
        )
        my_node_low = MinimaxNode(move_id=1, player="maximizer", score=-5, children=[])
        my_node_high = MinimaxNode(move_id=1, player="maximizer", score=5, children=[])

        # WHEN
        actual = my_node_none.node_max(my_node_low, my_node_high)

        # THEN
        expected = my_node_high
        self.assertEqual(expected, actual)
