import random
import numpy as np
from abc import ABCMeta, abstractmethod


class Cluster:

    def __init__(self, database, K=4, max_iterations=10):
        self.database = database
        self.max_iterations = max_iterations
        self.K = K

    def random_initialization(self):
        return random.sample(self.database.data)

    def compute(self):
        for t in range(self.max_iterations):
            pass


