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


# Handy for seeing board state from pdb
[print(f"{row}") for row in board_state]

[print(child) for child in tree_0809_0414.root_node.get_children()[3].get_children()[7].get_children()[7].get_children()[10].get_children()[0].board_state]


(Pdb) [print(row) for row in tree_0809_0414.root_node.get_children()[3].board_state]
['●', '○', '+', '+', '+']
['○', '+', '+', '+', '+']
['●', '+', '+', '+', '+']
['+', '+', '+', '+', '+']
['+', '+', '+', '+', '+']
[None, None, None, None, None]
(Pdb) [print(row) for row in tree_0809_0414.root_node.get_children()[3].get_children()[7].board_state]
['●', '○', '+', '+', '+']
['○', '+', '+', '+', '+']
['●', '●', '+', '+', '+']
['+', '+', '+', '+', '+']
['+', '+', '+', '+', '+']
[None, None, None, None, None]
(Pdb) [print(row) for row in tree_0809_0414.root_node.get_children()[3].get_children()[7].get_children()[7].board_state]
['●', '○', '+', '+', '+']
['○', '+', '+', '+', '+']
['●', '●', '○', '+', '+']
['+', '+', '+', '+', '+']
['+', '+', '+', '+', '+']
[None, None, None, None, None]
(Pdb) [print(row) for row in tree_0809_0414.root_node.get_children()[3].get_children()[7].get_children()[7].get_children[10].board_state]
*** TypeError: 'method' object is not subscriptable
(Pdb) [print(row) for row in tree_0809_0414.root_node.get_children()[3].get_children()[7].get_children()[7].get_children()[10].board_state]
['●', '○', '+', '+', '+']
['○', '+', '+', '+', '+']
['●', '●', '○', '+', '+']
['+', '●', '+', '+', '+']
['+', '+', '+', '+', '+']
[None, None, None, None, None]


[
['●', '○', '●', '+', '+'],
['○', '+', '●', '+', '+'],
['+', '+', '+', '+', '+'],
['+', '+', '+', '+', '+'],
['+', '+', '+', '+', '+'],
]

TIMING MINIMAX:
I timed running minimax on the second move in the game with board state of latest move black to (1, 0):

     0   1    2   3   4   5    6   7   8
0     ●   ●   +   +   +   +   +   +   +
1     ○   +   +   +   +   +   +   +   +
2     +   +   +   +   +   +   +   +   +
3     +   +   +   +   +   +   +   +   +
4     +   +   +   +   +   +   +   +   +
5     +   +   +   +   +   +   +   +   +
6     +   +   +   +   +   +   +   +   +
7     +   +   +   +   +   +   +   +   +
8     +   +   +   +   +   +   +   +   +

## 1

BOARD_SIZE = 9
WINNING_SCORE = 5
MAX_TREE_DEPTH = 2
child getter = get_all_children_and_rank_by_proximity

Calculated white move: (1,1)
Minimax seconds to execute: 0.6395

## 2
BOARD_SIZE = 9
WINNING_SCORE = 5
MAX_TREE_DEPTH = 3
child getter = get_all_children_and_rank_by_proximity

Calculated white move: (1,1)
Minimax seconds to execute: 60.1060

## 3
BOARD_SIZE = 9
WINNING_SCORE = 5
MAX_TREE_DEPTH = 3
child getter = generate_next_child

Calculated white move: (0,2)
Minimax seconds to execute: 48.8770

## 4
BOARD_SIZE = 9
WINNING_SCORE = 5
MAX_TREE_DEPTH = 3
child getter = generate_next_child_and_rank_by_proximity

Calculated white move: (1,1)
Minimax seconds to execute: 55.3870

## 5
Reduce board size
    0   1    2   3   4
0     ●   ●   +   +   +
1     ○   +   +   +   +
2     +   +   +   +   +
3     +   +   +   +   +
4     +   +   +   +   +


BOARD_SIZE = 5
WINNING_SCORE = 3
MAX_TREE_DEPTH = 2
child getter = generate_next_child_and_rank_by_proximity

Calculated white move: (1,0)
Minimax seconds to execute: 0.0127

## 6
BOARD_SIZE = 5
WINNING_SCORE = 3
MAX_TREE_DEPTH = 3
child getter = generate_next_child_and_rank_by_proximity

Calculated white move:          (1,0)
Minimax seconds to execute:     0.1270

## 7
BOARD_SIZE = 5
WINNING_SCORE = 3
MAX_TREE_DEPTH = 4
child getter = generate_next_child_and_rank_by_proximity

Calculated white move:          (1,0)
Minimax seconds to execute:     0.7301

## 8
BOARD_SIZE = 5
WINNING_SCORE = 3
MAX_TREE_DEPTH = 5
child getter = generate_next_child_and_rank_by_proximity

Calculated white move:          (1,0)
Minimax seconds to execute:     3.5241

## 9
BOARD_SIZE = 5
WINNING_SCORE = 3
MAX_TREE_DEPTH = 6
child getter = generate_next_child_and_rank_by_proximity

Calculated white move:          (1,0)
Minimax seconds to execute:     19.7513

## 10
BOARD_SIZE = 5
WINNING_SCORE = 3
MAX_TREE_DEPTH = 6
child getter = generate_next_child_and_rank_by_proximity
minimax algo = prune_game_tree_recursive

Calculated white move:          (1,0)
Minimax seconds to execute:     22.0170

## 11
Removes all logging and reference to node ids from prune_game_tree_recursive

BOARD_SIZE = 5
WINNING_SCORE = 3
MAX_TREE_DEPTH = 6
child getter = generate_next_child_and_rank_by_proximity
minimax algo = prune_game_tree_recursive

Calculated white move:          (1,0)
Minimax seconds to execute:     20.9708

## 12
Use generate_next_child_and_rank_by_proximity_to_latest_move

BOARD_SIZE = 5
WINNING_SCORE = 3
MAX_TREE_DEPTH = 6
child getter = generate_next_child_and_rank_by_proximity_to_latest_move
minimax algo = prune_game_tree_recursive

Calculated white move:          (1,0)
Minimax seconds to execute:     46.4902

## 13
Pass in latest move coordinates

BOARD_SIZE = 5
WINNING_SCORE = 3
MAX_TREE_DEPTH = 6
child getter = generate_next_child_and_rank_by_proximity_to_latest_move
minimax algo = prune_game_tree_recursive

Calculated white move:          (1,0)
Minimax seconds to execute:     3.2719

## 14
BOARD_SIZE = 5
WINNING_SCORE = 3
MAX_TREE_DEPTH = 7
child getter = generate_next_child_and_rank_by_proximity_to_latest_move
minimax algo = prune_game_tree_recursive

Calculated white move:          (1,0)
Minimax seconds to execute:     18.7037

## 15
BOARD_SIZE = 5
WINNING_SCORE = 3
MAX_TREE_DEPTH = 6
child getter = generate_next_child_and_rank_by_proximity_to_latest_move
minimax algo = prune_game_tree_recursive

Calculated white move:          (1,0)
Minimax seconds to execute:     14.6365

## 16
BOARD_SIZE = 5
WINNING_SCORE = 4
MAX_TREE_DEPTH = 6
child getter = generate_next_child_and_rank_by_proximity_to_latest_move
minimax algo = prune_game_tree_recursive

Calculated white move:          unknown
Minimax seconds to execute:     more than I had patience for

## 17
BOARD_SIZE = 5
WINNING_SCORE = 4
MAX_TREE_DEPTH = 5
child getter = generate_next_child_and_rank_by_proximity_to_latest_move
minimax algo = prune_game_tree_recursive

Calculated white move:          unknown
Minimax seconds to execute:     more than I had patience for

## 17
BOARD_SIZE = 5
WINNING_SCORE = 4
MAX_TREE_DEPTH = 4
child getter = generate_next_child_and_rank_by_proximity_to_latest_move
minimax algo = prune_game_tree_recursive

Calculated white move:          (4,0)
Minimax seconds to execute:     7.3933

## 17
BOARD_SIZE = 5
WINNING_SCORE = 5
MAX_TREE_DEPTH = 4
child getter = generate_next_child_and_rank_by_proximity_to_latest_move
minimax algo = prune_game_tree_recursive

Calculated white move:          (4,0)
Minimax seconds to execute:     8.2440

