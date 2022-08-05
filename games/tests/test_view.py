from django.test import TestCase
from games.views import Board, find_game_by_ip, get_white_response


class BoardTestCase(TestCase):
    def setUp(self):
        self.my_board = Board()
        ip = "000.00.0.0"
        self.user_game = find_game_by_ip(ip)

    def test_board_update(self):
        """Board can be rendered"""
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

        self.my_board.update(moves)

        actual = self.my_board.state
        self.assertEqual(actual, expected)

    def test_board_make_move(self):
        self.my_board.make_move(0, 0, "Black")
        expected = "Black"
        actual = self.my_board.state[0][0]
        self.assertEqual(actual, expected)


class HelpersTestCase(TestCase):
    def test_get_white_response_3x3(self):
        # GIVEN
        board_state = [
            ["●", "●", "+"],
            ["○", "+", "+"],
            ["+", "+", "+"],
        ]
        winning_score = 3

        # WHEN
        actual = get_white_response(
            board_state=board_state, winning_score=winning_score, depth=4
        )

        # THEN
        expected = (0, 2)
        self.assertEqual(expected, actual)

    def test_get_white_response_two_calls(self):
        # GIVEN
        board_state_1 = [
            ["●", "+", "+", "+"],
            ["+", "+", "+", "+"],
            ["+", "+", "+", "+"],
            ["+", "+", "+", "+"],
        ]

        board_state_2 = [
            ["●", "●", "+", "+"],
            ["○", "+", "+", "+"],
            ["+", "+", "+", "+"],
            ["+", "+", "+", "+"],
        ]
        winning_score = 3
        depth = 4

        # WHEN
        first_call = get_white_response(
            board_state_1, winning_score=winning_score, depth=depth
        )
        actual = get_white_response(
            board_state_2, winning_score=winning_score, depth=depth
        )

        # THEN
        expected = (0, 2)
        self.assertEqual(expected, actual)

    def test_get_white_response_depth_greater_than_remaining_moves(self):
        # GIVEN
        board_state = [
            ["●", "●", "○", "●"],
            ["○", "○", "●", "+"],
            ["○", "●", "○", "+"],
            ["●", "○", "●", "+"],
        ]
        winning_score = 3
        depth = 4

        # WHEN
        actual = get_white_response(
            board_state, winning_score=winning_score, depth=depth
        )

        # THEN
        expected = (1, 3)
        self.assertEqual(expected, actual)
