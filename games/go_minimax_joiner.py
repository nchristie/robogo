from .minimax import Node

class LeafGetter:
    def __init__(self):
        self.EMPTY_POSITION = "+"
        self.WHITE_STONE = "○"
        self.BLACK_STONE = "●"
        return
    
    def get_node_array(self, board_state=None, player=None):
        # returns an array of Nodes representing the
        # candidates for next move in game  
        return [self.make_node(i) for i in range(3)]
    
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
                if cell != self.EMPTY_POSITION:
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

