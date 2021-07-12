from sklearn.cluster import KMeans, AgglomerativeClustering as ac, SpectralClustering
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

def cluster_data(data, model = 'agglom', k = 5, linkage = 'complete'):
    """
    Trains a clustering model given the model type, number of clusters, linkage type, and MWD data.

    Parameters
    ----------
    data: Pandas DataFrame
        The data to be used for clustering. Can be normalized weighted data, normalized unweighted data, or
        Principle Components of data for dimension reduction.
    model: String
        A String stating which Clustering Algorithm to be used. Default is Agglomerative.
    k: int
        The number of clusters to use. Default is 4.
    linkage: String
        The type of linkage to be used for Agglomerative clustering. Default is Complete

    Returns
    -------
    A list of the cluster labels
    """
    if model == 'kmeans':
        km = KMeans(n_clusters=k)
        km_labels = km.fit_predict(data)
        return km_labels
    elif model == 'agglom':
        acCluster = ac(n_clusters=k, affinity="euclidean", linkage=linkage)
        ac_labels = acCluster.fit_predict(data)
        return ac_labels
    else:
        spectral = SpectralClustering(n_clusters=k, assign_labels='kmeans', affinity='rbf')
        spec_labels = spectral.fit_predict(data)
        return spec_labels

def modify_data(data, data_type):
    """
    Normalizes the data, Adds weights to the data if wanted for weighted clustering/WMDS, or computes
    the first 3 Principal Components if PCA is wanted for Clustering/Dimension Reduction.

    Parameters
    ----------
    data: Pandas DataFrame
        The data to be normalized, weighted, or PCA computed upon.
    data_type: String
         A String stating how to modify the data. If 'weighted' is provided, weights are added to the
         features of the normalized data. If 'PCA' is provided, PCA is performed upon the
         normalized data.

    Returns
    -------
    A Pandas DataFrame with the modified data.
    """
    data = pd.DataFrame(StandardScaler().fit_transform(data), columns = data.columns)
    if data_type == 'weighted':
        # Weight values will be tweaked as more features are added
        weights = pd.Series([1.15, 1, 1, 1, 1.25], index=data.columns)
        data = data * (weights / weights.sum())
    elif data_type == 'PCA':
        pca_model = PCA(n_components=3)
        data = pd.DataFrame(pca_model.fit_transform(data), columns = ['PC1', 'PC2', 'PC3'])
    return data
