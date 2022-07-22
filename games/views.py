from django.shortcuts import render
from django.views import View
from .models import Game, Move
from .forms import MoveForm
from .stones import EMPTY_POSITION, WHITE_STONE, BLACK_STONE
from .go_minimax_joiner import GoNode
from .game_logic import get_score_dict, WINNING_SCORE, transpose_board

import logging

logger = logging.getLogger(__name__)

DEPTH = 100000

# TODO remove drop down with ip addresses and form entry for player colour
# TODO create button for starting new game


class Index(View):
    def get(self, request):
        # TODO figure out what the get request should do instead of just
        # forwarding to post request
        return self.post(request)

    def post(self, request):
        user_game = find_game_by_ip(get_client_ip(request))
        game_id = user_game.id
        logger.info(f"user_game id: {game_id}")

        initial_state = {"game": game_id, "player": "black"}
        form = MoveForm(request.POST, initial=initial_state)
        if form.is_valid():
            form.save()

        my_board = Board()
        moves = user_game.move_set.all().order_by("-id")
        my_board.update(moves)

        scores = get_score_dict(my_board.state)
        black_score = scores[BLACK_STONE]
        white_score = scores[WHITE_STONE]
        winner = "No-one"
        if black_score >= WINNING_SCORE:
            winner = "Black"
        elif white_score >= WINNING_SCORE:
            winner = "White"

        if winner == "No-one":
            # get white response
            # TODO split some logic here out into other function
            try:
                white_x, white_y = get_white_response(my_board.state)
                white_move = Move(
                    game=user_game,
                    player="white",
                    x_coordinate=white_x,
                    y_coordinate=white_y,
                )
                white_move.save()
            except Exception as e:
                logger.error(f"Failed to get white move with exception: {e}")

        # Update board with white response
        moves = user_game.move_set.all().order_by("-id")
        my_board.update(moves)
        transposed_board = transpose_board(my_board.state)

        context = {
            "board_state": transposed_board,
            "all_moves": moves,
            "form": form,
            "black_score": black_score,
            "white_score": white_score,
            "winner": winner,
        }
        return render(request, "games/index.html", context)


class Board:
    def __init__(self, size=9):
        self.state = [[EMPTY_POSITION for j in range(size)] for i in range(size)]
        self.size = size

    def update(self, moves):
        for move in moves:
            player = BLACK_STONE
            if len(move.player) > 0 and move.player[0].lower() == "w":
                player = WHITE_STONE
            self.make_move(move.x_coordinate, move.y_coordinate, player)

    def make_move(self, x, y, player=BLACK_STONE):
        legal_move = 0 <= x < self.size
        legal_move = legal_move & 0 <= y < self.size
        if not legal_move:
            logger.error("Illegal move, try again")
            return
        self.state[x][y] = player


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
        logger.info(f"Found game for ip: {ip}")
    # Initiate new game if not
    except:
        logger.info(f"Couldn't find game for ip: {ip}, creating new game")
        user_game = Game()
        user_game.user_ip = ip
        user_game.save()
    return user_game


def get_white_response(board_state):
    my_node = GoNode(
        move_id=0,
        player="maximizer",
        score=None,
        children=[],
        board_state=board_state,
    )

    maximizer_choice_node = GoNode(
        move_id=0,
        player="minimizer",
        score=-float("inf"),
        children=[],
        board_state=board_state,
    )

    minimizer_choice_node = GoNode(
        move_id=0,
        player="minimizer",
        score=float("inf"),
        children=[],
        board_state=board_state,
    )

    white_move_node = my_node.evaluate_node(
        my_node, maximizer_choice_node, minimizer_choice_node, DEPTH
    )
    # TODO once evaluate_node is updated we should have a built a tree and be able to use that to assess
    # the best move with the following lines of code:
    # white_move_node = my_node.children[0]
    # for node in my_node.children:
    # white_move_node = node if node.get_score() > white_move_node.get_score()
    white_move = white_move_node.move_coordinates
    logger.info(f"white_move: {white_move}")
    return white_move
