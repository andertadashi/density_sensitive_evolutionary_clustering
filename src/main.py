#!/usr/bin/python
# -*- coding: utf-8 -*-
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
# a = [('spiral.txt', 3)]
#a = [('R15.txt', 15)]
#a = [('Compound.txt', 6)]

a = [('flame.txt', 2), ('pathbased.txt', 3), ('spiral.txt', 3), ('jain.txt', 2),
     ('Compound.txt', 6), ('R15.txt', 15)]

results_lines = []
results = {}
for t in range(10):
    file_dict = {}
    for f, K in a:
        fi = '../datasets/{}'.format(f)
        database = TwoDimensionData(fi, '\t')

        base_name = os.path.basename(fi)
        name = os.path.splitext(base_name)[0]
        rhos = {}
        # for rho in np.arange(1.0, 3.4, 0.2):
        # for rho in [1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4, 2.6, 2.8, 3.0, 3.2, 10, 30, 100]:
        for rho in [1.0, 1.2, 1.4]:

            if (f, rho) in results:
                result_vect = results[(f, rho)]
            else:
                result_vect = []

            dissimilarity = DensityDistance(rho=rho)

            cluster = Cluster(database, dissimilarity, P_size=50, K=K, max_iterations=70)

            score, score_normalized = cluster.compute()
            results_lines.append("{};{};{};{};{};{}".format(t, f, K, rho, score, score_normalized))

            result_vect.append((score, score_normalized))
            results[(f, rho)] = result_vect

print("\n\nresultados:")
for rl in results_lines:
    print rl


print("\n\nmédias:")
for key in results.keys():

    score_vector = results[key][0]
    score_norm_vector = results[key][1]

    score_vector_avg = np.sum(score_vector) / len(score_vector)
    score_norm_vector_avg = np.sum(score_norm_vector) / len(score_norm_vector)

    print ("file={} rho={} size={} score_avg={} score_norm_avg={}".format(
        key[0], key[1], len(results), score_vector_avg, score_norm_vector_avg))
