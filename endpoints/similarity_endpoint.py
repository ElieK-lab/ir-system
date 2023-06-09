from flask import Flask, request
from services.similarity_service import calc_similarity_service
from models.response_model import response_model
import services.data_service as ds
import services.indexing_service as indexing

app = Flask(__name__)


# take the query and related docs
@app.route('/calc-similarity', methods=['POST'])
def calc_similarity():
    request_data = request.get_json()
    clean_query = request_data['clean_query']
    related_docs = request_data['related_docs']
    result = calc_similarity_service(related_docs, clean_query)
    return response_model(result, 200)


@app.route('/reload-data')
def reload_data():
    ds.initiate_data()
    indexing.create_docs_index()
    return response_model("done", 200)


if __name__ == '__main__':
    ds.initiate_data()
    indexing.create_docs_index()
    app.run(port=8003, debug=True)
