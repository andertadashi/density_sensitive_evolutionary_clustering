import random
import numpy as np
import networkx as nx
import itertools
from abc import ABCMeta, abstractmethod


class Cluster:

    def __init__(self, database, dissimilarity, P_size=10, K=3, max_iterations=100):
        self.database = database
        self.max_iterations = max_iterations
        self.K = K
        self.P = []  # population at time t
        self.P_size = P_size
        self.P_cluster_dist = []  # (individual, cluster, dist(individual, cluster))
        self.data = database.load_data()
        self.N = len(self.data)
        self.graph = None
        self.dissimilarity = dissimilarity
        self.assigned_to_cluster = []
        self.distances = self.compute_distances()
        self.crossover_percentage = 0.8
        self.mutate_percentage = 0.2

    def population_random_initialization(self):
        print "population_random_initialization"
        population = []
        i = 0
        while len(population) < self.P_size and i <= self.P_size * 10:
            c = sorted(random.sample(range(self.N), self.K))
            if c not in population:
                population.append(c)
            i += 1
        return population

    def get_ramdom_indices(self, range_sample, qtd):
        indices = sorted(random.sample(range(range_sample), qtd))
        return indices

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

        self.create_graph()

        distances = {}
        for (a, b) in itertools.combinations(range(self.N), 2):
            dist = nx.dijkstra_path_length(self.graph, a, b, 'distance')
            distances[tuple(sorted((a, b)))] = dist
            print "a={} b={} dist={}".format(a, b, dist)

        return distances

    def assign_points_to_clusters(self, t):
        print "assign_points_to_clusters"

        P_cluster_dist = []

        # population
        for p_idx, p in enumerate(self.P[t]):
            print("p_idx={} p={}".format(p_idx, p))
            data_cluster_dist = []

            # data index
            for d_idx in range(len(self.data)):
                # print("d_idx={}".format(d_idx))
                min_dist = None
                min_idx = None

                # cluster
                for c_idx, c in enumerate(p):

                    # if source and destination is the same continue
                    if d_idx == c:
                        continue

                    # print("c_idx={} c={}".format(d_idx, c))

                    # compute distance with data[d_idx] and C[c_idx]
                    dist = self.distances[tuple(sorted((d_idx, c)))]
                    # print("{} {} dist is {}".format(d_idx, c, dist))

                    if min_dist is None or dist < min_dist:
                        min_dist = dist
                        min_idx = c_idx

                data_cluster_dist.append((d_idx, p[min_idx], min_dist))

            P_cluster_dist.append(data_cluster_dist)
        return np.asarray(P_cluster_dist)

    def objective_function(self, t):
        population = self.P_cluster_dist[t]

        # select only distance column
        only_distances = population[:, :, 2]

        # sum all distances per cluster
        sum_distances_per_cluster = np.sum(only_distances, axis=1)

        # get indices of the sorted array based on the distance
        sorted_indices = np.argsort(sum_distances_per_cluster)

        # update Population and Population_cluster_distance ordering based on sum of distances
        self.P[t] = np.asarray(self.P[t])[sorted_indices]
        self.P_cluster_dist[t] = population[sorted_indices]

    def select_best_clusters(self, t):
        # select P_size individuals of the population from time t-1 to time t
        self.P_cluster_dist.append(self.P_cluster_dist[t - 1][0:self.P_size])
        self.P.append(self.P[t - 1][0:self.P_size])

    def crossover(self, t):
        # TODO choose better qtd value
        if self.K < 5:
            qtd = 1
        else:
            qtd = 2
        idxs = self.get_ramdom_indices(self.K, qtd)
        
        print("K={} qtd={} idxs={}".format(self.K, qtd, idxs))
        pass

    def compute(self):
        print "compute"

        t = 0

        pop = self.population_random_initialization()
        self.P.append(pop)

        while True:
            print ("\nt={}".format(t))

            # assign points to clusters based on minimum distance
            p_cluster_dist = self.assign_points_to_clusters(t)
            self.P_cluster_dist.append(p_cluster_dist)
            print("#pcluster={} pcluster={}".format(len(self.P[t]), self.P[t]))

            # compute objective function
            # sort P and P_cluster_dist based on objective function
            self.objective_function(t)

            t += 1
            if t < self.max_iterations:

                # select P(t) from P(t-1)
                self.select_best_clusters(t)

                # crossover P(t)
                self.crossover(t)


                # mutate P(t)
            else:
                break