## 18
BOARD_SIZE = 5
WINNING_SCORE = 5
MAX_TREE_DEPTH = 5
child getter = generate_next_child_and_rank_by_proximity_to_latest_move
minimax algo = prune_game_tree_recursive

Calculated white move:          unknown
Minimax seconds to execute:     more than I had patience for


## 19
Cap jump size to integer of board_size/2 and switch back to generate_next_child_and_rank_by_proximity

BOARD_SIZE = 5
WINNING_SCORE = 5
MAX_TREE_DEPTH = 4
child getter = generate_next_child_and_rank_by_proximity
minimax algo = prune_game_tree_recursive

Calculated white move:          (2,0)
Minimax seconds to execute:     0.1324

## 20
BOARD_SIZE = 5
WINNING_SCORE = 5
MAX_TREE_DEPTH = 5
child getter = generate_next_child_and_rank_by_proximity
minimax algo = prune_game_tree_recursive

Calculated white move:          (2,0)
Minimax seconds to execute:     1.5301

## 21
BOARD_SIZE = 6
WINNING_SCORE = 5
MAX_TREE_DEPTH = 5
child getter = generate_next_child_and_rank_by_proximity
minimax algo = prune_game_tree_recursive

Calculated white move:          unknown
Minimax seconds to execute:     more than I had patience for

## 22
Cap jump size to roundup(board_size/3)
BOARD_SIZE = 5
WINNING_SCORE = 5
MAX_TREE_DEPTH = 5
child getter = generate_next_child_and_rank_by_proximity
minimax algo = prune_game_tree_recursive

Calculated white move:          (2,0)
Minimax seconds to execute:     1.4438

## 23
Cap jump size to roundup(board_size/3)
BOARD_SIZE = 5
WINNING_SCORE = 5
MAX_TREE_DEPTH = 6
child getter = generate_next_child_and_rank_by_proximity
minimax algo = prune_game_tree_recursive

Calculated white move:          (2,0)
Minimax seconds to execute:     16.0951

## 24
Cap jump size to roundup(board_size/3)
BOARD_SIZE = 6
WINNING_SCORE = 5
MAX_TREE_DEPTH = 5
child getter = generate_next_child_and_rank_by_proximity
minimax algo = prune_game_tree_recursive

Calculated white move:          (2,0)
Minimax seconds to execute:     1.8772

## 25
Cap jump size to roundup(board_size/3)
BOARD_SIZE = 7
WINNING_SCORE = 5
MAX_TREE_DEPTH = 5
child getter = generate_next_child_and_rank_by_proximity
minimax algo = prune_game_tree_recursive

Calculated white move:          unknown
Minimax seconds to execute:     more than I had patience for

## 26
Cap jump size to roundup(board_size/3)
BOARD_SIZE = 7
WINNING_SCORE = 5
MAX_TREE_DEPTH = 4
child getter = generate_next_child_and_rank_by_proximity
minimax algo = prune_game_tree_recursive

Calculated white move:          (3,0)
Minimax seconds to execute:     9.5427

## 27
Cap jump size to roundup(board_size/3)
Vary depth of tree search by how many moves left on board
BOARD_SIZE = 9
WINNING_SCORE = 5
MAX_TREE_DEPTH = 10
child getter = generate_next_child_and_rank_by_proximity
minimax algo = prune_game_tree_recursive

Found that some moves took up to around 10 seconds to calculate but human still was able to easily win

## 28
Cap jump size to roundup(board_size/3)
Vary depth of tree search by how many moves left on board
BOARD_SIZE = 5
WINNING_SCORE = 4
MAX_TREE_DEPTH = 5
child getter = generate_next_child_and_rank_by_proximity
minimax algo = prune_game_tree_recursive
move 1 black (3, 3)
move 2 white (3, 2)
move 3 black (1, 3)
move 4 white (2, 3) - blocks

web_1  | Executing minimax, searching to depth of 4, open moves: 88%
web_1  |
web_1  | >>> >>> Minimax seconds to execute: 1.0535 <<< <<<


## 29
Cap jump size to roundup(board_size/3)
Fixed depth
BOARD_SIZE = 5
WINNING_SCORE = 4
MAX_TREE_DEPTH = 4
child getter = generate_next_child_and_rank_by_proximity
minimax algo = build_and_prune_game_tree_recursive
move 1 black (3, 3)
move 2 white (2, 2)
move 3 black (1, 3)
move 4 white (2, 3) - blocks

web_1  | >>> >>> Minimax seconds to execute: 1.6575 <<< <<<




## Example game output:

