__author__ = 'Desmond'

import csv

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler



##############################################################################
# Generate sample data
X = []
with open("../temp/uid_features.csv", 'r') as f:
    reader = csv.reader(f)
    reader.next()
    for line in reader:
        X.append(line)
X = StandardScaler().fit_transform(X)

###############################################################################
# Visualize the results on PCA-reduced data

kmeans = KMeans(init='k-means++', n_clusters=100, n_init=100)
kmeans.fit(X)

# Obtain labels for each point in mesh. Use last trained model.
Z = kmeans.predict(X)

with open("../temp/uid_features_clu.csv", 'wb') as f:
    writer = csv.writer(f)
    writer.writerow([''])
    for i in Z:
        writer.writerow([i])
