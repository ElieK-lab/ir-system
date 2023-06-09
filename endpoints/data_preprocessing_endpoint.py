from flask import Flask, request
from services.data_preprocessing_service import apply_preprocessing_text
from models.response_model import response_model

app = Flask(__name__)


@app.route('/get-data-preprocessed')
def get_data_preprocessed():
    if request.args.get('query') is None:
        return response_model("you should pass query var in query params", 400)
    return response_model(apply_preprocessing_text(request.args.get('query')).strip(), 200)


if __name__ == '__main__':
    app.run(port=8001, debug=True)
