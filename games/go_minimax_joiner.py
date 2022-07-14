from .minimax import MinimaxNode
import uuid
from copy import deepcopy
from .game_logic import is_move_valid, get_score_dict
from .stones import EMPTY_POSITION, BLACK_STONE


class GoNode(MinimaxNode):
    def __init__(
        self,
        move_id=None,
        player=None,
        score=None,
        is_terminal=False,
        leaves=[],
        board_state=None,
        move_coordinates=(),
        optimal_move_coordinates=None,
    ):
        super().__init__(move_id, player, score, is_terminal, leaves)
        self.board_state = board_state
        self.move_coordinates = move_coordinates
        self.optimal_move_coordinates = optimal_move_coordinates

    def set_leaves(self):
        # returns an array of Nodes representing the
        # candidates for next move in game
        for leaf in self.get_potential_moves():
            self.add_leaf(leaf)

        optimal_move_id = self.get_optimal_move().move_id
        for leaf in self.leaves:
            if leaf.move_id == optimal_move_id:
                self.optimal_move_coordinates = leaf.move_coordinates

    def add_leaf(self, leaf):
        self.leaves.append(leaf)

    def get_potential_moves(self):
        # Currently only gives moves around existing stones on board
        # TODO give all potential moves on board
        for x_coordinate, row in enumerate(self.board_state):
            for y_coordinate, cell in enumerate(row):
                if cell != EMPTY_POSITION:
                    all_intersecting_positions = self.find_moves_around_position(
                        x_coordinate, y_coordinate
                    )
                    for move_coordinates in all_intersecting_positions:
                        if is_move_valid(self.board_state, move_coordinates):
                            new_board_state = deepcopy(self.board_state)
                            x = move_coordinates[0]
                            y = move_coordinates[1]
                            new_board_state[x][y] = BLACK_STONE
                            leaf = GoNode(
                                move_id=self.generate_move_id(),
                                player="minimizer",
                                board_state=new_board_state,
                                move_coordinates=move_coordinates,
                            )
                            leaf.set_score(leaf.get_utility())
                            yield leaf

    def find_moves_around_position(self, x_coordinate, y_coordinate):
        up = (x_coordinate - 1, y_coordinate)
        left = (x_coordinate, y_coordinate - 1)
        right = (x_coordinate, y_coordinate + 1)
        down = (x_coordinate + 1, y_coordinate)
        return [up, left, right, down]

    def generate_move_id(self):
        return str(uuid.uuid4())

    def get_utility(self):
        score_dict = get_score_dict(self.board_state)
        return score_dict["relative_black_score"]

    def find_connecting_stones():
        # TODO build out this function
        return
