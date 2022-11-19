from mesa import Model, agent
from mesa.time import RandomActivationByType
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from agent import RandomAgent, ObstacleAgent, DirtAgent, EndPointAgent

class RandomModel(Model):
    """ 
    Creates a new model with random agents.
    Args:
        N: Number of agents in the simulation
        height, width: The size of the grid to model
    """
    def __init__(self, N, O, T, P, width, height):
        self.num_agents = N
        self.num_obstacles = O
        self.num_trash = T
        self.num_points = P
        self.grid = MultiGrid(width,height,torus = False) 
        self.schedule = RandomActivationByType(self)
        self.running = True 
        self.max_steps = 100
        self.endPointsM = []

        self.grid_size = (width) * (height)

        self.datacollector = DataCollector( 
        agent_reporters={"Steps": lambda a: a.steps_taken if isinstance(a, RandomAgent) else 0},
        model_reporters={
            "Dirt": lambda x: x.schedule.get_type_count(DirtAgent),
           "Clean": lambda y: y.grid_size - y.schedule.get_type_count(DirtAgent)
        })
        
        # Creates the border of the grid height x width. The loop repeats while y and x are in range
        border = [(x,y) for y in range(height) for x in range(width) if y in [0, height - 1] or x in [0, width - 1]]

        # Place an obstacle in every position in the border
        for pos in border:
            obs = ObstacleAgent(pos, self)
            # self.schedule.add(obs)
            self.grid.place_agent(obs, pos)

        # Add the agent to the 1,1 cell
        for i in range(self.num_agents):
            b = RandomAgent(i+1000, self) 
            self.schedule.add(b)

            pos_gen = lambda w, h: (self.random.randrange(w), self.random.randrange(h))
            pos = pos_gen(self.grid.width, self.grid.height)
            while (not self.grid.is_cell_empty(pos)):
                pos = pos_gen(self.grid.width, self.grid.height)
            self.grid.place_agent(a, pos)

        # Add the agent to the 1,1 cell
        for i in range(self.num_agents):
            b = RandomAgent(i+1000, self) 
            self.schedule.add(b)
            
            pos_gen = lambda w, h: (self.random.randrange(w), self.random.randrange(h))
            pos = pos_gen(self.grid.width, self.grid.height)
            while (not self.grid.is_cell_empty(pos)):
                pos = pos_gen(self.grid.width, self.grid.height)
            self.grid.place_agent(b, pos)
        
        # Add the dirt to a random empty grid cell
        for i in range(self.num_trash):
            c = DirtAgent(i+5000, self) 
            self.schedule.add(c)

            pos_gen = lambda w, h: (self.random.randrange(w), self.random.randrange(h))
            pos = pos_gen(self.grid.width, self.grid.height)
            while (not self.grid.is_cell_empty(pos)):
                pos = pos_gen(self.grid.width, self.grid.height)
            self.grid.place_agent(c, pos)
            
        
        # Manually add the checkpoints to the grid 
        for i in range(self.num_points):
            d = EndPointAgent(i+4000, self) 
            self.schedule.add(d)

            pos_gen = lambda w, h: (self.random.randrange(w), self.random.randrange(h))
            pos = pos_gen(self.grid.width, self.grid.height)
            while (not self.grid.is_cell_empty(pos)):
                pos = pos_gen(self.grid.width, self.grid.height)
            self.endPointsM.append(pos)
            self.grid.place_agent(d, pos)
        
        self.datacollector.collect(self)
        
        
    def step(self):
        '''Advance the model by one step.'''
        self.schedule.step()
        self.datacollector.collect(self)

        if (self.schedule.get_type_count(DirtAgent) != 0):
            self.running = True

        else:
            self.running = False
