from django.shortcuts import render
# from django.http import HttpResponse
# from pprint import pformat
from django.views import View

class Index(View):
    template = 'index.html'

    def get(self, request):
        return render(request, self.template)

# class Index(View):
#     template = 'index.html'

#     def get(self, request):
#         return render(request, self.template)

# def index(request):
#     game_board = Board()
#     return HttpResponse(f"{pformat(game_board.draw())}")

# class Board():
#   def __init__(self, size=9):
#     self.state = [ [None for j in range(size)] for i in range(size) ]

#   def draw(self):
#     return self.state

#   def make_move(self, x, y, player):
#     self.state[x][y] = player

#   def get_scores(self, player):
#     player_score = 0
#     return player_score


