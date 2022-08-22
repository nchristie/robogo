import logging
from .game_logic import *


logger = logging.getLogger(__name__)


class MinimaxNode:
    def __init__(self, node_id=None, score=None, player_to_move=None):
        self.node_id = node_id
        self.score = score
        self.player_to_move = player_to_move

    def __str__(self):
        return (
            f"node_id: {self.get_node_id()}, "
            f"player_to_move: {self.get_player_to_move()} "
        )

    def get_player_to_move(self):
        valid_options = ["maximizer", "minimizer"]
        player_to_move = self.player_to_move
        if player_to_move not in valid_options:
            raise Exception(
                f"Error for {self.node_id}, get_player_to_move returned invalid option: {player_to_move}"
            )
        return player_to_move

    def set_player_to_move(self, player_to_move):
        self.player_to_move = player_to_move

    def get_node_id(self):
        return self.node_id

    def find_utility(self):
        raise Exception(
            "In minimax find_utility, this should be implemented by class which inherits"
        )

    def make_node_id(self, depth, index, parent_node_id="NA"):
        """
        Creates a unique id for each move
        Returns (str):
        """
        return f"d{depth}-i{index}_{parent_node_id}"

    def alternate_player_to_move(self):
        """
        Returns:
            str: The opposite player_to_move to that of the current
            node. Valid options: "minimizer", "maximizer".
        """
        if self.player_to_move == "minimizer":
            return "maximizer"
        return "minimizer"


# Helpers
def minimax_with_alpha_beta_pruning_algorithm(
    parent,
    depth=MAX_TREE_DEPTH,
    winning_score=WINNING_SCORE,
):
    """
    Searches game tree to a given depth and calculates best next move
    using minimax and alpha-beta pruning

    Parameters:
        parent (MinimaxNode): the node from which we build down
        depth (int): how far down the tree we want to build
        node_ids (set): all the move ids which have been
            encountered so far
        winning_score: how many stones in a row constitutes a win

    Returns:
        object containing best score and best node
    """
    # Make sure we don't use same node twice
    parent_utility = parent.find_utility(winning_score=winning_score)

    raise_error_if_depth_less_than_zero(depth)

    # Base case
    # If we're at a leaf node leave the recursion
    # a leaf node is a node at full depth or a winning node
    if depth == 0 or is_win_state(parent, parent_utility):
        return {"best_score": parent_utility, "move_node": parent}

    alpha = -INFINITY
    beta = INFINITY
    player_to_move = parent.get_player_to_move()

    if player_to_move == "maximizer":
        best_score = LOWEST_SCORE
        func = max
    elif player_to_move == "minimizer":
        best_score = HIGHEST_SCORE
        func = min

    # recurse case
    for child in parent.generate_next_child_and_rank_by_proximity(
        depth=depth, parent_node_id=parent.get_node_id()
    ):
        # **************************************************************************
        # use recursion to build tree vertically
        res = minimax_with_alpha_beta_pruning_algorithm(child, depth - 1, winning_score=winning_score)
        best_score = func(
            res["best_score"],
            best_score,
        )

        if res["best_score"] == best_score:
            best_node = child
        # **************************************************************************

        # To get to this stage we've:
        # 1. reached the end of depth count-down
        # or
        # 2. encountered a win state
        # This means first we'll get to the point we want to stop building vertically
        # and then evaluate children at this level. Once all children are evaluated
        # or a break condition is met we will work
        # back up the tree and add child nodes at higher levels

        # set alpha and beta
        if player_to_move == "maximizer":
            alpha = func(best_score, alpha)
        elif player_to_move == "minimizer":
            beta = func(best_score, beta)

        # break loop if beta <= alpha or win state encountered
        if break_conditions_are_met(alpha, beta):
            logger.debug(child.get_node_id())
            [logger.debug(row) for row in transpose_board(child.get_board_state())]
            break
    return {"best_score": best_score, "move_node": best_node}


def break_conditions_are_met(alpha, beta):
    prune_tree = alpha >= beta
    maximizer_win = alpha == HIGHEST_SCORE
    minimizer_win = beta == LOWEST_SCORE
    if prune_tree or maximizer_win or minimizer_win:
        logger.debug(
            f"alpha >= beta: {prune_tree}, alpha: {alpha}, beta: {beta}, maximizer_win: {maximizer_win}, minimizer_win: {minimizer_win}"
        )
    return prune_tree or maximizer_win or minimizer_win


def is_win_state(node, node_utility):
    if abs(node_utility) == HIGHEST_SCORE:
        winner = "Maximizer" if node_utility == HIGHEST_SCORE else "Minimizer"
        logger.debug(f"{winner} win found at: {node.get_node_id()}")
        return True
    return False


def raise_error_if_depth_less_than_zero(depth):
    if depth < 0:
        raise Exception(f"Maximum tree depth exceeded")
