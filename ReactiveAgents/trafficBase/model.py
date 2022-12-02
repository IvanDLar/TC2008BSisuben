from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from agent import *
import json

class RandomModel(Model):
    """ 
    Creates a new model with random agents.
    Args:
        N: Number of agents in the simulation
    """
    def __init__(self, N): 
        self.num_agents = 10 
        dataDictionary = json.load(open("mapDictionary.json"))
        self.endPointsM = []
        self.endPointAgents = []
        self.endPointDict = {}
        self.traffic_lights = []
        self.roadList = []
        self.maxAgents = 1000
        self.currentAgents = 0

        with open('2022_base.txt') as baseFile:
            lines = baseFile.readlines()
            self.width = len(lines[0])
            self.height = len(lines)
            self.grid = MultiGrid(self.width, self.height, torus = False) 
            self.schedule = RandomActivation(self)
            
        
            for r, row in enumerate(lines):
                for c, col in enumerate(row):
                    if col in ["v", "^", ">", "<"]:
                        agent = Road(f"r_{r*self.width+c}", self, dataDictionary[col])
                        self.roadList.append((c, self.height - r - 1)) #Make a list of positions of Road
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                    elif col in ["S", "s"]:
                        agent = Road(f"r_{r*self.width+c}", self, dataDictionary[col])
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        agent = Traffic_Light(f"tl_{r*self.width+c}", self, False if col == "S" else True, int(dataDictionary[col]))
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.schedule.add(agent)
                        self.traffic_lights.append(agent)
                    elif col == "#":
                        agent = Obstacle(f"ob_{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                    elif col == "D":
                        agent = Destination(f"d_{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.endPointsM.append((c, self.height - r - 1))
                        self.endPointsM.append((c, self.height - r - 1))
                        self.endPointAgents.append(agent)
                        #Relate the position of a point to the eal specific object in the model
                        self.endPointDict = dict(zip(self.endPointAgents, self.endPointsM))

        def cellList(posx, posy):
            road = self.grid.get_cell_list_contents((posx,posy))
            return(road)
        
        def checkDirection(rode, dir1, dir2, posx,posy, typeAgent, nextcheck): 
            road2 = cellList(posx, posy)
            for agentR in road:
                if agentR.direction == dir1 or agentR.direction == dir2:
                    for agentRP in road2:
                        if isinstance(agentRP, typeAgent):
                            agentRP.direction = agentR.direction
                else:
                    for agentR2 in nextcheck:
                        if agentR2.direction == dir1 or agentR2.direction == dir2:
                            for agentRP in road2:
                                if isinstance(agentRP, typeAgent):
                                    agentRP.direction = agentR.direction



        for i in self.traffic_lights:
            if i.state:
                road = cellList(i.pos[0]+1, i.pos[1]) #Right
                road2 = cellList(i.pos[0]-1, i.pos[1]) #Left
                checkDirection(road, "Left", "Right", i.pos[0],i.pos[1], Road, road2)
            else:
                road = cellList(i.pos[0],i.pos[1]+1) #Up
                road2 = cellList(i.pos[0],i.pos[1]-1) #Down
                checkDirection(road, "Up", "Down", i.pos[0],i.pos[1], Road, road2)
                                        
       
        if self.currentAgents < self.maxAgents:
            for i in range(self.num_agents):
                pos = self.random.choice(self.roadList)
                a = Car(i, self, pos) 
                self.schedule.add(a)
                self.currentAgents += 1
                
                self.grid.place_agent(a, pos)

        self.running = True

    def step(self):
        '''Advance the model by one step.'''
        if self.schedule.steps % 8 == 0:
            if self.currentAgents < self.maxAgents:
                pos = self.random.choice(self.roadList)
                print("Number of Cars: ",self.currentAgents)
                a = Car(self.currentAgents, self, pos) 
                self.schedule.add(a)
                self.currentAgents += 1
                
                self.grid.place_agent(a, pos)
                
        if self.schedule.steps % 10 == 0:
            for agent in self.traffic_lights:
                agent.state = not agent.state
        self.schedule.step()