import flask
from flask import request, jsonify,Flask,make_response, abort
from flask_restful import Resource, Api
import json



def saveDeviceList():
    json.dump(deviceList, open(filename, 'w'))

def loadDeviceList():
    global deviceList
    deviceList = json.load(open(filename, 'r'))

filename = "config\devices.json"
deviceList = ""
loadDeviceList()


app = Flask(__name__)
api = Api(app)
app.config["DEBUG"] = True

#API HANDLING

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/api/led/', methods=['GET'])
def led_all():
    json.load("config/ledStripState.json")
    return jsonify()



@app.route('/api/devices/', methods=['GET'])
def devices_all():
    return jsonify(deviceList)

@app.route('/api/devices/<int:device_id>', methods=['GET'])
def get_device(device_id):
    device = [device for device in deviceList if device.get('id') == device_id]
    if len(device) == 0:
        abort(404)
    return jsonify({'device': device[0]})

@app.route('/api/devices/', methods=['POST'])
def add_device():
    if not request.json or not 'name' in request.json or not 'mac' in request.json:
        print('error',request.form['data'])
        abort(400)
    id = max([num.get('id') for num in deviceList]) + 1
    name = request.json.get('title')
    mac = request.json.get('mac')
    device = {'name': name,'mac':mac,'id':id}
    deviceList.append(device)
    saveDeviceList()
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
    saveDeviceList()
    return jsonify({'result': True})

Flask.run(app)