#!/usr/bin/python

from Algorithms import Cluster
from Database import DatabaseSimepar
from Dissimilarity import DensityDistance
from Database import DatabaseIris
from Database import TwoDimensionData


database = TwoDimensionData("../database/D31.txt", '\t')
dissimilarity = DensityDistance(rho=1.2)

data = database.data
labels = database.labels

cluster = Cluster(database, dissimilarity, P_size=5, K=3, max_iterations=10)


cluster.compute()
