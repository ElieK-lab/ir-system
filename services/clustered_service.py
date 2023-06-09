import json
import os
import pickle
import numpy as np
from sklearn.cluster import KMeans
from sklearn.decomposition import TruncatedSVD
import services.data_service as ds
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

vectorizer = TfidfVectorizer(stop_words='english')

object_path = "C:\\Users\\Elie\\Desktop\\testpython\\objects\\"
with open('C:\\Users\\Elie\\Desktop\\testpython\\data_set_name.json') as json_file:
    dataset_name = json.load(json_file)['name']

clustered_vectorizer = pickle.load(open(os.path.join(object_path + dataset_name + "_vectorizer.pkl"), 'rb'))
clustered_vectorizer_docs = pickle.load(
    open(os.path.join(object_path + dataset_name + "_vectorized_docs.pkl"), 'rb'))
svd = pickle.load(open(os.path.join(object_path + dataset_name + "_svd.pkl"), 'rb'))
kmeans = pickle.load(open(os.path.join(object_path + dataset_name + "_kmeans_model.pkl"), 'rb'))

cv_svd = svd.fit_transform(clustered_vectorizer_docs)
kmeans = kmeans.fit(cv_svd)
labels = kmeans.labels_


def get_documents_from_clusters(clean_query):
    query_vector = clustered_vectorizer.transform([clean_query])

    ################ Reduce the dimensionality of the vectorized data
    query_vector_svd = svd.transform(query_vector)

    ################ Find the nearest cluster
    nearest_cluster = kmeans.predict(query_vector_svd)[0]

    ################ Retrieve documents
    cluster_indices = np.where(labels == nearest_cluster)[0]
    cluster_documents = ds.get_docs().iloc[cluster_indices]

    ################ Rank the documents
    similarity_scores = cosine_similarity(query_vector, clustered_vectorizer_docs[cluster_indices])
    cluster_documents['score'] = similarity_scores.flatten()

    ################ Sort the documents by score
    cluster_documents = cluster_documents.sort_values('score', ascending=False)
    return cluster_documents


def document_clustering():
    docs_clean = ds.get_docs_clean()
    docs_clean = docs_clean.fillna('')

    vectorized_docs = vectorizer.fit_transform(docs_clean['text'])

    svd = TruncatedSVD(n_components=100)
    vectorized_docs_svd = svd.fit_transform(vectorized_docs)
    kmeans = KMeans(n_clusters=8, random_state=0, n_init=1)
    kmeans.fit(vectorized_docs_svd)

    pickle.dump(vectorizer, open(os.path.join(os.getcwd(), "objects", ds.dataset_name + "_vectorizer.pkl"), 'wb'))
    pickle.dump(svd, open(os.path.join(os.getcwd(), "objects", ds.dataset_name + "_svd.pkl"), 'wb'))
    pickle.dump(vectorized_docs,
                open(os.path.join(os.getcwd(), "objects", ds.dataset_name + "_vectorized_docs.pkl"), 'wb'))
    pickle.dump(kmeans, open(os.path.join(os.getcwd(), "objects", ds.dataset_name + "_kmeans_model.pkl"), 'wb'))
