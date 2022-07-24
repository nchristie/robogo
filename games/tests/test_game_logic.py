from games.game_logic import *
import pytest
from games.go_minimax_joiner import GoNode


def test_find_groups_one_group():
    # GIVEN
    board_state = [
        ["+", "+", "+", "+"],
        ["+", "●", "●", "+"],
        ["+", "+", "+", "+"],
        ["+", "+", "+", "+"],
    ]

    # WHEN
    actual = find_groups(board_state)

    # THEN
    expected = [[(1, 1), (1, 2)]]
    assert expected == actual


# TODO implement this logic in code
@pytest.mark.xfail
def test_find_groups_two_in_a_row():
    # GIVEN
    board_state = [
        ["+", "+", "+", "+", "+", "+"],
        ["+", "●", "●", "+", "●", "+"],
        ["+", "+", "+", "+", "+", "+"],
        ["+", "+", "+", "+", "+", "+"],
    ]

    # WHEN
    actual = find_groups(board_state)

    # THEN
    expected = [[(1, 1), (1, 2)], [(1, 4)]]
    assert expected == actual


# TODO implement this logic in code
@pytest.mark.xfail
def test_find_groups_many_rows():
    # GIVEN
    board_state = [
        ["+", "+", "+", "+", "+", "+"],
        ["+", "●", "●", "+", "●", "+"],
        ["+", "+", "+", "+", "+", "+"],
        ["+", "●", "●", "+", "+", "+"],
    ]

    # WHEN
    actual = find_groups(board_state)

    # THEN
    expected = [[(1, 1), (1, 2)], [(1, 4)], [(3, 1), (3, 2)]]
    assert expected == actual


def test_find_groups_one_column():
    # GIVEN
    board_state = [["+", "+", "+"], ["+", "●", "+"], ["+", "●", "+"], ["+", "+", "+"]]

    # WHEN
    actual = find_groups(board_state)

    # THEN
    expected = [[(1, 1), (2, 1)]]
    assert expected == actual


def test_transpose_board():
    # GIVEN
    board_state = [["●", "+", "+"], ["●", "+", "+"], ["+", "+", "+"]]

    # WHEN
    actual = transpose_board(board_state)

    # THEN
    expected = [["●", "●", "+"], ["+", "+", "+"], ["+", "+", "+"]]
    assert expected == actual


def test_find_groups_in_row_one_group():
    # GIVEN
    row = ["+", "●", "●", "+"]

    # WHEN
    actual = find_groups_in_row(row, 0)

    # THEN
    expected = [[(0, 1), (0, 2)]]
    assert expected == actual


def test_find_groups_in_row_two_groups():
    # GIVEN
    row = ["+", "●", "●", "+", "●"]

    # WHEN
    actual = find_groups_in_row(row, 0)

    # THEN
    expected = [[(0, 1), (0, 2)], [(0, 4)]]
    assert expected == actual


def test_find_groups_in_row_three_groups():
    # GIVEN
    row = [
        "+",
        "●",
        "●",
        "+",
        "●",
        "+",
        "●",
        "●",
        "●",
        "+",
    ]

    # WHEN
    actual = find_groups_in_row(row, 0)

    # THEN
    expected = [[(0, 1), (0, 2)], [(0, 4)], [(0, 6), (0, 7), (0, 8)]]
    assert expected == actual


def test_find_all_moves():
    # GIVEN
    board_state = [
        ["+", "+", "+", "+", "+", "+"],
        ["+", "●", "●", "+", "●", "+"],
        ["+", "+", "+", "+", "+", "+"],
        ["+", "●", "●", "+", "+", "+"],
    ]

    # WHEN
    actual = find_all_moves(board_state)

    # THEN
    expected = [(1, 1), (1, 2), (1, 4), (3, 1), (3, 2)]
    assert expected == actual


def test_get_row_score():
    # GIVEN
    row = ["+", "+", "+"]

    # WHEN
    actual = get_row_score(row, BLACK_STONE)

    # THEN
    expected = 0
    assert expected == actual


def test_get_row_score_one():
    # GIVEN
    row = ["●", "+", "+"]

    # WHEN
    actual = get_row_score(row, BLACK_STONE)

    # THEN
    expected = 1
    assert expected == actual


def test_get_row_score_one_but_two_stones():
    # GIVEN
    row = ["●", "+", "●"]

    # WHEN
    actual = get_row_score(row, BLACK_STONE)

    # THEN
    expected = 1
    assert expected == actual


def test_get_row_score_two_groups():
    # GIVEN
    row = ["●", "+", "●", "●"]

    # WHEN
    actual = get_row_score(row, BLACK_STONE)

    # THEN
    expected = 2
    assert expected == actual


def test_get_row_score_row_begins_and_ends_with_empty_space():
    # GIVEN
    row = ["+", "+", "●", "●", "+", "●", "●", "●", "+"]

    # WHEN
    actual = get_row_score(row, BLACK_STONE)

    # THEN
    expected = 3
    assert expected == actual


def test_list_all_moves_on_board():
    # WHEN
    board_size = 9
    all_moves = list_all_moves_on_board(board_size)
    actual = len(all_moves)

    # THEN
    expected = 81
    assert expected == actual

