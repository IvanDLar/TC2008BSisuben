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
        self.num_agents = N
        dataDictionary = json.load(open("mapDictionary.json"))
        
        self.traffic_lights = []

        with open('2022_base.txt') as baseFile:
            lines = baseFile.readlines()
            self.width = len(lines[0])-1
            self.height = len(lines)
            self.grid = MultiGrid(self.width, self.height, torus = False) 
            self.schedule = RandomActivation(self)

            for r, row in enumerate(lines):
                for c, col in enumerate(row):
                    if col in ["v", "^", ">", "<"]:
                        agent = Road(f"r_{r*self.width+c}", self, dataDictionary[col])
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

       
        for i in self.traffic_lights:
            if i.state:
                road = self.grid.get_cell_list_contents((i.pos[0]+1,i.pos[1]))
                for agentR in road:
                    if agentR.direction == "Left" or agentR.direction == "Right":
                        roadpos = self.grid.get_cell_list_contents((i.pos[0],i.pos[1]))
                        for agentRP in roadpos:
                            if isinstance(agentRP, Road):
                                agentRP.direction = agentR.direction
                    else:
                        road = self.grid.get_cell_list_contents((i.pos[0]-1,i.pos[1]))
                        for agentR in road:
                            if agentR.direction == "Left" or agentR.direction == "Right":
                                roadpos = self.grid.get_cell_list_contents((i.pos[0],i.pos[1]))
                                for agentRP in roadpos:
                                    if isinstance(agentRP, Road):
                                        agentRP.direction = agentR.direction
            else:
                road = self.grid.get_cell_list_contents((i.pos[0],i.pos[1]+1))
                for agentR in road:
                    if agentR.direction == "Up" or agentR.direction == "Down":
                        roadpos = self.grid.get_cell_list_contents((i.pos[0],i.pos[1]))
                        for agentRP in roadpos:
                            if isinstance(agentRP, Road):
                                agentRP.direction = agentR.direction
                    else:
                        road = self.grid.get_cell_list_contents((i.pos[0],i.pos[1]-1))
                        for agentR in road:
                            if agentR.direction == "Up" or agentR.direction == "Down":
                                roadpos = self.grid.get_cell_list_contents((i.pos[0],i.pos[1]))
                                for agentRP in roadpos:
                                    if isinstance(agentRP, Road):
                                        agentRP.direction = agentR.direction
                                        
                
        for i in range(self.num_agents):
            pos = (12,18)
            a = Car(i+1000, self, pos) 
            self.schedule.add(a)

            self.grid.place_agent(a, pos)

        self.running = True

    def step(self):
        '''Advance the model by one step.'''
        if self.schedule.steps % 10 == 0:
            for agent in self.traffic_lights:
                agent.state = not agent.state
        self.schedule.step()