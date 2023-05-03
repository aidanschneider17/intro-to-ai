import math
import random
from Problem import *

def Hill_Climbing(problem: Problem, initial:T):
    """
    Hill Climbing search
    :param problem: Class that possess search operators
    :return: returns a state that is a local maximum
    """
    current = initial
    while True:
        neighbors = problem.successors(current)
        weights = list(map(lambda x: problem.evaluation(x), neighbors))
        best_neighbor = neighbors[np.argmax(weights)]
        if problem.evaluation(best_neighbor)>problem.evaluation(current):
            current = best_neighbor
        else:
            return current

def Simulated_Annealing(problem: Problem, schedule, initial:T):
    current = initial
    t = 1
    while True:
        T = schedule(t)
        if T == 0 or problem.evaluation(current) == 1:
            return current
        neighbors = problem.successors(current)
        weights = list(map(lambda x: problem.evaluation(x), neighbors))
        # best_neighbor = neighbors[np.argmax(weights)]
        random_neighbor = random.choice(neighbors)

        dE = problem.evaluation(random_neighbor) - problem.evaluation(current)

        if dE > 0:
            # print("Random better than current")
            # print(f"Going from {problem.evaluation(current)} to {problem.evaluation(random_neighbor)}")
            # print(f"random neighbor is better at {t} with {problem.evaluation(random_neighbor)}")
            current = random_neighbor
        elif random.random() < math.exp(dE/T):
            #print(f"Difference, time, and prob is {dE}, {T}, and {math.exp(dE / T)}")
            #print(f"Random neighbor at")
            # print(f"Picking random neighbor with probabiliy of {math.exp(dE/T)}")
            # print(f"Going from {problem.evaluation(current)} to {problem.evaluation(random_neighbor)}")
            current = random_neighbor
        else:
            pass
            # print("Not updating current")

        t += 1

def Genetic_Algorithm(problem:Problem, initial:List[T], num_epochs:int=10,):
    """
    Genetic Algorithm implementation
    :param problem: Class the posses attributes for the initial population and methods for GA operator
    :param num_epochs: How many iterations to
    :return: Individual with the best fitness found after num_epochs or until a solution is found
    """

    population = initial
    current_epochs = 0

    while current_epochs < num_epochs:
        weights = []
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

        current_epochs += 1

    return population[np.argmax(weights)]


