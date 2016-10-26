import random
import numpy as np
import networkx as nx
import itertools
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
        self.graph = None
        self.dissimilarity = dissimilarity
        self.assigned_to_cluster = []
        self.create_graph()
        self.compute_distances()
        self.distances = None

    def population_random_initialization(self):
        print "population_random_initialization"
        population = []
        i = 0
        while len(population) <= self.P_size and i <= self.P_size * 10:
            c = sorted(random.sample(range(self.N), self.K + 1))
            if c not in population:
                population.append(c)
            i += 1
        return population

    def create_graph(self):
        print "create_graph"
        self.graph = nx.Graph()
        for i in range(self.N):
            for j in range(self.N):
                if i == j:
                    continue
                dist = self.dissimilarity.distance(i, j)
                # print dist
                assert dist >= 0, "dist is negative!"
                self.graph.add_edge(i, j, distance=dist)

    def compute_distances(self):
        print "compute_distances"
        distances = {}
        for (a, b) in itertools.combinations(range(self.N), 2):
            dist = nx.dijkstra_path_length(self.graph, a, b, 'distance')
            distances[(a, b)] = dist
            print "a={} b={} dist={}".format(a, b, dist)
        self.distances = distances

    def assign_points_to_clusters(self, t):
        print "assign_points_to_clusters"
        P_cluster_dist = []

        # population
        for p_idx, p in enumerate(self.P[t]):
            data_cluster_dist = []

            # data index
            for d_idx in range(len(self.data)):
                min_dist = None
                min_idx = None
                print ""
                # cluster
                for c_idx, c in enumerate(p):
                    # compute distance with data[d_idx] and C[c_idx]
                    dist = self.distances[tuple(sorted((d_idx, c)))]
                    print("{} {} dist is {}".format(d_idx, c, dist))
                    if min_dist is None or dist < min_dist:
                        min_dist = dist
                        min_idx = c_idx
                data_cluster_dist.append((d_idx, p[min_idx], min_dist))

            P_cluster_dist.append(data_cluster_dist)
        return P_cluster_dist

    def compute(self):
        print "compute"

        self.P.append(self.population_random_initialization())
        print self.P[0]

        for t in range(self.max_iterations):
            print ("\nt={}".format(t))

            # assign points to clusters
            pcluster = self.assign_points_to_clusters(t)
            print pcluster
            # compute objective function

            if t != 0:
                # select P(t) from P(t-1)
                # crossover P(t)
                # mutate P(t)

                pass



