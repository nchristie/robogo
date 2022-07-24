from .minimax import MinimaxNode
from copy import deepcopy
from .game_logic import *
from .stones import *
import logging

logger = logging.getLogger(__name__)

PLAYER_DICT = {"maximizer": BLACK_STONE, "minimizer": WHITE_STONE}

STONE_DICT = {BLACK_STONE: "maximizer", WHITE_STONE: "minimizer"}

MAX_TREE_DEPTH = 5


class GoNode(MinimaxNode):
    """
    Node which inherits from MinimaxNode and layers over the logic
    relevant to five-in-a-row Go
    """

    def __init__(
        self,
        move_id=None,
        player=None,
        score=None,
        children=[],
        board_state=None,
        move_coordinates=(),
        optimal_move_coordinates=None,
    ):
        super().__init__(move_id, player, score, children)
        self.board_state = board_state
        self.move_coordinates = move_coordinates
        self.optimal_move_coordinates = optimal_move_coordinates

    def alternate_player(self):
        """
        Returns:
            str: The opposite player to that of the current
            node. Valid options: "minimizer", "maximizer".
        """
        if self.player == "minimizer":
            return "maximizer"
        return "minimizer"

    def generate_next_child(self, depth):
        """
        Yields:
            GoNode: next possible move on the board
        """
        # TODO return a dictionary with the parameters to go into the GoNode
        #   instead of the GoNode itself - this is so we can use the add_child
        #   method instead of doing an append to node.children

        # logger.debug(f"In generate_next_child, own id = {self.move_id}")
        player = self.alternate_player()
        stone = PLAYER_DICT[player]
        board_size = len(self.board_state)
        all_moves_on_board = list_all_moves_on_board(board_size)
        for i, move_coordinates in enumerate(all_moves_on_board):
            move_id = self.make_move_id(depth, i)
            if not is_move_valid(self.board_state, move_coordinates):
                continue
            new_board_state = deepcopy(self.board_state)
            x = move_coordinates[0]
            y = move_coordinates[1]
            new_board_state[x][y] = stone

            next_node = GoNode(
                move_id=move_id,
                player=player,
                board_state=new_board_state,
                move_coordinates=move_coordinates,
                children=[],
            )
            yield next_node

    def generate_next_child_around_existing_moves(self, player="minimizer", depth=0):
        # I've returned this function to the code as I think I may want it later
        for x_coordinate, row in enumerate(self.board_state):
            for y_coordinate, cell in enumerate(row):
                if cell != EMPTY_POSITION:
                    all_intersecting_positions = self.find_moves_around_position(
                        x_coordinate, y_coordinate
                    )
                    for i, move_coordinates in enumerate(all_intersecting_positions):
                        if is_move_valid(self.board_state, move_coordinates):
                            new_board_state = deepcopy(self.board_state)
                            x = move_coordinates[0]
                            y = move_coordinates[1]
                            new_board_state[x][y] = BLACK_STONE
                            child = GoNode(
                                move_id=self.make_move_id(depth, i),
                                player=player,
                                board_state=new_board_state,
                                move_coordinates=move_coordinates,
                            )
                            # child.set_score(child.get_utility())
                            yield child

    def find_moves_around_position(self, x_coordinate, y_coordinate):
        # I've returned this function to the code as I think I may want it later
        up = (x_coordinate - 1, y_coordinate)
        left = (x_coordinate, y_coordinate - 1)
        right = (x_coordinate, y_coordinate + 1)
        down = (x_coordinate + 1, y_coordinate)
        return [up, left, right, down]

    def make_move_id(self, depth, index):
        """
        Creates a unique id for each move
        Returns (str):
        """
        return f"d{depth}-i{index}"

    def get_utility(self):
        """
        Finds value of node. To be used for terminal nodes only
        Returns:
            int corresponding to black's score relative to white's
        """
        logger.debug(f"In get_utility for node: {self.move_id}")
        score_dict = get_score_dict(self.board_state)

        score = score_dict["relative_black_score"]
        if score_dict[BLACK_STONE] >= WINNING_SCORE:
            score = PLUS_INF
        if score_dict[WHITE_STONE] >= WINNING_SCORE:
            score = MINUS_INF
        if not score and score != 0:
            raise Exception(f"Score could not be set score_dict: {score_dict}")
        else:
            logger.debug(f"Utility for node {self.move_id} = {score}")
        return score

    # TODO find_connecting_stones():


class GoTree(GoNode):
    def __init__(self, root_node):
        self.root_node = root_node

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


    def find_depth_iterative(self, node, max_depth):
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
    def build_game_tree_recursive(self, node, depth, board_states):
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
            if not self.build_game_tree_recursive(child, depth - 1, board_states):

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

    def evaluate(self, node, depth, board_states, alpha, beta):
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
            func, alpha_or_beta = self.apply_strategy(node.player, alpha, beta)
            best_score = func(alpha_or_beta, self.evaluate(child, depth - 1, board_states, alpha, beta))
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


    def get_optimal_value(self, old_optimal_value, new_value, player):
        if player == "minimizer":
            return min(old_optimal_value, new_value)
        if player == "maximizer":
            return max(old_optimal_value, new_value)


    def get_best_next_move(self, node, best_score):
        for child in node.children:
            if child.get_score() == best_score:
                return child
        raise Exception(f"Best score: {best_score} not found in children of node: {node.move_id} whose children are: {[child.get_score() for child in node.children]}")

    def apply_strategy(self, player, alpha, beta):
        strategy_dict = {
            "maximizer": max,
            "minimizer": min
        }
        player_dict = {
            "maximizer": alpha,
            "minimizer": beta
        }

        return (strategy_dict[player], player_dict[player])