web_1  | [16/Aug/2022 04:09:22] "POST /games/ HTTP/1.1" 200 764
web_1  | Couldn't find game for ip: 172.24.0.1, creating new game
web_1  | user_game id: 775
web_1  | No black stones on board
web_1  | [16/Aug/2022 04:09:29] "GET /games/ HTTP/1.1" 200 1822
web_1  | Found game for ip: 172.24.0.1
web_1  | user_game id: 775
web_1  | last move coordinates: (3, 3)
web_1  |
web_1  | >>> >>> Minimax seconds to execute: 0.5817 <<< <<<
web_1  |
web_1  | root node: node_id: root_node, number of children: 8, player_to_move: minimizer, move_coordinates: (), path_depth: 0
web_1  | Move 0 score: 1
web_1  | ['+', '+', '+', '+', '+']
web_1  | ['+', '+', '+', '+', '+']
web_1  | ['+', '+', '○', '+', '+']
web_1  | ['+', '+', '+', '●', '+']
web_1  | ['+', '+', '+', '+', '+']
web_1  | Move 1 score: 1
web_1  | ['+', '+', '+', '+', '+']
web_1  | ['+', '+', '+', '+', '+']
web_1  | ['+', '+', '○', '+', '+']
web_1  | ['+', '+', '●', '●', '+']
web_1  | ['+', '+', '+', '+', '+']
web_1  | Move 2 score: 1
web_1  | ['+', '+', '+', '+', '+']
web_1  | ['+', '+', '+', '+', '+']
web_1  | ['+', '○', '○', '+', '+']
web_1  | ['+', '+', '●', '●', '+']
web_1  | ['+', '+', '+', '+', '+']
web_1  | Move 3 score: 1
web_1  | ['+', '+', '+', '+', '+']
web_1  | ['+', '+', '+', '+', '+']
web_1  | ['+', '○', '○', '+', '+']
web_1  | ['+', '●', '●', '●', '+']
web_1  | ['+', '+', '+', '+', '+']
web_1  | white_move_node: node_id: d4-i0_root_node, number of children: 12, player_to_move: maximizer, move_coordinates: (2, 2), path_depth: 0
web_1  | [16/Aug/2022 04:09:37] "POST /games/ HTTP/1.1" 200 1624
web_1  | Found game for ip: 172.24.0.1
web_1  | user_game id: 775
web_1  | last move coordinates: (3, 1)
web_1  |
web_1  | >>> >>> Minimax seconds to execute: 1.8170 <<< <<<
web_1  |
web_1  | root node: node_id: root_node, number of children: 15, player_to_move: minimizer, move_coordinates: (), path_depth: 0
web_1  | Move 0 score: 0
web_1  | ['+', '+', '+', '+', '+']
web_1  | ['+', '+', '+', '●', '+']
web_1  | ['+', '+', '○', '○', '+']
web_1  | ['+', '+', '+', '●', '+']
web_1  | ['+', '+', '+', '+', '+']
web_1  | Move 1 score: 0
web_1  | ['+', '+', '+', '+', '+']
web_1  | ['+', '●', '+', '●', '+']
web_1  | ['+', '+', '○', '○', '+']
web_1  | ['+', '+', '+', '●', '+']
web_1  | ['+', '+', '+', '+', '+']
web_1  | Move 2 score: 0
web_1  | ['+', '+', '+', '+', '+']
web_1  | ['+', '●', '+', '●', '+']
web_1  | ['+', '○', '○', '○', '+']
web_1  | ['+', '+', '+', '●', '+']
web_1  | ['+', '+', '+', '+', '+']
web_1  | Move 3 score: 0
web_1  | ['+', '+', '+', '+', '+']
web_1  | ['+', '●', '●', '●', '+']
web_1  | ['+', '○', '○', '○', '+']
web_1  | ['+', '+', '+', '●', '+']
web_1  | ['+', '+', '+', '+', '+']
web_1  | white_move_node: node_id: d4-i4_root_node, number of children: 14, player_to_move: maximizer, move_coordinates: (3, 2), path_depth: 0
web_1  | [16/Aug/2022 04:09:47] "POST /games/ HTTP/1.1" 200 1628
web_1  | Found game for ip: 172.24.0.1
web_1  | user_game id: 775
web_1  | last move coordinates: (1, 2)
web_1  |
web_1  | >>> >>> Minimax seconds to execute: 4.4745 <<< <<<
web_1  |
web_1  | root node: node_id: root_node, number of children: 16, player_to_move: minimizer, move_coordinates: (), path_depth: 0
web_1  | Move 0 score: 0
web_1  | ['+', '+', '+', '+', '+']
web_1  | ['○', '+', '+', '●', '+']
web_1  | ['+', '●', '○', '○', '+']
web_1  | ['+', '+', '+', '●', '+']
web_1  | ['+', '+', '+', '+', '+']
web_1  | Move 1 score: 0
web_1  | ['+', '+', '+', '+', '+']
web_1  | ['○', '●', '+', '●', '+']
web_1  | ['+', '●', '○', '○', '+']
web_1  | ['+', '+', '+', '●', '+']
web_1  | ['+', '+', '+', '+', '+']
web_1  | Move 2 score: 0
web_1  | ['+', '+', '+', '+', '+']
web_1  | ['○', '●', '+', '●', '+']
web_1  | ['+', '●', '○', '○', '○']
web_1  | ['+', '+', '+', '●', '+']
web_1  | ['+', '+', '+', '+', '+']
web_1  | Move 3 score: 0
web_1  | ['+', '●', '+', '+', '+']
web_1  | ['○', '●', '+', '●', '+']
web_1  | ['+', '●', '○', '○', '○']
web_1  | ['+', '+', '+', '●', '+']
web_1  | ['+', '+', '+', '+', '+']
web_1  | white_move_node: node_id: d4-i0_root_node, number of children: 17, player_to_move: maximizer, move_coordinates: (0, 1), path_depth: 0
web_1  | [16/Aug/2022 04:10:04] "POST /games/ HTTP/1.1" 200 1632
web_1  | Found game for ip: 172.24.0.1
web_1  | user_game id: 775
web_1  | last move coordinates: (1, 1)
web_1  |
web_1  | >>> >>> Minimax seconds to execute: 1.4713 <<< <<<
web_1  |
web_1  | root node: node_id: root_node, number of children: 16, player_to_move: minimizer, move_coordinates: (), path_depth: 0
web_1  | node_id: d3-i0_d4-i1_root_node, number of children: 14, player_to_move: minimizer, move_coordinates: (0, 2), path_depth: 0
web_1  | node_id: d3-i1_d4-i1_root_node, number of children: 14, player_to_move: minimizer, move_coordinates: (0, 0), path_depth: 0
web_1  | node_id: d3-i2_d4-i1_root_node, number of children: 14, player_to_move: minimizer, move_coordinates: (2, 1), path_depth: 0
web_1  | node_id: d3-i3_d4-i1_root_node, number of children: 14, player_to_move: minimizer, move_coordinates: (2, 0), path_depth: 0
web_1  | node_id: d3-i4_d4-i1_root_node, number of children: 16, player_to_move: minimizer, move_coordinates: (0, 3), path_depth: 0
web_1  | node_id: d3-i5_d4-i1_root_node, number of children: 16, player_to_move: minimizer, move_coordinates: (1, 3), path_depth: 0
web_1  | node_id: d3-i6_d4-i1_root_node, number of children: 15, player_to_move: minimizer, move_coordinates: (2, 3), path_depth: 0
web_1  | node_id: d3-i7_d4-i1_root_node, number of children: 14, player_to_move: minimizer, move_coordinates: (4, 2), path_depth: 0
web_1  | node_id: d3-i8_d4-i1_root_node, number of children: 14, player_to_move: minimizer, move_coordinates: (4, 1), path_depth: 0
web_1  | node_id: d3-i9_d4-i1_root_node, number of children: 14, player_to_move: minimizer, move_coordinates: (4, 0), path_depth: 0
web_1  | node_id: d3-i10_d4-i1_root_node, number of children: 14, player_to_move: minimizer, move_coordinates: (3, 0), path_depth: 0
web_1  | node_id: d3-i11_d4-i1_root_node, number of children: 14, player_to_move: minimizer, move_coordinates: (4, 3), path_depth: 0
web_1  | node_id: d3-i12_d4-i1_root_node, number of children: 15, player_to_move: minimizer, move_coordinates: (2, 4), path_depth: 0
web_1  | node_id: d3-i13_d4-i1_root_node, number of children: 14, player_to_move: minimizer, move_coordinates: (3, 4), path_depth: 0
web_1  | node_id: d3-i14_d4-i1_root_node, number of children: 14, player_to_move: minimizer, move_coordinates: (4, 4), path_depth: 0
web_1  | Move 0 score: 1
web_1  | ['+', '○', '+', '+', '+']
web_1  | ['○', '●', '+', '●', '+']
web_1  | ['+', '●', '○', '○', '+']
web_1  | ['+', '+', '+', '●', '+']
web_1  | ['+', '+', '+', '+', '+']
web_1  | Move 1 score: 1
web_1  | ['+', '○', '+', '+', '+']
web_1  | ['○', '●', '●', '●', '+']
web_1  | ['+', '●', '○', '○', '+']
web_1  | ['+', '+', '+', '●', '+']
web_1  | ['+', '+', '+', '+', '+']
web_1  | Move 2 score: 1
web_1  | ['+', '○', '+', '+', '+']
web_1  | ['○', '●', '●', '●', '○']
web_1  | ['+', '●', '○', '○', '+']
web_1  | ['+', '+', '+', '●', '+']
web_1  | ['+', '+', '+', '+', '+']
web_1  | Move 3 score: 1
web_1  | ['+', '○', '+', '+', '+']
web_1  | ['○', '●', '●', '●', '○']
web_1  | ['●', '●', '○', '○', '+']
web_1  | ['+', '+', '+', '●', '+']
web_1  | ['+', '+', '+', '+', '+']
web_1  | white_move_node: node_id: d4-i1_root_node, number of children: 15, player_to_move: maximizer, move_coordinates: (1, 0), path_depth: 0
web_1  | [16/Aug/2022 04:10:20] "POST /games/ HTTP/1.1" 200 1636
web_1  | Found game for ip: 172.24.0.1
web_1  | user_game id: 775
web_1  | last move coordinates: (2, 1)
web_1  |
web_1  | >>> >>> Minimax seconds to execute: 0.7950 <<< <<<
web_1  |
web_1  | root node: node_id: root_node, number of children: 14, player_to_move: minimizer, move_coordinates: (), path_depth: 0
web_1  | Move 0 score: 1
web_1  | ['+', '○', '+', '+', '+']
web_1  | ['○', '●', '●', '●', '○']
web_1  | ['+', '●', '○', '○', '+']
web_1  | ['+', '+', '+', '●', '+']
web_1  | ['+', '+', '+', '+', '+']
web_1  | Move 1 score: 1
web_1  | ['+', '○', '+', '+', '+']
web_1  | ['○', '●', '●', '●', '○']
web_1  | ['+', '●', '○', '○', '+']
web_1  | ['+', '●', '+', '●', '+']
web_1  | ['+', '+', '+', '+', '+']
web_1  | Move 2 score: 1
web_1  | ['+', '○', '+', '+', '+']
web_1  | ['○', '●', '●', '●', '○']
web_1  | ['+', '●', '○', '○', '+']
web_1  | ['+', '●', '+', '●', '+']
web_1  | ['+', '○', '+', '+', '+']
web_1  | Move 3 score: 1
web_1  | ['+', '○', '+', '+', '+']
web_1  | ['○', '●', '●', '●', '○']
web_1  | ['●', '●', '○', '○', '+']
web_1  | ['+', '●', '+', '●', '+']
web_1  | ['+', '○', '+', '+', '+']
web_1  | white_move_node: node_id: d4-i8_root_node, number of children: 13, player_to_move: maximizer, move_coordinates: (4, 1), path_depth: 0
web_1  | [16/Aug/2022 04:10:32] "POST /games/ HTTP/1.1" 200 1640
web_1  | Found game for ip: 172.24.0.1
web_1  | user_game id: 775
web_1  | last move coordinates: (1, 3)
web_1  |
web_1  | >>> >>> Minimax seconds to execute: 0.2856 <<< <<<
web_1  |
web_1  | root node: node_id: root_node, number of children: 14, player_to_move: minimizer, move_coordinates: (), path_depth: 0
web_1  | Move 0 score: 100
web_1  | ['+', '○', '+', '+', '+']
web_1  | ['○', '●', '●', '●', '○']
web_1  | ['○', '●', '○', '○', '+']
web_1  | ['+', '●', '+', '●', '+']
web_1  | ['+', '+', '+', '+', '+']
web_1  | Move 1 score: 100
web_1  | ['+', '○', '+', '+', '+']
web_1  | ['○', '●', '●', '●', '○']
web_1  | ['○', '●', '○', '○', '+']
web_1  | ['●', '●', '+', '●', '+']
web_1  | ['+', '+', '+', '+', '+']
web_1  | Move 2 score: 100
web_1  | ['○', '○', '+', '+', '+']
web_1  | ['○', '●', '●', '●', '○']
web_1  | ['○', '●', '○', '○', '+']
web_1  | ['●', '●', '+', '●', '+']
web_1  | ['+', '+', '+', '+', '+']
web_1  | Move 3 score: 100
web_1  | ['○', '○', '+', '+', '+']
web_1  | ['○', '●', '●', '●', '○']
web_1  | ['○', '●', '○', '○', '+']
web_1  | ['●', '●', '+', '●', '+']
web_1  | ['+', '●', '+', '+', '+']
web_1  | white_move_node: node_id: d4-i0_root_node, number of children: 2, player_to_move: maximizer, move_coordinates: (0, 2), path_depth: 0
web_1  | [16/Aug/2022 04:10:52] "POST /games/ HTTP/1.1" 200 1644
web_1  | Found game for ip: 172.24.0.1
web_1  | user_game id: 775
web_1  | last move coordinates: (2, 3)
web_1  |
web_1  | >>> >>> Minimax seconds to execute: 0.0292 <<< <<<
web_1  |
web_1  | root node: node_id: root_node, number of children: 12, player_to_move: minimizer, move_coordinates: (), path_depth: 0
web_1  | Move 0 score: 100
web_1  | ['+', '○', '○', '+', '+']
web_1  | ['○', '●', '●', '●', '○']
web_1  | ['○', '●', '○', '○', '+']
web_1  | ['+', '●', '●', '●', '+']
web_1  | ['+', '+', '+', '+', '+']
web_1  | Move 1 score: 100
web_1  | ['●', '○', '○', '+', '+']
web_1  | ['○', '●', '●', '●', '○']
web_1  | ['○', '●', '○', '○', '+']
web_1  | ['+', '●', '●', '●', '+']
web_1  | ['+', '+', '+', '+', '+']
web_1  | Move 2 score: 100
web_1  | ['●', '○', '○', '+', '+']
web_1  | ['○', '●', '●', '●', '○']
web_1  | ['○', '●', '○', '○', '+']
web_1  | ['○', '●', '●', '●', '+']
web_1  | ['+', '+', '+', '+', '+']
web_1  | Move 3 score: 100
web_1  | ['●', '○', '○', '+', '+']
web_1  | ['○', '●', '●', '●', '○']
web_1  | ['○', '●', '○', '○', '+']
web_1  | ['○', '●', '●', '●', '+']
web_1  | ['+', '●', '+', '+', '+']
web_1  | white_move_node: node_id: d4-i2_root_node, number of children: 1, player_to_move: maximizer, move_coordinates: (2, 0), path_depth: 0
web_1  | [16/Aug/2022 04:11:02] "POST /games/ HTTP/1.1" 200 1648
web_1  | Found game for ip: 172.24.0.1
web_1  | user_game id: 775
web_1  | [16/Aug/2022 04:11:16] "POST /games/ HTTP/1.1" 200 775


