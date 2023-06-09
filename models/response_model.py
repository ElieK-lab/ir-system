def response_model(result, status_code):
    return {
        'data': result,
        'status_code': status_code
    }
