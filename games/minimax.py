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

    def generate_leaves(self):
        # implemented by inheritor
        return

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
        print("In minimax get_utility")
        # Implemented by class which inherits
        return

    def evaluate_node(self, node, maximizer_choice_node, minimizer_choice_node, depth):
        # input is node, output is node
        # adapted from: https://www.hackerearth.com/blog/developers/minimax-algorithm-alpha-beta-pruning/
        # and https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-4-alpha-beta-pruning/
        depth -= 1

        if depth <= 0:
            node.is_terminal = True

        if node.is_terminal:
            print(f"terminal node found at depth of {depth}")
            node.set_score(node.get_utility())
            return node

        if node.player == "minimizer":
            for leaf in node.generate_leaves():
                minimizer_choice_node = node.node_min(
                    minimizer_choice_node,
                    node.evaluate_node(leaf, maximizer_choice_node, minimizer_choice_node, depth),
                )
                if (
                    minimizer_choice_node.get_score()
                    <= maximizer_choice_node.get_score()
                ):
                    return minimizer_choice_node
                return minimizer_choice_node

        if node.player == "maximizer":
            for leaf in node.generate_leaves():
                maximizer_choice_node = node.node_max(
                    maximizer_choice_node,
                    node.evaluate_node(leaf, maximizer_choice_node, minimizer_choice_node, depth),
                )
                if (
                    minimizer_choice_node.get_score()
                    <= maximizer_choice_node.get_score()
                ):
                    return maximizer_choice_node
                return maximizer_choice_node

    def build_minimax_alpha_beta_game_tree(self, node, maximizer_choice_node, minimizer_choice_node, depth):
        # input is node, output is node
        # TODO input is node, output is the best available value,
        # TODO side effect is setting values on entire tree
        # adapted from: https://www.hackerearth.com/blog/developers/minimax-algorithm-alpha-beta-pruning/
        # and https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-4-alpha-beta-pruning/
        depth -= 1

        if depth < 0:
            raise Exception("Error: depth is <0")

        if depth == 0:
            node.is_terminal = True

        if node.is_terminal:
            print(f"terminal node found at depth of {depth}")
            node_score = node.get_utility()
            node.set_score(node_score)
            return node_score

        if node.player == "minimizer":
            for leaf in node.generate_leaves():
                node.add_leaf(leaf)
                minimizer_choice_node = node.node_min(
                    minimizer_choice_node,
                    node.evaluate_node(leaf, maximizer_choice_node, minimizer_choice_node, depth),
                )
                if (
                    minimizer_choice_node.get_score()
                    <= maximizer_choice_node.get_score()
                ):
                    node.set_score(minimizer_choice_node.get_score())
                    return minimizer_choice_node.get_score()
                node.set_score(minimizer_choice_node.get_score())
                return minimizer_choice_node.get_score()

        if node.player == "maximizer":
            for leaf in node.generate_leaves():
                node.add_leaf(leaf)
                maximizer_choice_node = node.node_max(
                    maximizer_choice_node,
                    node.evaluate_node(leaf, maximizer_choice_node, minimizer_choice_node, depth),
                )
                if (
                    minimizer_choice_node.get_score()
                    <= maximizer_choice_node.get_score()
                ):
                    node.set_score(maximizer_choice_node.get_score())
                    return maximizer_choice_node.get_score()
                node.set_score(maximizer_choice_node.get_score())
                return maximizer_choice_node.get_score()


    def node_min(self, first_node, second_node):
        if second_node.get_score() < first_node.get_score():
            return second_node
        return first_node

    def node_max(self, first_node, second_node):
        if second_node.get_score() > first_node.get_score():
            return second_node
        return first_node
