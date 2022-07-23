from .minimax import MinimaxNode
import uuid
from copy import deepcopy
from .game_logic import (
    WINNING_SCORE,
    PLUS_INF,
    MINUS_INF,
    is_move_valid,
    get_score_dict,
    list_all_moves_on_board,
)
from .stones import EMPTY_POSITION, BLACK_STONE, WHITE_STONE
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
        parent=None,
        board_state=None,
        move_coordinates=(),
        optimal_move_coordinates=None,
    ):
        super().__init__(move_id, player, score, children, parent)
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
                logger.debug(f"Invalid move for: {move_id}")
                continue
            new_board_state = deepcopy(self.board_state)
            x = move_coordinates[0]
            y = move_coordinates[1]
            new_board_state[x][y] = stone

            # TODO add parent node
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
