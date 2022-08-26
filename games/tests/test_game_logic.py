from typing import Any
from games.game_logic import *
import pytest
from games.go_minimax_joiner import GoNode


def test_transpose_board():
    # GIVEN
    board_state = [["●", "+", "+"], ["●", "+", "+"], ["+", "+", "+"]]

    # WHEN
    actual = transpose_board(board_state)

    # THEN
    expected = [["●", "●", "+"], ["+", "+", "+"], ["+", "+", "+"]]
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


def test_find_moves_around_position():
    # GIVEN
    # board_state = [
    #     ["+", "+", "+"],
    #     ["+", "●", "+"],
    #     ["+", "+", "+"]
    # ]
    x_coordinate = 1
    y_coordinate = 1
    jump_size = 1

    # WHEN
    actual = find_moves_around_position(x_coordinate, y_coordinate, jump_size=jump_size)

    # THEN
    expected = [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (2, 1), (2, 0), (1, 0)]
    assert expected == actual


def test_find_moves_around_position():
    # GIVEN
    # board_state = [
    #     ["+", "+", "+", "+", "+"],
    #     ["+", "+", "+", "+", "+"],
    #     ["+", "+", "●", "+", "+"],
    #     ["+", "+", "+", "+", "+"],
    #     ["+", "+", "+", "+", "+"],
    # ]
    x_coordinate = 2
    y_coordinate = 2
    jump_size = 2

    # WHEN
    actual = find_moves_around_position(x_coordinate, y_coordinate, jump_size=jump_size)

    # THEN
    expected = [
        (0, 0),  # top_left
        (0, 1),
        (0, 2),
        (0, 3),
        (0, 4),  # top_right
        (1, 4),
        (2, 4),
        (3, 4),
        (4, 4),  # bottom_left
        (4, 3),
        (4, 2),
        (4, 1),
        (4, 0),  # bottom_right
        (3, 0),
        (2, 0),
        (1, 0),
    ]
    assert expected == actual

def test_choose_search_depth_1():
    # GIVEN
    open_moves = 24

    # WHEN
    actual = choose_search_depth(open_moves)

    # THEN
    expected = 4
    assert expected == actual

def test_choose_search_depth_2():
    # GIVEN
    open_moves = 22

    # WHEN
    actual = choose_search_depth(open_moves)

    # THEN
    expected = 5
    assert expected == actual

def test_choose_search_depth_3():
    # GIVEN
    open_moves = 2

    # WHEN
    actual = choose_search_depth(open_moves)

    # THEN
    expected = 2
    assert expected == actual

