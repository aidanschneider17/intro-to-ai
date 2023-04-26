import csv
from NeuralNetwork import NeuralNetwork

def load_network(filename):
    ret = []
    with open(filename, newline = '') as csvfile:
        lines = csv.reader(csvfile, delimiter = ',')
        for i,line in enumerate(lines):
            if i == 0: # layer values
                ret.append([int(i) for i in line])
            else:
                ret.append([float(i) for i in line])

    return ret

def test_or(type:int==1):
    print(f"\nTesting OR type {type}")
    debug = True
    if type == 1:
        filename = "or_network1.csv"
    else:
        filename = "or_network2.csv"

    layers, weight_values, bias_values = load_network(filename)

    network = NeuralNetwork(layers)
    network.weight_values = weight_values
    network.bias_values = bias_values
    if debug:
        network.print_network()

    inputs = [[0,0],[1,0],[0,1],[1,1]]
    expected = [0,1,1,1]
    for i,input in enumerate(inputs):
        result = network.step(input)
        if debug:
            print(f"Expected: {expected[i]}, Actual: {result}")
        assert expected[i] == result[0]

def test_and(type:int==1):

    print(f"\nTesting AND type {type}")
    debug = True
    if type == 1:
        filename = "and_network1.csv"
    else:
        filename = "and_network2.csv"

    layers, weight_values, bias_values = load_network(filename)

    network = NeuralNetwork(layers)
    network.weight_values = weight_values
    network.bias_values = bias_values

    if debug:
        network.print_network()

    inputs = [[0, 0], [1, 0], [0, 1], [1, 1]]
    expected = [0,0,0,1]
    for i, input in enumerate(inputs):
        result = network.step(input)
        if debug:
            print(f"Expected: {expected[i]}, Actual: {result[0]}")
        assert expected[i] == result[0]

def test_xor(type:int==1):
    print(f"\nTesting XOR type {type}")
    debug = True
    if type == 1:
        filename = "xor_network2.csv"
    else:
        filename = None

    layers, weight_values, bias_values = load_network(filename)

    network = NeuralNetwork(layers)
    network.weight_values = weight_values
    network.bias_values = bias_values

    if debug:
        network.print_network()

    inputs = [[0, 0], [1, 0], [0, 1], [1, 1]]
    expected = [0, 1, 1, 0]
    for i, input in enumerate(inputs):
        result = network.step(input)
        if debug:
            print(f"Expected: {expected[i]}, Actual: {result[0]}")
        assert expected[i] == result[0]

def main():
    print(f"\nTesting OR")
    test_or(1)
    test_or(2)
    print(f"\nTesting AND")
    test_and(1)
    test_and(2)
    print(f"\nTesting AND")
    test_xor(1)


if __name__ == '__main__':
    main()