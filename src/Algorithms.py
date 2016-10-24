import random
import numpy as np
import networkx as nx
from abc import ABCMeta, abstractmethod


class Cluster:

    def __init__(self, database, dissimilarity, P_size=10, K=4, max_iterations=100):
        self.database = database
        self.max_iterations = max_iterations
        self.K = K
        self.P = []
        self.P_size = P_size
        self.data = database.load_data()
        self.N = len(self.data)
        self.create_graph()
        self.graph = None
        self.dissimilarity = dissimilarity
        self.assigned_to_cluster = []

    def population_random_initialization(self):
        population = []
        i = 0
        while self.P_size < len(population) and i <= self.P_size * 10:
            c = sorted(random.sample(range(self.N), self.K))
            if c not in population:
                population.append(c)
            i += 1
        return population

    def create_graph(self):
        graph = nx.Graph()
        for i in range(self.N):
            for j in range(self.N):
                if i == j:
                    continue
                dist = self.dissimilarity.distance(i, j)
                assert(dist >= 0, "dist is negative!")
                graph.add_edge(i, j, distance=dist)
        self.graph = graph

    def assign_points_to_clusters(self, t):
        data_weights = []
        for d in self.data:
            for p_idx, p in enumerate(self.P):
                min_dist = None
                for c in p:
                    pass

    def compute(self):

        self.P.append(self.population_random_initialization())

        for t in range(self.max_iterations):

            # assign points to clusters

            # compute objective function

            if t != 0:
                # select P(t) from P(t-1)
                # crossover P(t)
                # mutate P(t)

                pass



