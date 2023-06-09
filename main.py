import os
import json
import requests
import numpy as np
import pandas as pd
from textblob import TextBlob
from flask import Flask, request
import services.data_service as ds
from fast_autocomplete import AutoComplete
import services.indexing_service as indexing
from search_suggestion import SearchSuggestion
from services.data_service import initiate_data
from models.response_model import response_model
from sklearn.metrics.pairwise import cosine_similarity
from services.clustered_service import document_clustering
from services.clustered_service import get_documents_from_clusters
from sklearn.feature_extraction.text import TfidfVectorizer

app = Flask(__name__)
vectorizer = TfidfVectorizer()
active_cluster = False


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super().default(obj)


@app.route('/get-result')
def get_result():
    #################### take a query
    query = request.args.get("query")
    #################### send it to data_preprocessing_endpoint

    response = requests.get('http://localhost:8001/get-data-preprocessed?query=' + query)
    preprocessed_data = json.loads(response.text)
    if preprocessed_data['status_code'] != 200:
        return response_model(preprocessed_data['data'], preprocessed_data['status_code'])
    clean_query = preprocessed_data['data']
    print("PreProcessing Done : Clean Query is : " + clean_query)
    last_result = []
    if not active_cluster:
        #################### get related doc_ids from indexing_endpoint
        response = requests.get('http://localhost:8002/get-related-docs?clean_query=' + clean_query)
        related_docs_data = json.loads(response.text)

        if related_docs_data['status_code'] != 200:
            return response_model(related_docs_data['data'], related_docs_data['status_code'])

        related_docs_ids = related_docs_data['data']
        print("Get Related Docs from Index Done .... len of the array is :")
        print(len(related_docs_ids))

        #################### send it to similarity_endpoint and get cosine similarity
        response = requests.post('http://localhost:8003/calc-similarity', data=json.dumps({
            'clean_query': clean_query,
            'related_docs': related_docs_ids
        }), headers={'Content-Type': 'application/json'})

        similarity_data = json.loads(response.text)

        if similarity_data['status_code'] != 200:
            return response_model(similarity_data['data'], similarity_data['status_code'])

        similarity = similarity_data['data']
        print("Calc Similarity With Ranking Done ... len of the array :")
        print(len(similarity))
        #################### return the sorted result
        docs = ds.get_docs()
        for score in similarity[:100]:
            if score[1] > 0:
                last_result.append({
                    'doc_id': docs['doc_id'][related_docs_ids[score[0]]],
                    'text': str(docs['text'][related_docs_ids[score[0]]]),
                    'score': score[1]
                })

        return response_model(json.loads(json.dumps(last_result, cls=NumpyEncoder)), 200)
    elif active_cluster:
        similarity_ranked = get_documents_from_clusters(clean_query)
        print(similarity_ranked)
        for _, doc in similarity_ranked[:100].iterrows():
            if doc['score'] > 0:
                last_result.append({
                    'score': doc['score'],
                    'doc_id': doc['doc_id'],
                    'text': ds.get_docs()['text'][[doc['id']]].tolist()[0]
                })

    return response_model(last_result, 200)
    # return response_model(json.loads(json.dumps(last_result, cls=NumpyEncoder)), 200)


@app.route('/spell-correction')
def spell_correction():
    query = request.args.get("query")
    query = TextBlob(query)
    return response_model(str(query.correct()), 200)


@app.route('/auto-complete')
def auto_complete():
    query = request.args.get("query")
    autocomplete = AutoComplete(words=words)
    suggestions = autocomplete.search(query)

    return response_model(list(suggestions[1:]), 200)


@app.route('/query-suggestion')
def query_suggestion():
    query = request.args.get("query")
    queries = ds.get_queries()
    vector_model_query = vectorizer.transform([query])
    similarity = cosine_similarity(vector_model_query, vector_model_queries)
    results = list(enumerate(similarity[0]))
    sorted_results = sorted(results, key=lambda x: x[1], reverse=True)
    # print(sorted_results)
    last_result = []
    for (i, score) in sorted_results:
        # if score > 0.2:
        last_result.append({
            'query_id': queries['query_id'][i],
            'text': queries['text'][i],
            'score': score
        })
    # print(last_result)
    df = pd.DataFrame(last_result)

    ss = SearchSuggestion()

    ss.batch_insert(df['text'].str.lower())
    query = query.lower()

    result = ss.search(query)
    # print(result)
    return response_model(list(result), 200)


@app.route('/change-dataset', methods=['POST'])
def change_dataset():
    with open(os.path.join(os.getcwd(), "", "data_set_name.json"), 'r') as f:
        data = json.load(f)
    data['name'] = request.get_json()['dataset_name']

    with open(os.path.join(os.getcwd(), "", "data_set_name.json"), 'w') as f:
        json.dump(data, f)
    initiate()
    # indexing endpoint
    requests.get('http://localhost:8002/reload-data')
    # similarity endpoint
    requests.get('http://localhost:8003/reload-data')
    return response_model("done", 200)


def initiate():
    global vector_model_queries, words

    initiate_data()
    indexing.create_docs_index()
    docs_index = indexing.get_docs_index()
    queries = ds.get_queries()
    lower_queries = queries['text'].str.lower()
    vector_model_queries = vectorizer.fit_transform(lower_queries)
    words = {key: {} for key in docs_index.keys()}


if __name__ == '__main__':
    initiate()
    app.run(port=8000)
