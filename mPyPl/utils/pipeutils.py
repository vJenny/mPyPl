from pipe import *
import random, itertools
import numpy as np
import pickle

# trs note -- pass l in as
# a fixed data structure i.e. array/list because (len(l)) must work
@Pipe
def pshuffle(l):
    """
    Shuffle a given pipe.
    In the current implementation, it has to store the whole datastream into memory as a list, in order to perform shuffle.
    Please not, that the idiom [1,2,3] | pshuffle() | pcycle() will return the same order of the shuffled sequence (eg. something
    like [2,1,3,2,1,3,...]), if you want proper infinite shuffle use `infshuffle()` instead.
    :param l: input pipe generator
    :return: list of elements of the datastream in a shuffled order
    """
    l = list(l)
    random.shuffle(l)
    return l

@Pipe
def pcycle(l):
    """
    Infinitely cycle the input sequence
    :param l: input pipe generator
    :return: infinite datastream
    """
    return itertools.cycle(l)

@Pipe
def infshuffle(l):
    """
    Function that turns sequence into infinite shuffled sequence. It loads it into memory for processing.
    :param l: input pipe generator
    :return: result sequence
    """
    data = list(l)
    while True:
        random.shuffle(data)
        for x in data:
            yield x

@Pipe
def pexec(l,func):
    """
    Execute function func, passing the pipe sequence as an argument
    :param func: Function to execute, must accept 1 iterator parameter
    :return: result of func
    """
    return func(l)

@Pipe
def as_npy(l):
    """
    Convert the sequence into numpy array. Use as `seq | as_npy`
    :param l: input pipe generator (finite)
    :return: numpy array created from the generator
    """
    return np.array(list(l))

@Pipe
def pprint(l):
    """
    Print the values of a finite pipe generator and return a new copy of it. It has to convert generator into in-memory
    list, so better not to use it with big data. Use `seq | tee ...` instead.
    :param l: input pipe generator
    :return: the same generator
    """
    l = list(l)
    print(l)
    return l

@Pipe
def pconcat(l):
    for x in l:
        for y in x:
            yield y

@Pipe
def puniq(l):
    u = []
    for x in l:
        if x not in u:
            u.append(x)
    return u

@Pipe
def pbatch(l,n=10):
    """
    Split input sequence into batches of `n` elements.
    :param l: Input sequence
    :param n: Length of output batches (lists)
    :return: Sequence of lists of `n` elements
    """
    b = []
    for x in l:
        if len(b)<n:
            b.append(x)
        else:
            yield b
            b=[]
    if len(b)>0:
        yield b

@Pipe
def first(l):
    """
    Returns first element of a pipe
    :param datastream: input pipe generator
    :return: first element
    """
    for x in l:
        return x

@Pipe
def psave(datastream,filename):
    """
    Save whole datastream into a file for later use
    :param datastream: Datastream
    :param filename: Filename
    """
    datastream = list(datastream)
    with open(filename, 'wb') as output:
        pickle.dump(datastream, output, pickle.HIGHEST_PROTOCOL)

def pload(filename):
    """
    Load a datastream (list) from file and use it as a pipe
    :param filename: filename to use
    :return: datastream (list)
    """
    with open(filename, 'rb') as input:
        ls = pickle.load(input)
    return ls