## Same game as above, depth of 5

web_1  | /code/games/game_logic.py changed, reloading.
web_1  | /code/games/game_logic.py changed, reloading.
web_1  | Watching for file changes with StatReloader
web_1  | Watching for file changes with StatReloader
web_1  | Performing system checks...
web_1  |
web_1  | System check identified no issues (0 silenced).
web_1  | August 16, 2022 - 04:13:50
web_1  | Django version 3.2.15, using settings 'go_app.settings'
web_1  | Starting development server at http://0.0.0.0:8000/
web_1  | Quit the server with CONTROL-C.
web_1  | Couldn't find game for ip: 172.24.0.1, creating new game
web_1  | user_game id: 776
web_1  | No black stones on board
web_1  | [16/Aug/2022 04:13:59] "GET /games/ HTTP/1.1" 200 1822
web_1  | Found game for ip: 172.24.0.1
web_1  | user_game id: 776
web_1  | last move coordinates: (3, 3)
web_1  |
web_1  | >>> >>> Minimax seconds to execute: 9.4209 <<< <<<
web_1  |
web_1  | root node: node_id: root_node, number of children: 8, player_to_move: minimizer, move_coordinates: (), path_depth: 0
web_1  | Move 0 score: 0
web_1  | ['+', '+', '+', '+', '+']
web_1  | ['+', '+', '+', '+', '+']
web_1  | ['+', '+', '○', '+', '+']
web_1  | ['+', '+', '+', '●', '+']
web_1  | ['+', '+', '+', '+', '+']
web_1  | Move 1 score: 0
web_1  | ['+', '+', '+', '+', '+']
web_1  | ['+', '+', '+', '+', '+']
web_1  | ['+', '+', '○', '+', '+']
web_1  | ['+', '+', '●', '●', '+']
web_1  | ['+', '+', '+', '+', '+']
web_1  | Move 2 score: 0
web_1  | ['+', '+', '+', '+', '+']
web_1  | ['+', '+', '+', '+', '+']
web_1  | ['+', '○', '○', '+', '+']
web_1  | ['+', '+', '●', '●', '+']
web_1  | ['+', '+', '+', '+', '+']
web_1  | Move 3 score: 0
web_1  | ['+', '+', '+', '+', '+']
web_1  | ['+', '+', '+', '+', '+']
web_1  | ['+', '○', '○', '+', '+']
web_1  | ['+', '●', '●', '●', '+']
web_1  | ['+', '+', '+', '+', '+']
web_1  | Move 4 score: 0
web_1  | ['+', '+', '+', '+', '+']
web_1  | ['+', '+', '+', '+', '+']
web_1  | ['○', '○', '○', '+', '+']
web_1  | ['+', '●', '●', '●', '+']
web_1  | ['+', '+', '+', '+', '+']
web_1  | white_move_node: node_id: d5-i0_root_node, number of children: 12, player_to_move: maximizer, move_coordinates: (2, 2), path_depth: 0
web_1  | [16/Aug/2022 04:14:16] "POST /games/ HTTP/1.1" 200 1624
web_1  | Found game for ip: 172.24.0.1
web_1  | user_game id: 776
web_1  | last move coordinates: (3, 1)
web_1  |
web_1  | >>> >>> Minimax seconds to execute: 26.5336 <<< <<<
web_1  |
web_1  | root node: node_id: root_node, number of children: 15, player_to_move: minimizer, move_coordinates: (), path_depth: 1
web_1  | Move 0 score: -1
web_1  | ['+', '+', '+', '+', '+']
web_1  | ['+', '+', '+', '●', '+']
web_1  | ['+', '+', '○', '○', '+']
web_1  | ['+', '+', '+', '●', '+']
web_1  | ['+', '+', '+', '+', '+']
web_1  | Move 1 score: -1
web_1  | ['+', '+', '+', '+', '+']
web_1  | ['+', '+', '+', '●', '+']
web_1  | ['+', '●', '○', '○', '+']
web_1  | ['+', '+', '+', '●', '+']
web_1  | ['+', '+', '+', '+', '+']
web_1  | Move 2 score: -1
web_1  | ['+', '+', '+', '+', '+']
web_1  | ['○', '+', '+', '●', '+']
web_1  | ['+', '●', '○', '○', '+']
web_1  | ['+', '+', '+', '●', '+']
web_1  | ['+', '+', '+', '+', '+']
web_1  | Move 3 score: -1
web_1  | ['+', '+', '+', '+', '+']
web_1  | ['○', '+', '+', '●', '+']
web_1  | ['●', '●', '○', '○', '+']
web_1  | ['+', '+', '+', '●', '+']
web_1  | ['+', '+', '+', '+', '+']
web_1  | Move 4 score: -1
web_1  | ['+', '+', '+', '+', '+']
web_1  | ['○', '+', '+', '●', '+']
web_1  | ['●', '●', '○', '○', '○']
web_1  | ['+', '+', '+', '●', '+']
web_1  | ['+', '+', '+', '+', '+']
web_1  | white_move_node: node_id: d5-i4_root_node, number of children: 14, player_to_move: maximizer, move_coordinates: (3, 2), path_depth: 0
web_1  | [16/Aug/2022 04:15:06] "POST /games/ HTTP/1.1" 200 1628
web_1  | Found game for ip: 172.24.0.1
web_1  | user_game id: 776
web_1  | last move coordinates: (1, 2)
web_1  |
web_1  | >>> >>> Minimax seconds to execute: 61.0895 <<< <<<
web_1  |
web_1  | root node: node_id: root_node, number of children: 16, player_to_move: minimizer, move_coordinates: (), path_depth: 0
web_1  | Move 0 score: 0
web_1  | ['+', '+', '+', '+', '+']
web_1  | ['○', '+', '+', '●', '+']
web_1  | ['+', '●', '○', '○', '+']
web_1  | ['+', '+', '+', '●', '+']
web_1  | ['+', '+', '+', '+', '+']
web_1  | Move 1 score: 0
web_1  | ['+', '+', '+', '+', '+']
web_1  | ['○', '●', '+', '●', '+']
web_1  | ['+', '●', '○', '○', '+']
web_1  | ['+', '+', '+', '●', '+']
web_1  | ['+', '+', '+', '+', '+']
web_1  | Move 2 score: 0
web_1  | ['+', '+', '+', '+', '+']
web_1  | ['○', '●', '+', '●', '+']
web_1  | ['○', '●', '○', '○', '+']
web_1  | ['+', '+', '+', '●', '+']
web_1  | ['+', '+', '+', '+', '+']
web_1  | Move 3 score: 0
web_1  | ['+', '●', '+', '+', '+']
web_1  | ['○', '●', '+', '●', '+']
web_1  | ['○', '●', '○', '○', '+']
web_1  | ['+', '+', '+', '●', '+']
web_1  | ['+', '+', '+', '+', '+']
web_1  | Move 4 score: 0
web_1  | ['○', '●', '+', '+', '+']
web_1  | ['○', '●', '+', '●', '+']
web_1  | ['○', '●', '○', '○', '+']
web_1  | ['+', '+', '+', '●', '+']
web_1  | ['+', '+', '+', '+', '+']
web_1  | white_move_node: node_id: d5-i0_root_node, number of children: 17, player_to_move: maximizer, move_coordinates: (0, 1), path_depth: 0
web_1  | [16/Aug/2022 04:16:25] "POST /games/ HTTP/1.1" 200 1632
web_1  | Found game for ip: 172.24.0.1
web_1  | user_game id: 776
web_1  | last move coordinates: (1, 1)
web_1  |
web_1  | >>> >>> Minimax seconds to execute: 18.1879 <<< <<<
web_1  |
web_1  | root node: node_id: root_node, number of children: 16, player_to_move: minimizer, move_coordinates: (), path_depth: 1
web_1  | node_id: d4-i0_d5-i1_root_node, number of children: 14, player_to_move: minimizer, move_coordinates: (0, 2), path_depth: 0
web_1  | node_id: d4-i1_d5-i1_root_node, number of children: 14, player_to_move: minimizer, move_coordinates: (0, 0), path_depth: 0
web_1  | node_id: d4-i2_d5-i1_root_node, number of children: 14, player_to_move: minimizer, move_coordinates: (2, 1), path_depth: 1
web_1  | node_id: d4-i3_d5-i1_root_node, number of children: 14, player_to_move: minimizer, move_coordinates: (2, 0), path_depth: 0
web_1  | node_id: d4-i4_d5-i1_root_node, number of children: 16, player_to_move: minimizer, move_coordinates: (0, 3), path_depth: 0
web_1  | node_id: d4-i5_d5-i1_root_node, number of children: 16, player_to_move: minimizer, move_coordinates: (1, 3), path_depth: 1
web_1  | node_id: d4-i6_d5-i1_root_node, number of children: 15, player_to_move: minimizer, move_coordinates: (2, 3), path_depth: 0
web_1  | node_id: d4-i7_d5-i1_root_node, number of children: 14, player_to_move: minimizer, move_coordinates: (4, 2), path_depth: 0
web_1  | node_id: d4-i8_d5-i1_root_node, number of children: 14, player_to_move: minimizer, move_coordinates: (4, 1), path_depth: 1
web_1  | node_id: d4-i9_d5-i1_root_node, number of children: 14, player_to_move: minimizer, move_coordinates: (4, 0), path_depth: 0
web_1  | node_id: d4-i10_d5-i1_root_node, number of children: 14, player_to_move: minimizer, move_coordinates: (3, 0), path_depth: 0
web_1  | node_id: d4-i11_d5-i1_root_node, number of children: 14, player_to_move: minimizer, move_coordinates: (4, 3), path_depth: 0
web_1  | node_id: d4-i12_d5-i1_root_node, number of children: 15, player_to_move: minimizer, move_coordinates: (2, 4), path_depth: 0
web_1  | node_id: d4-i13_d5-i1_root_node, number of children: 14, player_to_move: minimizer, move_coordinates: (3, 4), path_depth: 0
web_1  | node_id: d4-i14_d5-i1_root_node, number of children: 14, player_to_move: minimizer, move_coordinates: (4, 4), path_depth: 0
web_1  | Move 0 score: 1
web_1  | ['+', '○', '+', '+', '+']
web_1  | ['○', '●', '+', '●', '+']
web_1  | ['+', '●', '○', '○', '+']
web_1  | ['+', '+', '+', '●', '+']
web_1  | ['+', '+', '+', '+', '+']
web_1  | Move 1 score: 1
web_1  | ['+', '○', '+', '+', '+']
web_1  | ['○', '●', '●', '●', '+']
web_1  | ['+', '●', '○', '○', '+']
web_1  | ['+', '+', '+', '●', '+']
web_1  | ['+', '+', '+', '+', '+']
web_1  | Move 2 score: 1
web_1  | ['+', '○', '+', '+', '+']
web_1  | ['○', '●', '●', '●', '○']
web_1  | ['+', '●', '○', '○', '+']
web_1  | ['+', '+', '+', '●', '+']
web_1  | ['+', '+', '+', '+', '+']
web_1  | Move 3 score: 1
web_1  | ['+', '○', '+', '+', '+']
web_1  | ['○', '●', '●', '●', '○']
web_1  | ['+', '●', '○', '○', '●']
web_1  | ['+', '+', '+', '●', '+']
web_1  | ['+', '+', '+', '+', '+']
web_1  | Move 4 score: 1
web_1  | ['+', '○', '+', '+', '+']
web_1  | ['○', '●', '●', '●', '○']
web_1  | ['○', '●', '○', '○', '●']
web_1  | ['+', '+', '+', '●', '+']
web_1  | ['+', '+', '+', '+', '+']
web_1  | white_move_node: node_id: d5-i1_root_node, number of children: 15, player_to_move: maximizer, move_coordinates: (1, 0), path_depth: 0
web_1  | [16/Aug/2022 04:16:55] "POST /games/ HTTP/1.1" 200 1636
web_1  | Found game for ip: 172.24.0.1
web_1  | user_game id: 776
web_1  | last move coordinates: (2, 1)
web_1  |
web_1  | >>> >>> Minimax seconds to execute: 7.4991 <<< <<<
web_1  |
web_1  | root node: node_id: root_node, number of children: 14, player_to_move: minimizer, move_coordinates: (), path_depth: 1
web_1  | Move 0 score: 1
web_1  | ['+', '○', '+', '+', '+']
web_1  | ['○', '●', '●', '●', '○']
web_1  | ['+', '●', '○', '○', '+']
web_1  | ['+', '+', '+', '●', '+']
web_1  | ['+', '+', '+', '+', '+']
web_1  | Move 1 score: 1
web_1  | ['+', '○', '+', '+', '+']
web_1  | ['○', '●', '●', '●', '○']
web_1  | ['+', '●', '○', '○', '+']
web_1  | ['+', '●', '+', '●', '+']
web_1  | ['+', '+', '+', '+', '+']
web_1  | Move 2 score: 1
web_1  | ['+', '○', '+', '+', '+']
web_1  | ['○', '●', '●', '●', '○']
web_1  | ['+', '●', '○', '○', '+']
web_1  | ['+', '●', '+', '●', '+']
web_1  | ['+', '○', '+', '+', '+']
web_1  | Move 3 score: 1
web_1  | ['+', '○', '+', '+', '+']
web_1  | ['○', '●', '●', '●', '○']
web_1  | ['+', '●', '○', '○', '●']
web_1  | ['+', '●', '+', '●', '+']
web_1  | ['+', '○', '+', '+', '+']
web_1  | Move 4 score: 1
web_1  | ['+', '○', '+', '+', '+']
web_1  | ['○', '●', '●', '●', '○']
web_1  | ['○', '●', '○', '○', '●']
web_1  | ['+', '●', '+', '●', '+']
web_1  | ['+', '○', '+', '+', '+']
web_1  | white_move_node: node_id: d5-i8_root_node, number of children: 13, player_to_move: maximizer, move_coordinates: (4, 1), path_depth: 0
web_1  | [16/Aug/2022 04:17:20] "POST /games/ HTTP/1.1" 200 1640
web_1  | Found game for ip: 172.24.0.1
web_1  | user_game id: 776
web_1  | last move coordinates: (1, 3)
web_1  |
web_1  | >>> >>> Minimax seconds to execute: 1.9950 <<< <<<
web_1  |
web_1  | root node: node_id: root_node, number of children: 14, player_to_move: minimizer, move_coordinates: (), path_depth: 1
web_1  | Move 0 score: 100
web_1  | ['+', '○', '+', '+', '+']
web_1  | ['○', '●', '●', '●', '○']
web_1  | ['○', '●', '○', '○', '+']
web_1  | ['+', '●', '+', '●', '+']
web_1  | ['+', '+', '+', '+', '+']
web_1  | Move 1 score: 100
web_1  | ['+', '○', '+', '+', '+']
web_1  | ['○', '●', '●', '●', '○']
web_1  | ['○', '●', '○', '○', '+']
web_1  | ['●', '●', '+', '●', '+']
web_1  | ['+', '+', '+', '+', '+']
web_1  | Move 2 score: 100
web_1  | ['○', '○', '+', '+', '+']
web_1  | ['○', '●', '●', '●', '○']
web_1  | ['○', '●', '○', '○', '+']
web_1  | ['●', '●', '+', '●', '+']
web_1  | ['+', '+', '+', '+', '+']
web_1  | Move 3 score: 100
web_1  | ['○', '○', '+', '+', '+']
web_1  | ['○', '●', '●', '●', '○']
web_1  | ['○', '●', '○', '○', '+']
web_1  | ['●', '●', '+', '●', '+']
web_1  | ['+', '●', '+', '+', '+']
web_1  | white_move_node: node_id: d5-i0_root_node, number of children: 2, player_to_move: maximizer, move_coordinates: (0, 2), path_depth: 1
web_1  | [16/Aug/2022 04:17:44] "POST /games/ HTTP/1.1" 200 1644
web_1  | Found game for ip: 172.24.0.1
web_1  | user_game id: 776
web_1  | last move coordinates: (2, 3)
web_1  |
web_1  | >>> >>> Minimax seconds to execute: 0.0416 <<< <<<
web_1  |
web_1  | root node: node_id: root_node, number of children: 12, player_to_move: minimizer, move_coordinates: (), path_depth: 1
web_1  | Move 0 score: 100
web_1  | ['+', '○', '○', '+', '+']
web_1  | ['○', '●', '●', '●', '○']
web_1  | ['○', '●', '○', '○', '+']
web_1  | ['+', '●', '●', '●', '+']
web_1  | ['+', '+', '+', '+', '+']
web_1  | Move 1 score: 100
web_1  | ['●', '○', '○', '+', '+']
web_1  | ['○', '●', '●', '●', '○']
web_1  | ['○', '●', '○', '○', '+']
web_1  | ['+', '●', '●', '●', '+']
web_1  | ['+', '+', '+', '+', '+']
web_1  | Move 2 score: 100
web_1  | ['●', '○', '○', '+', '+']
web_1  | ['○', '●', '●', '●', '○']
web_1  | ['○', '●', '○', '○', '+']
web_1  | ['○', '●', '●', '●', '+']
web_1  | ['+', '+', '+', '+', '+']
web_1  | Move 3 score: 100
web_1  | ['●', '○', '○', '+', '+']
web_1  | ['○', '●', '●', '●', '○']
web_1  | ['○', '●', '○', '○', '+']
web_1  | ['○', '●', '●', '●', '+']
web_1  | ['+', '●', '+', '+', '+']
web_1  | white_move_node: node_id: d5-i2_root_node, number of children: 1, player_to_move: maximizer, move_coordinates: (2, 0), path_depth: 1
web_1  | [16/Aug/2022 04:18:07] "POST /games/ HTTP/1.1" 200 1648
web_1  | Found game for ip: 172.24.0.1
web_1  | user_game id: 776
web_1  | [16/Aug/2022 04:18:14] "POST /games/ HTTP/1.1" 200 775


