#!/usr/bin/python

import sys
from Algorithms import Cluster
from Database import DatabaseSimepar
from Dissimilarity import DensityDistance
from Database import DatabaseIris
from Database import TwoDimensionData
from Graph import GraphTest
# from graph_tool.all import *

print("database reading")
database = TwoDimensionData("../datasets/R15.txt", '\t')

print("dissimilarity class")
dissimilarity = DensityDistance(rho=1.2)

data = database.data
labels = database.labels

# cluster = Cluster(database, dissimilarity, P_size=5, K=3, max_iterations=10)
# cluster.compute()

print("create graph")

g = GraphTest()

g.get_graph_dictionary(data, dissimilarity)


