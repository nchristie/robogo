import logging
from .game_logic import *
import itertools

logger = logging.getLogger(__name__)


class MinimaxNode:
    def __init__(
        self, node_id=None, score=None, children=[], player_to_move=None, path_depth=0
    ):
        self.children = children
        self.node_id = node_id
        self.score = score
        self.player_to_move = player_to_move
        self.path_depth = path_depth

    def __str__(self):
        return (
            f"node_id: {self.get_node_id()}, "
            # f"score: {self.get_score()}, "
            f"number of children: {len(self.get_children())}, "
            f"player_to_move: {self.get_player_to_move()} "
            f"path_depth:  {self.path_depth}"
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

    def set_score(self, score):
        logger.debug(f"In set_score for node: {self.get_node_id()}, score: {score}")
        if type(score) not in [int, float]:
            raise Exception(
                f"set_score error: score must be int or float got {type(score)} for node: {self.get_node_id()}"
            )
        self.score = score

    def get_score(self):
        if not self.score and self.score != 0:
            e = f"Score has not been set for node {self.get_node_id()}"
            logger.error(e)
            # raise Exception(e)
        return self.score

    def get_node_id(self):
        return self.node_id

    def get_short_node_id(self):
        # TODO test
        return self.get_node_id().split("_")[0]

    def get_path_depth(self):
        return self.path_depth

    def set_path_depth(self, depth):
        self.path_depth = depth

    def add_child(self, child):
        child_depth = get_depth_from_node_id(child.get_node_id())
        parent_depth = get_depth_from_node_id(self.get_node_id())
        if child_depth == parent_depth:
            raise Exception(
                f"Attempt to append two nodes at same depth: child_depth: {child_depth}, parent_depth: {parent_depth}"
            )
        logger.debug(f"add_child {child.get_node_id()} to parent {self.get_node_id()}")
        self.children.append(child)

    def get_children(self):
        return self.children

    def get_optimal_move(self):
        # output is Node
        if not self.children:
            raise Exception(
                f"get_optimal_move error for {self.get_node_id()}: node has no children {[child for child in self.children]}"
            )
        best_move = self.children[0]
        player_to_move = self.player_to_move
        best_score = best_move.get_score()
        best_path_depth = best_move.get_path_depth()

        strategy = self.maximizer_strategy
        if player_to_move == "minimizer":
            strategy = self.minimizer_strategy

        for child in self.children:
            child_score = child.get_score()
            child_path_depth = child.get_path_depth()
            if player_to_move == "maximizer" and child_score == HIGHEST_SCORE:
                best_move = child
            if player_to_move == "minimizer" and child_score == LOWEST_SCORE:
                best_move = child
            elif minimizer_is_on_losing_path(player_to_move, child_score, best_score):
                if child_path_depth < best_path_depth:
                    best_path_depth = child_path_depth
                    best_move = child
            elif strategy(child_score, best_score):
                best_move = child
                best_score = best_move.get_score()
        return best_move

    def maximizer_strategy(self, child_score, best_score):
        return child_score > best_score

    def minimizer_strategy(self, child_score, best_score):
        return child_score < best_score

    def find_utility(self):
        raise Exception(
            "In minimax find_utility, this should be implemented by class which inherits"
        )

    def generate_next_child(self, depth, parent_node_id="NA"):
        raise Exception(
            f"In minimax generate_next_child, this should be implemented by class which inherits depth: {depth} parent_node_id: {parent_node_id}"
        )

    def is_leaf_node(self):
        # logger.debug(f"Checking if leaf node, number of children = {len(self.children)}, node_id = {self.get_node_id()}")
        return not self.children

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


class MinimaxTree:
    def __init__(self, root_node):
        self.root_node = root_node

    def prune_game_tree_recursive(
        self,
        parent,
        depth=MAX_TREE_DEPTH,
        winning_score=WINNING_SCORE,
    ):
        """
        Builds game tree to a given depth

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
        for child in parent.generate_next_child_and_rank_by_proximity(depth=depth):
            # **************************************************************************
            # use recursion to build tree vertically
            res = self.prune_game_tree_recursive(
                child, depth - 1, winning_score=winning_score
            )
            best_score = func(
                res["best_score"],
                best_score,
            )

            if res["best_score"] == best_score:
                best_node = child
            # **************************************************************************

            # to get to this stage:
            # 1. we've reached the end of depth count-down
            # This means first we'll get to the point we want to stop building vertically
            # and then add children at this level. Once all children are added we will work
            # back up the tree and add child nodes at higher levels

            # set alpha and beta
            if player_to_move == "maximizer":
                alpha = func(best_score, alpha)
            elif player_to_move == "minimizer":
                beta = func(best_score, beta)

            # break loop if beta <= alpha
            if break_conditions_are_met(alpha, beta):
                break
        return {"best_score": best_score, "move_node": best_node}


# Helpers
def get_depth_from_node_id(node_id):
    return str(node_id).split("-")[0]


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


def raise_error_if_node_has_children(node, depth, message=""):
    if node.children != []:
        e = f"{message}. Node at depth {depth} shouldn't have children node_id: {node.get_node_id()}, number of children: {len(node.children)} first child id: {node.children[0].get_node_id()}"
        logger.error(e)
        raise Exception(e)


def raise_error_if_depth_less_than_zero(depth):
    if depth < 0:
        raise Exception(f"Maximum tree depth exceeded")


def node_already_visited(node_id, node_ids):
    # Make sure we don't use same node twice
    if node_id in node_ids:
        logger.debug(f"node_id: {node_id} already visited, skipping")
        return True


def minimizer_is_on_losing_path(player_to_move, child_score, best_score):
    return (
        player_to_move == "minimizer"
        and child_score == HIGHEST_SCORE
        and child_score == best_score
    )
