from .minimax import Node
import uuid

EMPTY_POSITION = "+"
WHITE_STONE = "○"
BLACK_STONE = "●"

class LeafGetter:
    def __init__(self):
        return
    
    def get_node_array(self, board_state=None, player=None):
        # returns an array of Nodes representing the
        # candidates for next move in game
        potential_moves = self.get_potential_moves(board_state)
        move_id = self.generate_move_id()
        return [self.make_node(move_id) for item in potential_moves]
    
    def make_node(self, move_id):
        return Node(
            move_id=move_id,
            player=None,
            leaf_getter=LeafGetter
        )
    
    def make_terminal_node(self, move_id, score):
        return Node(
            move_id=move_id,
            score=score,
            player=None,
            leaf_getter=LeafGetter
        )
    
    def get_potential_moves(self, board_state):
        potential_moves = []
        board_size = len(board_state[0])
        for i, row in enumerate(board_state):
            for j, cell in enumerate(row):
                if cell != EMPTY_POSITION:
                    intersections = self.find_intersections(i, j, board_size)
                    potential_moves.extend(intersections)
        return potential_moves
    
    def find_intersections(self, x_coordinate, y_coordinate, board_size):
        up = (x_coordinate - 1, y_coordinate)
        left = (x_coordinate, y_coordinate - 1)
        right = (x_coordinate, y_coordinate + 1)
        down = (x_coordinate + 1, y_coordinate)
        potential_moves = [up, left, right, down]

        potential_moves_within_boundaries = []
        for move in potential_moves:
            if (move[0] >= board_size) or (move[0] < 0):
                continue
            elif (move[1] >= board_size) or (move[1] < 0):
                continue
            else:
                potential_moves_within_boundaries.append(move)

        return potential_moves_within_boundaries
    
    def generate_move_id(self):
        return str(uuid.uuid4())

    def get_scores(self, board_state):
        white_score = 0
        black_score = 0
        relative_black_score = black_score - white_score

        return {
            WHITE_STONE: white_score,
            BLACK_STONE: black_score,
            "relative_black_score": relative_black_score
        }

