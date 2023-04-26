from LocalSearch import Hill_Climbing,Simulated_Annealing, MAX_FITNESS
from Problem import*
from mazes import *

# hyper parameters
SCHEDULE = lambda t: 0.3 - t / 1000
MAX_FITNESS = 1

def Run_HillClimbing(problem: Problem, restarts: int = 1, visualize: bool = False):
    success = 0
    for i in range(restarts):
        ans = Hill_Climbing(problem, problem.random_state())
        if visualize:
            problem.visualize(ans)
        score = problem.evaluation(ans)
        if score == MAX_FITNESS:
            success += 1
    print("Hill Climbing with restarts.")
    print(f"Number of successes: {success} out of {restarts}")


def Run_Simulated_Annealing(problem: Problem, restarts: int = 1, visualize: bool = False):
    success = 0
    for i in range(restarts):
        ans = Simulated_Annealing(problem, SCHEDULE, problem.random_state())
        if visualize:
            problem.visualize(ans)
        score = problem.evaluation(ans)
        if score == MAX_FITNESS:
            success += 1
    print("Simulated Annealing with restarts.")
    print(f"Number of successes: {success} out of {restarts}")


def main():
    algorithm = input(f"Which algorithm do you want to run: "
                      f"\n(a)Hill Climbing "
                      f"\n(b)Simulated Annealing\n")

    restarts = int(input(f"How many restarts (1 - 100). Restart of 1 will turn on visualization. "))

    problem_type = input(f"Which problem do you want to run:"
                         f"\n(a) MazeNavigation "
                         f"\n(b) BitString \n")

    to_run = None
    problem = None
    if restarts == 1:
        visualize = True
    else:
        visualize = False

    if algorithm == "a":
        to_run = Run_HillClimbing
    elif algorithm == "b":
        to_run = Run_Simulated_Annealing
    else:
        print("Invalid algorithm option: "+algorithm)

    if problem_type == "a":
        start, target, maze = None, None, None
        maze_type = input(f"Which maze do you want to run: "
                          f"\n(a) Open Maze "
                          f"\n(b) Deceptive Maze 1 "
                          f"\n(c) Deceptive Maze 2\n")
        if maze_type == "a":
            start, target, maze = open_maze()
        elif maze_type == "b":
            start, target, maze = deceptive_maze3()
        elif maze_type == "c":
            start, target, maze = deceptive_maze4()
        else:
            print(f"Invalid maze option: "+maze_type)
        if maze is not None:
            genome_size = 20
            problem = MazeNavigation(genome_size, start,target,maze)

    elif problem_type == "b":
        genome_size = 10
        target = [1 for i in range(genome_size)]
        problem = BitString(genome_size, target)
    else:
        print(f"Invalid problem type: "+problem_type)

    if to_run is not None and problem is not None:
        to_run(problem, restarts, visualize)


if __name__ == '__main__':
    main()


