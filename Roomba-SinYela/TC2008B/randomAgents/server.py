from model import RandomModel, ObstacleAgent, EndPointAgent ,DirtAgent
from mesa.visualization.modules import CanvasGrid, BarChartModule, PieChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

def agent_portrayal(agent):
    if agent is None: return
    
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 2,
                 "Color": "red",
                 "r": 0.5}

    portrayal2 = {"Shape": "square",
                 "Filled": "true",
                 "Layer": 2,
                 "Color": "red",
                 "r": 0.5}                 

    if (isinstance(agent, ObstacleAgent)):
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.3

    if (isinstance(agent, DirtAgent)):
        portrayal["Color"] = "green"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.2

    if (isinstance(agent, EndPointAgent)):
        portrayal["Color"] = "purple"
        portrayal["Layer"] = 0
        portrayal["r"] = 1

    return portrayal

model_params = {"N": UserSettableParameter("slider", "Number of roombas", 1, 1, 20, 1)
                ,"T": UserSettableParameter("slider", "Number of Dirt Tiles", 10, 1, 25, 1)
                , "O":UserSettableParameter("slider", "Number of Obstacle ", 7, 1, 20, 1)
                , "P":UserSettableParameter("slider", "Number of End Points ", 2, 1, 20, 1)
                , "width":10
                , "height":10}

grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)

bar_chart = BarChartModule(
    [{"Label":"Steps", "Color":"#AA0000"}], 
    scope="agent", sorting="ascending", sort_by="Steps")
#Create pie chart of dirt vs clean tiles
pie_chart = PieChartModule(
    [{"Label":"Dirt", "Color":"green"},{"Label":"Clean", "Color":"red"}])
    
server = ModularServer(RandomModel, [grid, pie_chart, bar_chart], "Random Agents", model_params)
                       
server.port = 8521 # The default
server.launch()