## Same moves as above, but using get_white_response_no_tree

web_1  | /code/games/views.py changed, reloading.
web_1  | Watching for file changes with StatReloader
web_1  | Watching for file changes with StatReloader
web_1  | Performing system checks...
web_1  |
web_1  | System check identified no issues (0 silenced).
web_1  | August 16, 2022 - 04:19:51
web_1  | Django version 3.2.15, using settings 'go_app.settings'
web_1  | Starting development server at http://0.0.0.0:8000/
web_1  | Quit the server with CONTROL-C.
web_1  | Couldn't find game for ip: 172.24.0.1, creating new game
web_1  | user_game id: 777
web_1  | No black stones on board
web_1  | [16/Aug/2022 04:20:01] "GET /games/ HTTP/1.1" 200 1822
web_1  | Found game for ip: 172.24.0.1
web_1  | user_game id: 777
web_1  | last move coordinates: (3, 3)
web_1  | Executing minimax, searching to depth of 2, open moves: 96%
web_1  |
web_1  | >>> >>> Minimax seconds to execute: 0.0063 <<< <<<
web_1  |
web_1  | [16/Aug/2022 04:20:07] "POST /games/ HTTP/1.1" 200 1624
web_1  | Found game for ip: 172.24.0.1
web_1  | user_game id: 777
web_1  | last move coordinates: (3, 1)
web_1  | percentage_multiplier: 0.99
web_1  | percentage_multiplier: 0.94
web_1  | Executing minimax, searching to depth of 4, open moves: 88%
web_1  |
web_1  | >>> >>> Minimax seconds to execute: 1.1997 <<< <<<
web_1  |
web_1  | [16/Aug/2022 04:20:58] "POST /games/ HTTP/1.1" 200 1628
web_1  | Found game for ip: 172.24.0.1
web_1  | user_game id: 777
web_1  | last move coordinates: (1, 2)
web_1  | percentage_multiplier: 0.99
web_1  | percentage_multiplier: 0.94
web_1  | percentage_multiplier: 0.89
web_1  | percentage_multiplier: 0.84
web_1  | Executing minimax, searching to depth of 5, open moves: 80%
web_1  |
web_1  | >>> >>> Minimax seconds to execute: 44.4422 <<< <<<
web_1  |
web_1  | [16/Aug/2022 04:22:20] "POST /games/ HTTP/1.1" 200 1632
web_1  | Found game for ip: 172.24.0.1
web_1  | user_game id: 777
web_1  | last move coordinates: (1, 1)
web_1  | percentage_multiplier: 0.99
web_1  | percentage_multiplier: 0.94
web_1  | percentage_multiplier: 0.89
web_1  | percentage_multiplier: 0.84
web_1  | percentage_multiplier: 0.79
web_1  | Executing minimax, searching to depth of 5, open moves: 72%
web_1  |
web_1  | >>> >>> Minimax seconds to execute: 4.3118 <<< <<<
web_1  |
web_1  | [16/Aug/2022 04:22:40] "POST /games/ HTTP/1.1" 200 1636
web_1  | Found game for ip: 172.24.0.1
web_1  | user_game id: 777
web_1  | last move coordinates: (2, 1)
web_1  | percentage_multiplier: 0.99
web_1  | percentage_multiplier: 0.94
web_1  | percentage_multiplier: 0.89
web_1  | percentage_multiplier: 0.84
web_1  | percentage_multiplier: 0.79
web_1  | percentage_multiplier: 0.74
web_1  | percentage_multiplier: 0.69
web_1  | Executing minimax, searching to depth of 5, open moves: 64%
web_1  |
web_1  | >>> >>> Minimax seconds to execute: 0.2479 <<< <<<
web_1  |
web_1  | [16/Aug/2022 04:23:05] "POST /games/ HTTP/1.1" 200 1640
web_1  | Found game for ip: 172.24.0.1
web_1  | user_game id: 777
web_1  | last move coordinates: (1, 3)
web_1  | percentage_multiplier: 0.99
web_1  | percentage_multiplier: 0.94
web_1  | percentage_multiplier: 0.89
web_1  | percentage_multiplier: 0.84
web_1  | percentage_multiplier: 0.79
web_1  | percentage_multiplier: 0.74
web_1  | percentage_multiplier: 0.69
web_1  | percentage_multiplier: 0.64
web_1  | Executing minimax, searching to depth of 5, open moves: 56%
web_1  |
web_1  | >>> >>> Minimax seconds to execute: 0.1825 <<< <<<
web_1  |
web_1  | [16/Aug/2022 04:23:47] "POST /games/ HTTP/1.1" 200 772

