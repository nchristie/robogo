from .minimax import MinimaxNode, MinimaxTree
from copy import deepcopy
from .game_logic import *
from .stones import *
import logging

logger = logging.getLogger(__name__)

PLAYER_DICT = {"maximizer": WHITE_STONE, "minimizer": BLACK_STONE}

STONE_DICT = {BLACK_STONE: "maximizer", WHITE_STONE: "minimizer"}


class GoNode(MinimaxNode):
    """
    Node which inherits from MinimaxNode and layers over the logic
    relevant to five-in-a-row Go
    """

    def __init__(
        self,
        node_id=None,
        score=None,
        children=[],
        board_state=None,
        move_coordinates=(),
        optimal_move_coordinates=None,
        player_to_move=None,
        path_depth=0,
    ):
        super().__init__(node_id, score, children, player_to_move, path_depth)
        self.board_state = board_state
        self.set_move_coordinates(move_coordinates)
        self.optimal_move_coordinates = optimal_move_coordinates

    def __str__(self):
        return (
            f"node_id: {self.get_node_id()}, "
            f"score: {self.get_score()}, "
            f"number of children: {len(self.get_children())}, "
            f"player_to_move: {self.get_player_to_move()}, "
            f"move_coordinates: {self.get_move_coordinates()}, "
            f"path_depth: {self.get_path_depth()}"
        )

    def get_board_state(self):
        return self.board_state

    def set_board_state(self, board_state):
        self.board_state = board_state

    def set_move_coordinates(self, coordinates):
        self.move_coordinates = coordinates

    def get_move_coordinates(self):
        return self.move_coordinates

    def generate_next_child(self, depth, parent_node_id="NA"):
        """
        Yields:
            GoNode: next possible move on the board
        """
        player_to_move = self.alternate_player_to_move()
        stone = PLAYER_DICT[player_to_move]
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
                board_state=new_board_state,
                move_coordinates=move_coordinates,
                children=[],
                player_to_move=player_to_move,
            )
            i += 1
            yield next_node

    def generate_next_child_around_existing_moves(
        self, depth=0, player_to_move="maximizer"
    ):
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
                                board_state=new_board_state,
                                move_coordinates=move_coordinates,
                                player_to_move=player_to_move,
                            )
                            yield child

    def find_moves_around_position(self, x_coordinate, y_coordinate):
        # I've returned this function to the code as I think I may want it later
        up = (x_coordinate - 1, y_coordinate)
        left = (x_coordinate, y_coordinate - 1)
        right = (x_coordinate, y_coordinate + 1)
        down = (x_coordinate + 1, y_coordinate)
        return [up, left, right, down]

    def find_utility(self, winning_score=WINNING_SCORE):
        """
        Finds value of node. To be used for terminal nodes only
        Returns:
            int corresponding to black's score relative to white's
        """
        score_dict = get_score_dict(self.board_state)

        score = score_dict["relative_black_score"]
        if score_dict[BLACK_STONE] >= winning_score:
            score = HIGHEST_SCORE
            logger.debug(
                f"Maximizer win found for {self.get_node_id()}, {self.move_coordinates}"
            )
        if score_dict[WHITE_STONE] >= winning_score:
            score = LOWEST_SCORE
            logger.debug(
                f"Minimizer win found for {self.get_node_id()}, {self.move_coordinates}"
            )
        if not score and score != 0:
            raise Exception(f"Score could not be set score_dict: {score_dict}")
        else:
            logger.debug(
                f"Utility for node {self.get_node_id()} with coordinates {self.move_coordinates} = {score}"
            )
        if not score and score != 0:
            raise Exception(f"Couldn't get utility for {self.get_node_id()}")
        return score

    # TODO find_connecting_stones():


class GoTree(MinimaxTree):
    def __init__(self, root_node):
        self.root_node = root_node

    def minimax_depth_of_2(self, winning_score=WINNING_SCORE):
        depth = 2
        self.build_and_prune_game_tree_recursive(self.root_node, depth, set())

        current_node = self.root_node

        for child in current_node.get_children():
            for child2 in child.get_children():
                child2.set_score(child2.find_utility(winning_score=winning_score))
            child2_optimal_move = child.get_optimal_move()
            child.set_score(child2_optimal_move.get_score())

        return self.root_node.get_optimal_move()
