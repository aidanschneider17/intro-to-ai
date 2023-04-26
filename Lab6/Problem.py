from __future__ import annotations  # needed in order to reference a Class within itself

import ast
import random
from copy import copy
from math import sqrt

from typing import List, Any, Generic, TypeVar, Tuple
from abc import ABC, abstractmethod
import numpy as np

from NeuralNetwork import NeuralNetwork

# https://realpython.com/python-type-checking/
T = TypeVar('T')


class Problem(ABC, Generic[T]):
    def __init__(self):
        """
        Generic problem that uses a neural networks as the state
         and can be solved with a Genetic Algorithm.
        """

    @abstractmethod
    def evaluation(self, current:T) -> float:
        """
        Evaluates a current state and returns a score the represents the fitness of that state.
        Larger scores means better.
        :param current: current state
        :return: fitness for the current state
        """
        pass

    @abstractmethod
    def random_state(self) -> T:
        """
        Creates a random state
        :return: new state object
        """
        pass

    @abstractmethod
    def visualize(self, current: T):
        """
        Method to visualize or print a state
        :param current: current state
        """
        pass

    def selection(self, current_population:List[T], weights:List[float], num_parents:int) -> List[T]:
        """
        Performs selection on the passed in population.
        Makes use of the fitness_proportionate_selection method
        :param current_population: List of genomes where each genome is a NN
        :param weights: List of fitness values for each genome in current_population.
        Assumes bigger is better (maximization).
        :param num_parents: number of individuals to return from the selection
        :return: list of individuals that are selected for the parents.
        """
        ret = []
        for i in range(num_parents):
            index = self.fitness_proportionate_selection(weights)
            ret.append(current_population[index])
        return ret

    def fitness_proportionate_selection(self, weights:List[float]) -> int:
        """
        Performs fitness proportionate selection.
        :param current_population: List of genomes where each genome is a NN
        :param weights: List of fitness values for each genome in current_population.
        Assumes bigger is better (maximization).
        :return: index of individual to choose
        """

        return 0

    def crossover(self, parent1:T, parent2:T) -> T:
        """
        Performs crossover on the two passed in parents.
        :param parent1: Genome which is a NN
        :param parent2: Genome which is a NN
        :return: child that is the combination of parent1 and parent2
        """
        pass


    def mutate(self, child:T) -> T:
        """
        Performs mutation of a genome
        :param child: Genome which is a NN
        :return: Genome that has been mutated
        """
        pass


class NNClassification(Problem[NeuralNetwork]):

    """
    Class the represents a classification problem that uses a NeuralNetwork as the state.
    Class uses a list of training data to perform evaluations. Each sample of the training data
    contains the input and expected output for that sequence. See the evaluation method for more details.
    The NeuralNetwork contains two lists that represent the normal and bias weights of the network.
    See develop_weights() and develop_bias() in Neural Network for a detailed explanation of how the
    weights map onto the connections of the network.
    """

    def __init__(self, layers:List[int], training_data: List[List[float]]):
        """
        Initializes a Neural Network Classification type search problem.
        :param layers: List of ints that specify the number of input, hidden, and output nodes
        :param training_data: List of samples where sample consist of the network input and expect output
        """
        super().__init__()
        self._training_data = training_data
        self._layers = layers


    def evaluation(self, current:T) -> float:
        """
        Evaluates the current state and returns a score the represents
        the fitness of that state. Higher means better.
        The training data is a list of lists. Each inner list is referred to as
        sample or sequence. Each sample is a list of values. The first n values
        correspond to the inputs to the network and the last m values correspond
        to the output of that network.
        For example, for the OR task the network will have two inputs and 1 output.
        The training data would have four samples: [[0,0,0],[0,1,1],[1,0,1],[1,1,1]].
        For each sample, the first two values would be the input and the last value
        would be the expected output. So for the first sample, [0,0] would be the
        input to the network and [1] would be the expected output.
        :param current: Current state which is a NeuralNetwork object
        :return: Score that represents how close the output of the network
        matches the expected output across all the samples in the training data
        """

        return 0.1


    def random_state(self) -> T:
        """
        Generates a random state (i.e. genome) of the given size.
        :return: New random list of 1s and 0s of size self._genome_size
        """
        return NeuralNetwork(self._layers)


    def visualize(self, solution:T):
        """
        Debugging printing.
        :param solution: Test solution
        """
        solution.print_network()

    def crossover(self, parent1:T,parent2:T) -> T:
        """
        Performs crossover over on a Neural Network object.
        For this implementation of crossover, you need to create a child
        whose normal and bias weights values are the combination of the normal
        and bias weight values of the two parents. To combine the normal weights
        values of the parents, you would compute a crossover point and create
        a new list of normal weights values from parent1 and parent2 based off that
        crossover point. You would repeat process for the bias weight values
        :param parent1: NeuralNetwork object that has a list of normal and bias weight values
        :param parent2: NeuralNetwork object that has a list of normal and bias weight values
        :return: New child which is a NeuralNetwork object
        """

        return parent1

    def single_point_crossover_NN(self, parent1:T, parent2:T, cw:int, cb:int) -> T:
        """H
        elper method for the crossover method. See the docstring of crossover
        for a full explanation of how crossover should work for a NeuralNetwork object.
        :param parent1: NeuralNetwork object that has a list of normal and bias weight values
        :param parent2: NeuralNetwork object that has a list of normal and bias weight values
        :param cw: Crossover point for the normal weight values
        :param cb: Crossover point for the biasa weight values
        """

        return parent1

    def mutate(self, child:T) -> T:
        """
        Performs a bit mutation on a NeuralNetwork object that has two lists
        of weight values: normal and bias weights values. This method should iterate
        over all the normal weight values and mutate one with a probability of 1/n,
        where n is the number of normal weights values. It should then iterate over
        all the weights the bias weight values and mutate a weight with a probability
        of 1/b where b is the number fo bias weight values.
        :param child:
        :return:
        """
        ret = copy(child)

        return ret
    def mutate_weight(self, child: T, weight_index: int, normal_weight:bool = True) -> T:
        """
        Performs a bit-mutation on the passed in list of weights. Add a random uniform
        value to the weight at the specified index. If normal_weight is True, it modifies
        a weight in the normal weight values list. If normal_weight if False, it modifies
        a weight in the bias weight values list.
        :param child: Genome which is a list of type T
        :param weight_index: Which bit to mutate
        :param normal_weight: Whether the mutated weight is in the normal weights or bias weights list
        :return: Genome that has been mutated
        """
        ret = copy(child)

        return ret
