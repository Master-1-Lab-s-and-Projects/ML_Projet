from src.Module.module import Module


class Sequential(Module):
    def __init__(self, modules):
        self._modules = modules

    def append_module(self, module):
        self._modules.append(module)

    def forward(self, X):
        list = [X]
        for m in self._modules:
            list.append(m.foward(list[-1]))
        return list

    def backward(self, list, delta):
        d = delta
        for m in list[::-1]:
            m.backward_update_gradient(m, d)
            d = m.backward_delta(m, d)
        return d

    def update_parameters(self):
        for m in list:
            m.update_parameters(m)

    def zero_grad(self):
        for m in list:
            m.zero_grad(m)
