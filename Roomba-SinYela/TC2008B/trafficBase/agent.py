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
        self.pos = pos
        self.directions = [4, 6, 3, 1]
        self.steps_taken = 0
        self.front = (self.pos[0]-1,self.pos[1]) 
        super().__init__(unique_id, model)
        
    def roadCheck(self,road):
        for agentR in road:
            if isinstance(agentR, Road):
                if agentR.direction == "Right":
                    newpos = (self.pos[0]+1,self.pos[1])
                    self.front = (self.pos[0]+2,self.pos[1]) 
                    
                elif agentR.direction == "Left":
                    newpos = (self.pos[0]-1,self.pos[1])
                    self.front = (self.pos[0]-2,self.pos[1]) 
                    
                elif agentR.direction == "Down":
                    newpos = (self.pos[0],self.pos[1]-1)
                    self.front = (self.pos[0],self.pos[1]-2) 
                    
                elif agentR.direction == "Up":
                    newpos = (self.pos[0],self.pos[1]+1)
                    self.front = (self.pos[0],self.pos[1]+2) 
                    
        return newpos
    def cambiarCarril(self,road):
        for agentR in road:
            if agentR.direction == "Right":
                self.pos = (self.pos[0]+1,self.pos[1]-1)
                
            elif agentR.direction == "Left":
                newpos = (self.pos[0]-1,self.pos[1])
                
            elif agentR.direction == "Down":
                newpos = (self.pos[0],self.pos[1]-1)
                
            elif agentR.direction == "Up":
                newpos = (self.pos[0],self.pos[1]+1)
                    
        return newpos


    def move(self):
        """ 
        Determines if the agent can move in the direction that was chosen
        """ 

        road = self.model.grid.get_cell_list_contents(self.pos)
        trafLight = self.model.grid.get_cell_list_contents(self.front)
    
        for agentL in trafLight:
            if isinstance(agentL, Traffic_Light):
                if not agentL.state:
                    return
            elif isinstance(agentL, Car):
                return
                    
    
        
        self.model.grid.move_agent(self, self.roadCheck(road))
        
                    
                    

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
