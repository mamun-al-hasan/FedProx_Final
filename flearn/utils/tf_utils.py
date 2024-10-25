import numpy as np
import tensorflow as tf
import os
os.environ['CUDA_VISIBLE_DEVICES'] = ''

def __num_elems(shape):
    num = 1
    for i in shape:
        num *= int(i)
    return num

def graph_size(graph):
    tot_size = 0
    with graph.as_default():
        vs = tf.compat.v1.trainable_variables()
        for v in vs:
            tot_elems = __num_elems(v.shape)
            dtype_size = int(v.dtype.size)
            var_size = tot_elems * dtype_size
            tot_size += var_size
    return tot_size

def process_sparse_grad(grads):
    indices = grads[0].indices
    values =  grads[0].values
    first_layer_dense = np.zeros((80,8))
    for i in range(indices.shape[0]):
        first_layer_dense[indices[i], :] = values[i, :]

    client_grads = first_layer_dense
    for i in range(1, len(grads)):
        client_grads = np.append(client_grads, grads[i]) # output a flattened array

    return client_grads

def process_grad(grads):
    client_grads = grads[0]
    for i in range(1, len(grads)):
        client_grads = np.append(client_grads, grads[i]) # output a flattened array

    return client_grads

def cosine_sim(a,b):
    return np.dot(a,b)/(np.linalg.norm(a)*np.linalg.norm(b))

# def test_graph_size():
#     graph = tf.Graph()
#     with graph.as_default():
#         # Create a simple model
#         a = tf.Variable(tf.random.normal([80, 8]), name='a')
#         b = tf.Variable(tf.random.normal([8, 1]), name='b')
#
#     size = graph_size(graph)
#     print(f"Graph size (in bytes): {size}")
#
# test_graph_size()

# def test_process_sparse_grad():
#     # Creating mock sparse gradient data
#     indices = np.array([[0], [1], [2], [3], [4]])  # Example sparse indices
#     values = np.random.randn(5, 8)  # Example values for sparse matrix
#
#     class MockSparseGradient:
#         def __init__(self, indices, values):
#             self.indices = indices
#             self.values = values
#
#     sparse_grads = [MockSparseGradient(indices, values)]
#     client_grads = process_sparse_grad(sparse_grads)
#
#     print("Processed sparse gradients (flattened):")
#     print(client_grads)
#
# test_process_sparse_grad()

# def test_process_grads():
#     # Creating mock dense gradient data
#     dense_grads = [np.random.randn(80, 8), np.random.randn(8, 1)]
#
#     client_grads = process_grads(dense_grads)
#
#     print("Processed dense gradients (flattened):")
#     print(client_grads)
# test_process_grads()

# def test_cosine_similarity():
#     # Mock vectors for cosine similarity
#     a = np.random.randn(10)
#     b = np.random.randn(10)
#
#     similarity = cosine_sim(a, b)
#     print(f"Cosine Similarity: {similarity}")
# test_cosine_similarity()