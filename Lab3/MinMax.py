from typing import Tuple, Any, List

from TicTacToe import *

def minimax_search(game:TicTacToe, board:List[int], current_player:int) -> list[Any]:
    """
    Start of the minimax algorithm
    :param game: Instance of a game
    :param board: List of 0s, 1s, and 2s that represents the state of the board.
    0s indicate where player 1 has moved, 1 indicates where player 2 has moved, and
    2s indicate an empty space
    :param current_player: ID of the max player and player for which utility
    scores are calculated. This can either be 0 or 1.
    :return: value and action that corresponds to the optimal move
    """
    value, action = max_value(game, board, 0, current_player)
    return [value,action]


def max_value(game, board, d, current_player) -> list[Any]:
    """
    Recursive function to find the max of possible successors
    to the game board.
    :param game: Instance of a game
    :param board: List of 0s, 1s, and 2s that represents the state of the board.
    0s indicate where player 1 has moved, 1 indicates where player 2 has moved, and
    2s indicate an empty space
    :param d: Maximum depth minimax can go
    :param current_player: ID of the max player and player for which utility
    scores are calculated. This can either be 0 or 1.
    :return: value and action that corresponds to the optimal move
    """

    # place-holder so code compiles. Should be replaced with the
    # actual max_value code
    if game.is_cutoff(board, d):
        return game.eval(board, current_player), None
    v = float('-inf')

    for a in game.actions(board):
        v2, a2 = min_value(game, game.result(board, a), d+1, current_player)

        if v2 > v:
            v, move = v2, a

    return v, move
    


def min_value(game, board, d, current_player):
    """
    Recursive function to find the min of possible successors
    to the game board.
    :param game: Instance of a game
        :param board: List of 0s, 1s, and 2s that represents the state of the board.
    0s indicate where player 1 has moved, 1 indicates where player 2 has moved, and
    2s indicate an empty space
    :param d: Maximum depth minimax can go
    :param current_player: ID of the max player and player for which utility
    scores are calculated. This can either be 0 or 1.
    :return: value and action that corresponds to the optimal move
    """

    if game.is_cutoff(board, d):
        return game.eval(board, current_player), None

    v = float('inf')

    for a in game.actions(board):
        v2, a2 = max_value(game, game.result(board, a), d+1, current_player)
        if v2 < v:
            v, move = v2, a

    return v, move