## Trying to win instead
web_1  | user_game id: 778
web_1  | No black stones on board
web_1  | [16/Aug/2022 04:24:42] "GET /games/ HTTP/1.1" 200 1822
web_1  | Found game for ip: 172.24.0.1
web_1  | user_game id: 778
web_1  | last move coordinates: (3, 3)
web_1  | Executing minimax, searching to depth of 2, open moves: 96%
web_1  |
web_1  | >>> >>> Minimax seconds to execute: 0.0081 <<< <<<
web_1  |
web_1  | [16/Aug/2022 04:24:50] "POST /games/ HTTP/1.1" 200 1624
web_1  | Found game for ip: 172.24.0.1
web_1  | user_game id: 778
web_1  | last move coordinates: (1, 3)
web_1  | percentage_multiplier: 0.99
web_1  | percentage_multiplier: 0.94
web_1  | Executing minimax, searching to depth of 4, open moves: 88%
web_1  |
web_1  | >>> >>> Minimax seconds to execute: 1.1478 <<< <<<
web_1  |
web_1  | [16/Aug/2022 04:25:15] "POST /games/ HTTP/1.1" 200 1628
web_1  | Found game for ip: 172.24.0.1
web_1  | user_game id: 778
web_1  | last move coordinates: (1, 2)
web_1  | percentage_multiplier: 0.99
web_1  | percentage_multiplier: 0.94
web_1  | percentage_multiplier: 0.89
web_1  | percentage_multiplier: 0.84
web_1  | Executing minimax, searching to depth of 5, open moves: 80%
web_1  |
web_1  | >>> >>> Minimax seconds to execute: 13.7849 <<< <<<
web_1  |
web_1  | [16/Aug/2022 04:25:43] "POST /games/ HTTP/1.1" 200 1632

