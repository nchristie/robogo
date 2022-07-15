from .minimax import MinimaxNode
import uuid
from copy import deepcopy
from .game_logic import is_move_valid, get_score_dict, list_all_moves_on_board, WINNING_SCORE
from .stones import EMPTY_POSITION, BLACK_STONE, WHITE_STONE

PLAYER_DICT = {
    "maximizer": BLACK_STONE,
    "minimizer": WHITE_STONE
}

STONE_DICT = {
    BLACK_STONE: "maximizer",
    WHITE_STONE: "minimizer"
}

class GoNode(MinimaxNode):
    def __init__(
        self,
        move_id=None,
        player=None,
        score=None,
        is_terminal=False,
        branches=[],
        board_state=None,
        move_coordinates=(),
        optimal_move_coordinates=None,
    ):
        super().__init__(move_id, player, score, is_terminal, branches)
        self.board_state = board_state
        self.move_coordinates = move_coordinates
        self.optimal_move_coordinates = optimal_move_coordinates

    def build_game_tree(self, depth):
        # Base case
        # If we're at a terminal node leave the recursion
        if self.is_terminal:
            return

        # recurse case
        branches = [branch for branch in self.generate_branches()]
        for branch in branches:
            if depth == 0:
                # once we're at full depth make these nodes terminal
                branch.is_terminal = True
            self.branches.append(branch)
            branch.build_game_tree(depth-1)

    def alternate_player(self):
        if self.player == "minimizer":
            return "maximizer"
        return "minimizer"

    def generate_branches(self):
        """
        Yields:
            GoNode: next possible move on the board
        """
        player = self.alternate_player()
        stone = PLAYER_DICT[player]
        board_size = len(self.board_state)
        all_moves_on_board = list_all_moves_on_board(board_size)
        for move_coordinates in all_moves_on_board:
            if is_move_valid(self.board_state, move_coordinates):
                new_board_state = deepcopy(self.board_state)
                x = move_coordinates[0]
                y = move_coordinates[1]
                new_board_state[x][y] = stone
                branch = GoNode(
                    move_id=self.generate_move_id(),
                    player=player,
                    board_state=new_board_state,
                    move_coordinates=move_coordinates,
                )
                score_dict = get_score_dict(branch.board_state)
                if score_dict[stone] >= WINNING_SCORE:
                    branch.is_terminal = True
                yield branch

    def generate_branches_around_existing_moves(self, player="minimizer"):
        # I've returned this function to the code as I think I may want it later
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
                            branch = GoNode(
                                move_id=self.generate_move_id(),
                                player=player,
                                board_state=new_board_state,
                                move_coordinates=move_coordinates,
                            )
                            branch.set_score(branch.get_utility())
                            yield branch

    def find_moves_around_position(self, x_coordinate, y_coordinate):
        # I've returned this function to the code as I think I may want it later
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

    # TODO find_connecting_stones():
