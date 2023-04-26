from __future__ import annotations  # needed in order to reference a Class within itself

import ast
import random
from copy import copy
from typing import List, Any, Generic, TypeVar, Tuple
from abc import ABC, abstractmethod
import numpy as np

from shapes import *

# https://realpython.com/python-type-checking/
T = TypeVar('T')


class Problem(ABC, Generic[T]):
    def __init__(self, genome_size):
        """
        Generic problem that can be solved with a Local Search algorithm.
        Has operations to manipulate a state which is a python list of type T
        :param genome_size: size of the genome
        """
        self._genome_size = genome_size

    @abstractmethod
    def evaluation(self, current:List[T]) -> float:
        """
        Evaluates a current state and returns a score the represents the fitness of that state.
        Larger scores means better.
        :param current: current state
        :return: fitness for the current state
        """
        pass

    @abstractmethod
    def successors(self, current: List[T]) -> List[T]:
        """
        Creates a new list of states that are neighboring(successor) states of current.
        The number of neighboring states is equal to the number of states that are "one step"
        away from current. "One step" usually means one permutation of an element with the state.
        :param current: Current state
        :return: List of successors to the current state that are one step (i.e. one permutation) away
        """
        pass


    @abstractmethod
    def random_state(self) -> List[T]:
        """
        Creates a random state
        :return: new state object
        """
        pass

    @abstractmethod
    def visualize(self, current: List[T]):
        """
        Method to visualize or print a state
        :param current: current state
        :return:
        """
        pass


class MazeNavigation(Problem[Tuple[int, int]]):
    """
    Class the represents a MazeNavigation Problem that can be solved with a Local Search.
    Contains functions needed to manipulate a state (also called a genome) that is a python
    list of tuples. Each tuple represents a vertical (dy) and horizontal (dx) movement.
    For example, a state could be [(0,1), (1,0),(0,1)] which represents a North, Each, and
    then North movement.
    """

    def __init__(self, genome_size:int, start_position: Tuple[int, int], target_position: Tuple[int, int], maze: np.array):
        """
        Initializes a MazeNavigation type search problem.
        :param genome_size: Length of the state (genome)
        :param start_position: Starting location from which to execute moves
        :param target_position: Target location used to calculate fitness score (self.evaluation())
        :param maze: Numpy array that represents the maze. See the legend below for what the numbers mean
        """
        super().__init__(genome_size)
        self._start_pos = start_position
        self._target_pos = target_position
        self._maze = maze

        # what each of the numbers in the maze means
        self._character = 2
        self._walkable = 1
        self._impassable = 0
        # North, East, South, West, Stay
        self._moves = [(0, -1), (1, 0), (0, 1), (-1, 0), (0, 0)]

        # Used to draw and visualize the maze
        self._w = 640
        self._h = 640
        self._paper = Paper(self._w, self._h)

    @property
    def maze(self) -> np.array:
        return self._maze

    def evaluation(self, current: List[T]) -> float:
        """
        Evaluates a current state and returns a score the represents the fitness of that state.
        Simulates the moves of the passed in state to figure out the end position and then compares
        that to the target position
        :param current: list of tuples that represent 2D moves
        :return: distance between the position reached by following the moves in state to self._end_pos
        """

        path = self._generate_path(current)
        score = abs(path[-1][0] - self._target_pos[0]) + abs(path[-1][1] - self._target_pos[1])
        # Max distance two points can be from one another in the maze
        max_distance = self._maze.shape[0] + self._maze.shape[1]
        return (max_distance - score) / max_distance  # normalizes it to be between 0 and 1

    def _generate_path(self, current: List[T]):
        """
        Runs through the moves in current and generates a path through the maze. Starts the
        path at self._start_pos
        :param current: list of tuples that represent 2D moves
        :return: Path through the maze given the moves in current
        """
        current_loc = self._start_pos
        path = [current_loc]
        for m in current:
            new_loc = (current_loc[0] + m[0], current_loc[1] + m[1])
            # checks to see if the new location is out of bounds or impassable
            if 0 <= new_loc[0] < np.shape(self._maze)[0] and 0 <= new_loc[1] < np.shape(self._maze)[1] \
                    and self._maze[new_loc] != self._impassable:
                current_loc = new_loc
            path.append(current_loc)

        return path

    def successors(self, current: List[T]) -> List[T]:
        """
        Creates a new list of state objects that are neighboring(successor) states of current.
        The number of neighboring states is equal to the number of states that are "one step"
        away from current. "One step" usually means one permutation of an element with the state.
        :param current: list of tuples that represent 2D moves
        :return: List of successors to the current state that are one step (i.e. one permutation) away
        """
        ret = []
        for a in self._actions(current):
            next_state = self._result(current, a)
            ret.append(next_state)
        return ret

    def _actions(self, current: List[T]) -> List[str]:
        """
        Returns a list of actions available for the given state.
        :param current: list of tuples that represent 2D moves
        :return: List of actions encoded as Strings
        """
        ret = []
        state: T

        # current is a list of moves and each move has 5 possible
        # permutations (see self._moves) An action is a tuple consisting
        # of the index of a move in current and one of the possible moves is self._moves
        # For example, if current is [(0,1), (1,0),(0,1)] #North, East, North
        # actions are:
        # [(0:(0,1)), (0:(1,0)), (0:(0,-1)), (0:(-1,0)), (0:(0,0)),
        # [(1:(0,1)), (1:(1,0)), (0:(1,-1)), (1:(-1,0)), (1:(0,0)),
        # [(2:(0,1)), (2:(1,0)), (0:(2,-1)), (2:(-1,0)), (2:(0,0))]
        # The first five actions change the first move to North, East, South, West, or Stay.
        # The next five actions chant the second move to North, East, South, West, or Stay.
        # The next five actions...
        # Note it is possible that a move will cause the agent to run
        # into a wall. That's fine and will be taken care of in the
        # evaluation function
        for i in range(len(current)):
            for j in range(len(self._moves)):
                ret.append(f"{i}:{self._moves[j]}")

        return ret

    def _result(self, current: List[T], action: str) -> T:
        """
        Returns the state generated given the passed in state and action
        :param current: list of tuples that represent 2D moves
        :param action: String that represents an action
        :return: state that is the result of applying an action to the current state
        """

        # a state is a list of moves where each move is a tuple
        # For example [(0,1), (1,0),(0,1)] is North, East, North
        ret = copy(current)
        # action is a string that holds an index and a new move
        i = int(action.split(":")[0])
        m = ast.literal_eval(action.split(":")[1])

        # replace the move at index i with move m
        ret[i] = m
        return ret

    def random_state(self):
        """
        Generates a random state (i.e. genome) of the given size. For MN
        a state is a list of moves.
        :return: List of moves
        """
        ret = []
        for i in range(self._genome_size):
            ret.append(random.choice(self._moves))
        return ret

    def visualize(self, current: List[T]):
        """
        Draws the maze and the path made by the current state(genome).
        :param current: list of tuples that represent 2D moves
        """
        # self._paper.clear()
        grid_size = min(int(self._h / self._maze.shape[0]), int(self._w / self._maze.shape[1]))
        r = Rectangle()
        r.set_width(grid_size)
        r.set_height(grid_size)

        for i in range(self._maze.shape[0]):
            for j in range(self._maze.shape[1]):
                r.set_x(j * grid_size)
                r.set_y(i * grid_size)
                if i == self._start_pos[0] and j == self._start_pos[1]:
                    r.set_color("green")
                elif i == self._target_pos[0] and j == self._target_pos[1]:
                    r.set_color("red")
                elif self._maze[i][j] == 0:  # impassable
                    r.set_color("black")
                elif self._maze[i][j] == -1:  # higher path cost
                    r.set_color("gray")
                else:
                    r.set_color("white")
                r.draw()

        path = self._generate_path(current)
        print("Path is ")
        print(path)
        # draw the path
        for p in path:
            r.set_x(p[1] * grid_size)
            r.set_y(p[0] * grid_size)
            r.set_color("cyan")
            r.draw()
        r.set_x(path[-1][1] * grid_size)
        r.set_y(path[-1][0] * grid_size)
        r.set_color("blue")
        r.draw()

        self._paper.display()


