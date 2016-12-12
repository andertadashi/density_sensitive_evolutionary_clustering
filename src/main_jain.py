#!/usr/bin/python

import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')

import numpy as np
import os
from Algorithms import Cluster
from Database import DatabaseSimepar
from Dissimilarity import DensityDistance
from Database import DatabaseIris, TwoDimensionData

# database = DatabaseIris()
# a = ['Compound.txt'  , 'flame.txt' ,'D31.txt',  'jain.txt' , 'pathbased.txt' , 'R15.txt' , 'spiral.txt']
#a = ['Aggregation.txt' ] 
# a = ['flame.txt', 'jain.txt']
#a = [('spiral.txt', 3)]
#a = [('pathbased.txt', 3)]
a = [('jain.txt', 2)]

results = []

for f, K in a:
    fi = '../datasets/{}'.format(f)
    database = TwoDimensionData(fi, '\t')

    base_name = os.path.basename(fi)
    name = os.path.splitext(base_name)[0]

    for rho in np.arange(1.0, 3.4, 0.2):
    # for rho in [2.8]:
        dissimilarity = DensityDistance(rho=rho)

        cluster = Cluster(database, dissimilarity, P_size=50, K=K, max_iterations=100)

        score, score_normalized = cluster.compute()
        results.append((name, K, rho, score, score_normalized))


for name, K, rho, score, score_normalized in results:
    print("{};{};{};{:.8f};{:.8f}".format(name, K, rho, score, score_normalized))
