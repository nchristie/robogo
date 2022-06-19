from django.test import TestCase
from games.views import Board


class BoardTestCase(TestCase):
    def setUp(self):
        self.my_board = Board()
        # Board.objects.create()

    def test_board_draw(self):
        """Board can be drawn"""
        expected = [
            [None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None],
        ]
        actual = self.my_board.draw()
        self.assertEqual(actual, expected)

    def test_board_make_move(self):
        self.my_board.make_move(0, 0, "Black")
        expected = "Black"
        actual = self.my_board.state[0][0]
        self.assertEqual(actual, expected)
