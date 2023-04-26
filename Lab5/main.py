from LocalSearch import Hill_Climbing,Simulated_Annealing, Genetic_Algorithm
from Problem import*
from mazes import *

#Hyperparameters
SCHEDULE = lambda x: 0.3 - x / 1000
POP_SIZE = 100
NUM_EPOCHS = 10

def Run_HillClimbing(problem: Problem, restarts: int = 1, visualize: bool = False):
    success = 0
    solutions = []
    avg_score = 0
    for i in range(restarts):
        ans = Hill_Climbing(problem, problem.random_state())
        print(f"answer is ")
        print(ans)
        if visualize:
            problem.visualize(ans)
        score = problem.evaluation(ans)
        avg_score += score
        if score == 1:
            success += 1
        solutions.append((score,ans))
    print("Hill Climbing with restarts.")
    print(f"Number of successes: {success} out of {restarts}")
    print(f"Average score is {avg_score / restarts}")


def Run_Simulated_Annealing(problem: Problem, restarts: int = 1, visualize: bool = False):
    rate = 0
    avg_score = 0
    solutions = []
    for i in range(restarts):
        ans = Simulated_Annealing(problem, SCHEDULE, problem.random_state())
        if visualize:
            problem.visualize(ans)
        score = problem.evaluation(ans)
        avg_score += score
        if score == 1:
            rate += 1
        solutions.append((score,ans))
    print("Simulated Annealing with restarts.")
    print(f"Number of successes: {rate} out of {restarts}")
    print(f"Average score: {avg_score/restarts}")


def Run_Genetic_Algorithm(problem: Problem, restarts: int = 1, visualize: bool = False):
    rate = 0
    avg_score = 0
    solutions = []
    initial_population = [problem.random_state() for _ in range(POP_SIZE)]
    for i in range(restarts):
        ans = Genetic_Algorithm(problem, initial_population, NUM_EPOCHS)
        if visualize:
            problem.visualize(ans)
        score = problem.evaluation(ans)
        avg_score += score
        if score == 1:
            rate += 1
        solutions.append((score,ans))
    print("Genetic Algorithm with restarts.")
    print(f"Number of successes: {rate} out of {restarts}")
    print(f"Average score: {avg_score/restarts}")

def main():
    algorithm = input(f"Which algorithm do you want to run: "
                      f"\n(a)Hill Climbing "
                      f"\n(b)Simulated Annealing"
                      f"\n(c)Genetic Algorith\n")

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
    elif algorithm == "c":
        to_run = Run_Genetic_Algorithm
    else:
        print("Invalid algorithm option: "+algorithm)

    if problem_type == "a":
        start, end, maze = None, None, None
        maze_type = input(f"Which maze do you want to run: "
                          f"\n(a) Open Maze "
                          f"\n(b) Deceptive Maze 1 "
                          f"\n(c) Deceptive Maze 2\n")
        if maze_type == "a":
            start, end, maze = open_maze()
        elif maze_type == "b":
            start, end, maze = deceptive_maze3()
        elif maze_type == "c":
            start, end, maze = deceptive_maze4()
        else:
            print(f"Invalid maze option: "+maze_type)
        if maze is not None:
            genome_size = 20
            problem = MazeNavigation(genome_size, start,end,maze)

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


