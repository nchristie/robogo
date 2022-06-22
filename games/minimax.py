import uuid

class Node:
    def __init__(
        self, 
        move_id=None, 
        player=None, 
        score=None,
        leaf_getter=None
    ):
        self.leaves = []
        self.move_id=move_id
        self.player=player
        self.score = score   
        self.leaf_getter = leaf_getter 
    
    def set_score(self, score):
        self.score = score
    
    def get_score(self):
        return self.score
    
    def get_move_id(self):
        return self.move_id
    
    def add_leaf(self, move_id=None, player=None, score=None):
        leaf = Node(move_id, player, score)
        self.leaves.append(leaf)
    
    def get_leaves(self):
        return self.leaves
    
    def get_logical_move(self):
        leaves = self.get_leaves()
        player = leaves[0].player
        if player == "maximizer":
            return self.get_maximizer_move(leaves)
        if player == "minimizer":
            return self.get_minimizer_move(leaves)
    
    def get_maximizer_move(self, leaves):
        maximizer_move = leaves[0]
        for leaf in leaves:
            leaf_score = leaf.get_score()
            max_score = maximizer_move.get_score()
            if leaf_score > max_score:
                maximizer_move = leaf
        return maximizer_move
    
    def get_minimizer_move(self, leaves):
        minimizer_move = leaves[0]
        for leaf in leaves:
            leaf_score = leaf.get_score()
            min_score = minimizer_move.get_score()
            if leaf_score < min_score:
                minimizer_move = leaf
        return minimizer_move

class LeafGetter:
    def __init__(self):
        self.INTERSECTION = "+"
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
        for i, row in enumerate(board_state):
            for j, cell in enumerate(row):
                if cell == self.BLACK_STONE:
                    continue
                    

        return
    
    def find_intersections(self, x_coordinate, y_coordinate, board_size):
        up = (x_coordinate - 1, y_coordinate)
        left = (x_coordinate, y_coordinate - 1)
        right = (x_coordinate, y_coordinate + 1)
        down = (x_coordinate + 1, y_coordinate)
        return [up, left, right, down]



def generate_move_id():
    return str(uuid.uuid4())

    
