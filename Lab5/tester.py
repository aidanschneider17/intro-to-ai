from Problem import BitString, MazeNavigation
from mazes import open_maze
from math import isclose
from random import random,randint

def test_crossover(type):
    if type == 1:
        problem = BitString(4, [1 for i in range(4)])
        results = [[0,0,0,0], [1,0,0,0], [1,1,0,0],[1,1,1,0]]
        for i in range(4):
            assert results[i] == problem.single_point_crossover([1,1,1,1],[0,0,0,0],i)

    elif type == 2:
        start, end, maze = open_maze()
        problem = MazeNavigation(4,start,end,maze)

        p1 = [(0, -1), (1, 0), (0, 1), (-1, 0), (0, 0)]
        p2 = [(0, 0), (-1, 0), (0, 1), (1, 0), (0, -1)]
        results = [[(0, 0), (-1, 0), (0, 1), (1, 0), (0, -1)],
                   [(0, -1), (-1, 0), (0, 1), (1, 0), (0, -1)],
                   [(0, -1), (1, 0), (0, 1), (1, 0), (0, -1)],
                   [(0, -1), (1, 0), (0, 1), (1, 0), (0, -1)],
                   [(0, -1), (1, 0), (0, 1), (-1, 0), (0, -1)]]
        for i in range(5):
            assert results[i] == problem.single_point_crossover(p1, p2, i)

def test_mutate(type):
    if type == 1:
        problem = BitString(4, [1 for i in range(4)])
        child = [0, 0, 0, 0]
        expected = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
        for i in range(len(child)):
            assert expected[i] == problem.mutate_bit(child, i)

    elif type == 2:
        start, end, maze = open_maze()
        problem = MazeNavigation(4, start, end, maze)

        child = [(0, -1), (1, 0), (0, 1), (-1, 0), (0, 0)]
        bit_index = 0
        expected = [[(1, 0), (1, 0), (0, 1), (-1, 0), (0, 0)],
                    [(0, 1), (1, 0), (0, 1), (-1, 0), (0, 0)],
                    [(-1, 0), (1, 0), (0, 1), (-1, 0), (0, 0)],
                    [(0, 0), (1, 0), (0, 1), (-1, 0), (0, 0)]]
        for i in range(100):
            result = problem.mutate_bit(child,bit_index)
            assert result in expected

def test_selection(type):
    problem = BitString(4, [1 for i in range(4)])
    if type == 1:
        pop = [[1,1,1,1] for i in range(5)]
        weights = [2,3,1,3,1]
        prob = [w/sum(weights) for w in weights]

        counts = [0 for i in range(len(weights))]
        num_runs = 100000
        tolerance = 0.01
        for i in range(num_runs):
            index = problem.fitness_proportionate_selection(pop,weights)
            counts[index] += 1

        for i in range(len(prob)):
            index_prob = counts[i]/num_runs
            print(f"Selected prob: {index_prob}, Expected prob: {prob[i]}")
            assert isclose(index_prob,prob[i], abs_tol=tolerance)
    if type == 2:
        pop = [[1, 1, 1, 1] for i in range(randint(1,5))]
        weights = [random() for i in range(len(pop))]
        prob = [w / sum(weights) for w in weights]
        for i in range(len(pop)):
            print(f"{pop[i]}:{weights[i]}")
        counts = [0 for i in range(len(weights))]
        num_runs = 100000
        tolerance = 0.01
        for i in range(num_runs):
            index = problem.fitness_proportionate_selection(pop, weights)
            counts[index] += 1

        for i in range(len(prob)):
            index_prob = counts[i] / num_runs
            print(f"Selected prob: {index_prob}, Expected prob: {prob[i]}")
            assert isclose(index_prob, prob[i], abs_tol=tolerance)

if __name__ == '__main__':
    #test_crossover(1)
    #test_crossover(2)
    #test_mutate(1)
    test_mutate(2)
    #test_selection(2)

