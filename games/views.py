from django.shortcuts import render
from django.forms import ModelForm, IntegerField
from django.views import View
from .models import Game, Move

INTERSECTION = "+"
WHITE_STONE = "○"
BLACK_STONE = "●"

class Index(View):
    def get(self, request):
        form = MoveForm(request.POST)
        user_game = None
        # Find existing game for user if there is one
        try:
          user_game = Game.objects.find_by('-user_ip')
        # Initiate new game if not
        except:
          user_game = Game()
          ip = get_client_ip(request)
          user_game.user_ip = ip
          user_game.save()

        moves = Move.objects.order_by('-id')
        my_board = Board()
        my_board.make_move(4, 4, BLACK_STONE)
        
        for move in moves:
          print(move.x_coordinate)
        #   my_board.make_move(move.x_coordinate, move.y_coordinate)
        context = {
          "my_board": my_board,
          "user_ip": ip,
          "all_moves": moves,
          "form": form
        }
        return render(request, 'games/index.html', context)
  
    def post(self, request):
        form = MoveForm(request.POST)
        if form.is_valid():
          form.save()
        user_game = None
        # Find existing game for user if there is one
        try:
          user_game = Game.objects.find_by('-user_ip')
        # Initiate new game if not
        except:
          user_game = Game()
          ip = get_client_ip(request)
          user_game.user_ip = ip
          user_game.save()

        moves = Move.objects.order_by('-id')
        my_board = Board()

        my_board.make_move(4, 4, BLACK_STONE)
        
        # for move in moves:
        #   print(f"move.x_coordinate {move.x_coordinate}")
        #   my_board.make_move(move.x_coordinate, move.y_coordinate, move.player)
        context = {
          "my_board": my_board,
          "user_ip": ip,
          "all_moves": moves,
          "form": form
        }
        return render(request, 'games/index.html', context)
class Board():
  def __init__(self, size=9):
    self.state = [ [INTERSECTION for j in range(size)] for i in range(size) ]

  def make_move(self, x, y, player=BLACK_STONE):
    self.state[x][y] = player

  def get_scores(self, player):
    # TODO this should identify lines of stones and return longest line length for each player
    player_score = 0
    return player_score


class MoveForm(ModelForm):
    player = "black"
    x_coordinate = IntegerField(label='x coordinate:')
    y_coordinate = IntegerField(label='y coordinate:')
    class Meta:
      model = Move
      exclude = ["player"]

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

