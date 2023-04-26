from LocalSearch import Genetic_Algorithm
from Problem import *
import csv

#Hyperparameters
POP_SIZE = 100
NUM_EPOCHS = 100

def Run_Genetic_Algorithm(problem: Problem, restarts: int = 1, visualize: bool = False):
    rate = 0
    avg_score = 0
    solutions = []
    initial_population = [problem.random_state() for _ in range(POP_SIZE)]
    for i in range(restarts):
        ans = Genetic_Algorithm(problem, initial_population, NUM_EPOCHS)
        score = problem.evaluation(ans)
        avg_score += score
        if score == 1:
            rate += 1
        solutions.append((score,ans))
    print("Genetic Algorithm with restarts.")
    print(f"Number of successes: {rate} out of {restarts}")
    print(f"Average score: {avg_score/restarts}")
    return solutions[0][1]

def verify_network(network:NeuralNetwork, training_data:List[float]):
    print(f"Visualizing network")
    network.print_network()
    num_inputs = network.layers[0]
    for i in range(len(training_data)):
        input = training_data[i][0:num_inputs]
        expected = training_data[i][num_inputs:]
        result = network.step(input)
        print(f"Expected: {expected}, Actual: {result}")

def load_tictactoe_csv(filename:str):
    NUM_INPUTS = 9
    inputs = []
    expected = []
    with open(filename, newline='') as csvfile:
        lines = csv.reader(csvfile, delimiter=',')
        for i, line in enumerate(lines):
            newLine = list(map(lambda x: 0 if x == 'x' or x == 'Xwin' else 1, line))
            inputs.append(newLine[0:NUM_INPUTS])
            expected.append(newLine[NUM_INPUTS:])
    return inputs,expected

def load_training(problem_name:str):
    inputs = []
    expected = []
    if "OR" in problem_name and "XOR" not in problem_name:
        inputs = [[0,0],[0,1],[1,0],[1,1]]
        expected = [[0],[1],[1],[1]]
    elif "AND" in problem_name:
        inputs = [[0,0],[0,1],[1,0],[1,1]]
        expected = [[0],[0],[0],[1]]
    elif "XOR" in problem_name:
        inputs = [[0, 0], [0, 1], [1, 0], [1, 1]]
        expected = [[0], [1], [1], [0]]
    elif "TTT" in problem_name:
        inputs,expected = load_tictactoe_csv("tic-tac-toe.csv")

    ret = []
    for i in range(len(inputs)):
        ret.append(inputs[i] + expected[i])
    #    return list(zip(inputs, expected))
    return ret


def main():
    verify = False
    restarts = 1

    print("Training with a Genetic Algorithm")
    restarts = int(input(f"How many restarts (1 - 100). Restart of 1 will turn on verification. "))
    if restarts == 1:
        verify = True

    ga_problems = [["No Hidden Layer OR",[2,1]], ["No Hidden Layer AND",[2,1]],
                  ["No Hidden XOR",[2,1]], ["No Hidden Layer TTT",[9,1]],
                  ["Single Hidden Layer OR",[2,1,1]],["Single Hidden Layer AND",[2,1,1]],
                  ["Single Hidden XOR",[2,2,1]], ["Single Hidden Layer TTT",[9,3,1]]]


    print(f"Available problems:\n")
    for i, p in enumerate(ga_problems):
        print(f"{i}) {p}")
    problem_type = int(input())
    td = load_training(ga_problems[problem_type][0])
    layers = ga_problems[problem_type][1]
    problem = NNClassification(layers,td)
    ans = Run_Genetic_Algorithm(problem,restarts,verify)
    if verify:
        verify_network(ans,td)
if __name__ == '__main__':
    main()


