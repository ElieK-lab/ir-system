from flask import Flask, request
import services.data_service as data
from models.response_model import response_model

app = Flask(__name__)


@app.route('/get-docs')
def get_docs():
    return response_model(data.get_docs().values.tolist(), 200)


@app.route('/get-docs-clean')
def get_docs_clean():
    return response_model(data.get_docs_clean().values.tolist(), 200)


@app.route('/get-queries')
def get_queries():
    return response_model(data.get_queries().values.tolist(), 200)


@app.route('/get-queries-clean')
def get_queries_clean():
    return response_model(data.get_queries_clean().values.tolist(), 200)


if __name__ == '__main__':
    data.initiate_data()
    app.run(port=8010, debug=True)
