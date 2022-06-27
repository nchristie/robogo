from .stones import EMPTY_POSITION
from copy import deepcopy

def is_move_valid(board_state, move_coordinates):
    checks = [
        is_move_within_board_boudaries,
        is_move_in_free_position
    ]
    for check in checks:
        if not check(board_state, move_coordinates):
            return False
    return True
    
def is_move_within_board_boudaries(board_state, move_coordinates):
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
    return True

def find_all_moves(board_state):
    moves = []
    for i, row in enumerate(board_state):
        for j, stone_colour in enumerate(row):
            coordinates = (i,j)
            contains_stone = stone_colour != EMPTY_POSITION
            if contains_stone:
                moves.append(coordinates)
    return moves


# TODO find all groups on board
def find_groups(board_state):
    moves = find_all_moves(board_state)
    groups = []

    for move in moves:
        group = [move]
        intersections = find_intersecting_positions(move)
        for intersection in intersections:
            if intersection in moves:
                group.append(intersection)
                moves.remove(intersection)
        groups.append(group)
        moves.remove(move)
        
    return groups

def find_groups_in_row(row, row_index, is_transposed=False):
    groups = []
    group = []
    for i, stone_colour in enumerate(row):
        contains_stone = stone_colour != EMPTY_POSITION
        if contains_stone:
            if is_transposed:
                group.append((i, row_index))
            else:
                group.append((row_index, i))
        else:
            if group != []:
                groups.append(group)
                group = []
    if group:
        groups.append(group)
    return groups


# TODO doesn't bring board back to prior state (ko rule)

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

def get_board_size(board_state):
    return len(board_state[0])

def find_intersecting_positions(position):
    x_coordinate = position[0]
    y_coordinate = position[1]
    up = (x_coordinate - 1, y_coordinate)
    left = (x_coordinate, y_coordinate - 1)
    right = (x_coordinate, y_coordinate + 1)
    down = (x_coordinate + 1, y_coordinate)
    return [up, left, right, down]
