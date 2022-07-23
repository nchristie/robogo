import logging
from .game_logic import short_id

logger = logging.getLogger(__name__)


class MinimaxNode:
    def __init__(self, move_id=None, player=None, score=None, parent=None, children=[]):
        self.parent = parent
        self.children = children
        self.move_id = move_id
        self.player = player
        self.score = score

    def __str__(self):
        return (
            f"move_id: {self.get_move_id()}, "
            f"score: {self.get_score()}, "
            f"number of children: {len(self.get_children())}"
        )

    def set_score(self, score):
        self.score = score

    def get_score(self):
        if not self.score:
            raise Exception(f"Score has not been set for node {short_id(self.move_id)}")
        return self.score

    def get_move_id(self):
        return self.move_id

    def add_child(self, move_id=None, player=None, score=None):
        # TODO this is only used in the tests, probably worth
        # rewriting to append a node, and have a separate
        # node making method instead
        child = MinimaxNode(move_id, player, score)
        self.children.append(child)

    def set_parent(self, parent):
        self.parent = parent

    def get_children(self):
        return self.children

    def generate_next_child(self):
        # implemented by inheritor
        return

    def get_optimal_move(self):
        # input is Node, output is Node
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
        return best_move

    def maximizer_strategy(self, child_score, best_score):
        return child_score > best_score

    def minimizer_strategy(self, child_score, best_score):
        return child_score < best_score

    def get_utility(self):
        logger.debug("In minimax get_utility")
        # Implemented by class which inherits
        return

    def evaluate_node(self, node, maximizer_choice_node, minimizer_choice_node, depth):
        # input is node, output is node
        # adapted from: https://www.hackerearth.com/blog/developers/minimax-algorithm-alpha-beta-pruning/
        # and https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-4-alpha-beta-pruning/
        depth -= 1

        if depth <= 0:
            return

        if node.is_leaf_node():
            logger.debug(f"terminal node found at depth of {depth}")
            node.set_score(node.get_utility())
            return node

        if node.player == "minimizer":
            for child in node.generate_next_child():
                minimizer_choice_node = node.node_min(
                    minimizer_choice_node,
                    node.evaluate_node(
                        child, maximizer_choice_node, minimizer_choice_node, depth
                    ),
                )
                if (
                    minimizer_choice_node.get_score()
                    <= maximizer_choice_node.get_score()
                ):
                    return minimizer_choice_node
                return minimizer_choice_node

        if node.player == "maximizer":
            for child in node.generate_next_child():
                maximizer_choice_node = node.node_max(
                    maximizer_choice_node,
                    node.evaluate_node(
                        child, maximizer_choice_node, minimizer_choice_node, depth
                    ),
                )
                if (
                    minimizer_choice_node.get_score()
                    <= maximizer_choice_node.get_score()
                ):
                    return maximizer_choice_node
                return maximizer_choice_node

    def build_minimax_alpha_beta_game_tree(
        self, node, maximizer_choice_node, minimizer_choice_node, depth
    ):
        # input is node, output is node
        # TODO input is node, output is the best available value,
        # TODO side effect is setting values on entire tree
        # adapted from: https://www.hackerearth.com/blog/developers/minimax-algorithm-alpha-beta-pruning/
        # and https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-4-alpha-beta-pruning/
        depth -= 1

        if depth < 0:
            raise Exception("Error: depth is <0")

        if depth == 0:
            return

        if node.is_leaf_node():
            logger.debug(f"terminal node found at depth of {depth}")
            node_score = node.get_utility()
            node.set_score(node_score)
            return node_score

        if node.player == "minimizer":
            for child in node.generate_next_child():
                node.add_child(child)
                minimizer_choice_node = node.node_min(
                    minimizer_choice_node,
                    node.evaluate_node(
                        child, maximizer_choice_node, minimizer_choice_node, depth
                    ),
                )
                if (
                    minimizer_choice_node.get_score()
                    <= maximizer_choice_node.get_score()
                ):
                    node.set_score(minimizer_choice_node.get_score())
                    return minimizer_choice_node.get_score()
                node.set_score(minimizer_choice_node.get_score())
                return minimizer_choice_node.get_score()

        if node.player == "maximizer":
            for child in node.generate_next_child():
                node.add_child(child)
                maximizer_choice_node = node.node_max(
                    maximizer_choice_node,
                    node.evaluate_node(
                        child, maximizer_choice_node, minimizer_choice_node, depth
                    ),
                )
                if (
                    minimizer_choice_node.get_score()
                    <= maximizer_choice_node.get_score()
                ):
                    node.set_score(maximizer_choice_node.get_score())
                    return maximizer_choice_node.get_score()
                node.set_score(maximizer_choice_node.get_score())
                return maximizer_choice_node.get_score()

    def node_min(self, first_node, second_node):
        if second_node.get_score() < first_node.get_score():
            return second_node
        return first_node

    def node_max(self, first_node, second_node):
        if second_node.get_score() > first_node.get_score():
            return second_node
        return first_node

    def is_leaf_node(self):
        # logger.debug(f"Checking if leaf node, number of children = {len(self.children)}, move_id = {self.move_id}")
        return not self.children
