from flask import Flask, request
from services.indexing_service import get_query_related_docs_ids, create_docs_index, get_docs_index
from models.response_model import response_model
from services.data_service import initiate_data
app = Flask(__name__)


@app.route('/get-related-docs')
def get_related_docs():
    if request.args.get('clean_query') is None:
        return response_model("you should pass clean_query var in query params", 400)

    result = get_query_related_docs_ids(request.args.get('clean_query'))
    return response_model(list(result), 200)


@app.route('/reload-data')
def reload_data():
    initiate_data()
    return response_model("done", 200)


if __name__ == '__main__':
    initiate_data()
    create_docs_index()
    app.run(port=8002, debug=True)
