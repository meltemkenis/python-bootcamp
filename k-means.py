
from sklearn.cluster import KMeans
from sklearn import datasets
import matplotlib.pyplot as plt
import numpy as np


iris = datasets.load_iris()
X = iris.data
y = iris.target

kmeans = KMeans(n_clusters=3).fit_predict(X)

plt.scatter(X[:, 0], y, c=kmeans)
