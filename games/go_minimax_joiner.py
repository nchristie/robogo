from .minimax import MinimaxNode, MinimaxTree
from copy import deepcopy
from .game_logic import *
from .stones import *
import logging

logger = logging.getLogger(__name__)

PLAYER_DICT = {"maximizer": BLACK_STONE, "minimizer": WHITE_STONE}

STONE_DICT = {BLACK_STONE: "maximizer", WHITE_STONE: "minimizer"}


class GoNode(MinimaxNode):
    """
    Node which inherits from MinimaxNode and layers over the logic
    relevant to five-in-a-row Go
    """

    def __init__(
        self,
        node_id=None,
        player=None,
        score=None,
        children=[],
        board_state=None,
        move_coordinates=(),
        optimal_move_coordinates=None,
    ):
        super().__init__(node_id, player, score, children)
        self.board_state = board_state
        self.move_coordinates = move_coordinates
        self.optimal_move_coordinates = optimal_move_coordinates

    def generate_next_child(self, depth, parent_node_id="NA"):
        """
        Yields:
            GoNode: next possible move on the board
        """
        player = self.alternate_player()
        stone = PLAYER_DICT[player]
        board_size = len(self.board_state)
        all_moves_on_board = list_all_moves_on_board(board_size)
        i = 0
        for move_coordinates in all_moves_on_board:
            if not is_move_valid(self.board_state, move_coordinates):
                continue
            node_id = self.make_node_id(depth, i, parent_node_id)
            new_board_state = deepcopy(self.board_state)
            x = move_coordinates[0]
            y = move_coordinates[1]
            new_board_state[x][y] = stone

            next_node = GoNode(
                node_id=node_id,
                player=player,
                board_state=new_board_state,
                move_coordinates=move_coordinates,
                children=[],
            )
            i += 1
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
                                node_id=self.make_node_id(depth, i),
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

    def get_utility(self):
        """
        Finds value of node. To be used for terminal nodes only
        Returns:
            int corresponding to black's score relative to white's
        """
        score_dict = get_score_dict(self.board_state)

        score = score_dict["relative_black_score"]
        if score_dict[BLACK_STONE] >= WINNING_SCORE:
            score = PLUS_INF
            logger.info(f"Black win found for {self.node_id}, {self.move_coordinates}")
        if score_dict[WHITE_STONE] >= WINNING_SCORE:
            score = MINUS_INF
            logger.info(f"White win found for {self.node_id}, {self.move_coordinates}")
        if not score and score != 0:
            raise Exception(f"Score could not be set score_dict: {score_dict}")
        else:
            logger.debug(
                f"Utility for node {self.node_id} with coordinates {self.move_coordinates} = {score}"
            )
        return score

    # TODO find_connecting_stones():


class GoTree(MinimaxTree):
    def __init__(self, root_node):
        self.root_node = root_node

    # TODO this function should be removable once alpha-beta
    # function works

    def evaluate(self, node, depth, node_ids, alpha, beta):
        """
        Starts from current node and builds game tree to a given
        depth then returns the best next move using the information
        gathered. Only builds branches which have optimal game moves

        Parameters:
            depth (int): how far down the tree we want to build
            node_ids (set): all the move ids which have been
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
            f"In evaluate, node: {node.node_id} depth: {depth}, player: {node.player}, alpha: {alpha}, beta: {beta}"
        )

        # Make sure we don't use same node twice
        node_ids.add(node.node_id)

        # error handling
        if depth < 0:
            e = f"Maximum tree depth exceeded at node: {node.node_id}"
            logger.error(e)
            raise Exception(e)

        # Base case
        # If we're at a terminal node leave the recursion
        if depth == 0:
            # error handling
            assert (
                not node.children
            ), f"Node at depth 0 shouldn't have children node_id: {node.node_id}, number of children: {len(node.children)}"

            node_score = node.get_utility()
            node.set_score(node_score)

            logger.debug(
                f"Returning at depth of {depth} with score of {node_score} at node: {node.node_id}"
            )
            return node.get_score()

        # recurse case

        # error handling
        if node.children != []:
            e = f"Node {node.node_id} children == None, all nodes should be initialised with children of []"
            logger.error(e)
            raise Exception(e)

        for child in node.generate_next_child(depth, self.root_node.get_node_id()):
            # Don't add board states which have already been visited
            if str(child.node_id) in node_ids:
                logger.debug("Board state already seen, skipping this node")
                continue

            # TODO if child score is a winning score then don't build branches further

            # use recursion to build tree vertically
            # set best score to the max or min of alpha vs recurse or beta vs recurse
            if node.player == "maximizer":
                best_score = max(
                    alpha, self.evaluate(child, depth - 1, node_ids, alpha, beta)
                )
                alpha = best_score
                logger.debug(f"alpha set to {alpha}")
            if node.player == "minimizer":
                best_score = min(
                    beta, self.evaluate(child, depth - 1, node_ids, alpha, beta)
                )
                beta = best_score
                logger.debug(f"beta set to {beta}")
            if beta <= alpha:
                logger.debug(
                    f"Breakpoint reached for {node.player} alpha: {alpha}, beta: {beta}, node score: {best_score}, node id: {node.node_id}"
                )
                # build tree horizontally
                node.add_child(child)
                node.set_score(best_score)
                return best_score

            # build tree horizontally
            node.add_child(child)
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
        raise Exception(
            f"Best score: {best_score} not found in children of node: {node.node_id} whose children are: {[child.get_score() for child in node.children]}"
        )

    def minimax_depth_of_2(self):
        depth = 2
        self.build_game_tree_recursive(self.root_node, depth, set())

        current_node = self.root_node

        for child in current_node.get_children():
            for child2 in child.get_children():
                child2.set_score(child2.get_utility())
            child2_optimal_move = child.get_optimal_move()
            child.set_score(child2_optimal_move.get_score())

        return self.root_node.get_optimal_move()