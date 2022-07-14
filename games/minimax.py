class MinimaxNode:
    def __init__(
        self,
        move_id=None,
        player=None,
        score=None,
        is_terminal=False,
        leaves=[],
    ):
        self.leaves = leaves
        self.move_id = move_id
        self.player = player
        self.is_terminal = is_terminal
        self.score = score

    def __str__(self):
        return (
            f"move_id: {self.get_move_id()}, "
            f"score: {self.get_score()}, "
            f"number of leaves: {len(self.get_leaves())}"
        )

    def set_score(self, score):
        self.score = score

    def get_score(self):
        return self.score

    def get_move_id(self):
        return self.move_id

    def add_leaf(self, move_id=None, player=None, score=None):
        leaf = MinimaxNode(move_id, player, score)
        self.leaves.append(leaf)

    def get_leaves(self):
        return self.leaves

    def get_optimal_move(self):
        # input is Node, output is Node
        best_move = self.leaves[0]
        player = best_move.player
        best_score = best_move.get_score()

        strategy = self.maximizer_strategy
        if player == "minimizer":
            strategy = self.minimizer_strategy

        for leaf in self.leaves:
            leaf_score = leaf.get_score()
            if strategy(leaf_score, best_score):
                best_move = leaf
                best_score = best_move.get_score()
        return best_move

    def maximizer_strategy(self, leaf_score, best_score):
        return leaf_score > best_score

    def minimizer_strategy(self, leaf_score, best_score):
        return leaf_score < best_score

    def get_utility(self):
        # Implemented by class which inherits
        return

    def evaluate_node(self, leaf, maximizer_choice_node, minimizer_choice_node):
        # input is node, output is node
        # adapted from: https://www.hackerearth.com/blog/developers/minimax-algorithm-alpha-beta-pruning/
        if self.is_terminal:
            self.set_score(self.get_utility())
            return self

        if self.player == "minimizer":
            for leaf in self.leaves:
                minimizer_choice_node = self.node_min(
                    minimizer_choice_node,
                    self.evaluate(leaf, maximizer_choice_node, minimizer_choice_node),
                )
                if (
                    minimizer_choice_node.get_score()
                    <= maximizer_choice_node.get_score()
                ):
                    return minimizer_choice_node
                return minimizer_choice_node

        if self.player == "maximizer":
            for leaf in self.leaves:
                maximizer_choice_node = self.node_max(
                    maximizer_choice_node,
                    self.evaluate(leaf, maximizer_choice_node, minimizer_choice_node),
                )
                if (
                    minimizer_choice_node.get_score()
                    <= maximizer_choice_node.get_score()
                ):
                    return maximizer_choice_node
                return maximizer_choice_node

    def node_min(self, first_node, second_node):
        if second_node.get_score() < first_node.get_score():
            return second_node
        return first_node

    def node_max(self, first_node, second_node):
        if second_node.get_score() > first_node.get_score():
            return second_node
        return first_node
