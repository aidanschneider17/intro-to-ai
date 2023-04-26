from Problem import *
import random
from math import e
MAX_FITNESS = 1

def Best_Successor(problem: Problem, state: T) -> List[T]:
    """
    Best Successor
    Helper function that finds the best successor 
    around a particular state
    :param problem: Class that posses search operators
    :param state: The current state
    :return: The best state
    """
    neighbors = problem.successors(state)
    best_score = 0
    best_neighbor = None

    for n in neighbors:
        current_score = problem.evaluation(n)

        if current_score > best_score:
            best_score = current_score
            best_neighbor = n

    return best_neighbor

def Hill_Climbing(problem: Problem, initial:T):
    """
    Hill Climbing
    :param problem: Class that possess search operators
    :return: returns a state that is a local maximum
    """

    current = initial
    while True:
        neighbor = Best_Successor(problem, current)

        if problem.evaluation(neighbor) <= problem.evaluation(current):
            return current
        current = neighbor

def Simulated_Annealing(problem: Problem, schedule, initial:T):
    """
    Simulated Annealing
    :param problem: Class that possess search operators
    :return: returns a state that is a local maximum
    """
    current = initial

    t = 1
    while True:
        temperature = schedule(t)
        
        if temperature == 0 or problem.evaluation(current) == MAX_FITNESS:
            return current
        neighbor = random.choice(problem.successors(current))
        deltaE = problem.evaluation(neighbor) - problem.evaluation(current)
        
        if deltaE > 0:
            current = neighbor
        elif random.random() < e**(deltaE/temperature):
            current = neighbor

        t += 1
