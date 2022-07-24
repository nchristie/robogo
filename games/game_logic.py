from .stones import EMPTY_POSITION, BLACK_STONE, WHITE_STONE
import logging

logger = logging.getLogger(__name__)

WINNING_SCORE = 5
MAX_TREE_DEPTH = 5

PLUS_INF = float("inf")
MINUS_INF = -float("inf")

INITIAL_OPTIMAL_VALUES = {"maximizer": MINUS_INF, "minimizer": PLUS_INF}


def is_move_valid(board_state, move_coordinates):
    checks = [is_move_within_board_boudaries, is_move_in_free_position]
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


# TODO doesn't bring board back to prior state (ko rule)
def move_doesnt_violate_ko_rule():
    return


def find_all_moves(board_state):
    moves = []
    for i, row in enumerate(board_state):
        for j, stone_colour in enumerate(row):
            coordinates = (i, j)
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


def find_intersecting_positions(position):
    x_coordinate = position[0]
    y_coordinate = position[1]
    up = (x_coordinate - 1, y_coordinate)
    left = (x_coordinate, y_coordinate - 1)
    right = (x_coordinate, y_coordinate + 1)
    down = (x_coordinate + 1, y_coordinate)
    return [up, left, right, down]


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


def find_depth_recursive(node, depth):
    if depth > MAX_TREE_DEPTH:
        raise Exception(f"Maximum tree depth of {MAX_TREE_DEPTH} exceeded")

    # Base case
    # If we're at a terminal node leave the recursion
    if node.is_leaf_node():
        logger.debug(f"child {type(node)}")
        logger.debug(
            f"depth: {depth}, move_id: {node.move_id} is_leaf_node: {node.is_leaf_node()}"
        )
        logger.debug(f"returning at depth of {depth} owing to terminal node")
        return depth

    # recurse case
    for i, child in enumerate(node.children):
        logger.debug(
            f"depth: {depth}, child index: {i}, move_id: {child.move_id} is_leaf_node: {child.is_leaf_node()}, child {type(child)}"
        )
        return find_depth_recursive(child, depth + 1)

    logger.debug(f"Returning because end of function depth {depth}")
    return


def find_depth_iterative(node, max_depth):
    # Source: https://stackoverflow.com/questions/71846315/depth-limited-dfs-general-non-binary-tree-search
    stack = [(node, 0)]
    visited = set()
    while stack:
        node, node_depth = stack.pop()
        if node in visited:
            continue
        visited.add(node)

        # Any other processing for this node comes here
        if node.is_leaf_node():
            return node_depth

        if node_depth < max_depth:
            for child in reversed(node.children):
                stack.append((child, node_depth + 1))
    return node_depth


# TODO this function should be removable once alpha-beta
# function works
def build_game_tree_recursive(node, depth, board_states):
    """
    Starts from current node and builds game tree to a given
    depth

    Parameters:
        depth (int): how far down the tree we want to build
    """
    logger.debug(f"In build_game_tree_recursive, {node.move_id} {depth}")
    logger.debug(node.board_state)

    board_states.add(str(node.board_state))

    if depth < 0:
        raise Exception(f"Maximum tree depth exceeded")

    # Base case
    # If we're at a terminal node leave the recursion
    if depth == 0:
        logger.debug(f"Returning at depth of {depth}")
        assert (
            not node.children
        ), f"Node at depth 0 shouldn't have children move_id: {node.move_id}, board_state: {node.board_state}, number of children: {len(node.children)}"
        return

    # recurse case
    for child in node.generate_next_child(depth):
        if str(child.board_state) in board_states:
            continue
        # use recursion to build tree vertically

        # TODO s/ with following line
        if node.children == None:
            node.children = []
        if child.children == None:
            child.children = []
        if not build_game_tree_recursive(child, depth - 1, board_states):

            # not build_game_tree_recursive(..) will be True if we've reached the end of
            # depth count-down or if we've visited every potential child node horizontally,
            # so this means first we'll get to the point we want to stop building and add
            # children, then work back up the tree and add child nodes

            # build tree horizontally
            logger.debug(f"Appending nodes at depth of {depth}")
            node.children.append(child)
            logger.debug(f"number of children: {len(node.children)}")

    logger.debug("Returning at end of function")
    return

