#!/usr/bin/python

import numpy as np
from Algorithms import Cluster
from Database import DatabaseSimepar
from Dissimilarity import DensityDistance
from Database import DatabaseIris, TwoDimensionData

# database = DatabaseIris()
database = TwoDimensionData('../database/spiral.txt', '\t')
for rho in np.arange(1, 3, 0.2):
    dissimilarity = DensityDistance(rho=rho)

    cluster = Cluster(database, dissimilarity, P_size=5, K=3, max_iterations=10)

    # cluster.compute()