## another attempt at winning:
web_1  | user_game id: 779
web_1  | No black stones on board
web_1  | [16/Aug/2022 04:26:24] "GET /games/ HTTP/1.1" 200 1822
web_1  | Found game for ip: 172.24.0.1
web_1  | user_game id: 779
web_1  | last move coordinates: (3, 3)
web_1  | Executing minimax, searching to depth of 2, open moves: 96%
web_1  |
web_1  | >>> >>> Minimax seconds to execute: 0.0062 <<< <<<
web_1  |
web_1  | [16/Aug/2022 04:26:34] "POST /games/ HTTP/1.1" 200 1624
web_1  | Found game for ip: 172.24.0.1
web_1  | user_game id: 779
web_1  | last move coordinates: (2, 3)
web_1  | percentage_multiplier: 0.99
web_1  | percentage_multiplier: 0.94
web_1  | Executing minimax, searching to depth of 4, open moves: 88%
web_1  |
web_1  | >>> >>> Minimax seconds to execute: 0.4691 <<< <<<
web_1  |
web_1  | [16/Aug/2022 04:26:42] "POST /games/ HTTP/1.1" 200 1628
web_1  | Found game for ip: 172.24.0.1
web_1  | user_game id: 779
web_1  | last move coordinates: (1, 1)
web_1  | percentage_multiplier: 0.99
web_1  | percentage_multiplier: 0.94
web_1  | percentage_multiplier: 0.89
web_1  | percentage_multiplier: 0.84
web_1  | Executing minimax, searching to depth of 5, open moves: 80%
web_1  |
web_1  | >>> >>> Minimax seconds to execute: 59.9882 <<< <<<
web_1  |
web_1  | [16/Aug/2022 04:27:54] "POST /games/ HTTP/1.1" 200 1632
web_1  | Found game for ip: 172.24.0.1
web_1  | user_game id: 779
web_1  | last move coordinates: (3, 1)
web_1  | percentage_multiplier: 0.99
web_1  | percentage_multiplier: 0.94
web_1  | percentage_multiplier: 0.89
web_1  | percentage_multiplier: 0.84
web_1  | percentage_multiplier: 0.79
web_1  | Executing minimax, searching to depth of 5, open moves: 72%
web_1  |
web_1  | >>> >>> Minimax seconds to execute: 20.3041 <<< <<<
web_1  |
web_1  | [16/Aug/2022 04:29:02] "POST /games/ HTTP/1.1" 200 1636

## Still trying to win

