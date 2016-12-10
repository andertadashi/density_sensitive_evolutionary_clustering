import random
import numpy as np
from abc import ABCMeta, abstractmethod


class Dissimilarity:

    __metaclass__ = ABCMeta

    def __init__(self):
        self.rho = 0
        pass

    @abstractmethod
    def distance(self, a, b):
        pass


class EuclideanDistance(Dissimilarity):

    def __init__(self):
        Dissimilarity.__init__(self)

    def distance(self, a, b):
        a = np.asarray(a)
        b = np.asarray(b)
        return np.linalg.norm(a-b)


class DensityDistance(Dissimilarity):

    def __init__(self, rho):
        Dissimilarity.__init__(self)
        self.rho = rho

    def distance(self, a, b):
        a = np.asarray(a)
        b = np.asarray(b)
        if self.rho == 1.0:
            L = np.linalg.norm(a - b)
        else:
            L = pow(self.rho, np.linalg.norm(a-b)) - 1
        # print("a={} b={} a-b={} dist_euc={} dist={}".format(a, b, a-b, np.linalg.norm(a-b), L))
        return L
