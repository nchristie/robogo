from django.shortcuts import render
from django import forms
from django.http import HttpResponse
from django.views import View
from random import randint

INTERSECTION = "+"
WHITE_STONE = "○"
BLACK_STONE = "●"

class Index(View):
    template = 'index.html'

    def get(self, request):
        my_board = Board()
        context = {
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

class MoveForm(forms.Form):
    your_move = forms.CharField(label='Your move (x,y)', max_length=3)

def get_move(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = MoveForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponse('/games/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = MoveForm()

    return render(request, 'index.html', {'form': form})

