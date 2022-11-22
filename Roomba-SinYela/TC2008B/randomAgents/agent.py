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
        #Top Rigth Down Left
        self.directions = [4, 6, 3, 1]
        self.steps_taken = 0
        self.visited = []
        self.hasBox = False

    #def nearestPoint(myPos, endPoints):

    def move(self):
        """ 
        Determines if the agent can move in the direction that was chosen
        """
        # Detect the types of neighbours the agent has
        listOfNeighbours = self.model.grid.get_neighbors(self.pos, moore = True, include_center = True, radius = 1)
        listOfNeighboursPoints = self.model.grid.get_neighbors(self.pos, moore = False, include_center = True, radius = 1)
        isNear = []
        endPointsM = self.model.endPointsM
        
        #If there are any boxes around the robot, add them to the list
        boxes = [box_agent for box_agent in self.model.grid.get_neighbors(
            self.pos, moore=True
        ) if isinstance(box_agent, BoxAgent)]
        
        if self.hasBox == False:
            if len(boxes) > 0:
                # If we have trash agents in the trash list we move to the trash's position
                next_move = boxes[-1].pos
                self.model.grid.move_agent(self, next_move)
                # We use remove_agent method to remove the trash agent
                self.model.grid.remove_agent(boxes[-1])
                #Agent leave the box in the endpoint
                print("Has Box State: ", self.hasBox)
                self.hasBox = True
                
            else:
                possible_steps = self.model.grid.get_neighborhood(
                    self.pos,
                    # Boolean for whether to use Moore neighborhood (including diagonals) or Von Neumann (only up/down/left/right).
                    moore=False,
                    include_center=True)

                # Checks which grid cells are empty
                freeSpaces = list(
                    map(self.model.grid.is_cell_empty, possible_steps))

                next_moves = [p for p, f in zip(
                    possible_steps, freeSpaces) if f == True]
                next_move = self.random.choice(next_moves)

                empty = not self.visited
                nextMove = next_move not in self.visited
                allVisited = all(cell in self.visited for cell in next_moves)

                # escapes if roomba is traped
                if allVisited:
                    next_move = self.random.choice(next_moves)
                    self.model.grid.move_agent(self, next_move)
                    self.steps_taken += 1
                    # if there is none cell visited it moves wherever
                if empty:
                    self.model.grid.move_agent(self, next_move)
                    self.steps_taken += 1
                    self.visited.append(next_move)
                    # if the selected cell is not visited it moves
                if nextMove:
                    self.model.grid.move_agent(self, next_move)
                    self.steps_taken += 1
                    self.visited.append(next_move)  
                    
        elif self.hasBox == True:  
            #Manhattan Distance
            def getShortestDistance(endPoints, myX, myY):
                #Aux array
                distanceArray = []
                for endPoint in endPoints:
                    endPointX = endPoint[0]
                    endPointY = endPoint[1]
                    print("X:", endPointX)
                    print("Y:", endPointY)

                    distance = abs(myX - endPointX) + abs(myY - endPointY)
                    distanceArray.insert(0, distance)

                closetsPoint = endPoints[distanceArray.index(max(distanceArray))]
                print("End Points: ", endPoints)
                print("Distance Array", distanceArray)
                
                
                print("Closest index: ", distanceArray.index(max(distanceArray)))
                print("Closest Point: ", closetsPoint)
                return closetsPoint


            shortestDistance = getShortestDistance(endPointsM, self.pos[0], self.pos[1]);    

            possible_steps = self.model.grid.get_neighborhood(
                self.pos,
                moore=True, # Boolean for whether to use Moore neighborhood (including diagonals) or Von Neumann (only up/down/left/right).
                ) 
            possible_end_points = self.model.grid.get_neighborhood(
                self.pos,
                moore=False, # Boolean for whether to use Moore neighborhood (including diagonals) or Von Neumann (only up/down/left/right).
                include_center=True) 
            
            # Checks which grid cells are empty
            freeSpaces = list(map(self.model.grid.is_cell_empty, possible_steps))

            for i in listOfNeighboursPoints:
                if isinstance(i, EndPointAgent):
                    isNear.append(i)

            #If there is an element in the list move towards the endpoint
            if(len(isNear) > 0 and self.pos != isNear[0].pos):
                print("-----------------")
                print("I AM GOING TO THE POINT")
                print("-----------------")
                self.model.grid.move_agent(self, possible_end_points[possible_end_points.index(isNear[0].pos)])
            
            elif (len(isNear) > 0 and self.pos == isNear[0].pos):
                #Stop Moving (later drop the box)
                print("Has Box State: ", self.hasBox)
                self.hasBox = False
            
            #If the robot is not inside the point nor near
            else:
                    #Initialice the move to station state and within we will modify the state of the robot
                #Move towards the point if it gets farther from the roobot
                #Update X
                if (self.pos[0] > shortestDistance[0] and freeSpaces[self.directions[3]]):
                    self.model.grid.move_agent(self, possible_steps[self.directions[3]])
                    print(f"Se mueve de {self.pos} a {possible_steps[self.directions[3]]}; direction self.directions[3]")          
                elif (self.pos[0] < shortestDistance[0] and freeSpaces[self.directions[1]]):
                    self.model.grid.move_agent(self, possible_steps[self.directions[1]])
                    print(f"Se mueve de {self.pos} a {possible_steps[self.directions[1]]}; direction self.directions[1]")           
                #When X is the same but there is an obstacle to the right move up
                elif (self.pos[0] == shortestDistance[0] and freeSpaces[self.directions[1]] and not freeSpaces[self.directions[2]]):
                    self.model.grid.move_agent(self, possible_steps[self.directions[1]])
                    print("When X is the same but there is an obstacle to the right move up")
                #When X is the same but there is an obstacle to the left move up
                elif (self.pos[0] == shortestDistance[0] and freeSpaces[self.directions[1]] and not freeSpaces[self.directions[0]]):
                    self.model.grid.move_agent(self, possible_steps[self.directions[1]])
                    print("When X is the same but there is an obstacle to the left move up")
                #When X is the same but there is an obstacle to the left and to the rigth, move up
                elif (self.pos[0] == shortestDistance[0] and freeSpaces[self.directions[1]] and not freeSpaces[self.directions[0]] and not freeSpaces[self.directions[2]]):
                    self.model.grid.move_agent(self, possible_steps[self.directions[1]])
                    print("When X is the same but there is an obstacle to the left and to the rigth, move up")      

                #Update Y
                if (self.pos[1] > shortestDistance[1] and freeSpaces[self.directions[2]]):
                    self.model.grid.move_agent(self, possible_steps[self.directions[2]])
                    print(f"Se mueve de {self.pos} a {possible_steps[self.directions[2]]}; direction self.directions[3]")          
                elif (self.pos[1] < shortestDistance[1] and freeSpaces[self.directions[0]]):
                    self.model.grid.move_agent(self, possible_steps[self.directions[0]])
                    print(f"Se mueve de {self.pos} a {possible_steps[self.directions[0]]}; direction self.directions[1]")          
                #When Y is the same but there is an obstacle to the right, move up
                elif (self.pos[0] == shortestDistance[1] and freeSpaces[self.directions[0]] and not freeSpaces[self.directions[1]]):
                    self.model.grid.move_agent(self, possible_steps[self.directions[0]])
                    print("When Y is the same but there is an obstacle to the right, move up")
                #When Y is the same but there is an obstacle to the left, move up
                elif (self.pos[0] == shortestDistance[1] and freeSpaces[self.directions[0]] and not freeSpaces[self.directions[3]]):
                    self.model.grid.move_agent(self, possible_steps[self.directions[0]])
                    print("When Y is the same but there is an obstacle to the left, move up")
                #When Y is the same but there is an obstacle to the right and to the left, move down
                elif (self.pos[0] == shortestDistance[1] and freeSpaces[self.directions[0]] and not freeSpaces[self.directions[1]] and not freeSpaces[self.directions[3]]):
                    self.model.grid.move_agent(self, possible_steps[self.directions[0]]) 
                    print("#When Y is the same but there is an obstacle to the right and to the left and bottom, move up and to the left")
                elif (self.pos[0] == shortestDistance[1] and freeSpaces[self.directions[2]] and not freeSpaces[self.directions[1]] and not freeSpaces[self.directions[3]] and not freeSpaces[self.directions[2]]):
                    self.model.grid.move_agent(self, possible_steps[self.directions[0]]) 
                    print("#When Y is the same but there is an obstacle to the right and to the left, move up")

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
                #freeSpaces = list(map(self.model.grid.is_cell_empty, possible_steps))

                # next_moves = [p for p,f in zip(possible_steps, freeSpaces) if f == True]
                # next_move = self.random.choice(next_moves)

                # # Now move:
                # if self.random.random() < 0.1:
                #     self.model.grid.move_agent(self, next_move)
                #     self.steps_taken+=1

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

class BoxAgent(Agent):
    """
    Box agent. Just to add obstacles to the grid.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.condition = "Box"

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