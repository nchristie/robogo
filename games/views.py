from django.shortcuts import render
from django.views import View
from .models import Game, Move
from .forms import MoveForm
from .stones import EMPTY_POSITION, WHITE_STONE, BLACK_STONE
from .go_minimax_joiner import GoNode, GoTree
from .minimax import are_break_conditions_met
from .game_logic import *
import itertools

import logging

logger = logging.getLogger(__name__)

DEPTH = 100000

INF = float("inf")

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
            if BLACK_STONE in list(itertools.chain(*my_board.state)):
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
            else:
                logger.error(f"No black stones on board")

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
    root_node = GoNode(
        node_id="root_node",
        player="maximizer",
        score=None,
        children=[],
        board_state=board_state,
    )
    try:
        white_move_node = minimax_depth_of_3(root_node)
        assert (
            type(white_move_node) == GoNode
        ), f"White move node isn't of type GoNode for node: {white_move_node.node_id}"
        white_move = white_move_node.move_coordinates
        # logger.info(f"white_move: {white_move}, best_score: {white_move_node.get_score()}")
        return white_move
    except Exception as e:
        logger.error(f"minimax_depth_of_X failed with error: {e}")


def minimax_depth_of_2(root_node):
    depth = 2
    game_tree = GoTree(root_node)
    game_tree.build_game_tree_recursive(root_node, depth, set())

    current_node = game_tree.root_node

    for child in current_node.get_children():
        for child2 in child.get_children():
            child2.set_score(child2.get_utility())
        child2_optimal_move = child.get_optimal_move()
        child.set_score(child2_optimal_move.get_score())

    return game_tree.root_node.get_optimal_move()


def minimax_depth_of_3(root_node):
    logger.info("In minimax_depth_of_3")

    game_tree = GoTree(root_node)

    current_node = game_tree.root_node
    alpha = -INF
    beta = INF

    for child2 in current_node.generate_next_child(
        depth=2, parent_node_id=current_node.node_id
    ):
        if abs(child2.get_utility()) == INF:
            child2.set_score(child2.get_utility())
            continue
        for child1 in child2.generate_next_child(
            depth=1, parent_node_id=child2.node_id
        ):
            if abs(child1.get_utility()) == INF:
                child1.set_score(child1.get_utility())
                continue
            for child0 in child1.generate_next_child(
                depth=0, parent_node_id=child1.node_id
            ):
                # get utility for each leaf node
                child0.set_score(child0.get_utility())

                # use that utility to update the value of alpha or beta
                alpha, beta = game_tree.set_alpha_and_beta(child0, alpha, beta)

                child1.add_child(child0)
                child1.set_score(child1.get_optimal_move().get_score())
                if are_break_conditions_met(alpha, beta):
                    logger.info(f"Pruning at {child0.node_id}")
                    break

            # use the inherited value of child1 to update alpha or beta
            alpha, beta = game_tree.set_alpha_and_beta(child1, alpha, beta)
            child2.add_child(child1)
            child2.set_score(child2.get_optimal_move().get_score())
            if are_break_conditions_met(alpha, beta):
                logger.info(f"Pruning at {child1.node_id}")
                break

        # use the inherited value of child2 to update alpha or beta
        alpha, beta = game_tree.set_alpha_and_beta(child2, alpha, beta)
        child2.set_score(child2.get_optimal_move().get_score())
        current_node.add_child(child2)
        current_node.set_score(current_node.get_optimal_move().get_score())
        if are_break_conditions_met(alpha, beta):
            logger.info(f"Pruning at {child2.node_id}")
            break

    logger.info("*** printing move_coordinates based on best path ***")
    logger.info("best child at depth 2:")
    move = current_node.get_optimal_move()
    logger.info(f"{move.player}, {move.move_coordinates}, {move.get_score()}")

    logger.info("best child at depth 1:")
    move = current_node.get_optimal_move().get_optimal_move()
    logger.info(f"{move.player}, {move.move_coordinates}, {move.get_score()}")

    logger.info("best child at depth 0:")
    move = current_node.get_optimal_move().get_optimal_move().get_optimal_move()
    logger.info(f"{move.player}, {move.move_coordinates}, {move.get_score()}")

    return current_node.get_optimal_move()
