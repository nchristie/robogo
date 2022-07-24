import logging

logger = logging.getLogger(__name__)


class MinimaxNode:
    def __init__(self, move_id=None, player=None, score=None, children=[]):
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
        logger.debug(f"In set_score for node: {self.move_id}, score: {score}")
        self.score = score

    def get_score(self):
        if not self.score and self.score != 0:
            e = f"Score has not been set for node {self.move_id}"
            logger.error(e)
            raise Exception(e)
        return self.score

    def get_move_id(self):
        return self.move_id

    def add_child(self, move_id=None, player=None, score=None):
        # TODO this is only used in the tests, probably worth
        # rewriting to append a node, and have a separate
        # node making method instead
        child = MinimaxNode(move_id, player, score)
        self.children.append(child)

    def get_children(self):
        return self.children

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
