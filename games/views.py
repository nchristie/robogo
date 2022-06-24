from string import printable
from django.shortcuts import render
from django.views import View
from .models import Game, Move
from .forms import MoveForm
from random import randint
from .go_minimax_joiner import EMPTY_POSITION, WHITE_STONE, BLACK_STONE

class Index(View):
    def get(self, request):
        return self.post(request)

    def post(self, request):
        user_game = find_game_by_ip(get_client_ip(request))
        game_id = user_game.id
        print(f"user_game id: {game_id}")
        initial_state = {"game": game_id, "player": "black"}
        form = MoveForm(request.POST, initial=initial_state)
        if form.is_valid():
            form.save()

        moves = user_game.move_set.all().order_by("-id")
        my_board = Board()

        my_board.draw(moves)

        # get white response
        white_x, white_y = get_white_response()
        white_move = Move(
          game=user_game, 
          player='white', 
          x_coordinate=white_x, 
          y_coordinate=white_y
        )
        white_move.save()

        context = {"my_board": my_board, "all_moves": moves, "form": form}
        return render(request, "games/index.html", context)


class Board:
    def __init__(self, size=9):
        self.state = [[EMPTY_POSITION for j in range(size)] for i in range(size)]

    def draw(self, moves):
        for move in moves:
            player = BLACK_STONE 
            if len(move.player) > 0 and move.player[0].lower() == "w":
              player = WHITE_STONE
            self.make_move(move.x_coordinate, move.y_coordinate, player)

    def make_move(self, x, y, player=BLACK_STONE):
        self.state[x][y] = player

    def get_scores(self, player):
        # TODO this should identify lines of stones and return longest line length for each player
        player_score = 0
        return player_score


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def find_game_by_ip(ip):
    # Find existing game for user if there is one
    try:
        user_game = Game.objects.get(user_ip=ip)
        print(f"Found game for ip: {ip}")
    # Initiate new game if not
    except:
        print(f"Couldn't find game for ip: {ip}, creating new game")
        user_game = Game()
        user_game.user_ip = ip
        user_game.save()
    return user_game

def get_white_response():
      white_x = randint(0,8)
      white_y = randint(0,8)
      return (white_x, white_y)
