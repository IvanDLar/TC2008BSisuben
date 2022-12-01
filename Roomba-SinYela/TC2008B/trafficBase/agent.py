from mesa import Agent
from collections import deque
import random

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
        super().__init__(unique_id, model)
         #Top Rigth Down Left
        self.pos = pos
        self.steps_taken = 0
        self.front = (self.pos[0]-1,self.pos[1]) 
        self.randPoint = random.choice(self.model.endPointsM)
        self.path = self.BFS()
        self.stepsBFS = 0
        
        
    def BFS(self):
        
        """ BFS BEARBONES"""
        typeArray = []
        prev = []
        path = []
        rPoint = self.randPoint

        print("Height", self.model.grid.height)
        print("Width", self.model.grid.width)

        for i in range(self.model.grid.height):
            rowList = []
            prevList = []
            for j in range(self.model.grid.width):
                if(len(self.model.grid[i, j]) > 0):
                    rowList.append(self.model.grid[i, j][0])
                    prevList.append(0)
                else:
                    rowList.append(self.model.grid[i, j])
                    prevList.append(0)
            prev.append(prevList)
            typeArray.append(rowList)
            # To move left, right, up and down, and diagonally
        delta_x = [-1, 1, 0, 0, 1, -1, -1, 1] 
        delta_y = [0, 0, 1, -1, -1, 1, -1, 1]

        def valid(x, y):
            if x < 0 or x >= len(typeArray) or y < 0 or y >= len(typeArray[x]):
                return False
            return (not isinstance(typeArray[x][y], Obstacle))

        def solve(start, end):
            Q = deque([start])
            print("Q: ", Q)
            dist = {start: 0}
            while len(Q):
                curPoint = Q.popleft() #Move to one of the neighbors, remove visited
                curDist = dist[curPoint] #Gets the nums of levels it took to reach this node
                if curPoint == end: #If we have found a mathc to the endpoint
                    path.append(curPoint)
                    return prev, curDist
                
                for dx, dy in zip(delta_x, delta_y):
                    nextPoint = (0,0)
                    if isinstance(typeArray[curPoint[0]][curPoint[1]], Road):
                        dir = (typeArray[curPoint[0]][curPoint[1]]).direction
                        print("Current Point!:" ,(typeArray[curPoint[0]][curPoint[1]]).direction)
                        if dir == "Up" and dy == 1:
                            nextPoint = (curPoint[0] + dx, curPoint[1] + dy)
                            # print("Object type: ", typeArray[nextPoint[0]][nextPoint[1]])
                            # print("----------------TOP-----------------")
                        elif dir == "Down" and dy == -1:
                            nextPoint = (curPoint[0] + dx, curPoint[1] + dy)
                            # print("Object type: ", typeArray[nextPoint[0]][nextPoint[1]])
                            # print("----------------BOTTOM-----------------")
                        elif dir == "Right" and dx == 1:
                            nextPoint = (curPoint[0] + dx, curPoint[1] + dy)
                            # print("Object type: ", typeArray[nextPoint[0]][nextPoint[1]])
                            # print("----------------RIGHT-----------------")
                        elif dir == "Left" and dx == -1:
                            nextPoint = (curPoint[0] + dx, curPoint[1] + dy)
                            # print("Object type: ", typeArray[nextPoint[0]][nextPoint[1]])
                            # print("----------------LEFT-----------------")
                    elif isinstance(typeArray[curPoint[0]][curPoint[1]], Destination):
                        nextPoint = (curPoint[0] + dx, curPoint[1] + dy)
                        break
                    


                    if not valid(nextPoint[0], nextPoint[1]) or nextPoint in dist.keys(): #Node within boundaries, and not of type obstacle and not visited
                        continue
                    dist[nextPoint] = curDist + 1
                    
                    Q.append(nextPoint) #Add the next unvisited node
                    prev[nextPoint[0]][nextPoint[1]] = curPoint #Keep track of the parent node of the next node
                    path.append(curPoint)

        def reconstructPath(s, e, prev):
            #Rebuild the path and invert it
            path = []
            at = e
            # print("Prev", prev) Print preview of the rebuilded path
            #print(prev[0][at[0]][at[1]]) 
            for i in range(len(prev[0])):
                while at != 0:
                    #print("i", at) where it is moving
                    at = prev[0][at[0]][at[1]]
                    path.append(at)
                        
            path.reverse()

            path.pop(0) #Remove garbage data (if i remove the code, the BFS will break)
            path.append(e) #Add the goal at the end of the array

            if path[0] == s:
                return path
            else:
                return []
                    # path.append((curPoint[0], curPoint[1])
                    # prev[nextPoint[0]][nextPoint[1]] = curPoint
                    
        return reconstructPath(self.pos, rPoint, solve(self.pos, rPoint))

    def randomPoint(self):
        """ Get End Points """
        endPointsM = self.model.endPointsM
        # endPointDictionary = self.model.endPointDict
        return(random.choice(endPointsM))

    def newFront(self, road):
        for agentR in road:
            if isinstance(agentR, Road):
                if agentR.direction == "Right":
                    self.front = (self.pos[0]+1,self.pos[1]) 
                elif agentR.direction == "Left":
                    self.front = (self.pos[0]-1,self.pos[1]) 
                elif agentR.direction == "Down":
                    self.front = (self.pos[0],self.pos[1]-1)     
                elif agentR.direction == "Up":
                    self.front = (self.pos[0],self.pos[1]+1) 
    
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
        # stepsBFS = 0

        """ Get End Points """
        endPointsM = self.model.endPointsM
        endPointDictionary = self.model.endPointDict
        listOfNeighboursPoints = self.model.grid.get_neighbors(self.pos, moore = True, include_center = True, radius = 1)
        getEndPointKey = {i for i in endPointDictionary if endPointDictionary[i] == endPointsM[0]}
        isNear = []
        # print("---------------Get End Points-----------------")
        # print(self.randomPoint())
        #Manhattan Distance
        

        
        possible_steps = self.model.grid.get_neighborhood(
                self.pos,
                moore=True, # Boolean for whether to use Moore neighborhood (including diagonals) or Von Neumann (only up/down/left/right).
            )
        possible_end_points = self.model.grid.get_neighborhood(
            self.pos,
            moore=True, # Boolean for whether to use Moore neighborhood (including diagonals) or Von Neumann (only up/down/left/right).
            include_center=True)
        
        """Movimineto Ejec"""
        finalPath = self.path
        road = self.model.grid.get_cell_list_contents(self.pos)
        self.newFront(road)
        trafLight = self.model.grid.get_cell_list_contents(self.front)
        
        # for agentL in trafLight:
        #     print(trafLight)
        #     if isinstance(agentL, Traffic_Light):
        #         if not agentL.state:
        #             return
        #     elif isinstance(agentL, Car):
        #         return
        print("Final Path", finalPath)
        
        #If the traffic light is red, dont move else move
        if self.pos != self.randPoint:
            for agentL in trafLight:
                print(trafLight)
                if isinstance(agentL, Traffic_Light):
                    if not agentL.state:
                        return
                elif isinstance(agentL, Car):
                    return
            if(isinstance(finalPath[self.stepsBFS], Car)):
                self.path = self.BFS()
            else:
                print("Moving to: ",finalPath[self.stepsBFS], " Steps: ", self.stepsBFS)
                self.stepsBFS += 1
                print("Steps: ", self.stepsBFS)
                self.model.grid.move_agent(self, finalPath[self.stepsBFS])
                #self.model.grid.move_agent(self, self.roadCheck(road))
        else:
            self.model.grid.move_agent(self, possible_end_points[possible_end_points.index(self.randPoint)])
            newpos = random.choice(self.model.roadList)
            if(isinstance(newpos, Car)):
                newpos = random.choice(self.model.roadList)
            self.model.grid.move_agent(self, newpos)
            self.steps_taken = 0
            self.front = (self.pos[0]-1,self.pos[1]) 
            self.randPoint = random.choice(self.model.endPointsM)
            self.path = self.BFS()
            self.stepsBFS = 0
            
        """ BFS BEARBONES """


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
