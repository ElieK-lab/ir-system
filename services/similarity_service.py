import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import services.data_service as ds

vectorizer = TfidfVectorizer()


def calc_similarity_service(related_docs, clean_query):
    docs_clean = ds.get_docs_clean()
    if len(related_docs) == 0:
        print("empty returned result")
        return []
    vector_model_docs = vectorizer.fit_transform(docs_clean['text'][related_docs])
    vector_model_query = vectorizer.transform([clean_query])
    similarity = cosine_similarity(vector_model_query, vector_model_docs)

    results = list(enumerate(similarity[0]))
    sorted_results = sorted(results, key=lambda x: x[1], reverse=True)
    return sorted_results
