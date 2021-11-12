import json

from data import Data

from flask import *


app = Flask(__name__)


@app.errorhandler(404) 
def invalid_route(error): 
    return Response(
        json.dumps({
            'message' : 'not found',
            'error_code' : 404,
            'status': False,
            'data': ''
        }
    ), status=404, mimetype="application/json")

@app.route('/category/', methods=['GET'])
def category():
    data = Data()
    load_data = data.load()
    if 'query' not in request.args:
        return Response(
            json.dumps({
                'message' : 'all category',
                'error_code' : 200,
                'status': True,
                'data': load_data['category']
            }
        ), status=200, mimetype="application/json")
    else:
        if request.args['query'] in load_data['category'].keys():
            return Response(
                json.dumps({
                    'message' : 'all category',
                    'error_code' : 200,
                    'status': True,
                    'data': load_data['category'][request.args['query']]
                }
            ), status=200, mimetype="application/json")
        else:
            return Response(
                json.dumps({
                    'message' : 'category not found',
                    'error_code' : 404,
                    'status': False,
                    'data': ''
                }
            ), status=404, mimetype="application/json")
    

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080, threaded=True, use_reloader=False)