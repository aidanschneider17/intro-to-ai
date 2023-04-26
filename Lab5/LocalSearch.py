import math
import random
from Problem import *

def Best_State(problem: Problem, states: List[T]) -> List[T]:
    """
    Best Successor
    Helper function that finds the best successor 
    around a particular state
    :param problem: Class that posses search operators
    :param state: The current state
    :return: The best state
    """
    best_score = 0
    best_neighbor = None

    for s in states:
        current_score = problem.evaluation(s)

        if current_score > best_score:
            best_score = current_score
            best_neighbor = s

    return best_neighbor

def Contains_Max_Fitness(weights: List[T]) -> int:
    max_index = -1

    for i in range(len(weights)):
        if weights[i] == 1:
            max_index = i

    return max_index


def Hill_Climbing(problem: Problem, initial: T):
    """
    Hill Climbing search
    :param problem: Class that possess search operators
    :return: returns a state that is a local maximum
    """
    current = initial
    while True:
        neighbor = Best_State(problem, problem.successors(current))

        if problem.evaluation(neighbor) <= problem.evaluation(current):
            return current
        current = neighbor

def Simulated_Annealing(problem: Problem, schedule, initial: T):
    """
    Simulated Annealing
    :param problem: Class that possess search operators
    :return: returns a state that is a local maximum
    """

    current = initial

    t = 1
    while True:
        temperature = schedule(t)
        
        if temperature == 0 or problem.evaluation(current) == 1:
            return current
        neighbor = random.choice(problem.successors(current))
        deltaE = problem.evaluation(neighbor) - problem.evaluation(current)
        
        if deltaE > 0:
            current = neighbor
        elif random.random() < math.e**(deltaE/temperature):
            current = neighbor

        t += 1

def Genetic_Algorithm(problem:Problem, initial:List[List[T]], num_epochs:int=10,):
    """
    Genetic Algorithm implementation
    :param problem: Class the posses attributes for the initial population and methods for GA operator
    :param initial: Initial population
    :param num_epochs: How many iterations to
    :return: Individual with the best fitness found after num_epochs or until a solution is found
    """
    
    population = initial
    current_epochs = 0
    weights = []

    while current_epochs < num_epochs:
        for p in population:
            weights.append(problem.evaluation(p))
        if 1.0 in weights:
            return population[weights.index(1.0)]

        parents = problem.selection(population, weights, len(population))
        population2 = []
        for i in range(1, len(parents)+1):
            if i < len(parents):
                child = problem.crossover(parents[i-1], parents[i])
            else:
                child = problem.crossover(parents[0], parents[-1])
            child = problem.mutate(child)
            population2.append(child)

        population = population2

        weights = []
        current_epochs += 1

    return Best_State(problem, population)
