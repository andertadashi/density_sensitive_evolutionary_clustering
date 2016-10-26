#!/usr/bin/python

from Algorithms import Cluster
from Database import DatabaseSimepar
from Dissimilarity import DensityDistance
from src.Database import DatabaseIris

database = DatabaseIris()
dissimilarity = DensityDistance(rho=1.2)

cluster = Cluster(database, dissimilarity, P_size=5, K=3, max_iterations=10)

cluster.compute()
