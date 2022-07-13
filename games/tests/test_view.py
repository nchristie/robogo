from django.test import TestCase
from games.views import Board, find_game_by_ip


class BoardTestCase(TestCase):
    def setUp(self):
        self.my_board = Board()
        ip = "000.00.0.0"
        self.user_game = find_game_by_ip(ip)

    def test_board_draw(self):
        """Board can be drawn"""
        expected = [
            ["+", "+", "+", "+", "+", "+", "+", "+", "+"],
            ["+", "+", "+", "+", "+", "+", "+", "+", "+"],
            ["+", "+", "+", "+", "+", "+", "+", "+", "+"],
            ["+", "+", "+", "+", "+", "+", "+", "+", "+"],
            ["+", "+", "+", "+", "+", "+", "+", "+", "+"],
            ["+", "+", "+", "+", "+", "+", "+", "+", "+"],
            ["+", "+", "+", "+", "+", "+", "+", "+", "+"],
            ["+", "+", "+", "+", "+", "+", "+", "+", "+"],
            ["+", "+", "+", "+", "+", "+", "+", "+", "+"],
        ]
        moves = self.user_game.move_set.all().order_by("-id")

        self.my_board.draw(moves)

        actual = self.my_board.state
        self.assertEqual(actual, expected)

    def test_board_make_move(self):
        self.my_board.make_move(0, 0, "Black")
        expected = "Black"
        actual = self.my_board.state[0][0]
        self.assertEqual(actual, expected)
