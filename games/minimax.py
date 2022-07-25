import logging

logger = logging.getLogger(__name__)

MAX_TREE_DEPTH = 5


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
        logger.error(
            "In minimax get_utility, this should be implemented by class which inherits"
        )
        return

    def generate_next_child(self, depth):
        logger.error(
            f"In minimax generate_next_child, this should be implemented by class which inherits depth: {depth}"
        )
        child_node_depth = depth - 1
        for i in range(5):
            yield MinimaxNode(
                move_id=self.make_move_id(child_node_depth, i),
                player=self.alternate_player(),
            )

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

    def make_move_id(self, depth, index):
        """
        Creates a unique id for each move
        Returns (str):
        """
        return f"d{depth}-i{index}"

    def alternate_player(self):
        """
        Returns:
            str: The opposite player to that of the current
            node. Valid options: "minimizer", "maximizer".
        """
        if self.player == "minimizer":
            return "maximizer"
        return "minimizer"


class MinimaxTree:
    def __init__(self, root_node):
        self.root_node = root_node

    def build_game_tree_recursive(self, node, depth, move_ids):
        """
        Starts from current node and builds game tree to a given
        depth

        Parameters:
            depth (int): how far down the tree we want to build
        """
        logger.debug(
            f"In build_game_tree_recursive, move_id: {node.move_id} depth: {depth}"
        )

        move_ids.add(node.move_id)

        if depth < 0:
            raise Exception(f"Maximum tree depth exceeded")

        # Base case
        # If we're at a leaf node leave the recursion
        if depth == 0:
            logger.debug(f"Returning at depth of {depth}")
            # import pdb; pdb.set_trace()
            assert (
                not node.children
            ), f"Leaf node at depth {depth} shouldn't have children move_id: {node.move_id}, number of children: {len(node.children)} first child id: {node.children[0].move_id}"
            return

        # recurse case
        for child in node.generate_next_child(depth):
            if child.move_id in move_ids:
                continue
            # use recursion to build tree vertically
            if not self.build_game_tree_recursive(child, depth - 1, move_ids):

                # not build_game_tree_recursive(..) will be True if we've reached the end of
                # depth count-down or if we've visited every potential child node horizontally,
                # so this means first we'll get to the point we want to stop building and add
                # children, then work back up the tree and add child nodes

                # build tree horizontally
                message = f"child {child.move_id} to parent {node.move_id} at depth of {depth}"
                if self.get_depth_from_move_id(
                    child.move_id
                ) == self.get_depth_from_move_id(node.move_id):
                    raise Exception(
                        f"Shouldn't append nodes at same depth of tree: {message}"
                    )
                logger.debug(f"Appending {message}")
                node.children.append(child)
                logger.debug(f"number of children: {len(node.children)}")

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
                f"depth: {depth}, move_id: {node.move_id} is_leaf_node: {node.is_leaf_node()}"
            )
            logger.debug(f"returning at depth of {depth} owing to terminal node")
            return depth

        # recurse case
        for i, child in enumerate(node.children):
            logger.debug(
                f"depth: {depth}, child index: {i}, move_id: {child.move_id} is_leaf_node: {child.is_leaf_node()}, child {type(child)}"
            )
            return self.find_depth_recursive(child, depth + 1)

        logger.debug(f"Returning because end of function depth {depth}")
        return

    def get_depth_from_move_id(self, move_id):
        return move_id.split("-")[0]
