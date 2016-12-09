import sys
from graph_tool.all import *


class GraphTest:

    def __init__(self):
        pass

    def get_graph_dictionary(self, data, dissimilarity):
        N = len(data)

        print("graph V={}".format(N))

        # g = Graph()
        g = Graph(directed=False)
        e_weight = g.new_edge_property("float")
        list = []
        dist = []
        for i in range(N):
            for j in range(N):
                if i == j:
                    continue
                d = dissimilarity.distance(i, j)
                # print dist
                assert dist >= 0, "dist is negative!"
                list.append((i, j))
                dist.append(d)
        print("add list to graph")
        g.add_edge_list(list)
        print("add weight to graph")
        e_weight.a = dist

        for i in range(N):
            for j in range(N):
                if i == j:
                    continue
                d = graph_tool.topology.shortest_distance(g, source=g.vertex(i), target=g.vertex(j), weights=e_weight)
                print("i={} j={} dist={}".format(i, j, d))
