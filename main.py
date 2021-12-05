import json
import os
from dotenv import load_dotenv
from threading import Thread

from data import Data

from flask import *

load_dotenv()
PORT = os.environ['PORT']

app = Flask(__name__, static_url_path='/static')

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

@app.errorhandler(405)
def method_not_allowed(error): 
    return Response(
        json.dumps({
            'message' : 'method not allowed',
            'error_code' : 405,
            'status': False,
            'data': ''
        }
    ), status=405, mimetype="application/json")

@app.route('/data/update/', methods=['POST'])
@app.route('/data/update', methods=['POST'])
def data_update():
    data = Data()

    def _update(data):
        data.update()

    thread = Thread(target=_update, kwargs={'data': data})
    thread.start()

    return Response(
        json.dumps({
            'message' : 'data successfully updated',
            'error_code' : 200,
            'status': False,
            'data': ''
        }
    ), status=200, mimetype="application/json")

@app.route('/category/', methods=['GET'])
def category():
    data = Data()
    load_data = data.load()

    if 'query' not in request.args:
        return Response(
            json.dumps({
                'message' : 'no query parameter',
                'error_code' : 400,
                'status': False,
                'data': ''
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
                    'error_code' : 400,
                    'status': False,
                    'data': ''
                }
            ), status=200, mimetype="application/json")

@app.route('/item/', methods=['GET'])
def item():
    data = Data()
    all_items = data.get_all_items()

    return Response(
        json.dumps({
            'message' : 'all item',
            'error_code' : 200,
            'status': True,
            'data': all_items
        }
    ), status=200, mimetype="application/json")

@app.route('/item/raw', methods=['GET'])
def item_raw():
    data = Data()
    raw = data.get_raw()

    return Response(
        json.dumps({
            'message' : 'raw',
            'error_code' : 200,
            'status': True,
            'data': raw
        }
    ), status=200, mimetype="application/json")

@app.route('/item/name/', methods=['GET'])
def item_name():
    data = Data()
    all_items = data.get_all_items()

    if 'query' not in request.args:
        return Response(
            json.dumps({
                'message' : 'no query parameter',
                'error_code' : 400,
                'status': False,
                'data': ''
            }
        ), status=200, mimetype="application/json")
    else:
        if request.args['query'] in all_items.keys():
            return Response(
                json.dumps({
                    'message' : 'item',
                    'error_code' : 200,
                    'status': True,
                    'data': all_items[request.args['query']]
                }
            ), status=200, mimetype="application/json")
        else:
            return Response(
                json.dumps({
                    'message' : 'item not found',
                    'error_code' : 400,
                    'status': False,
                    'data': ''
                }
            ), status=200, mimetype="application/json")

@app.route('/item/id/', methods=['GET'])
def item_id():
    data = Data()
    all_items = data.get_all_items()

    if 'query' not in request.args:
        return Response(
            json.dumps({
                'message' : 'no query parameter',
                'error_code' : 400,
                'status': False,
                'data': ''
            }
        ), status=200, mimetype="application/json")
    else:
        if request.args['query'] in [str(i['id']) for i in all_items.values()]:
            return Response(
                json.dumps({
                    'message' : 'item',
                    'error_code' : 200,
                    'status': True,
                    'data': data.get_item_by_id(request.args['query'])
                }
            ), status=200, mimetype="application/json")
        else:
            return Response(
                json.dumps({
                    'message' : 'item not found',
                    'error_code' : 400,
                    'status': False,
                    'data': ''
                }
            ), status=200, mimetype="application/json")

@app.route('/item/search/', methods=['GET'])
def item_search():
    data = Data()
    all_items = data.get_all_items()

    if 'query' not in request.args:
        return Response(
            json.dumps({
                'message' : 'no query parameter',
                'error_code' : 400,
                'status': False,
                'data': ''
            }
        ), status=200, mimetype="application/json")
    else:
        data_search = data.search_item_by_name(request.args['query'])
        if data_search != {}:
            return Response(
                json.dumps({
                    'message' : 'item',
                    'error_code' : 200,
                    'status': True,
                    'data': data_search
                }
            ), status=200, mimetype="application/json")
        else:
            return Response(
                json.dumps({
                    'message' : 'item not found',
                    'error_code' : 400,
                    'status': False,
                    'data': ''
                }
            ), status=200, mimetype="application/json")

@app.route('/item/category/', methods=['GET'])
def item_category():
    data = Data()
    load = data.load()

    if 'query' not in request.args:
        return Response(
            json.dumps({
                'message' : 'no query parameter',
                'error_code' : 400,
                'status': False,
                'data': ''
            }
        ), status=200, mimetype="application/json")
    else:
        data_category = data.get_items_by_category(request.args['query'])
        if data_category != {}:
            return Response(
                json.dumps({
                    'message' : 'category',
                    'error_code' : 200,
                    'status': True,
                    'data': data_category
                }
            ), status=200, mimetype="application/json")
        else:
            return Response(
                json.dumps({
                    'message' : 'category not found',
                    'error_code' : 400,
                    'status': False,
                    'data': ''
                }
            ), status=200, mimetype="application/json")

def run():
    app.run(debug=True, host='0.0.0.0', port=int(PORT), threaded=True, use_reloader=False)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(PORT), threaded=True, use_reloader=False)
