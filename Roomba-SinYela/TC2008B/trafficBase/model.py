from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from agent import *
import json

import random



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
                                        

           
        for i in range(self.num_agents):
            xrand = random.randrange(0,2)
            yrand = random.randrange(0,24)
            pos = (xrand, yrand)
            # while (not self.grid.is_cell_empty(pos)):
            #     xrand = random.randrange(0,24)
            #     yrand = random.randrange(0,24)
            #     pos = (xrand, yrand)
            a = Car(i+1000, self, pos)
            self.schedule.add(a)
            self.grid.place_agent(a, pos)


        # Add the dirt to a random empty grid cell
        # for i in range(self.num_trash):
        #     c = BoxAgent(i+5000,  
        #     selfself).schedule.add(c)

        #     pos_gen = lambda w, h: (self.random.randrange(w), self.random.randrange(h))
        #     pos = pos_gen(self.grid.width, self.grid.height)
        #     while (not self.grid.is_cell_empty(pos)):
        #         pos = pos_gen(self.grid.width, self.grid.height)
            # self.grid.place_agent(c, pos)

        self.running = True

    def step(self):
        '''Advance the model by one step.'''
        if self.schedule.steps % 10 == 0:
            for agent in self.traffic_lights:
                agent.state = not agent.state
        self.schedule.step()