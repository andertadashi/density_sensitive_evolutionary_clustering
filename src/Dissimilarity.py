import random
import numpy as np
from abc import ABCMeta, abstractmethod


class Dissimilarity:

    __metaclass__ = ABCMeta

    def __init__(self):

        pass

    @abstractmethod
    def distance(self, a, b):
        pass


class EuclideanDistance(Dissimilarity):

    def __init__(self):
        Dissimilarity.__init__(self)

    def distance(self, a, b):
        return np.linalg.norm(a-b)


class DensityDistance(Dissimilarity):

    def __init__(self, rho):
        Dissimilarity.__init__(self)
        self.rho = rho

    def distance(self, a, b):
        L = pow(self.rho, np.linalg.norm(a-b)) - 1
        return L
