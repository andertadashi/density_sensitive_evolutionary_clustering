#!/usr/bin/python

import numpy as np
from Algorithms import Cluster
from Database import DatabaseSimepar
from Dissimilarity import DensityDistance
from Database import DatabaseIris, TwoDimensionData

# database = DatabaseIris()

# a = ['flame.txt', 'jain.txt' ]
# a = ['spiral.txt']
#a = ['Aggregation.txt'  ,'Compound.txt'  ,'D31.txt'  ,'flame.txt' ,  'jain.txt' , 'pathbased.txt' , 'R15.txt' , 'spiral.txt']
a = ['flame.txt', 'pathbased.txt', 'spiral.txt', 'jain.txt', 'Compound.txt', 'R15.txt']
for f in reversed(a):
    print f
    fi = '../datasets/{}'.format(f)
    database = TwoDimensionData(fi, '\t')
    for rho in np.arange(1.0, 3.4, 0.2):
        dissimilarity = DensityDistance(rho=rho)

        cluster = Cluster(database, dissimilarity, P_size=15, K=3, max_iterations=2)

        # cluster.compute()
