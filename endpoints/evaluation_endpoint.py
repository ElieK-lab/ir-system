from flask import Flask
from models.response_model import response_model
from services.evaluation_service import get_evaluation_values
from services.data_service import initiate_data
from services.indexing_service import create_docs_index

app = Flask(__name__)


@app.route('/get-evaluation-values')
def get_eval_values():
    result = get_evaluation_values()
    return response_model(result, 200)


if __name__ == '__main__':
    initiate_data()
    create_docs_index()
    print(get_evaluation_values())
    app.run(port=8005)
