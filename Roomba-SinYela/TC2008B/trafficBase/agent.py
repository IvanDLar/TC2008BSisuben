from mesa import Agent

class Car(Agent):
    """
    Agent that moves randomly.
    Attributes:
        unique_id: Agent's ID 
        direction: Randomly chosen direction chosen from one of eight directions
    """
    def __init__(self, unique_id, model, pos):
        """
        Creates a new random agent.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
        """
         #Top Rigth Down Left
        self.directions = [4, 6, 3, 1]
        self.steps_taken = 0
        super().__init__(unique_id, model)

    def move(self):
        """ 
        Determines if the agent can move in the direction that was chosen
        """        
        # possible_steps = self.model.grid.get_neighborhood(
        #     self.pos,
        #     moore=True, # Boolean for whether to use Moore neighborhood (including diagonals) or Von Neumann (only up/down/left/right).
        #     include_center=False) 
        
         # Checks which grid cells are empty
        
        # freeSpaces = list(map(self.model.grid.is_cell_empty, possible_steps))
        # road = [road_agent for road_agent in self.model.grid.get_neighbors(
        #     self.pos, moore=True, include_center=True
        # )]
        road = self.model.grid.get_cell_list_contents(self.pos)
        for agentR in road:
            if isinstance(agentR, Road):
                if agentR.direction == "Right":
                    newpos = (self.pos[0]+1,self.pos[1])
                    self.model.grid.move_agent(self, newpos)
                elif agentR.direction == "Left":
                    newpos = (self.pos[0]-1,self.pos[1])
                    self.model.grid.move_agent(self, newpos)
                elif agentR.direction == "Down":
                    newpos = (self.pos[0],self.pos[1]-1)
                    self.model.grid.move_agent(self, newpos)
                elif agentR.direction == "Up":
                    newpos = (self.pos[0],self.pos[1]+1)
                    self.model.grid.move_agent(self, newpos)
        # print(thin)

        # for agentR in road:
        #     if agentR.pos == self.pos:
        #         print(agentR.direction)
        # print(road)
        
        # next_moves = [p for p,f in zip(possible_steps, freeSpaces) if f == True]
       
        # next_move = self.random.choice(next_moves)

        # if self.random.random() < 0.1:
        #     self.model.grid.move_agent(self, next_move)
        #     self.steps_taken+=1

        # self.model.grid.move_to_empty(self)

    def step(self):
        """ 
        Determines the new direction it will take, and then moves
        """
        self.move()

class Traffic_Light(Agent):
    """
    Traffic light. Where the traffic lights are in the grid.
    """
    def __init__(self, unique_id, model, state = False, timeToChange = 10):
        super().__init__(unique_id, model)
        """
        Creates a new Traffic light.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
            state: Whether the traffic light is green or red
            timeToChange: After how many step should the traffic light change color 
        """
        self.state = state
        self.timeToChange = timeToChange

    def step(self):
        """ 
        To change the state (green or red) of the traffic light in case you consider the time to change of each traffic light.
        """
        # if self.model.schedule.steps % self.timeToChange == 0:
        #     self.state = not self.state
        pass

class Destination(Agent):
    """
    Destination agent. Where each car should go.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass

class Obstacle(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass

class Road(Agent):
    """
    Road agent. Determines where the cars can move, and in which direction.
    """
    def __init__(self, unique_id, model, direction= "Left"):
        """
        Creates a new road.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
            direction: Direction where the cars can move
        """
        super().__init__(unique_id, model)
        self.direction = direction

    def step(self):
        pass
