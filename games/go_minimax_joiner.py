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
                    intersections = self.find_liberties(i, j, board_size)
                    potential_moves.extend(intersections)
        return potential_moves

    def find_liberties(self, x_coordinate, y_coordinate, board_size):
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

        score_dict = {
            WHITE_STONE: 0,
            BLACK_STONE: 0,
            "relative_black_score": 0
        }
        # first check if there's a string of stones to the right, and if so add up score
        score_dict = self.get_scores_by_row(board_state, score_dict)

        # then check if there's a string of stones below and add up score
        transposed_board = self.transpose_board(board_state)
        score_dict = self.get_scores_by_row(transposed_board, score_dict)

        # update relative black score
        score_dict["relative_black_score"] = score_dict[BLACK_STONE] - score_dict[WHITE_STONE]

        return score_dict

    def get_scores_by_row(self, board_state, score_dict):
        for row in board_state:
            # compare score to max score and replace if it's higher,
            white_score = self.get_row_score(row, WHITE_STONE)
            black_score = self.get_row_score(row, BLACK_STONE)
            if white_score > score_dict[WHITE_STONE]:
                score_dict[WHITE_STONE] = white_score
            if black_score > score_dict[BLACK_STONE]:
                score_dict[BLACK_STONE] = black_score
        return score_dict


    def transpose_board(self, board_state):
        board_size = self.get_board_size(board_state)
        transposed_board = []
        for i in range(board_size):
            transposed_board.append([])
            for j in range(board_size):
                transposed_board[i].append("+")

        for i in range(board_size):
            for j in range(board_size):
                old_board_move = board_state[i][j]
                transposed_board[j][i] = old_board_move
        return transposed_board

    def get_board_size(self, board_state):
        return len(board_state[0])

    def get_row_score(self, row, stone_colour):
        row_score = [ 0  for x in row]
        score_count = 0
        for cell in row:
            if cell == stone_colour:
                row_score[score_count] += 1
            else:
                score_count += 1
        return max(row_score)

