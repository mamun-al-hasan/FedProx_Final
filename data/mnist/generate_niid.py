from sklearn.datasets import fetch_openml
from tqdm import trange
import numpy as np
import random
import json
import os

train_path = './data/train/all_data_0_niid_0_keep_10_train_9.json'
test_path = './data/test/all_data_0_niid_0_keep_10_test_9.json'
dir_path = os.path.dirname(train_path)

if not os.path.exists(dir_path):
    os.makedirs(dir_path)

dir_path = os.path.dirname(test_path)
if not os.path.exists(dir_path):
    os.makedirs(dir_path)

# Load the data
mnist = fetch_openml('mnist_784', version=1, data_home='./data')

mnist_data_array = mnist.data.to_numpy()
mnist_target_array = mnist.target.astype(int).to_numpy()

mu = np.mean(mnist_data_array.astype(np.float32), 0)
sigma = np.std(mnist_data_array.astype(np.float32), 0)
mnist_data_array = (mnist_data_array.astype(np.float32) - mu) / (sigma + 0.001)

mnist_data = []

for i in trange(10):
    idx = mnist_target_array == i
    mnist_data.append(mnist_data_array[idx])

# print(mnist.data.shape)

print([len(v) for v in mnist_data])

X = [[] for _ in range(1000)]
y = [[] for _ in range(1000)]
idx = np.zeros(10, dtype=np.int64)
for user in range(1000):
    for j in range(2):
        l = (user + j) % 10
        X[user] += mnist_data[l][idx[l]:idx[l] + 5].tolist()
        y[user] += (l * np.ones(5)).tolist()
        idx[l] += 5
print(idx)

# Assign remaining samples by power law
props = np.random.lognormal(0, 2.0, (10, 100, 2))
props = np.array([[[len(v) - 1000]] for v in mnist_data]) * props / np.sum(props, (1, 2), keepdims=True)

for user in trange(1000):
    for j in range(2):
        l = (user + j) % 10
        num_samples = int(props[l, user // 10, j])
        if idx[l] + num_samples < len(mnist_data[l]):
            X[user] += mnist_data[l][idx[l]:idx[l] + num_samples].tolist()
            y[user] += (l * np.ones(num_samples)).tolist()
            idx[l] += num_samples

print(idx)

train_data = {'users': [], 'user_data':{}, 'num_samples':[]}
test_data = {'users': [], 'user_data':{}, 'num_samples':[]}

for i in trange(1000, ncols=120):
    uname = 'f_{0:05d}'.format(i)

    combined = list(zip(X[i], y[i]))
    random.shuffle(combined)
    X[i][:], y[i][:] = zip(*combined)
    num_samples = len(X[i])
    train_len = int(0.9 * num_samples)
    test_len = num_samples - train_len

    train_data['users'].append(uname)
    train_data['user_data'][uname] = {'x': X[i][:train_len], 'y': y[i][:train_len]}
    train_data['num_samples'].append(train_len)
    test_data['users'].append(uname)
    test_data['user_data'][uname] = {'x': X[i][train_len:], 'y': y[i][train_len:]}
    test_data['num_samples'].append(test_len)

print(train_data['num_samples'])
print(sum(train_data['num_samples']))

with open(train_path, 'w') as outfile:
    json.dump(train_data, outfile)
with open(test_path, 'w') as outfile:
    json.dump(test_data, outfile)
