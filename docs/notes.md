# Useful Notes

Run via docker-compose using:
```
docker-compose run --rm web django-admin [django command here]
```

Migrations
```
docker-compose run --rm web python manage.py makemigrations games

docker-compose run --rm web python manage.py migrate
```

Bring up server
```
docker-compose up --rm web
docker-compose run --rm web python manage.py runserver
```

Tests
```
docker-compose run --rm web python manage.py test
```

shell:
docker-compose run --rm web python manage.py shell

from games.models import Game, Move; games = Game.objects.order_by('-id'); [game.delete() for game in games] # deletes all games

My IP:
172.24.0.1

def evaluate(self, maximizer_choice, minimizer_choice):
    # adapted from: https://www.hackerearth.com/blog/developers/minimax-algorithm-alpha-beta-pruning/
    if self.is_terminal():
        return self.utility()

    if self.player == "minimizer":
        for leaf in self.leaves:
            minimizer_choice = min(minimizer_choice, self.evaluate(leaf, maximizer_choice, minimizer_choice))
            if minimizer_choice <= maximizer_choice:
                return minimizer_choice
            return minimizer_choice

    if self.player == "maximizer":
        for leaf in self.leaves:
            maximizer_choice = max(maximizer_choice, self.evaluate(leaf, maximizer_choice, minimizer_choice))
            if minimizer_choice <= maximizer_choice:
                return maximizer_choice
            return maximizer_choice

def build_game_tree(board_state):
    my_node.set_leaves(player="minimizer", is_terminal=False) # depth of 1
    for child_node in my_node.leaves:
        child_node.set_leaves(player="minimizer", is_terminal=False) # depth of 2
        for grandchild_node in child_node.leaves:
            grandchild_node.set_leaves(player="minimizer", is_terminal=True) # depth of 3

# Generator example:
# source https://wiki.python.org/moin/Generators
def firstn(n):
    num = 0
    while num < n:
        yield num
        num += 1

x = firstn(10)
next(x)

# very simple recursion
def count_down(start):
    print(start)
    next = start - 1
    if next > 0:
        count_down(next)

NEXT PLAYER:
Whether the node is a maximizing node or a minimizing node depends on whose turn it is next to play. In our game, white (the computer) wants the lowest possible score for black (the human). So if the node was a white player's turn (i.e. the move coordinates represent a white move on the board) then that node is not a minimizer node, as the next player to move is black, i.e. the maximizer. I'm pretty sure I've had this backwards for the whole time I've been working on the algorithm so need to make some big changes.

Looking at the function: get_optimal_move, it seems originally the way I was handling this was to use the player from the child node. One option is to continue doing this as it will mean fewer changes required to the unit tests. Another option is to flip maximizer and minimizer in all the unit tests and get the value from the parent node.