web_1  | Couldn't find game for ip: 172.24.0.1, creating new game
web_1  | user_game id: 780
web_1  | No black stones on board
web_1  | [16/Aug/2022 04:30:02] "GET /games/ HTTP/1.1" 200 1822
web_1  | Found game for ip: 172.24.0.1
web_1  | user_game id: 780
web_1  | last move coordinates: (1, 1)
web_1  | Executing minimax, searching to depth of 2, open moves: 96%
web_1  |
web_1  | >>> >>> Minimax seconds to execute: 0.0064 <<< <<<
web_1  |
web_1  | [16/Aug/2022 04:30:18] "POST /games/ HTTP/1.1" 200 1624
web_1  | Found game for ip: 172.24.0.1
web_1  | user_game id: 780
web_1  | last move coordinates: (3, 3)
web_1  | percentage_multiplier: 0.99
web_1  | percentage_multiplier: 0.94
web_1  | Executing minimax, searching to depth of 4, open moves: 88%
web_1  |
web_1  | >>> >>> Minimax seconds to execute: 2.2011 <<< <<<
web_1  |
web_1  | [16/Aug/2022 04:30:30] "POST /games/ HTTP/1.1" 200 1628
web_1  | Found game for ip: 172.24.0.1
web_1  | user_game id: 780
web_1  | last move coordinates: (3, 0)
web_1  | percentage_multiplier: 0.99
web_1  | percentage_multiplier: 0.94
web_1  | percentage_multiplier: 0.89
web_1  | percentage_multiplier: 0.84
web_1  | Executing minimax, searching to depth of 5, open moves: 80%
web_1  |
web_1  | >>> >>> Minimax seconds to execute: 38.5438 <<< <<<
web_1  |
web_1  | [16/Aug/2022 04:31:23] "POST /games/ HTTP/1.1" 200 1632
db_1   | 2022-08-16 04:31:28.931 UTC [34] WARNING:  could not open statistics file "pg_stat_tmp/global.stat": Operation not permitted
web_1  | Found game for ip: 172.24.0.1
web_1  | user_game id: 780
web_1  | last move coordinates: (1, 3)
web_1  | percentage_multiplier: 0.99
web_1  | percentage_multiplier: 0.94
web_1  | percentage_multiplier: 0.89
web_1  | percentage_multiplier: 0.84
web_1  | percentage_multiplier: 0.79
web_1  | Executing minimax, searching to depth of 5, open moves: 72%
web_1  |
web_1  | >>> >>> Minimax seconds to execute: 27.5036 <<< <<<
web_1  |
web_1  | [16/Aug/2022 04:32:12] "POST /games/ HTTP/1.1" 200 1636
web_1  | Found game for ip: 172.24.0.1
web_1  | user_game id: 780
web_1  | last move coordinates: (2, 3)
web_1  | percentage_multiplier: 0.99
web_1  | percentage_multiplier: 0.94
web_1  | percentage_multiplier: 0.89
web_1  | percentage_multiplier: 0.84
web_1  | percentage_multiplier: 0.79
web_1  | percentage_multiplier: 0.74
web_1  | percentage_multiplier: 0.69
web_1  | Executing minimax, searching to depth of 5, open moves: 64%
web_1  |
web_1  | >>> >>> Minimax seconds to execute: 3.8798 <<< <<<
web_1  |
web_1  | [16/Aug/2022 04:32:56] "POST /games/ HTTP/1.1" 200 1640
web_1  | Found game for ip: 172.24.0.1
web_1  | user_game id: 780
web_1  | last move coordinates: (1, 2)
web_1  | percentage_multiplier: 0.99
web_1  | percentage_multiplier: 0.94
web_1  | percentage_multiplier: 0.89
web_1  | percentage_multiplier: 0.84
web_1  | percentage_multiplier: 0.79
web_1  | percentage_multiplier: 0.74
web_1  | percentage_multiplier: 0.69
web_1  | percentage_multiplier: 0.64
web_1  | Executing minimax, searching to depth of 5, open moves: 56%
web_1  |
web_1  | >>> >>> Minimax seconds to execute: 1.2955 <<< <<<
web_1  |
web_1  | [16/Aug/2022 04:33:07] "POST /games/ HTTP/1.1" 200 1644
web_1  | Found game for ip: 172.24.0.1
web_1  | user_game id: 780
web_1  | last move coordinates: (4, 1)
web_1  | percentage_multiplier: 0.99
web_1  | percentage_multiplier: 0.94
web_1  | percentage_multiplier: 0.89
web_1  | percentage_multiplier: 0.84
web_1  | percentage_multiplier: 0.79
web_1  | percentage_multiplier: 0.74
web_1  | percentage_multiplier: 0.69
web_1  | percentage_multiplier: 0.64
web_1  | percentage_multiplier: 0.59
web_1  | percentage_multiplier: 0.54
web_1  | Executing minimax, searching to depth of 5, open moves: 48%
web_1  |
web_1  | >>> >>> Minimax seconds to execute: 6.0956 <<< <<<
web_1  |
web_1  | [16/Aug/2022 04:33:43] "POST /games/ HTTP/1.1" 200 1648
web_1  | Found game for ip: 172.24.0.1
web_1  | user_game id: 780
web_1  | last move coordinates: (3, 1)
web_1  | percentage_multiplier: 0.99
web_1  | percentage_multiplier: 0.94
web_1  | percentage_multiplier: 0.89
web_1  | percentage_multiplier: 0.84
web_1  | percentage_multiplier: 0.79
web_1  | percentage_multiplier: 0.74
web_1  | percentage_multiplier: 0.69
web_1  | percentage_multiplier: 0.64
web_1  | percentage_multiplier: 0.59
web_1  | percentage_multiplier: 0.54
web_1  | percentage_multiplier: 0.49
web_1  | percentage_multiplier: 0.44
web_1  | Executing minimax, searching to depth of 5, open moves: 40%
web_1  |
web_1  | >>> >>> Minimax seconds to execute: 0.5744 <<< <<<
web_1  |
web_1  | [16/Aug/2022 04:34:23] "POST /games/ HTTP/1.1" 200 1652
web_1  | Found game for ip: 172.24.0.1
web_1  | user_game id: 780
web_1  | last move coordinates: (2, 4)
web_1  | percentage_multiplier: 0.99
web_1  | percentage_multiplier: 0.94
web_1  | percentage_multiplier: 0.89
web_1  | percentage_multiplier: 0.84
web_1  | percentage_multiplier: 0.79
web_1  | percentage_multiplier: 0.74
web_1  | percentage_multiplier: 0.69
web_1  | percentage_multiplier: 0.64
web_1  | percentage_multiplier: 0.59
web_1  | percentage_multiplier: 0.54
web_1  | percentage_multiplier: 0.49
web_1  | percentage_multiplier: 0.44
web_1  | percentage_multiplier: 0.39
web_1  | Executing minimax, searching to depth of 5, open moves: 32%
web_1  |
web_1  | >>> >>> Minimax seconds to execute: 0.6111 <<< <<<
web_1  |
web_1  | [16/Aug/2022 04:34:51] "POST /games/ HTTP/1.1" 200 1656
web_1  | Found game for ip: 172.24.0.1
web_1  | user_game id: 780
web_1  | last move coordinates: (0, 2)
web_1  | percentage_multiplier: 0.99
web_1  | percentage_multiplier: 0.94
web_1  | percentage_multiplier: 0.89
web_1  | percentage_multiplier: 0.84
web_1  | percentage_multiplier: 0.79
web_1  | percentage_multiplier: 0.74
web_1  | percentage_multiplier: 0.69
web_1  | percentage_multiplier: 0.64
web_1  | percentage_multiplier: 0.59
web_1  | percentage_multiplier: 0.54
web_1  | percentage_multiplier: 0.49
web_1  | percentage_multiplier: 0.44
web_1  | percentage_multiplier: 0.39
web_1  | percentage_multiplier: 0.34
web_1  | percentage_multiplier: 0.29
web_1  | Executing minimax, searching to depth of 5, open moves: 24%
web_1  |
web_1  | >>> >>> Minimax seconds to execute: 0.1383 <<< <<<
web_1  |
web_1  | [16/Aug/2022 04:35:12] "POST /games/ HTTP/1.1" 200 1660
web_1  | Found game for ip: 172.24.0.1
web_1  | user_game id: 780
web_1  | last move coordinates: (0, 0)
web_1  | percentage_multiplier: 0.99
web_1  | percentage_multiplier: 0.94
web_1  | percentage_multiplier: 0.89
web_1  | percentage_multiplier: 0.84
web_1  | percentage_multiplier: 0.79
web_1  | percentage_multiplier: 0.74
web_1  | percentage_multiplier: 0.69
web_1  | percentage_multiplier: 0.64
web_1  | percentage_multiplier: 0.59
web_1  | percentage_multiplier: 0.54
web_1  | percentage_multiplier: 0.49
web_1  | percentage_multiplier: 0.44
web_1  | percentage_multiplier: 0.39
web_1  | percentage_multiplier: 0.34
web_1  | percentage_multiplier: 0.29
web_1  | percentage_multiplier: 0.24
web_1  | Executing minimax, searching to depth of 4, open moves: 16%
web_1  |
web_1  | >>> >>> Minimax seconds to execute: 0.0140 <<< <<<
web_1  |
web_1  | [16/Aug/2022 04:35:26] "POST /games/ HTTP/1.1" 200 1664
db_1   | 2022-08-16 04:35:29.389 UTC [34] WARNING:  could not open statistics file "pg_stat_tmp/global.stat": Operation not permitted
web_1  | Found game for ip: 172.24.0.1
web_1  | user_game id: 780
web_1  | last move coordinates: (0, 1)
web_1  | percentage_multiplier: 0.99
web_1  | percentage_multiplier: 0.94
web_1  | percentage_multiplier: 0.89
web_1  | percentage_multiplier: 0.84
web_1  | percentage_multiplier: 0.79
web_1  | percentage_multiplier: 0.74
web_1  | percentage_multiplier: 0.69
web_1  | percentage_multiplier: 0.64
web_1  | percentage_multiplier: 0.59
web_1  | percentage_multiplier: 0.54
web_1  | percentage_multiplier: 0.49
web_1  | percentage_multiplier: 0.44
web_1  | percentage_multiplier: 0.39
web_1  | percentage_multiplier: 0.34
web_1  | percentage_multiplier: 0.29
web_1  | percentage_multiplier: 0.24
web_1  | percentage_multiplier: 0.19
web_1  | percentage_multiplier: 0.14
web_1  | Executing minimax, searching to depth of 2, open moves: 8%
web_1  |
web_1  | >>> >>> Minimax seconds to execute: 0.0018 <<< <<<
web_1  |
web_1  | [16/Aug/2022 04:35:35] "POST /games/ HTTP/1.1" 200 1668
web_1  | Found game for ip: 172.24.0.1
web_1  | user_game id: 780
web_1  | [16/Aug/2022 04:35:46] "POST /games/ HTTP/1.1" 200 776

Game Over

Black score: 3 | White score: 3

      0   1    2   3   4
0     ●   ○   ○   ●   ○
1     ●   ●   ○   ●   ●
2     ●   ●   ○   ○   ○
3     ○   ●   ●   ●   ○
4     ●   ○   ●   ○   ○