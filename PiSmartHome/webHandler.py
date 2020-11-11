import flask
from flask import request, jsonify,Flask,make_response, abort
from flask_restful import Resource, Api
import pickle

filename = "config/devices.json"
deviceList = pickle.load(open(filename, 'r'))

app = Flask(__name__)
api = Api(app)
app.config["DEBUG"] = True

#API HANDLING

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/api/led/', methods=['GET'])
def led_all():
    pickle.load("config/ledStripState.json")
    return jsonify()



@app.route('/api/devices/', methods=['GET'])
def led_all():
    pickle.load("config/devices.json")
    return jsonify()

@app.route('/api/devices/<int:device_id>', methods=['GET'])
def get_device(device_id):
    device = [device for device in deviceList if device['id'] == device_id]
    if len(device) == 0:
        abort(404)
    return jsonify({'device': device[0]})

@app.route('/api/devices/', methods=['POST'])
def add_device():
    if not request.json or not 'title' in request.json:
        abort(400)
    # #task device = {
    #     'id': tasks[-1]['id'] + 1,
    #     'title': request.json['title'],
    #     'description': request.json.get('description', ""),
    #     'done': False
    # }
    deviceList.append(device)
    return jsonify({'device': device}), 201

@app.route('/api/devices/<int:device_id>', methods=['PUT'])
def update_task(device_id):
    device = [device for device in deviceList if device['id'] == device_id]
    if len(device) == 0:
        abort(404)
    if not request.json:
        abort(400)
    # if 'address' in request.json and type(request.json['address']) != UNICODE:
    #     abort(400)
    # if 'description' in request.json and type(request.json['description']) is not unicode:
    #     abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    device[0]['title'] = request.json.get('title', device[0]['title'])
    device[0]['description'] = request.json.get('description', device[0]['description'])
    device[0]['done'] = request.json.get('done', device[0]['done'])
    return jsonify({'device': device[0]})

@app.route('/api/devices/<int:device_id>', methods=['DELETE'])
def delete_task(device_id):
    device = [device for device in deviceList if device['id'] == device_id]
    if len(device) == 0:
        abort(404)
    device.remove(device[0])
    return jsonify({'result': True})