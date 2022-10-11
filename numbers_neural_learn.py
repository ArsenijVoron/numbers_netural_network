import numpy as np
import json
import matplotlib.pyplot as mpl
import time

start_time = time.time()

with open('dataSet.json') as d: #open and load dataSet
    data_set = json.load(d)


answer_wariants = [i for i in range(10)]

# hyperparameter initialization

INPUT_DIM = 900
H1_DIM = 16
H2_DIM = 16
OUT_DIM = 10
LR = 0.001
EPOCH = 5_000_000

#loss data

loss_arr = []
right_answers = 0

#random distribution of weights and biases

W1 = np.random.rand(INPUT_DIM, H1_DIM)
b1 = np.random.rand(1, H1_DIM)
W2 = np.random.rand(H1_DIM, H2_DIM)
b2 = np.random.rand(1, H2_DIM)
W3 = np.random.rand(H2_DIM, OUT_DIM)
b3 = np.random.rand(1, OUT_DIM)

W1 = (W1 - 0.5) * 2 * np.sqrt(1 / INPUT_DIM)
b1 = (b1 - 0.5) * 2 * np.sqrt(1 / INPUT_DIM)
W2 = (W2 - 0.5) * 2 * np.sqrt(1 / H1_DIM)
b2 = (b2 - 0.5) * 2 * np.sqrt(1 / H1_DIM)
W3 = (W3 - 0.5) * 2 * np.sqrt(1 / H2_DIM)
b3 = (b3 - 0.5) * 2 * np.sqrt(1 / H2_DIM)


def to_normal_list(a : list) -> list: #function for accurately write data to json file
    res = '['
    for i in range(len(a)):
        res += '['
        for j in range(len(a[i])):
            res += f'{a[i][j]},'
        res = res[0: len(res) - 1] + '],'
    return res[0: len(res) - 1] + ']'

def softmax(x : int) -> int: #probability distribution
    ep = np.exp(x)
    return ep / np.sum(ep)

def sigmoid (t : float) -> float: #activator function
    return 1 / (1 + np.exp(-t))

def to_right_answer(y : int, num_classes : int) -> list: #find answer by index
    zeros = np.zeros((1, num_classes))
    zeros[0, y] = 1
    return zeros

def sparse_cross_entropy(z : list, y : int) -> float: #calculate loss 
    return -np.log(z[0, y])

def sigmoid_deriv(t : float) -> int: #derivative activator function
    return sigmoid(t) * (1 - sigmoid(t))

#back propogation

for i in range(EPOCH):
    
    #random learning data

    y = np.random.randint(0, 10)
    x = np.array([data_set[str(y)][np.random.randint(0, 60)]])

    #forward

    t1 = x @ W1 + b1
    h1 = sigmoid(t1)
    t2 = h1 @ W2 + b2
    h2 = sigmoid(t2)
    t3 = h2 @ W3 + b3
    z = softmax(t3)

    #write data about the pro-approximation of the neural network

    if answer_wariants[np.argmax(z)] == y:
        right_answers += 1

    E = sparse_cross_entropy(z, y)
    loss_arr.append(E)
    
    #backward

    y_full = to_right_answer(y, OUT_DIM)
    dE_dt3 = z - y_full
    dE_dW3 = h2.T @ dE_dt3
    dE_db3 = dE_dt3
    dE_dh2 = dE_dt3 @ W3.T
    dE_dt2 = dE_dh2 * sigmoid_deriv(t2)
    dE_dW2 = h1.T @ dE_dt2
    dE_db2 = dE_dt2
    dE_dh1 = dE_dt2 @ W2.T
    dE_dt1 = dE_dh1 * sigmoid_deriv(t1)
    dE_dW1 = x.T @ dE_dt1
    dE_db1 = dE_dt1

    #update the weights and biases on the gradient vector

    W3 = W3 - LR * dE_dW3
    b3 = b3 - LR * dE_db3
    W2 = W2 - LR * dE_dW2
    b2 = b2 - LR * dE_db2
    W1 = W1 - LR * dE_dW1
    b1 = b1 - LR * dE_db1

#show data about learning 
mpl.plot(loss_arr)
mpl.show()

print(f'completed {right_answers}/{EPOCH} or {right_answers * 100 // EPOCH}%')

print(f'{time.time() - start_time} seconds')

#write weight and biases
file = open('b1.json', 'w')
file.write(to_normal_list(b1))

file = open('W1.json', 'w')
file.write(to_normal_list(W1))

file = open('b2.json', 'w')
file.write(to_normal_list(b2))

file = open('W2.json', 'w')
file.write(to_normal_list(W2))

file = open('b3.json', 'w')
file.write(to_normal_list(b3))

file = open('W3.json', 'w')
file.write(to_normal_list(W3))


