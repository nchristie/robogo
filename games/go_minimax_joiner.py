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
        optimal_move_coordinates=None,
    ):
        super().__init__(move_id, player, score, is_terminal, leaves)
        self.board_state = board_state
        self.optimal_move_coordinates = optimal_move_coordinates

    def set_leaves(self, player=None):
        # returns an array of Nodes representing the
        # candidates for next move in game
        potential_moves = [move for move in self.get_potential_moves()]

        for item in potential_moves:
            x = item["move_coordinates"][0]
            y = item["move_coordinates"][1]
            new_board_state = deepcopy(self.board_state)
            new_board_state[x][y] = BLACK_STONE
            move_id = item["move_id"]
            terminal_node = self.make_terminal_node(
                new_board_state, move_id, player
            )
            self.add_go_leaf(
                move_id=item["move_id"],
                player=player,
                score=terminal_node.score,
                board_state=new_board_state,
            )

        optimal_move_id = self.get_optimal_move().move_id
        for move in potential_moves:
            if move["move_id"] == optimal_move_id:
                self.optimal_move_coordinates = move["move_coordinates"]

    def add_go_leaf(
        self, move_id=None, player=None, score=None, leaves=[], board_state=None
    ):
        leaf = GoNode(
            move_id=move_id,
            player=player,
            score=score,
            is_terminal=False,
            leaves=leaves,
            board_state=board_state,
        )
        self.leaves.append(leaf)

    def make_terminal_node(self, board_state, move_id, player):
        new_node = GoNode(
            move_id=move_id,
            player=player,
            score=None,
            is_terminal=True,
            board_state=board_state,
        )
        new_node.set_score(new_node.get_utility())
        return new_node

    def get_potential_moves(self):
        # Currently returns a list of dictionaries
        # Currently only gives moves around existing stones on board
        # TODO give all potential moves on board
        # TODO Return GoNode instead of dictionary
        for x_coordinate, row in enumerate(self.board_state):
            for y_coordinate, cell in enumerate(row):
                if cell != EMPTY_POSITION:
                    all_intersecting_positions = self.find_moves_around_position(x_coordinate, y_coordinate)
                    for move_coordinates in all_intersecting_positions:
                        if is_move_valid(self.board_state, move_coordinates):
                            move_id = self.generate_move_id()
                            move_dict = {"move_coordinates": move_coordinates, "move_id": move_id}
                            yield move_dict


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
        pass
