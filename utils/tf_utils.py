import tensorflow as tf


def __num_elems(shape):
    tot_elems = 1
    for s in shape:
        tot_elems *= int(s)
    return tot_elems


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
