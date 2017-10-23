""" 
A module to implement the stochastic gradient descent learning 
algorithm for a feedforward neural network. Gradients are calculated 
using backpropagation. 
"""

import random 
import numpy as np 


class Network(object):

        def __init__(self, sizes):
                self.num_layers = len(sizes)
                self.sizes = sizes #contains the number of neurons in the resp. layers
                self.biases = [np.random.randn(y, 1) for y in sizes[1:]]
                self.weights = [np.random.randn(y, x) #Gaussian distributions with mean 0 and std dev 1
                                                for x, y in zip(sizes[:-1], sizes[1:])]
                                                
#Network assumes the first layers is an input layer since Python's indexing starts from 0 
        
        def feedforward(self,a): 
                '''Return the output of the network if "a" is input'''
                for b, w in zip(self.biases, self.weights):
                        a = sigmoid(np.dot(w, a)+b) 
                return a 
        
        def SGD(self, training_data, epochs, mini_batch_size, eta, test_data = None):
                #Stochastic Gradient Descent 
        
                """Train the neural network using mini- batch stochastic gradient descent. 
                The "training_data" is a list of tuples "(x, y)" representing the training inputs
                and the desired outputs. The other non- optional parameters are self - explanatory. 
                If "test_data" is provided then the network will be evaluated against the 
                test data after each epoch and partial progress is printed out. This is useful 
                for tracking progress, but slows things down substantially. """
        
                #can do: Check test data one in 2 times or like binary search : O(logn)
        
                if test_data: n_test = len(test_data) #if test_data exists 
        
                n = len(training_data) 
        
                for j in xrange(epochs):
                        random.shuffle(training_data) 
                
                        mini_batches = [
                        training_data[k:k+mini_batch_size]
                        for k in xrange(0, n, mini_batch_size)] #Partitioning into mini-batches of appropriate size 
                
                        for mini_batch in mini_batches:
                                self.update_mini_batch(mini_batch, eta) #Perforimg a single iteration of  gradient descent 
                        
                        if test_data:
                                print "Epoch {0}: {1} / {2}". format(
                                j, self.evaluate(test_data), n_test) 
                        else: 
                                print "Epoch {0} complete". format(j)

        def update_mini_batch(self, mini_batch, eta): 
                """Update the network's weights and biases by applying 
                gradient descent using backpropagation to a single mini batch. 
                The "mini_batch" is a list of tuples "(x, y)", and "eta" is 
                the learning rate. """
        
                nabla_b = [np.zeros(b.shape) for b in self.biases] 
                nabla_w = [np.zeros(w.shape) for w in self.weights] 
        
                for x, y in mini_batch:
                        delta_nabla_b, delta_nabla_w = self.backprop(x, y)
                        nabla_b = [nb + dnb for nb, dnb in zip(nabla_b, delta_nabla_b)] 
                        nabla_w = [nd + dnw for nw, dnw in zip(nabla_w, delta_nabla_w)]
                
                self.weights = [w -(eta/len(mini_batch))*nw for w, nw in zip(self.weights, nabla_w)] 
                self.biases = [w - (eta/len(mini_batch))*nb for b, nb in zip(self.biases, nabla_b)] 
        
        
        def backprop(self, x, y):
                """Return a tuple ''(nabla_b, nabla_w)'' representing the 
                gradient for the cost function C_x. ''nabla_b'' and 
                ''nabla_w'' are layer-by-layer lists of numpy arrays, similar 
                to ''self.biases'' and ''self.weights''.""" 
        
                nabla_b = [np.zeros(b.shape) for b in self.biases] 
                nabla_w = [np.zeros(w.shape) for w in self.weights]
        
                #feedforward 
                activation = x 
                activations = [x] #list to store all the activations, layer by layer 
        
                zs = [] #list to store all the z vectors, layer by layer 
                # z = sigma(w*a + b)
        
                for b, w in zip(self.biases, self.weights):
                        z = np.dot(w, activation) + b              #Initially activation here is x or the input in accordance with the above equation 
                        zs.append(z)
                        activation = sigmoid(z) 
                        activations.append(activation) 
                
                #backward pass 
                delta = self.cost_derivative(activations[-1], y) * \
                        sigmoid_prime(zs[-1])
                nabla_b[-1] = delta
                nabla_w[-1] = np.dot(delta, activations[-2].transpose())

                for l in xrange(2, self.num_layers):
                        z = zs[-1]
                        sp = sigmoid_prime(z)
                        delta = np.dot(self.weights[-l+1].transpose(), delta) * sp
                        nabla_b[-1] = delta 
                        nabla_w[-1] = np.dot(delta, activations[-l-1].transpose()) #last but one layer
                return (nabla_b, nabla_w) 

        def evaluate(self, test_data):
                """Return the number of test inputs for which the neural network 
                outputs the correct result. Note that the neural network's output 
                is assumed to be the index of whichever neuron in the final layer 
                has the highest activation. """
        
                test_results = [np.argmax(self.feedforward(x)), y] #returns the indices of the maximum values along an axis 
                return sum(int(x == y) for (x, y) in test_results) 
        
        def cost_derivative(self, output_activations, y):
                """Return the vector of partial derivatives \partial C_x/ 
                \partial a for the output activations. """ 
                return(output_activations - y) 
                
###Miscellaneous functions 

def sigmoid(z): 
                return 1.0/(1.0 + np.exp(-z)) #Applies the exponent element wise 
                
def sigmoid_prime(z): 
        """Derivative of the sigmoid function. """ 
        return sigmoid(z)*(1 - sigmoid(z)) 
        
