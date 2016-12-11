#!/usr/bin/python

import numpy as np
from Algorithms import Cluster
from Database import DatabaseSimepar
from Dissimilarity import DensityDistance
from Database import DatabaseIris, TwoDimensionData

# database = DatabaseIris()
# a = ['Compound.txt'  , 'flame.txt' ,'D31.txt',  'jain.txt' , 'pathbased.txt' , 'R15.txt' , 'spiral.txt']
#a = ['Aggregation.txt' ] 
a = ['flame.txt', 'jain.txt']
for f in a:
    fi = '../datasets/{}'.format(f)
    database = TwoDimensionData(fi, '\t')
    for rho in np.arange(1.0, 3.4, 0.2):
        dissimilarity = DensityDistance(rho=rho)

        cluster = Cluster(database, dissimilarity, P_size=40, K=2, max_iterations=50)

        cluster.compute()
