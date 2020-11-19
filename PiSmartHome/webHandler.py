from flask import Flask, request, jsonify
from flask.wrappers import Response
from flask_restful import Resource, Api, abort, reqparse
import json
import os

app = Flask(__name__)
api = Api(app)

class device(Resource):
        
    def get(self, device_id):
        return {device_id: getDevice(device_id)}        

    def put(self, device_id):
        parser.add_argument('name', required=True, help="Name cannot be blank!")
        parser.add_argument('mac', required=True, help="Mac Address cannot be blank!")

        args = parser.parse_args()
        device = getDevice(device_id)
        args.found = False
        args.date = args.ip = ""
        updateDeviceByArgs(device,args)
        return jsonify(getDevice(device_id))

    # def patch(self, device_id):
    #     parser.add_argument('name')
    #     parser.add_argument('mac')
    #     args = parser.parse_args()
    #     if(all(arg is None for arg in args.values())):
    #         abort(400,message="No args found")
    #     device = getDevice(device_id)
    #     updateDeviceByArgs(device, args)

    #     return {device_id: getDevice(device_id)}
    
    def delete(self,device_id):
        deleteDevice(device_id)
        return '', 204
    

api.add_resource(device, '/api/devices/<int:device_id>')


class allDevices(Resource):
    def post(self):
        parser.add_argument('name', required=True, help="Name cannot be blank!")
        parser.add_argument('mac', required=True, help="Mac Address cannot be blank!")

        args = parser.parse_args()
        if(not devices):
            id = 0;
        else:
            id = max([num.get('id') for num in devices]) + 1
        args.id = id
        args.found = False
        args.date = args.ip = ""

        addDevice(args)
        return jsonify(getDevice(id))

    def get(self):
        loadDeviceList()
        return jsonify(devices)

api.add_resource(allDevices, '/api/devices/')
def saveDeviceList():
        json.dump(devices,open(filename, 'w'), ensure_ascii=False, indent=4)

def loadDeviceList():
    global devices

    f = open(filename, 'a')
    f.close()
    filesize = os.path.getsize(filename)
    print('fs',filesize)
    if (not filesize):
        return

    devices = json.load(open(filename, 'r'))
    id = 0;
    for d in devices:
        if not d.get('id'):
            d.setdefault('id', id)
            id+=1
        else:
            id=d.get('id')+1

def addDevice(device):
    devices.append(device)
    saveDeviceList()
    
def getDevice(id):
    for device in devices:
        if device.get('id') == id:
            return device
    abort(404,message="Device not found")

def updateDeviceByArgs(device, args):
    for key,value in args.items():
            if value:
                print("setting",key,"to",value)
                device[key] = value
    saveDeviceList()

def deleteDevice(id):
    devices.remove(getDevice(id))
    saveDeviceList()




if __name__ == '__main__':
    parser = reqparse.RequestParser()
    filename = "config\devices.json"
    devices = []
    loadDeviceList()
    app.run(debug=True)