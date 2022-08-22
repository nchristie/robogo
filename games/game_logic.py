from .stones import EMPTY_POSITION, BLACK_STONE, WHITE_STONE
import logging

logger = logging.getLogger(__name__)

BOARD_SIZE = 5
WINNING_SCORE = 4
MAX_TREE_DEPTH = 5

INFINITY = float("inf")

HIGHEST_SCORE = 100
LOWEST_SCORE = -HIGHEST_SCORE


def is_move_valid(board_state, move_coordinates):
    checks = [is_move_within_board_boundaries, is_move_in_free_position]
    for check in checks:
        if not check(board_state, move_coordinates):
            return False
    return True


def is_move_within_board_boundaries(board_state, move_coordinates):
    board_size = len(board_state[0])
    for coordinate in move_coordinates:
        if (coordinate >= board_size) or (coordinate < 0):
            return False
    return True


def is_move_in_free_position(board_state, move_coordinates):
    x_coordinate = move_coordinates[0]
    y_coordinate = move_coordinates[1]
    if board_state[x_coordinate][y_coordinate] != EMPTY_POSITION:
        return False
    return True


# TODO won't cause own group to be captured
def move_not_self_capture(board_state, move_coordinates):
    return


# TODO doesn't bring board back to prior state (ko rule)
def move_doesnt_violate_ko_rule():
    return


# TODO find all groups on board
def find_groups(board_state):
    return


def transpose_board(board_state):
    board_size = get_board_size(board_state)
    transposed_board = []
    for i in range(board_size):
        transposed_board.append([])
        for j in range(board_size):
            transposed_board[i].append("+")

    for i in range(board_size):
        for j in range(board_size):
            old_board_move = board_state[i][j]
            transposed_board[j][i] = old_board_move
    return transposed_board


def list_all_moves_on_board(board_size):
    all_moves = []
    for x in range(board_size):
        for y in range(board_size):
            move = (x, y)
            all_moves.append(move)
    return all_moves


def get_board_size(board_state):
    return len(board_state[0])


def get_score_dict(board_state):
    score_dict = {WHITE_STONE: 0, BLACK_STONE: 0, "relative_black_score": 0}
    # first check if there's a string of stones to the right, and if so add up score
    score_dict = get_scores_by_row(board_state, score_dict)

    # then check if there's a string of stones below and add up score
    score_dict = get_scores_by_row(board_state, score_dict, should_transpose_board=True)

    # update relative black score
    score_dict["relative_black_score"] = (
        score_dict[BLACK_STONE] - score_dict[WHITE_STONE]
    )

    return score_dict


def get_scores_by_row(board_state, score_dict, should_transpose_board=False):
    board = board_state
    if should_transpose_board:
        board = transpose_board(board_state)
    for row in board:
        # compare score to max score and replace if it's higher,
        white_score = get_row_score(row, WHITE_STONE)
        black_score = get_row_score(row, BLACK_STONE)
        if white_score > score_dict[WHITE_STONE]:
            score_dict[WHITE_STONE] = white_score
        if black_score > score_dict[BLACK_STONE]:
            score_dict[BLACK_STONE] = black_score
    return score_dict


def get_row_score(row, stone_colour):
    row_score = [0 for x in row]
    score_count = 0
    for cell in row:
        if cell == stone_colour:
            row_score[score_count] += 1
        else:
            score_count += 1
    return max(row_score)


def find_moves_around_position(x_coordinate, y_coordinate, jump_size=1):
    moves_around_position = []
    distance = jump_size * 2

    top_row_x_coordinate = x_coordinate - jump_size
    leftmost_y_coordinate = y_coordinate - jump_size
    rightmost_y_coordinate = y_coordinate + jump_size
    bottom_row_x_coordinate = x_coordinate + jump_size

    # find all coordinates between top_left (incl) and top_right (excl)
    for i in range(distance):
        moves_around_position.append((top_row_x_coordinate, leftmost_y_coordinate + i))

    # find all coordinates between top_right (incl) and bottom_right (excl)
    for i in range(distance):
        moves_around_position.append((top_row_x_coordinate + i, rightmost_y_coordinate))

    # find all coordinates between bottom_right (incl) and bottom_left (excl)
    for i in range(distance):
        moves_around_position.append(
            (bottom_row_x_coordinate, rightmost_y_coordinate - i)
        )

    # find all coordinates between bottom_left (incl) and top_left (excl)
    for i in range(distance):
        moves_around_position.append(
            (bottom_row_x_coordinate - i, leftmost_y_coordinate)
        )

    return moves_around_position
