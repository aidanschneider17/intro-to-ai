from typing import List, Tuple

import numpy as np

class NeuralNetwork():
    """
    Implementation of a Neural Network with variable number of layers and
    two lists that contain the weights for the bias and normal nodes. Can
    be used in conjunction with an Evolutionary Algorithm.
    """

    def __init__(self, layers):
        """
        :param layers: List of layer sizes. For example [2,4,1], creates
        a network with a input layer of 2 neurons, and hidden layer with 4 neurons,
        and an output layer of 1 neuron.
        """
        self._layers = layers
        num_normal = 0
        num_bias = 0
        for i in range(len(self._layers) - 1):
            num_normal += self._layers[i] * self._layers[i+1]
            num_bias += self._layers[i+1]

        # weight_values stores the weights that connect nodes. See develop_weights for
        # how these values map onto the connections of the NN
        self._weight_values = [np.random.normal(0,0.1) for i in range(num_normal)]
        # bias_values stores the weights that connect nodes. See develop_bias for
        # how these values map onto the connections of the NN
        self._bias_values = [np.random.normal(0,0.1) for i in range(num_bias)]

    @property
    def layers(self):
        return self._layers
    @property
    def weight_values(self):
        return self._weight_values

    @weight_values.setter
    def weight_values(self, w):
        self._weight_values = w

    @property
    def bias_values(self):
        return self._bias_values

    @bias_values.setter
    def bias_values(self, b):
        self._bias_values = b


    def develop_weights(self) -> List[np.ndarray]:
        """
        Turns the list of normal weights in self._weight_values into a list of numpy 2D arrays.
        Each elemnet in the list corresponds to the weight matrix between two adjacent layers.
        weight_values represent the weights of the NeuralNetwork. Let's say we had a NN with
        a topology of [3,2,1] and labeled the input, hidden, and output nodes to be [a,b,c],
        [d,e], and [f]. weight_values would hold weights that correspond to the following connections
        weight_values = [a->d, a->e, b->d, b->e, c->d, c->e,d->f,e->f] where a->d is the weight from
        node a to d, b->d is the weight from node b to d, etc.
        These arrays can be used to do matrix operations within the step() method.
        :return: List of numpy arrays
        """
        W = []
        # keeps track of how many weights have been processed
        wp = 0
        for i in range(len(self._layers) - 1):
            num_pre = self._layers[i]
            num_post = self._layers[i+1]

            W.append(np.array(self._weight_values[wp:wp+(num_pre * num_post)]).reshape((num_pre,num_post)))
            wp += num_pre * num_post
        return W

    def develop_bias(self) -> List[np.ndarray]:
        """
        Turns the list of bias weights in self._bias_values into a list of numpy 2D arrays.
        Each element in the list corresponds to the bias matrix for a layer except the input layer.
        bias_values represent the bias weights of the NeuralNetwork. Let's say we had a NN with
        a topology of [3,2,1] and labeled the input, hidden, and output nodes to be [a,b,c],
        [d,e], and [f]. bias_values would hold bias weights from bias nodes that feed into
        bias_values = [1->d, 1->e, 1->f] where 1->d is the weight of the bias feeding into
        d, 1->e is the weight of the bias feeding into e, etc.weight from
        These arrays can be used to do matrix operations within the step() method.
        :return: list of numpy arrays
        """
        B = []
        # keeps track of how many weights have been processed
        wp = 0
        for i in range(len(self._layers) - 1):
            num_pre = 1
            num_post = self._layers[i+1]
            B.append(np.array(self._bias_values[wp:wp+(num_pre * num_post)]).reshape((num_pre,num_post)))
            wp = num_pre * num_post
        return B


    def step(self, inputs:List[float]) -> Tuple[List[float],List[float]]:
        """
        Performs a single feed forward pass of the network.
        :param input: Single sample of the inputs. Length should be the same
         as the number of inputs
        :return: The activation of the output neurons as a numpy array
        """
        #TODO - Implement the step() method given the following psuedocode
        # 1. Call and store the weight matrix returned by develop_weights()
        # 2. Call and store the bias matrix returned by bias_weights()
        # 3. Iterate and calculate the activation for all the layers.
        # The activation for the input layer is just the input arguments that are passed in.
        # For every other layer, calculate its pre-activation (h), which is the weight sum of its inputs.
        # Use numpy's matrix multiplications to mutiply the inputs of a layer by its weights (W) and then add the bias (B).
        # The input of each non-input layer is the activation of the prior layer.
        # Feed the preactivation through an activation function (g) to get the final activation of that layer.
        # Activation function for the output (last) layer should be heavyside.
        # Activation function for every other layer should be sigmoid.
        # 4. Return the activation of the last layer.
        weights = self.develop_weights()
        bias = self.develop_bias()

        activations = [inputs]

        for i in range(0, len(self._layers)-1):
            h = np.matmul(activations[i], weights[i]) + bias[i]
            if i != len(self._layers) - 2:
                activations.append(self.sigmoid(h))
            else:
                return self.heavyside(h)





    def sigmoid(self, x):
        """This is a sigmoid activation function."""
        k = -10.0
        return 1.0 / (1.0 + np.exp(k * x))


    def heavyside(self,h):
        """Simple threshold method."""
        return list(map(lambda x: 1 if x >=0 else 0, h))


    def print_network(self):
        W = self.develop_weights()
        B = self.develop_bias()

        for i in range(len(self._layers)-1):
            if i == 0:
                print(f"Num inputs: {self._layers[i]}")
            elif i == len(self._layers)-1:
                print(f"Num outputs: {self._layers[i]}")
            else:
                print(f"Size hidden{1}: {self._layers[i]}")
            print(f"Weights: \n{W[i]}")
            print(f"Bias: \n{B[i]}")

