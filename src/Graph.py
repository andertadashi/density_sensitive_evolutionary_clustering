import sys
import os
try:
   import cPickle as pickle
except:
   import pickle
from __builtin__ import staticmethod

from graph_tool.all import *


class GraphTest:

    def __init__(self):
        pass

    @staticmethod
    def file_name(path, dissimilarity):
        dir_name = os.path.dirname(path)
        base_name = os.path.basename(path)
        name = os.path.splitext(base_name)[0]
        return "{}/{}_{}.pickle".format(dir_name, name, dissimilarity.rho)


    def get_graph_dictionary(self, path, data, dissimilarity):
        N = len(data)

        print("graph V={}".format(N))

        pickle_filename = self.file_name(path, dissimilarity)

        if os.path.exists(pickle_filename):
            with open(pickle_filename, "rb") as input_file:
                return pickle.load(input_file)
        else:
            # g = Graph()
            g = Graph(directed=False)
            e_weight = g.new_edge_property("float")
            data_list = []
            dist = []
            for i in range(N):
                for j in range(N):
                    if i == j:
                        continue
                    d = dissimilarity.distance(i, j)
                    # print dist
                    assert dist >= 0, "dist is negative!"
                    data_list.append((i, j))
                    dist.append(d)
            print("add data_list to graph")
            g.add_edge_list(data_list)
            print("add weight to graph")
            e_weight.a = dist

            dict = {}
            for i in range(N):
                for j in range(N):
                    if i == j:
                        continue
                    d = graph_tool.topology.shortest_distance(g, source=g.vertex(i), target=g.vertex(j), weights=e_weight)
                    dict[tuple(sorted([i, j]))] = d
                    print("path={} i={} j={} dist={}".format(path, i, j, d))
            with open(pickle_filename, "wb") as output_file:
                pickle.dump(dict, output_file)
            return dict
