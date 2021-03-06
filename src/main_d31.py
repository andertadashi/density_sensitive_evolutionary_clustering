#!/usr/bin/python

import numpy as np
from Algorithms import Cluster
from Database import DatabaseSimepar
from Dissimilarity import DensityDistance
from Database import DatabaseIris, TwoDimensionData

# database = DatabaseIris()
# a = ['Compound.txt'  , 'flame.txt' ,'D31.txt',  'jain.txt' , 'pathbased.txt' , 'R15.txt' , 'spiral.txt']
a = ['D31.txt', 'Aggregation.txt']
for f in a: 
    fi = '../datasets/{}'.format(f)
    database = TwoDimensionData(fi, '\t')
    for rho in np.arange(1.2, 3.8, 0.4):
        dissimilarity = DensityDistance(rho=rho)

        cluster = Cluster(database, dissimilarity, P_size=5, K=31, max_iterations=10)

        # cluster.compute()
