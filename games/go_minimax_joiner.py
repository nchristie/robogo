from .minimax import MinimaxNode
from copy import deepcopy
from .game_logic import *
from .stones import *
import logging
from math import ceil

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
        board_state=None,
        move_coordinates=(),
        player_to_move=None,
    ):
        super().__init__(node_id, player_to_move)
        self.board_state = board_state
        self.set_move_coordinates(move_coordinates)

    def __str__(self):
        return (
            f"node_id: {self.get_node_id()}, "
            f"player_to_move: {self.get_player_to_move()}, "
            f"move_coordinates: {self.get_move_coordinates()}, "
        )

    def get_board_state(self):
        return self.board_state

    def set_board_state(self, board_state):
        self.board_state = board_state

    def set_move_coordinates(self, coordinates):
        self.move_coordinates = coordinates

    def get_move_coordinates(self):
        return self.move_coordinates

    def generate_next_child_and_rank_by_proximity(
        self,
        depth=0,
        parent_node_id="NA",
    ):
        """
        Yields:
            GoNode: possible moves on the board sorted by proximity to other stones
        """
        all_positions = []
        player_to_move = self.alternate_player_to_move()
        stone = PLAYER_DICT[player_to_move]
        board_size = len(self.board_state)

        max_jump_size = ceil(board_size / 3)
        min_jump_size = 1
        if max_jump_size <= min_jump_size:
            max_jump_size = board_size

        populated_cells = find_populated_cells(self.board_state)

        i = 0
        for jump_size in range(min_jump_size, max_jump_size):
            for x_coordinate, y_coordinate in populated_cells:
                surrounding_positions = find_moves_around_position(
                    x_coordinate, y_coordinate, jump_size=jump_size
                )
                for move_coordinates in surrounding_positions:
                    if not is_move_valid(self.board_state, move_coordinates):
                        continue
                    if move_coordinates not in all_positions:
                        all_positions.append(move_coordinates)
                        new_board_state = deepcopy(self.board_state)
                        x = move_coordinates[0]
                        y = move_coordinates[1]
                        new_board_state[x][y] = stone
                        node_id = self.make_node_id(depth, i, parent_node_id)
                        child = GoNode(
                            node_id=node_id,
                            board_state=new_board_state,
                            move_coordinates=move_coordinates,
                            player_to_move=player_to_move,
                        )
                        i += 1
                        yield child


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
            raise Exception(
                f"Couldn't find utility for {self.get_node_id()} score_dict: {score_dict}"
            )
        else:
            logger.debug(
                f"Utility for node {self.get_node_id()} with coordinates {self.move_coordinates} = {score}"
            )
        return score
