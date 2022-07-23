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


def test_build_game_tree_recursive_depth():
    # GIVEN
    player = "maximizer"
    game_tree_node_3 = GoNode(
        move_id="root_node",
        player=player,
        board_state=[["●", "+"], ["+", "+"]],
    )

    node_3_depth = 3
    # hack to get around suspected test pollution
    game_tree_node_3.children = []
    build_game_tree_recursive(game_tree_node_3, node_3_depth, set())

    # WHEN
    actual = game_tree_node_3.children[0].children[0].children[0].children

    # THEN
    expected = []
    assert expected == actual


def test_find_depth_recursive():
    # GIVEN
    player = "maximizer"
    game_tree_node_1 = GoNode(
        move_id="root_node",
        player=player,
        board_state=[["●", "+", "+"], ["+", "+", "+"], ["+", "+", "+"]],
    )

    node_1_depth = 4
    # hack to get around suspected test pollution
    game_tree_node_1.children = []
    build_game_tree_recursive(game_tree_node_1, node_1_depth, set())

    # WHEN
    # actual = game_tree_node_1.children[0].children[0].children[0].children

    # # # THEN
    # expected = []
    # assert expected == actual

    actual = find_depth_recursive(game_tree_node_1, 0)
    expected = node_1_depth
    assert expected == actual


@pytest.mark.skip("WIP")
def test_evaluate_node():
    # GIVEN
    board_state = [
        ["+", "○", "○", "○", "○", "+", "+", "+", "+"],
        ["+", "+", "+", "+", "+", "●", "+", "+", "+"],
        ["+", "+", "+", "+", "+", "●", "+", "+", "+"],
        ["+", "+", "+", "+", "+", "●", "+", "+", "+"],
        ["+", "+", "+", "+", "+", "●", "+", "+", "+"],
        ["+", "+", "+", "+", "+", "○", "+", "+", "+"],
        ["+", "+", "+", "+", "+", "+", "+", "+", "+"],
        ["+", "+", "+", "+", "+", "+", "+", "+", "+"],
        ["+", "+", "+", "+", "+", "+", "+", "+", "+"],
    ]
    root_node = GoNode(move_id="root_node", player="black", board_state=board_state)

    depth = 2

    maximizer_choice_node = GoNode(
        move_id="dummy_node_maximizer",
        player="minimizer",
        score=-float("inf"),
        children=[],
        board_state=board_state,
    )

    minimizer_choice_node = GoNode(
        move_id="dummy_node_minimizer",
        player="minimizer",
        score=float("inf"),
        children=[],
        board_state=board_state,
    )

    # WHEN
    actual = root_node.evaluate_node(
        root_node, maximizer_choice_node, minimizer_choice_node, depth
    ).optimal_move

    # THEN
    expected = (0, 5)
    assert expected == actual


def test_evaluate_assigns_scores():
    # GIVEN
    player = "maximizer"
    game_tree_node_3 = GoNode(
        move_id="root_node",
        player=player,
        board_state=[["●", "●"], ["+", "+"]],
    )

    node_3_depth = 0
    alpha, beta = MINUS_INF, PLUS_INF
    # hack to get around suspected test pollution
    game_tree_node_3.children = []
    evaluate(game_tree_node_3, node_3_depth, set(), alpha, beta)

    # WHEN
    actual = game_tree_node_3.get_score()

    # THEN
    expected = 2
    assert expected == actual


def test_evaluate_assigns_scores_based_on_leaves():
    # GIVEN
    player = "maximizer"
    game_tree_node_3 = GoNode(
        move_id="root_node",
        player=player,
        board_state=[["●", "●"], ["+", "+"]],
    )

    node_3_depth = 1
    alpha, beta = MINUS_INF, PLUS_INF
    # hack to get around suspected test pollution
    game_tree_node_3.children = []
    evaluate(game_tree_node_3, node_3_depth, set(), alpha, beta)

    # WHEN
    actual = game_tree_node_3.get_score()

    # THEN
    expected = 2
    assert expected == actual
