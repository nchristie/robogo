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

MAX_TREE_DEPTH = 15

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
        branches=[],
        board_state=None,
        move_coordinates=(),
        optimal_move_coordinates=None,
    ):
        super().__init__(move_id, player, score, branches)
        self.board_state = board_state
        self.move_coordinates = move_coordinates
        self.optimal_move_coordinates = optimal_move_coordinates

    def build_game_tree(self, depth):
        """
        Starts from current node and builds game tree to a given
        depth

        Parameters:
            depth (int): how far down the tree we want to build
        """
        # Base case
        # If we're at a terminal node leave the recursion
        if depth == 0:
            # print(f"candidate_move_node {type(self)}")
            # print(f"depth: {depth}, move_id: {self.move_id} is_leaf_node: {self.is_leaf_node()}")
            # print(f"returning at depth of {depth} owing to terminal node")
            return

        # recurse case
        # first build tree horizontally
        for candidate_move_node in self.generate_next_node():
            # print(f"candidate_move_node {type(candidate_move_node)}")
            # print(f"depth: {depth}, move_id: {candidate_move_node.move_id} is_leaf_node: {candidate_move_node.is_leaf_node()}")
            self.branches.append(candidate_move_node)

        # next use recursion to build tree vertically
        depth-=1
        for branch in self.branches:
            return branch.build_game_tree(depth)

        # print(f"Returning because end of function depth {depth}")
        return


    def find_depth(self, depth):
        if depth > MAX_TREE_DEPTH:
            raise Exception(f"Maximum tree depth of {MAX_TREE_DEPTH} exceeded")

        # Base case
        # If we're at a terminal node leave the recursion
        if self.is_leaf_node():
            print(f"candidate_move_node {type(self)}")
            print(f"depth: {depth}, move_id: {self.move_id} is_leaf_node: {self.is_leaf_node()}")
            print(f"returning at depth of {depth} owing to terminal node")
            return depth

        # recurse case
        depth+=1
        for i, branch in enumerate(self.branches):
            print(f"candidate_move_node {type(branch)}")
            print(f"depth: {depth}, branch index: {i}, move_id: {branch.move_id} is_leaf_node: {branch.is_leaf_node()}")
            return branch.find_depth(depth)

        print(f"Returning because end of function depth {depth}")
        return


    def alternate_player(self):
        """
        Returns:
            str: The opposite player to that of the current
            node. Valid options: "minimizer", "maximizer".
        """
        if self.player == "minimizer":
            return "maximizer"
        return "minimizer"

    def generate_next_node(self):
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
                next_node = GoNode(
                    move_id=self.generate_move_id(),
                    player=player,
                    board_state=new_board_state,
                    move_coordinates=move_coordinates,
                )
                # print(next_node.move_id)
                # score_dict = get_score_dict(next_node.board_state)
                yield next_node

    def generate_next_node_around_existing_moves(self, player="minimizer"):
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
        """
        Creates a unique id for each move
        Returns:
            uuid
        """
        return str(uuid.uuid4())

    def get_utility(self):
        """
        Finds value of node. To be used for terminal nodes only
        Returns:
            int corresponding to black's score relative to white's
        """
        score_dict = get_score_dict(self.board_state)
        return score_dict["relative_black_score"]

    # TODO find_connecting_stones():
