from copy import copy
from random import randint
from typing import List

import numpy as np

DEPTH_LIMIT = 2

class TicTacToe:
    """
    Class that represents a Tic Tac Toe game. Includes methods to
    manipulate the board, get actions, execute moves, and evaluate
    states
    """
    def __init__(self):
        """
        symbol: Symbols displayed on the board. X corresponds to player 0 and O
        corresponds to player 1. # corresponds to an empty space (id 2)
        player: ids for the two players. These values show up on the actual
        board object and are used in various operations
        empty: id for the empty spots of the board
        s: dimensions of the board
        board: main data structure that holds the current board state which includes
        moves made by both players (0 and 1) and empty spaces (2). When printed, the
        symbols for each player (X for 0 and O of 1) are printed, not the actual ids.
        board is a list of [0s,1s, and 2s].
        """
        self._symbol: List[str] = ["X","O","#"]
        self._player: List[int] = [0, 1]
        self._empty: int = 2
        self._s: int = 3
        self._board: List[int] = [self._empty for i in range(self._s * self._s)]

    @property
    def symbol(self) -> List[str]:
        return self._symbol

    #@property
    #def empty(self) -> int:
    #    return self._empty

    @property
    def board(self) -> List[int]:
        return self._board

    #@property
    #def player(self) -> List[int]:
    #    return self._player

    @board.setter
    def board(self, b: List[int]):
        self._board = b

    def print_board(self, board:List[int]) -> None:
        """
        Prints the elements of the 1D list as an s x s square.
        Prints the elements based on their correspond symbol.
        :param board: List of 0s, 1s, and 2s that represent a game state.
        """
        res = ""
        for i in range(self._s):
            for j in range(self._s):
                res += self._symbol[board[i*self._s + j]]+"|"
            res += "\n"
        print(res)

    def random_move(self, board:List[int]) -> int:
        """
        Returns a random move/action
        :param board: List of 0s, 1s, and 2s that represent a game state.
        :return: Number from 1-9
        """
        avail = self.actions(board)
        return avail[randint(0, len(avail) - 1)]

    def is_cutoff(self, board:List[int], d: int) -> bool:
        """
        Returns true or false if the board is at the depth limit or terminal state.
        :param board: List of 0s, 1s, and 2s that represent a game state.
        :param d: current depth
        :return: true or false if we are at the depth limit or terminal state
        """
        return d >= DEPTH_LIMIT or self.terminal(board)

    def eval(self, board:List[int], current_player:int) -> float:
        """
        Returns either the utility or expected utility of the
        current board with respect to the current_player. High utility is
        if the current_player has a lot of possible ways
        left to win and the other player has few.
        :param board: List of 0s, 1s, and 2s that represent a game state.
        :param current_player: Which player (0 or 1) is currently MAX
        :return: a value for the current board. -1 to 1
        """
        if self.terminal(board):
            return self._utility(board, current_player)
        else:
            # Assumes the player that is not MAX is the MIN player
            other_player = self._get_other_player(current_player)
            max_eval = 5  # biggest possible eval score (8-4) ?
            current_player_options = self._count_options(board, current_player)
            other_player_options = self._count_options(board, other_player)
            return (current_player_options - other_player_options) / max_eval

    def actions(self, board:List[int]) -> List[int]:
        """
        Returns a list of possible actions left from 1-9
        Each action represent a possible place to move
        on the board.
        :param board: List of 0s, 1s, and 2s that represent a game state.
        :return: List of numbers from 1-9
        """
        return [i + 1 for i in range(len(board)) if board[i] == self._empty]

    def result(self, board:List[int], action:int) -> List[int]:
        """
        Executes an action by the current player p. This involves
        setting the location, indicated by action, to the value of p
        :param board: List of 0s, 1s, and 2s that represent a game state.
        :param action: A value from 1-9, which indicates which square
        the player per is moving to. Assumes the action is valid.
        :return: returns an altered copy of the board with the executed move
        """
        player = self._current_turn(board)
        new_board = copy(board)
        new_board[action - 1] = player
        return new_board

    def _current_turn(self, board:List[int]) -> int:
        """Evaluates the board and figures out whose turn it is.
        :param board: List of 0s, 1s, and 2s that represent a game state.
        Assumes 0 ("X") goes first"""
        if board.count(self._player[0]) > board.count(self._player[1]):
            return self._player[1]
        else:
            return self._player[0]

    def terminal(self, board:List[int]) -> bool:
        """
        Returns true or false if the board is at a terminal state.
        We are at a terminal state is a player has won or there
        are no moves left.
        :param board: List of 0s, 1s, and 2s that represent a game state.
        :return: true or false depending of if the board is in a terminal state
        """
        # a player has won
        for p in self._player:
            if self._winner(board, p):
                return True
        # no empty spaces
        # if (np.array(self._board) != self._empty).all():
        #     return True
        if board.count(self._empty) == 0:
            return True
        return False

    def _winner(self, board:List[int], player:int) -> int:
        """
        Checks if there is a line on the board of just player id
        :param board: List of 0s, 1s, and 2s that represent a game state.
        :param player: id of the player (0 or 1)
        :return: True or False if the passed in player has won
        """
        np_board = np.reshape(np.array(board),(self._s,self._s))

        #check rows equal player
        for i in range(np_board.shape[0]):
            if (np_board[i,:] == player).all():
                return True

        #check cols equal player
        for i in range(np_board.shape[1]):
            if (np_board[:,i] == player).all():
                return True

        #check diagonals
        if (np_board.diagonal() == player).all() or (np.fliplr(np_board).diagonal() == player).all():
            return True

    def _utility(self, board:List[int], current_player:int) -> float:
        """
        Returns the utility of the current board with respect to the
        max_player. The max_player could be 0 or 1, depending on whose
        turn it is. Should only be called if the board is at a terminal state.
        :param current_player: Which player (0 or 1) is currently MAX
        :return: Returns 1 if the winner is the max_player,
        0 if it is a draw (i.e. no spaces left),
        else -1 (assumes that the min_player won)
        """
        other_player = self._get_other_player(current_player)

        # current player has won
        if self._winner(board, current_player):
            return 1
        # other player was won
        elif self._winner(board, other_player):
            return -1
        #no spaces left
        #elif (np.array(board) != self._empty).all():
        #    return 0
        elif board.count(self._empty) == 0:
            return 0
        # should never reach this state
        else:
            raise RuntimeError("Bad board in self.utility")

    def _get_other_player(self, current_player) -> int:
        """
        Helper methods to get the id of the other player.
        :param current_player: ID of the player whose go is it
        :return: ID of player whose go it is not
        """
        other_player = -1
        for p in self._player:
            if p is not current_player:
                other_player = p

        if other_player == -1:
            raise RuntimeError("Bad current player or self._player in get_other_player")

        return other_player

    def _count_options(self, board:List[int], player:int) -> int:
        """
        Counts the number of options/lines the player has left available
        to win. Using the board below as an example, player 0 has 8 options
        to win. They can get the four cross lines, the top and bottom rows,
        left and right columns, and the two diagonals.
        222
        202
        222
        Using the board below, player 1 has four options. They can get the
        top and bottom rows and the left and right columns.
        212
        202
        222
        :param board: List of 0s, 1s, and 2s that represent a game state.
        :param player: Whose turn it is. Either 0 or 1
        :return: Number of lines the player could win
        """
        np_board = np.reshape(np.array(board), (self._s, self._s))
        count = 0
        #number of rows with just the current_player or empty
        for i in range(np_board.shape[0]):
            if ((np_board[i, :] == player) + (np_board[i, :] == self._empty)).all():
                count += 1

        #number of cols with just the current_player or empty
        for i in range(np_board.shape[1]):
            if ((np_board[:, i] == player) + (np_board[i, :] == self._empty)).all():
                count += 1

        #number of diags with just the current_player or emtpy
        if ((np_board.diagonal() == player) + (np_board.diagonal() == self._empty)).all():
           count += 1

        if ((np.fliplr(np_board).diagonal() == player) + (np.fliplr(np_board).diagonal() == self._empty)).all():
            count += 1

        return count

    def print_game_over(self, current_player:int, player_type:str):
        """
        Prints a game over message
        :param current_player: Id for the current player, 0 or 1
        :param player_type: Player type: human, AI, random
        :return:
        """
        print("----------------------\nGame Over\n")
        self.print_board(self._board)
        score = self._utility(self._board, current_player)
        msg = "\tWinner: "
        if score == 0:
            msg += "Draw"
        else:
            msg += "\n\tWinner: " + str(self._symbol[current_player]) + " (" + player_type[current_player] + ")"
        msg += "\n---------------------\n"
        print(msg)