def evaluate(node, depth, board_states, alpha, beta):
    """
    Starts from current node and builds game tree to a given
    depth then returns the best next move using the information
    gathered. Only builds branches which have optimal game moves

    Parameters:
        depth (int): how far down the tree we want to build
        board_states (set): all the board states which have been
            encountered so far
        alpha (int): best score from perspective of
            maximizing player
        beta (int): best score from perspective of
            minimizing player

    Returns:
        best available score

    Side effects:
        - builds tree from root node
        - applies scores at leaves, and inheritance of those
            scores up the tree
    """
    logger.debug(
        f"In evaluate, node: {node.move_id} depth: {depth}, player: {node.player}"
    )

    board_states.add(str(node.board_state))

    if depth < 0:
        e = f"Maximum tree depth exceeded at node: {node.move_id}"
        logger.error(e)
        raise Exception(e)

    # Base case
    # If we're at a terminal node leave the recursion
    if depth == 0:
        assert (
            not node.children
        ), f"Node at depth 0 shouldn't have children move_id: {node.move_id}, number of children: {len(node.children)}"

        node.set_score(node.get_utility())

        logger.debug(
            f"Returning at depth of {depth} with score of {node.get_score()} at node: {node.move_id}"
        )
        return node.get_score()

    # recurse case

    if node.children == None:
        e = f"Node {node.move_id} children == None, all nodes should be initialised with children of []"
        logger.error(e)
        raise Exception(e)

    # optimal_value = INITIAL_OPTIMAL_VALUES[node.player]
    for child in node.generate_next_child(depth):
        # Don't add board states which have already been visited
        if str(child.board_state) in board_states:
            logger.debug("Board state already seen, skipping this node")
            continue

        # TODO if child score is a winning score then don't build
        # branches further

        # use recursion to build tree vertically

        # TODO what value should the node have?
        # node.set_score(value)
        func, alpha_or_beta = apply_strategy(node.player, alpha, beta)
        best_score = func(alpha_or_beta, evaluate(child, depth - 1, board_states, alpha, beta))
        if node.player == "maximizer":
            alpha = best_score
            logger.debug(f"alpha set to {alpha}")
        if node.player == "minimizer":
            beta = best_score
            logger.debug(f"beta set to {beta}")
        if beta <= alpha:
            logger.debug(
                f"Breakpoint reached for {node.player} alpha: {alpha}, beta: {beta}, node score: {best_score}, node id: {node.move_id}"
            )
            # build tree horizontally
            logger.debug(
                f"Appending child node {child.move_id} with score of {child.get_score()} to parent node {node.move_id} at depth of {depth}"
            )
            node.children.append(child)
            node.set_score(best_score)
            return best_score

        # build tree horizontally
        logger.debug(
            f"Appending child node {child.move_id} to parent node {node.move_id} at depth of {depth}"
        )
        node.children.append(child)
        node.set_score(best_score)
        return best_score
    raise Exception("Reached end of evaluate function without returning")


def get_optimal_value(old_optimal_value, new_value, player):
    if player == "minimizer":
        return min(old_optimal_value, new_value)
    if player == "maximizer":
        return max(old_optimal_value, new_value)


def get_best_next_move(node, best_score):
    for child in node.children:
        if child.get_score() == best_score:
            return child
    raise Exception(f"Best score: {best_score} not found in children of node: {node.move_id} whose children are: {[child.get_score() for child in node.children]}")

def apply_strategy(player, alpha, beta):
    strategy_dict = {
        "maximizer": max,
        "minimizer": min
    }
    player_dict = {
        "maximizer": alpha,
        "minimizer": beta
    }

    return (strategy_dict[player], player_dict[player])