class BitString(Problem[List[int]]):
    """
    Class the represents a BitSTring Problem that can be solved with a Local Search.
    Contains functions needed to manipulate a state (also called a genome) that is a python
    lists of 1s and 0s.
    """

    def __init__(self, genome_size:int, target: List[int]):
        """
        Initializes a BitString type search problem. The state objects are
        python lists of 1s or 0s
        :param genome_size: lenght of the state list
        :param target:  target state
        """
        super().__init__(genome_size)
        self._target = target

    def evaluation(self, current: T) -> float:
        """
        Evaluates the current state and returns a score the represents
        the fitness of that state. Higher means better.
        :param current: Current state which is a list of 1s and 0s
        :return: Number of digits that match between current and target,
        normalized to be between 0 and 1
        """

        #  Should return the number of bits that are the same between
        #  current and self._target normalized to be between 0 and 1
        #  For example, if current is [0,0,0,0] and target is [0,1,1,1]
        #  then the score should be 0.25
        correct = 0.0;

        for i in range(self._genome_size):
            if current[i] == self._target[i]:
                correct += 1.0;

        return correct/self._genome_size

    def successors(self, current: T) -> List[T]:
        """
        Creates a new list of states that are one step away from the current state
        :param current: Current state which is a list of 1s and 0s
        :return: List of neighboring states
        """
        # TODO
        #  Generating the successors for a BitString is
        #  simple enough that you don't need an _actions or
        #  _result helper method. A BitString of length n has
        #  n successors where each successors is one bit different
        #  from the initial BitString. For example, if current is
        #  [1,0,1,0] it has 4 successors: [[0,0,1,0],[1,1,1,0],[1,0,0,0],[1,0,1,1]]
        neighbors = []

        for i in range(self._genome_size):
            neighbor = list(current)
            neighbor[i] = (neighbor[i] -1) * -1
            neighbors.append(neighbor)

        return neighbors

    def random_state(self):
        """
        Generates a random state (i.e. genome) of the given size.
        :return: New random list of 1s and 0s of size self._genome_size
        """
        ret = []
        for i in range(self._genome_size):
            ret.append(random.randint(0, 1))
        return ret

    def visualize(self, solution: T):
        """
        Debugging printing.
        :param solution: Test solution
        """
        print(f"Target is: {self._target}")
        print(f"Solution is: {solution}")
        print(f"Evaluation score: {self.evaluation(solution)}")
