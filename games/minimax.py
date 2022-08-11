import logging
from .game_logic import INFINITY, WINNING_SCORE, HIGHEST_SCORE, LOWEST_SCORE

logger = logging.getLogger(__name__)

MAX_TREE_DEPTH = 6


class MinimaxNode:
    def __init__(
        self,
        node_id=None,
        score=None,
        children=[],
        player_to_move=None,
    ):
        self.children = children
        self.node_id = node_id
        self.score = score
        self.player_to_move = player_to_move

    def __str__(self):
        return (
            f"node_id: {self.get_node_id()}, "
            f"score: {self.get_score()}, "
            f"number of children: {len(self.get_children())}, "
            f"player_to_move: {self.get_player_to_move()}"
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
            raise Exception(e)
        return self.score

    def get_node_id(self):
        return self.node_id

    def get_short_node_id(self):
        # TODO test
        return self.get_node_id().split("_")[0]

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
        # input is Node, output is Node
        if not self.children:
            raise Exception(
                f"get_optimal_move error for {self.get_node_id()}: node has no children {[child for child in self.children]}"
            )
        best_move = self.children[0]
        player_to_move = self.player_to_move
        best_score = best_move.get_score()

        strategy = self.maximizer_strategy
        if player_to_move == "minimizer":
            strategy = self.minimizer_strategy

        for child in self.children:
            child_score = child.get_score()
            if strategy(child_score, best_score):
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

    def build_and_prune_game_tree_recursive(
        self,
        parent,
        depth,
        node_ids=set(),
        winning_score=WINNING_SCORE,
    ):
        """
        Builds game tree to a given depth

        Parameters:
            parent (MinimaxNode): the node from which we build down
            depth (int): how far down the tree we want to build
            node_ids (set): all the move ids which have been
                encountered so far

        Returns:
            None

        Side effects:
            builds tree from parent
        """
        # Make sure we don't use same node twice
        parent_node_id = parent.get_node_id()
        node_ids.add(parent_node_id)

        parent_utility = parent.find_utility(winning_score=winning_score)

        raise_error_if_depth_less_than_zero(depth)

        # Base case
        # If we're at a leaf node leave the recursion
        # a leaf node is a node at full depth or a winning node
        if depth == 0 or is_win_state(parent, parent_utility):
            raise_error_if_node_has_children(
                parent, depth, message="Leaf nodes shouldn't have children"
            )
            parent.set_score(parent_utility)

            logger.debug(
                f"Returning at depth of {depth} with score of {parent_utility} at node: {parent_node_id}"
            )
            return parent_utility


        alpha = -INFINITY
        beta = INFINITY
        player_to_move = parent.get_player_to_move()

        if player_to_move == "maximizer":
            best_score = -INFINITY
            func = max
        elif player_to_move == "minimizer":
            best_score = INFINITY
            func = min

        # recurse case
        for child in parent.generate_next_child(depth, parent_node_id):
            child_node_id = child.get_node_id()
            raise_error_if_node_has_children(
                child, depth, message="Nodes should initialise without children"
            )

            # Make sure we don't use same node twice
            if node_already_visited(child_node_id, node_ids):
                continue

            # TODO don't build breadth or depth beyond win state

            # **************************************************************************
            # use recursion to build tree vertically
            best_score = func(self.build_and_prune_game_tree_recursive(
                child, depth - 1, node_ids, winning_score=winning_score
            ), best_score)
            # **************************************************************************

            # to get to this stage:
            # 1. we've reached the end of depth count-down
            # This means first we'll get to the point we want to stop building vertically
            # and then add children at this level. Once all children are added we will work
            # back up the tree and add child nodes at higher levels

            # build tree horizontally
            parent.add_child(child)
            parent.set_score(best_score)

            # set alpha and beta
            if player_to_move == "maximizer":
                alpha = func(best_score, alpha)
            elif player_to_move == "minimizer":
                beta = func(best_score, beta)

            # break loop if beta <= alpha
            if break_conditions_are_met(alpha, beta):
                logger.info(
                    f"Breaking at {parent.get_node_id()}"
                )
                break

        logger.debug(
            f"Returning at end of function {parent_node_id} alpha, beta: {(alpha, beta)}"
        )
        return best_score

    def find_depth_recursive(self, node, depth):
        if depth > MAX_TREE_DEPTH:
            raise Exception(f"Maximum tree depth of {MAX_TREE_DEPTH} exceeded")

        # Base case
        # If we're at a terminal node leave the recursion
        if node.is_leaf_node():
            logger.debug(f"child {type(node)}")
            logger.debug(
                f"depth: {depth}, node_id: {node.get_node_id()} is_leaf_node: {node.is_leaf_node()}"
            )
            logger.debug(f"returning at depth of {depth} owing to terminal node")
            return depth

        # recurse case
        for i, child in enumerate(node.children):
            logger.debug(
                f"depth: {depth}, child index: {i}, node_id: {child.get_node_id()} is_leaf_node: {child.is_leaf_node()}, child type: {type(child)}"
            )
            return self.find_depth_recursive(child, depth + 1)

        logger.debug(f"Returning because end of function depth {depth}")
        return


# Helpers
def get_depth_from_node_id(node_id):
    return str(node_id).split("-")[0]


def break_conditions_are_met(alpha, beta):
    prune_tree = alpha >= beta
    maximizer_win = alpha == HIGHEST_SCORE
    minimizer_win = beta == LOWEST_SCORE
    if prune_tree or maximizer_win or minimizer_win:
        logger.info(f"alpha >= beta: {prune_tree}, alpha: {alpha}, beta: {beta}, maximizer_win: {maximizer_win}, minimizer_win: {minimizer_win}")
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
