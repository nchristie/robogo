def is_move_valid(board_state, move_coordinates):
    checks = [
        is_move_within_board_boudaries
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

# TODO isn't where there's already a piece


# TODO won't cause own group to be captured

# TODO doesn't bring board back to prior state (ko rule)

