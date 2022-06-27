from .minimax import Node
import uuid
from copy import deepcopy
from .game_logic import is_move_valid, get_board_size, transpose_board
from .stones import EMPTY_POSITION, BLACK_STONE, WHITE_STONE

class GoNode(Node):
    def __init__(
        self,
        move_id=None,
        player=None,
        score=None,
        leaves=[],
        board_state=None,
        optimal_move_coordinates=None
    ):
        super().__init__(move_id, player, score, leaves)
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
                terminal_node = self.make_terminal_node(new_board_state, move_id, player)
                self.add_go_leaf(
                    move_id=item["move_id"], 
                    player=player, 
                    score=terminal_node.score,
                    board_state=new_board_state
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

    def add_go_leaf(self, move_id=None, player=None, score=None, leaves=[], board_state=None):
        leaf = GoNode(move_id, player, score, leaves, board_state)
        self.leaves.append(leaf)

    def make_terminal_node(self, board_state, move_id, player):
        new_node = GoNode(
            move_id=move_id,
            player=player,
            board_state=board_state
        )
        new_node.score = new_node.get_scores()
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
            move_dict = {
                "move_coordinates": move,
                "move_id": move_id
            }
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

    def get_scores(self):

        score_dict = {
            WHITE_STONE: 0,
            BLACK_STONE: 0,
            "relative_black_score": 0
        }
        # first check if there's a string of stones to the right, and if so add up score
        score_dict = self.get_scores_by_row(score_dict)

        # then check if there's a string of stones below and add up score
        score_dict = self.get_scores_by_row(score_dict, should_transpose_board=True)

        # update relative black score
        score_dict["relative_black_score"] = score_dict[BLACK_STONE] - score_dict[WHITE_STONE]

        return score_dict["relative_black_score"]

    def get_scores_by_row(self, score_dict, should_transpose_board=False):
        board = self.board_state
        if should_transpose_board:
            board = transpose_board(self.board_state)
        for row in board:
            # compare score to max score and replace if it's higher,
            white_score = self.get_row_score(row, WHITE_STONE)
            black_score = self.get_row_score(row, BLACK_STONE)
            if white_score > score_dict[WHITE_STONE]:
                score_dict[WHITE_STONE] = white_score
            if black_score > score_dict[BLACK_STONE]:
                score_dict[BLACK_STONE] = black_score
        return score_dict

    def get_row_score(self, row, stone_colour):
        row_score = [ 0  for x in row]
        score_count = 0
        for cell in row:
            if cell == stone_colour:
                row_score[score_count] += 1
            else:
                score_count += 1
        return max(row_score)

