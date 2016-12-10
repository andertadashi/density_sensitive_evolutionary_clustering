import random
import numpy as np
import networkx as nx
import itertools
import math
import matplotlib.pyplot as plt
from abc import ABCMeta, abstractmethod
from Graph import GraphTest

class Cluster:

    def __init__(self, database, dissimilarity, P_size=10, K=3, max_iterations=100):
        self.debug = True
        self.database = database
        self.max_iterations = max_iterations
        self.K = K
        self.P = []               # population at time t
        self.P_cluster_dist = []  # (individual, cluster, dist(individual, cluster))
        self.P_size = P_size  # population size
        self.data = database.load_data()
        self.N = len(self.data)
        self.dissimilarity = dissimilarity
        self.assigned_to_cluster = []
        self.distances = self.compute_distances()
        self.crossover_percentage = 0.8
        self.mutate_percentage = 0.1


    def population_random_initialization(self):
        if self.debug:
            print "\npopulation_random_initialization"
        population = []
        i = 0
        while len(population) < self.P_size and i <= self.P_size * 10:
            c = sorted(random.sample(range(self.N), self.K))
            if c not in population:
                population.append(c)
            i += 1
        print("P[0].size={}".format(len(population)))
        return population


    def get_random_indices(self, range_sample, qtd):
        indices = sorted(random.sample(range(range_sample), qtd))
        return indices


    def compute_distances(self):
        if self.debug:
            print "\ncompute_distances"

        g = GraphTest()

        distances = g.get_graph_dictionary(self.database.path, self.data, self.dissimilarity)

        return distances

    def assign_points_to_clusters(self, t):
        if self.debug:
            print("\nt={} assign_points_to_clusters".format(t))

        P_cluster_dist = []
        print("len(self.P)={} len(self.P[{}])={}".format(len(self.P), t, len(self.P[t])))
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
        P_cluster_dist = np.asarray(P_cluster_dist)
        # print("P_cluster_dist.size={} P_cluster_dist={}".format(len(P_cluster_dist), P_cluster_dist))
        return P_cluster_dist

    def objective_function(self, t):
        if self.debug:
            print("\nt={} objective_function".format(t))

        population = self.P_cluster_dist[t]
        print("population.shape={}".format(population.shape))

        # select only distance column
        only_distances = population[:, :, 2]
        print("only_distances.shape={}".format(only_distances.shape))

        # sum all distances per cluster
        sum_distances_per_cluster = np.sum(only_distances, axis=1)
        print("sum_distances_per_cluster.shape={} {}".format(sum_distances_per_cluster.shape, sum_distances_per_cluster))

        # get indices of the sorted array based on the distance
        sorted_indices = np.argsort(sum_distances_per_cluster)
        print("sorted_indices={}".format(sorted_indices))

        # update Population and Population_cluster_distance ordering based on sum of distances

        print("P[{}].shape={} sorted_idx={}".format(t, len(self.P[t]), sorted_indices.shape))
        self.P_cluster_dist[t] = population[sorted_indices]
        self.P[t] = np.asarray(self.P[t])[sorted_indices]


    def select_best_clusters(self, t):
        if self.debug:
            print("\nt={} select_best_clusters".format(t))

        # select P_size individuals of the population from time t-1 to time t

        print("P_cluster_dist={} P={}".format(self.P_cluster_dist[t - 1].shape, self.P[t - 1].shape))

        Pop_dist_t = self.P_cluster_dist[t - 1][0:self.P_size]
        # self.P_cluster_dist[t] = Pop_dist_t

        Pop_t = self.P[t - 1][0:self.P_size]
        # self.P.append(Pop_t)

        assert len(self.P) == len(self.P_cluster_dist), \
            "len(self.P)={} len(self.P_cluster_dist)={}".format(len(self.P), len(self.P_cluster_dist))
        return Pop_t, Pop_dist_t


    @staticmethod
    def is_valid(cluster):
        valid = np.unique(cluster).size == len(cluster)
        if not valid:
            print("cluster={} is not valid".format(cluster))
        return valid

    def crossover(self, t):

        if self.debug:
            print("\nt={} crossover".format(t))

        # TODO choose better qtd value
        if self.K < 5:
            qtd = 1
        else:
            qtd = 2

        qtd_crossover = int(len(self.P[t]) * self.crossover_percentage)

        idxs_for_crossover = self.get_random_indices(len(self.P[t]), qtd_crossover)
        print("qtd_crossover={} idxs_for_crossover={}".format(qtd_crossover, idxs_for_crossover))


        new_pop = []
        for i_mutation in range(len(idxs_for_crossover)-1):
            c0_idx = idxs_for_crossover[i_mutation]
            c1_idx = idxs_for_crossover[i_mutation + 1]
            c0 = self.P[t][c0_idx].copy()
            c1 = self.P[t][c1_idx].copy()

            idxs = self.get_random_indices(self.K, qtd)
            print("K={} qtd={} idxs={}".format(self.K, qtd, idxs))

            for i in idxs:
                tmp = c0[i]
                c0[i] = c1[i]
                c1[i] = tmp

            c0 = sorted(c0)
            c1 = sorted(c1)

            if self.is_valid(c0):
                new_pop.append(c0)

            if self.is_valid(c1):
                new_pop.append(c1)

        if self.debug:
            print ("P[{}]={}\nnew_pop={}  -> ".format(t, self.P[t], np.asarray(new_pop)))
        new_pop = np.append(self.P[t], np.asarray(new_pop), axis=0)

        # http://stackoverflow.com/questions/16970982/find-unique-rows-in-numpy-array
        self.P[t] = new_pop  #np.vstack(set(map(tuple, new_pop)))

    def mutate(self, t):
        if self.debug:
            print("\nt={} mutate".format(t))

        population_size = len(self.P[t])
        qtd_mutations = int(math.ceil(1.0 * population_size * self.mutate_percentage))
        idxs_for_mutation = self.get_random_indices(len(self.P[t]), qtd_mutations)

        for idx in idxs_for_mutation:
            print("idx={}".format(idx))
            p = self.P[t][idx]
            if self.debug:
                print("p={}".format(p))
            # index to mutate in p
            p_idx = self.get_random_indices(len(p), 1)
            # new data idx
            p_mutated = p.copy()
            if p_mutated[p_idx] + 10 < self.N:
                d_idx = p_mutated[p_idx] + 10
            else:
                d_idx = p_mutated[p_idx] - 10
            # d_idx = self.get_random_indices(self.N, 1)

            p_mutated[p_idx] = d_idx
            if self.debug:
                print("p_mutated={}".format(p_mutated))
            if self.is_valid(p_mutated):
                np.append(self.P[t], p_mutated)


    def compute(self):
        print "\ncompute"

        t = 0

        pop = self.population_random_initialization()
        self.P.append(pop)

        while True:
            print ("\nt={}".format(t))

            # assign points to clusters based on minimum distance
            p_cluster_dist = self.assign_points_to_clusters(t)
            print("compute -> p_cluster_dist={}".format(p_cluster_dist.shape))
            self.P_cluster_dist.append(p_cluster_dist)
            print("compute -> len(self.P)={} len(self.P_cluster_dist)={}".format(len(self.P), len(self.P_cluster_dist)))
            print("#P={} P={}".format(len(self.P[t]), self.P[t]))
            print("#P_dist={} P_dist={}".format(len(self.P_cluster_dist[t]), self.P_cluster_dist[t]))

            # compute objective function
            # sort P and P_cluster_dist based on objective function
            self.objective_function(t)

            t += 1
            if t < self.max_iterations:

                # select P(t) from P(t-1)
                P_t, P_dist_t = self.select_best_clusters(t)
                self.P.append(P_t)

                # crossover P(t)
                self.crossover(t)

                # mutate P(t)
                self.mutate(t)
            else:
                t -= 1
                print("result t={} \nP[{}]={}\nP_dist[{}]={}".format(t, t, self.P[t], t, self.P_cluster_dist[t]))
                labels = np.asarray(self.P_cluster_dist[t])
                print("===> labels={}".format(labels))
                l = labels[0][:, 1]
                print ("===> l={}".format(l))
                self.database.plot(self.dissimilarity.rho, self.data, l)
                break




