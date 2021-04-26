# -*- coding: utf-8 -*-

'''
Faire des tests sur les dimensions des fonctions, rapide juste un assert pour Ãªtre sur
'''
import numpy as np

from src.Module.Conv1D import Conv1D
from src.Pooling.maxPool1D import MaxPool1D



def transform_numbers(input, size):
    """Assume 1D array as input, len is the number of example
    Transform into proba
    """
    datay_r = np.zeros((len(input), size))
    # Re-arranging data to compute a probability
    for x in range(len(input)):
        datay_r[x][input[x]] = 1
    return datay_r

if __name__ == '__main__':
    batch_size = 25
    kernel_size = 3
    chan_input = 2
    chan_output = 32
    stride = 2
    length = 128
    
    i = 2 # pixel de test
    image = 0 # image de test
    filtre = 1 # filtre de test
    
    """
        Convolution
    """
    X = np.random.rand(batch_size,length,chan_input)
    convolution = Conv1D(kernel_size, chan_input, chan_output, stride=stride)
    
    # forward size
    forward_conv = convolution.forward(X)
    assert forward_conv.shape == (batch_size, (length-kernel_size)//stride +1,chan_output)
    
    # operateur forward result
    res = convolution.operateur(X,i*stride)[image][filtre]
    w = convolution._parameters[:,:,filtre]
    excepted = np.sum(w*X[image,i*stride:i*stride+kernel_size])   
    assert np.abs(excepted - res) < 1e-5
    
    # forward result
    res = forward_conv[image][i][filtre]
    assert np.abs(res - excepted) < 1e-5
    
    
    # backward size
    delta = np.random.rand(forward_conv.shape[0],forward_conv.shape[1],forward_conv.shape[2])
    backward_conv = convolution.backward_delta(X, delta)
    assert backward_conv.shape == (batch_size,length,chan_input)
    
    """
    # backward_delta result
    res = convolution.backward_delta(X,delta)#[image][filtre]
    print(res.shape)
    excepted = np.sum(convolution._parameters[:,:,filtre])
    assert np.abs(excepted - res) < 1e-5
    """
    
    """
        MaxPool1D
    """
    max_pool = MaxPool1D(kernel_size,stride)
    
    # forward size
    forward_pool = max_pool.forward(X)
    assert forward_pool.shape == (batch_size, (length-kernel_size)//stride +1,chan_input)
    
    # forward result
    res = forward_pool[image][i]
    excepted = np.max(X[image,i*stride:i*stride+kernel_size],axis=0).flatten()
    assert np.max(np.abs(res - excepted)) < 1e-5
    
    # backward_delta size
    delta = np.random.rand(forward_pool.shape[0],forward_pool.shape[1],forward_pool.shape[2])
    backward_pool = max_pool.backward_delta(X, delta)
    assert backward_pool.shape == (batch_size,length,chan_input)
    
    # backward_delta result
    
    res = backward_pool[image]
    
    excepted = np.zeros(res.shape)
    for i,x in enumerate(range(0,X.shape[1]-stride,stride)):
        maximum = np.argmax(X[image,x:x+kernel_size],axis=0) + x
        excepted[maximum,range(X.shape[2])] = delta[image,i]

    assert np.max(np.abs(res-excepted)) < 1e-5