from functools import wraps
from flask import request, jsonify
from marshmallow import ValidationError

def required_params(schema):
    '''
    validate api input params (marshmallow)
    '''
    def decorator(fn):

        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                if request.method == "GET":
                    schema.load(request.get_json())
                else:
                    schema.load(request.get_json())
            except ValidationError as err:
                error = {
                    "messages": err.messages
                }
                return {'result': error}, 400
            return fn(*args, **kwargs)

        return wrapper

    return decorator