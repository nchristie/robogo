from django.shortcuts import render
from django.views import View
from .models import Game, Move
from .forms import MoveForm
from .stones import EMPTY_POSITION, WHITE_STONE, BLACK_STONE
from .go_minimax_joiner import GoNode
from .minimax import minimax_with_alpha_beta_pruning_algorithm
from .game_logic import *
import itertools
from time import perf_counter

import logging

logger = logging.getLogger(__name__)

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

        my_board = Board(BOARD_SIZE)
        moves = user_game.move_set.all().order_by("-id")
        my_board.update(moves)

        scores = get_score_dict(my_board.state)
        black_score = scores[BLACK_STONE]
        white_score = scores[WHITE_STONE]

        open_moves = sum(x == "+" for x in list(itertools.chain(*my_board.state)))

        winner = "No-one"
        if black_score >= WINNING_SCORE:
            winner = "Black"
        elif white_score >= WINNING_SCORE:
            winner = "White"
        elif open_moves == 0:
            winner = "Stalemate"

        if winner == "No-one":
            # get white response
            # TODO split some logic here out into other function
            chained_state = list(itertools.chain(*my_board.state))
            if BLACK_STONE in chained_state:
                try:
                    last_move = user_game.move_set.last()
                    move_coordinates = (last_move.x_coordinate, last_move.y_coordinate)
                    logger.info(f"last move coordinates: {move_coordinates}")
                    white_x, white_y = get_white_response_no_tree(
                        board_state=my_board.state
                    )
                except Exception as e:
                    message = f"Failed to get white move with exception: {e}"
                    logger.error(message)
                    raise Exception(message)

                white_move = Move(
                    game=user_game,
                    player="white",
                    x_coordinate=white_x,
                    y_coordinate=white_y,
                )
                white_move.save()
            else:
                logger.error(f"No black stones on board")

        # Update board with white response
        moves = user_game.move_set.all().order_by("-id")
        my_board.update(moves)

        scores = get_score_dict(my_board.state)
        black_score = scores[BLACK_STONE]
        white_score = scores[WHITE_STONE]

        open_moves = sum(x == "+" for x in list(itertools.chain(*my_board.state)))

        winner = "No-one"
        if black_score >= WINNING_SCORE:
            winner = "Black"
        elif white_score >= WINNING_SCORE:
            winner = "White"
        elif open_moves == 0:
            winner = "Stalemate"

        transposed_board = transpose_board(my_board.state)

        context = {
            # transposed board here so that it makes sense to viewer when they input their moves
            "board_state": transposed_board,
            "all_moves": moves,
            "form": form,
            "black_score": black_score,
            "white_score": white_score,
            "winner": winner,
            "winning_score": WINNING_SCORE,
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
            # TODO currently this forfeits the move, write logic to raise error in UI and allow another attempt
            return
        self.state[x][y] = player


# Helpers
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


def get_white_response_no_tree(
    board_state, winning_score=WINNING_SCORE, depth=MAX_TREE_DEPTH
):

    root_node = GoNode(
        node_id="root_node",
        board_state=board_state,
        player_to_move="minimizer",
    )

    try:
        open_moves = sum(x == "+" for x in list(itertools.chain(*board_state)))

        depth = choose_search_depth(open_moves)
        logger.info(
            f"Executing minimax, searching to depth of {depth}, open moves: {open_moves}"
        )
        start_minimax = perf_counter()
        try:
            white_move_node = minimax_with_alpha_beta_pruning_algorithm(
                parent=root_node,
                depth=depth,
                winning_score=winning_score,
                start_time=start_minimax,
            )["move_node"]
        except Exception as e:
            message = f"Couldn't get white response {e}"
            logger.error(message)
            raise Exception(message)

        end_minimax = perf_counter()
        minimax_seconds_to_execute = f"{end_minimax - start_minimax:0.4f}"
        logger.info(
            f"\n>>> >>> Minimax seconds to execute: {minimax_seconds_to_execute} <<< <<<\n"
        )

    except Exception as e:
        message = f"get_white_response_no_tree failed with error: {e}"
        logger.error(message)
        raise Exception(message)

    logger.info(f"white_move_node: {white_move_node.__str__()}")

    assert (
        type(white_move_node) == GoNode
    ), f"White move node isn't of type GoNode for node: {white_move_node.get_node_id()}"
    white_move = white_move_node.move_coordinates
    logger.debug(f"white_move: {white_move}")
    return white_move
