import pandas as pd
from sklearn.metrics.pairwise import cosine_distances, euclidean_distances, cosine_similarity
import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score

path_to_file="/Users/macbook/Desktop/DATA.csv"

df = pd.read_csv(path_to_file, encoding="utf-8")

x = df.drop("y",1) 
y = df["y"] 

l1 = linear_model.LinearRegression(normalize=True)

l1.fit(x,y) 

x1 = "f1 = 1, f2 = 2, f3 = 3, f4 = 4"

p = l1.predict([[1,2,3,4]])
l1.coef_
mean_squared_error([80.71615999], p)
l1.intercept_
