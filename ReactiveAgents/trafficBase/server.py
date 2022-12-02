from flask import Flask, request, jsonify
from agent  import *
from model import RandomModel

# Size of the board:
number_agents = 1
randomModel = None
currentStep = 0

app = Flask("Traffic example")

# @app.route('/', methods=['POST', 'GET'])

@app.route('/init', methods=['POST', 'GET'])
def initModel():
    global currentStep, randomModel, number_agents

    if request.method == 'POST':
        number_agents = int(request.form.get('NAgents'))
        currentStep = 0

        print(request.form)
        print(number_agents)
        randomModel = RandomModel(number_agents)

        return jsonify({"message":"Parameters recieved, model initiated."})

@app.route('/getAgents', methods=['GET'])
def getAgents():
    global randomModel

    if request.method == 'GET':
        # agentPositions = [{"id": str(a.unique_id), "x": x, "y": 0.08, "z":z} for (a, x, z) in randomModel.grid.coord_iter() if isinstance(a, Car)]

        agentPositions = []

        for (a, x, z) in randomModel.grid.coord_iter():
            for agent in a:
             if isinstance(agent, Car):
                agentPositions.append({"id": str(agent.unique_id), "x": x, "y": 0.08, "z":z})



        return jsonify({'positions':agentPositions})


@app.route('/update', methods=['GET'])
def updateModel():
    global currentStep, randomModel
    if request.method == 'GET':
        randomModel.step()
        currentStep += 1
        return jsonify({'message':f'Model updated to step {currentStep}.', 'currentStep':currentStep})

if __name__=='__main__':
    app.run(host="localhost", port=8585, debug=True)