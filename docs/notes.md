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

from games.models import Game, Move

game = Game.objects.order_by('-id')[0]
game.move_set.all()  # queryset of related Moves
game.delete() # deletes current game

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