#!/usr/bin/python

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
#a = [('R15.txt', 15)]
#a = [('Compound.txt', 6)]

a = [('flame.txt', 2), ('pathbased.txt', 3), ('spiral.txt', 3), ('jain.txt', 2), ('Compound.txt', 6), ('R15.txt', 15)]

results = []

for f, K in a:
    fi = '../datasets/{}'.format(f)
    database = TwoDimensionData(fi, '\t')

    base_name = os.path.basename(fi)
    name = os.path.splitext(base_name)[0]

    # for rho in np.arange(1.0, 3.4, 0.2):
    for rho in [1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4, 2.6, 2.8, 3.0, 3.2, 10, 30, 100]:
        dissimilarity = DensityDistance(rho=rho)

        cluster = Cluster(database, dissimilarity, P_size=50, K=K, max_iterations=50)

        score, score_normalized = cluster.compute()
        results.append((name, K, rho, score, score_normalized))


for name, K, rho, score, score_normalized in results:
    print("{};{};{};{:.8f};{:.8f}".format(name, K, rho, score, score_normalized))
