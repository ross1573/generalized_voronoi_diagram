import math
import numpy as np


# get length of 2d vector
def length(vec2) -> float:
    return math.sqrt(pow(vec2[0], 2) + pow(vec2[1], 2))

# get distance between two 2d vectors
def distance(_1, _2) -> float:
    return length(_1 - _2)

# get angle between two 2d vectors
def radian(_1, _2) -> float:
    _1_n = _1 / length(_1)
    _2_n = _2 / length(_2)
    return math.acos(np.dot(_1_n, _2_n))

# get closest(but smaller) value index on vector
def find_closest(vec, ele) -> int:
    for i in range(len(vec)):
        if vec[i] > ele:
            return i
    return len(vec)
