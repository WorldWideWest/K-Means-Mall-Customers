import pandas as pd
from sklearn.cluster import KMeans

# Importing and cleaning the data
data = pd.read_csv('../source/datasets_177976_401124_Mall_Customers.csv')
data = data.drop(['CustomerID'], axis = 1)
data['Genre'] = data['Genre'].map({'Female': 1, 'Male': 0})

# KMeans algorithm
X = data.iloc[:,2:4]


# Data Frame object is a pandas dataFrame with the required columns "Annual Income (k$)	Spending Score (1-100)"
# This algorithm predicts the optimal number of clusters
def cluster(dataFrame:object) -> list:
    wcss = []
    for i in range(1, len(dataFrame)):
        kmeans = KMeans(i)
        kmeans.fit(dataFrame)
        wcssIter = kmeans.inertia_
        wcss.append(wcssIter)
    return wcss

# We segmentate the customers
def fit(clusters:int, dataSet:object) -> list:
    kmeans = KMeans(clusters)
    return kmeans.fit_predict(dataSet)

# Concatenating the clustered results with the given dataFrame
def save(dataSet:object, clusters:list) -> object:
    dataSet["Clusters"] = clusters
    dataSet.to_csv("../source/clustered.csv", index = False)
    return dataSet
    
numClusters = cluster(X)
clustered = fit(7, X)
data = save(data, clustered)

print(data)
