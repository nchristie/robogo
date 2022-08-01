import logging
from .game_logic import INFINITY

logger = logging.getLogger(__name__)

MAX_TREE_DEPTH = 5


class MinimaxNode:
    def __init__(
        self,
        node_id=None,
        player=None,
        score=None,
        children=[],
        alpha=-INFINITY,
        beta=INFINITY,
    ):
        self.children = children
        self.node_id = node_id
        self.player = player
        self.score = score
        self.alpha = alpha
        self.beta = beta

    def __str__(self):
        return (
            f"node_id: {self.get_node_id()}, "
            f"score: {self.get_score()}, "
            f"number of children: {len(self.get_children())}"
        )

    def get_player(self):
        return self.player

    def set_score(self, score):
        logger.debug(f"In set_score for node: {self.node_id}, score: {score}")
        if type(score) not in [int, float]:
            raise Exception(
                f"set_score error: score must be int or float got {type(score)} for node: {self.node_id}"
            )
        self.score = score

    def get_score(self):
        if not self.score and self.score != 0:
            e = f"Score has not been set for node {self.node_id}"
            logger.error(e)
            raise Exception(e)
        return self.score

    def get_node_id(self):
        return self.node_id

    def add_child(self, child):
        child_depth = get_depth_from_node_id(child.node_id)
        parent_depth = get_depth_from_node_id(self.node_id)
        if child_depth == parent_depth:
            raise Exception(
                f"Attempt to append two nodes at same depth: child_depth: {child_depth}, parent_depth: {parent_depth}"
            )
        logger.debug(f"add_child {child.node_id} to parent {self.node_id}")
        self.children.append(child)

    def get_children(self):
        return self.children

    def get_optimal_move(self):
        # input is Node, output is Node
        if not self.children:
            raise Exception(
                f"get_optimal_move error for {self.node_id}: node has no children"
            )
        best_move = self.children[0]
        player = best_move.player
        best_score = best_move.get_score()

        strategy = self.maximizer_strategy
        if player == "minimizer":
            strategy = self.minimizer_strategy

        for child in self.children:
            child_score = child.get_score()
            if strategy(child_score, best_score):
                best_move = child
                best_score = best_move.get_score()
        logger.debug(f"get_optimal_move player = {player}, best_score: {best_score}")
        return best_move

    def maximizer_strategy(self, child_score, best_score):
        return child_score > best_score

    def minimizer_strategy(self, child_score, best_score):
        return child_score < best_score

    def get_utility(self):
        raise Exception(
            "In minimax get_utility, this should be implemented by class which inherits"
        )

    def generate_next_child(self, depth, parent_node_id="NA"):
        raise Exception(
            f"In minimax generate_next_child, this should be implemented by class which inherits depth: {depth}"
        )

    def is_leaf_node(self):
        # logger.debug(f"Checking if leaf node, number of children = {len(self.children)}, node_id = {self.node_id}")
        return not self.children

    def make_node_id(self, depth, index, parent_node_id="NA"):
        """
        Creates a unique id for each move
        Returns (str):
        """
        # Can comment out the following line if we want to debug where a node came from
        parent_node_id = parent_node_id.split("_")[0]
        return f"d{depth}-i{index}_p{parent_node_id}"

    def alternate_player(self):
        """
        Returns:
            str: The opposite player to that of the current
            node. Valid options: "minimizer", "maximizer".
        """
        if self.player == "minimizer":
            return "maximizer"
        return "minimizer"

    def set_alpha_beta(self, alpha=-INFINITY, beta=INFINITY):
        self.alpha = alpha
        self.beta = beta

    def get_alpha_beta(self):
        return self.alpha, self.beta

    def calculate_alpha_and_beta(self, alpha=-INFINITY, beta=INFINITY):
        """
        Takes the highest and lowest scores seen so far, and compares with the current node score
        and updates alpha or beta depending on whether this node is a maximizer or minimizer

        Parameters:
            node (MinimaxNode): a node to check against running scores
            alpha (int or float): highest score seen so far
            beta (int or float): lowest score seen so far

        Returns:
            alpha, beta: as above
        """
        if self.score == None:
            logger.debug(
                f"calculate_alpha_and_beta >> Node: {self.node_id} hasn't got a score, returning without update"
            )
            return alpha, beta
        if self.get_player() == "minimizer":
            beta = min(beta, self.get_score())
        if self.get_player() == "maximizer":
            alpha = max(alpha, self.get_score())
        return alpha, beta


