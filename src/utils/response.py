from flask import jsonify

class CustomResponse:
    @staticmethod
    def success(data, status_code=200):
        response = {
            'status': 'success',
            'data': data,
            'code': status_code
        }
        return jsonify(response), status_code

    @staticmethod
    def failure(message, status_code):
        response = {
            'status': 'error',
            'message': message,
            'code': status_code
        }
        return jsonify(response), status_code
