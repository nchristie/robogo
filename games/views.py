from django.shortcuts import render
# from django.http import HttpResponse
# from pprint import pformat
from django.views import View
from random import randint

INTERSECTION = "+"
WHITE_STONE = "○"
BLACK_STONE = "●"

class Index(View):
    template = 'index.html'
    some_variable = "Hello"

    def get(self, request):
        my_board = Board()
        context = {
          "some_variable": self.some_variable,
          "my_board": my_board
        }
        return render(request, self.template, context)
class Board():
  def __init__(self, size=9):
    self.state = [ [INTERSECTION for j in range(size)] for i in range(size) ]
    stone_to_move = [BLACK_STONE, WHITE_STONE, INTERSECTION]
    for i in range(9):
      for j in range(9):
        stone = stone_to_move[randint(0,2)]
        self.make_move(i,j,stone)

  def draw(self):
    return self.state

  def make_move(self, x, y, player):
    self.state[x][y] = player

  def get_scores(self, player):
    player_score = 0
    return player_score


