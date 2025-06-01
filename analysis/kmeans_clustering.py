import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

def cluster_by_country_accident(df, n_clusters=3):
    df_clean = df.dropna(subset=['Country', 'Acc_Type'])
    le_country = LabelEncoder().fit_transform(df_clean['Country'])
    le_acc = LabelEncoder().fit_transform(df_clean['Acc_Type'])
    X = pd.DataFrame({'Country': le_country, 'Acc_Type': le_acc})
    kmeans = KMeans(n_clusters=n_clusters, random_state=42).fit(X)
    df_clean['Cluster'] = kmeans.labels_
    plt.scatter(X['Country'], X['Acc_Type'], c=df_clean['Cluster'], cmap='viridis')
    plt.title('K-means Clustering')
    plt.xlabel('Country')
    plt.ylabel('Accident Type')
    plt.show()
    return df_clean