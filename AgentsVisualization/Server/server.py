# TC2008B. Sistemas Multiagentes y Gráficas Computacionales
# Python flask server to interact with Unity. Based on the code provided by Sergio Ruiz.
# Octavio Navarro. October 2021

from flask import Flask, request, jsonify
from RandomAgents import *

# Size of the board:
number_agents = 1
number_boxes = 15;
number_end_points = 2;
width = 28
height = 28
randomModel = None
currentStep = 0

app = Flask("Traffic example")

# @app.route('/', methods=['POST', 'GET'])

@app.route('/init', methods=['POST', 'GET'])
def initModel():
    global currentStep, randomModel, number_agents, number_boxes, number_end_points, width, height

    if request.method == 'POST':
        number_agents = int(request.form.get('NAgents'))
        number_boxes = int(request.form.get('NBoxes'))
        number_end_points = int(request.form.get('NEndPoints'))
        width = int(request.form.get('width'))
        height = int(request.form.get('height'))
        currentStep = 0

        # print(request.form)
        # print(number_agents, number_boxes, number_end_points, width, height)
        randomModel = RandomModel(number_agents, number_boxes, number_end_points, width, height)

        return jsonify({"message":"Parameters recieved, model initiated."})

@app.route('/getAgents', methods=['GET'])
def getAgents():
    global randomModel

    if request.method == 'GET':
        agentPositions = [{"id": str(a.unique_id), "x": x, "y":0.5, "z":z} for (a, x, z) in randomModel.grid.coord_iter() if isinstance(a, RandomAgent)]

        return jsonify({'positions':agentPositions})

@app.route('/getObstacles', methods=['GET'])
def getObstacles():
    global randomModel

    if request.method == 'GET':
        carPositions = [{"id": str(a.unique_id), "x": x, "y":0.5, "z":z} for (a, x, z) in randomModel.grid.coord_iter() if isinstance(a, ObstacleAgent)]

        return jsonify({'positions':carPositions})

@app.route('/getBoxes', methods=['GET'])
def getBoxes():
    global randomModel

    if request.method == 'GET':
        boxPositions = [{"id": str(a.unique_id), "x": x, "y":0.5, "z":z} for (a, x, z) in randomModel.grid.coord_iter() if isinstance(a, BoxAgent)]

        return jsonify({'positions':boxPositions})

@app.route('/getEndPoints', methods=['GET'])
def getEndPoints():
    global randomModel

    if request.method == 'GET':
        endPointPositions = [{"id": str(a.unique_id), "x": x, "y":0.5, "z":z} for (a, x, z) in randomModel.grid.coord_iter() if isinstance(a, EndPointAgent)]

        return jsonify({'positions':endPointPositions})

@app.route('/update', methods=['GET'])
def updateModel():
    global currentStep, randomModel
    if request.method == 'GET':
        randomModel.step()
        currentStep += 1
        return jsonify({'message':f'Model updated to step {currentStep}.', 'currentStep':currentStep})

if __name__=='__main__':
    app.run(host="localhost", port=8585, debug=True)