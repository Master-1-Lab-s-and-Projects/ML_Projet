'''
Faire des tests sur les dimensions des fonctions, rapide juste un assert pour Ãªtre sur
'''
import matplotlib.pyplot as plt
import numpy as np

import src.utils.mltools as tools
from src.Activation.sigmoid import Sigmoid
from src.Activation.tanH import TanH
from src.Loss.MSE import MSE
from src.Module.linear import Linear
from src.Module.sequential import Sequential
from src.Optim.optim import Optim


def test_non_linear():
    # data generation
    datax, datay = tools.gen_arti(centerx=1, centery=1, sigma=0.1, nbex=1000, data_type=1, epsilon=0.1)
    testx, testy = tools.gen_arti(centerx=1, centery=1, sigma=0.1, nbex=1000, data_type=1, epsilon=0.1)

    datay = datay[..., None]
    testy = testy[..., None]

    datay = np.where(datay == -1, 0, 1)
    testy = np.where(testy == -1, 0, 1)
    nb_data = len(datax)

    # Input and Output size of our NN
    input_size = len(datax[0])
    hidden_size = 3
    final_size = 1

    # Initialize modules with respective size
    iteration = 100
    gradient_step = 10e-3

    m_linear_first = Linear(input_size, hidden_size, bias=True)
    m_linear_second = Linear(hidden_size, final_size, bias=True)
    m_sig = Sigmoid()
    m_tanh = TanH()
    m_mse = MSE()

    for _ in range(iteration):
        hidden_l = m_linear_first.forward(datax)
        hidden_l_tanh = m_tanh.forward(hidden_l)
        hidden_l2 = m_linear_second.forward(hidden_l_tanh)
        hidden_l2_sigmoid = m_sig.forward(hidden_l2)
        loss = m_mse.forward(datay, hidden_l2_sigmoid)

        print("max loss:", np.max(loss))

        loss_back = m_mse.backward(datay, hidden_l2_sigmoid)
        delta_sigmoid = m_sig.backward_delta(hidden_l2, loss_back)
        delta_linear_2 = m_linear_second.backward_delta(hidden_l_tanh, delta_sigmoid)
        delta_tanh = m_tanh.backward_delta(hidden_l, delta_linear_2)

        m_linear_second.backward_update_gradient(hidden_l_tanh, delta_sigmoid)
        m_linear_first.backward_update_gradient(datax, delta_tanh)

        m_linear_second.update_parameters(gradient_step=gradient_step)
        m_linear_first.update_parameters(gradient_step=gradient_step)

        m_linear_first.zero_grad()
        m_linear_second.zero_grad()

    def yhat(x):
        hidden_l = m_linear_first.forward(x)
        hidden_l_tanh = m_tanh.forward(hidden_l)
        hidden_l2 = m_linear_second.forward(hidden_l_tanh)
        yhat = m_sig.forward(hidden_l2)
        return np.where(yhat >= 0.5, 1, -1)

    tools.plot_frontiere(testx, yhat, step=100)
    tools.plot_data(testx, testy.reshape(-1))
    plt.show()


def test_non_linear_SGD():
    # data generation
    datax, datay = tools.gen_arti(centerx=1, centery=1, sigma=0.1, nbex=1000, data_type=1, epsilon=0.1)
    testx, testy = tools.gen_arti(centerx=1, centery=1, sigma=0.1, nbex=1000, data_type=1, epsilon=0.1)
    datay = datay[..., None]
    testy = testy[..., None]
    datay = np.where(datay == -1, 0, 1)
    testy = np.where(testy == -1, 0, 1)

    # NN parameters
    batch_size = len(datax)
    input_size = len(datax[0])
    hidden_size = 2
    final_size = 1
    iteration = 100
    gradient_step = 10e-3

    # Setup NN
    net = Sequential([Linear(input_size, hidden_size, bias=True),
                      TanH(),
                      Linear(hidden_size, final_size, bias=True),
                      Sigmoid()])

    opt = Optim(net=net, loss=MSE(), eps=gradient_step)
    opt.SGD(datax, datay, batch_size, maxiter=iteration, verbose=2)

    def yhat(x):
        yhat = opt.predict(x)
        return np.where(yhat >= 0.5, 1, -1)

    tools.plot_frontiere(testx, yhat, step=100)
    tools.plot_data(testx, testy.reshape(-1))
    plt.plot()
    plt.show()


if __name__ == '__main__':
    test_non_linear_SGD()
