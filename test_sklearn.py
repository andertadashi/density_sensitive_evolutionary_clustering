import numpy as np
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn import metrics

from Dissimilarity import DensityDistance
from Database import TwoDimensionData

database = TwoDimensionData("../database/D31.txt", '\t')
#dissimilarity = DensityDistance(rho=1.2)

data = np.asarray(database.data)
labels = np.asarray(database.labels)

kmeans = KMeans(n_clusters=31, random_state=1).fit_predict(data)
metrics.silhouette_score(data, labels, metric='euclidean')

plt.scatter(data[:, 0], data[:, 1], c=kmeans)
plt.title("K-means")
plt.show()