class MinimaxTree:
    def __init__(self, root_node):
        self.root_node = root_node

    def build_and_prune_game_tree_recursive(self, node, depth, node_ids):
        """
        Builds game tree to a given depth

        Parameters:
            node (MinimaxNode): the node from which we build down
            depth (int): how far down the tree we want to build
            node_ids (set): all the move ids which have been
                encountered so far

        Returns:
            None

        Side effects:
            builds tree from node
        """
        # Make sure we don't use same node twice
        node_ids.add(node.node_id)

        # error handling
        if depth < 0:
            raise Exception(f"Maximum tree depth exceeded")

        # Base case
        # If we're at a leaf node leave the recursion
        if depth == 0:
            logger.debug(f"Returning at depth of {depth}")

            # error handling
            if node.children != []:
                e = f"Leaf node at depth {depth} shouldn't have children node_id: {node.node_id}, number of children: {len(node.children)} first child id: {node.children[0].node_id}"
                logger.error(e)
                raise Exception(e)
            return

        # don't build past the end of the game
        if node.get_utility() == -INFINITY:
            logger.debug(f"Minimizer win found at: {node.node_id}")
            return
        if node.get_utility() == INFINITY:
            logger.debug(f"Maximizer win found at: {node.node_id}")
            return

        # recurse case
        parent_node_id = node.get_node_id()
        for child in node.generate_next_child(depth, parent_node_id):
            # error handling
            assert (
                child.children == []
            ), f"Error: Nodes should initialise without children. Node {child.get_node_id()} initialized with children including: {child.children[0].get_node_id()}"

            # Make sure we don't use same node twice
            if child.node_id in node_ids:
                logger.debug(f"node_id: {child.node_id} already visited, skipping")
                continue

            # use recursion to build tree vertically
            if not self.build_and_prune_game_tree_recursive(child, depth - 1, node_ids):

                # not self.build_and_prune_game_tree_recursive(..) will be True if:
                # 1. we've reached the end of depth count-down,
                # 2. there are no more child nodes to create at this depth
                # This means first we'll get to the point we want to stop building vertically
                # and then add children at this level. Once all children are added we will work
                # back up the tree and add child nodes at higher levels

                # build tree horizontally
                node.add_child(child)
        logger.debug("Returning at end of function")
        return

    def find_depth_recursive(self, node, depth):
        if depth > MAX_TREE_DEPTH:
            raise Exception(f"Maximum tree depth of {MAX_TREE_DEPTH} exceeded")

        # Base case
        # If we're at a terminal node leave the recursion
        if node.is_leaf_node():
            logger.debug(f"child {type(node)}")
            logger.debug(
                f"depth: {depth}, node_id: {node.node_id} is_leaf_node: {node.is_leaf_node()}"
            )
            logger.debug(f"returning at depth of {depth} owing to terminal node")
            return depth

        # recurse case
        for i, child in enumerate(node.children):
            logger.debug(
                f"depth: {depth}, child index: {i}, node_id: {child.node_id} is_leaf_node: {child.is_leaf_node()}, child {type(child)}"
            )
            return self.find_depth_recursive(child, depth + 1)

        logger.debug(f"Returning because end of function depth {depth}")
        return


# Helpers
def get_depth_from_node_id(node_id):
    return str(node_id).split("-")[0]


def are_break_conditions_met(alpha, beta):
    prune_tree = alpha > beta
    black_win = alpha == INFINITY
    white_win = beta == -INFINITY
    return prune_tree or black_win or white_win
