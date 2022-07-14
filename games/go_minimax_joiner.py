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

    def set_leaves(self, player=None, is_terminal=False):
        # returns an array of Nodes representing the
        # candidates for next move in game
        potential_moves = self.get_potential_moves()
        if is_terminal:
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
        else:
            for item in potential_moves:
                self.add_go_leaf(
                    move_id=item["move_id"],
                )

        if is_terminal:
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
        potential_moves = []
        for i, row in enumerate(self.board_state):
            for j, cell in enumerate(row):
                if cell != EMPTY_POSITION:
                    potential_move = self.find_legal_moves_around_position(i, j)
                    potential_moves.extend(potential_move)

        potential_moves_with_ids = []
        for move in potential_moves:
            move_id = self.generate_move_id()
            move_dict = {"move_coordinates": move, "move_id": move_id}
            potential_moves_with_ids.append(move_dict)
        return potential_moves_with_ids

    def find_legal_moves_around_position(self, x_coordinate, y_coordinate):
        up = (x_coordinate - 1, y_coordinate)
        left = (x_coordinate, y_coordinate - 1)
        right = (x_coordinate, y_coordinate + 1)
        down = (x_coordinate + 1, y_coordinate)
        all_intersecting_positions = [up, left, right, down]

        potential_moves = []
        for move_coordinates in all_intersecting_positions:
            if is_move_valid(self.board_state, move_coordinates):
                potential_moves.append(move_coordinates)

        return potential_moves

    def generate_move_id(self):
        return str(uuid.uuid4())

    def get_utility(self):
        score_dict = get_score_dict(self.board_state)
        return score_dict["relative_black_score"]

    def find_connecting_stones():
        pass
