from mesa import Agent

class RandomAgent(Agent):
    """
    Agent that moves randomly.
    Attributes:
        unique_id: Agent's ID 
        direction: Randomly chosen direction chosen from one of eight directions
    """
    def __init__(self, unique_id, model):
        self.condition = "Clean"
        """
        Creates a new random agent.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
        """
        super().__init__(unique_id, model)
        #Top Down Right Left
        self.directions = [4, 6, 3, 1]
        self.steps_taken = 0

    def move(self):
        """ 
        Determines if the agent can move in the direction that was chosen
        """
        # Detect the types of neighbours the agent has
        listOfNeighbours = self.model.grid.get_neighbors(self.pos, moore = False, include_center = True, radius = 1)

        dirt = []
        endPoints = self.model.endPointsM[1]
        # print(endPoints)
       
        # Check if there is a dirt tile in any of the 8 tiles that surrounds the agent, if there is add to auxiliary list
        # for i in listOfNeighbours:
        #     if isinstance(i, EndPointAgent):
        #         endPoints.append(i)

        #     if isinstance(i, DirtAgent):
        #         dirt.append(i)
        
        # if(len(endPoints) > 0):
        #     next_move = endPoints[0].pos
        #     self.model.grid.move_agent(self, next_move)
        #     #Initialice the move to station state and within we will modify the state of the robot
        #     if(self.pos == endPoints[0].pos):
        #         self.model.grid.remove_agent(self)

        # elif(len(dirt) <= 0):
        #     possible_steps = self.model.grid.get_neighborhood(
        #         self.pos,
        #         moore=False, # Boolean for whether to use Moore neighborhood (including diagonals) or Von Neumann (only up/down/left/right).
        #         ) 
            
        # #If there is an element in the list move to the coordinates and remove the first dirt agent in the list, if ther is another moove to the next dir neighbour
        # if(len(dirt) > 0):
        #     next_move = dirt[0].pos
        #     self.model.grid.move_agent(self, next_move)
        #     #Initialice the move to station state and within we will modify the state of the robot

        # elif(len(dirt) <= 0):
        #     possible_steps = self.model.grid.get_neighborhood(
        #         self.pos,
        #         moore=False, # Boolean for whether to use Moore neighborhood (including diagonals) or Von Neumann (only up/down/left/right).
        #         include_center=True) 
            
            # Checks which grid cells are empty

        

        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True, # Boolean for whether to use Moore neighborhood (including diagonals) or Von Neumann (only up/down/left/right).
            ) 

        freeSpaces = list(map(self.model.grid.is_cell_empty, possible_steps))

        next_moves = [p for p,f in zip(possible_steps, freeSpaces) if f == True]
        next_move = self.random.choice(next_moves)

        #Check if x of agent is bigger or smaller than the endpoints x
        if(self.pos[0] > endPoints[0]):
            print("x > end")
            self.directions[2]
        elif(self.pos[0] < endPoints[0]):
            self.directions[0]
        #Check if z of agent is bigger or smaller than the endpoints z
        if(self.pos[1] > endPoints[1]):
            print("z > end")
            self.directions[1]
        elif(self.pos[1] < endPoints[1]):
            self.directions[3]
        

            # Now move:
        if self.random.random() < 0.1:
            self.model.grid.move_agent(self, next_move)
            self.steps_taken+=1

        # If the cell is empty, moves the agent to that cell; otherwise, it stays at the same position
        # # if freeSpaces[self.direction]:
        # #     self.model.grid.move_agent(self, possible_steps[self.direction])
        # #     print(f"Se mueve de {self.pos} a {possible_steps[self.direction]}; direction {self.direction}")
        # # else:
        # #     print(f"No se puede mover de {self.pos} en esa direccion.")

    def step(self):
        """ 
        Determines the new direction it will take, and then moves
        """
        # self.direction = self.random.randint(0,8)
        # print(f"Agente: {self.unique_id} movimiento {self.direction}")
        self.move()


class ObstacleAgent(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.condition = "Clean"
    def step(self):
        pass  

class DirtAgent(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.condition = "Dirt"

    def step(self):
        pass  
    
class EndPointAgent(Agent):
    """
    Endpoint agent. Just to add a few endpoints to the grid.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass  