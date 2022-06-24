class Node:
    def __init__(
        self,
        move_id=None,
        player=None,
        score=None,
        leaves=[],
    ):
        self.leaves = leaves
        self.move_id=move_id
        self.player=player
        self.score = score

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

    def get_optimal_move(self):
        if self.player == "maximizer":
            return self.get_maximizer_move()
        if self.player == "minimizer":
            return self.get_minimizer_move()
        else:
            return self.get_maximizer_move()

    def get_maximizer_move(self):
        maximizer_move = self.leaves[0]
        for leaf in self.leaves:
            leaf_score = leaf.get_score()
            max_score = maximizer_move.get_score()
            if leaf_score > max_score:
                maximizer_move = leaf
        return maximizer_move

    def get_minimizer_move(self):
        minimizer_move = self.leaves[0]
        for leaf in self.leaves:
            leaf_score = leaf.get_score()
            min_score = minimizer_move.get_score()
            if leaf_score < min_score:
                minimizer_move = leaf
        return minimizer_move


