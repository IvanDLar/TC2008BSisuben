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
         #Top Rigth Down Left
        self.pos = pos
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
        stepsBFS = 0

        """ Get End Points """
        endPointsM = self.model.endPointsM
        endPointDictionary = self.model.endPointDict
        listOfNeighboursPoints = self.model.grid.get_neighbors(self.pos, moore = True, include_center = True, radius = 1)
        getEndPointKey = {i for i in endPointDictionary if endPointDictionary[i] == endPointsM[0]}
        isNear = []

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
            moore=True, # Boolean for whether to use Moore neighborhood (including diagonals) or Von Neumann (only up/down/left/right).
            include_center=True)

        # Checks which grid cells are empty
        freeSpaces = list(map(self.model.grid.is_cell_empty, possible_steps))
                    
        """ BFS BEARBONES"""
        typeArray = []
        prev = []
        path = []
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
            # To move left, right, up and down
        delta_x = [-1, 1, 0, 0] 
        delta_y = [0, 0, 1, -1]

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
                    nextPoint = (curPoint[0] + dx, curPoint[1] + dy)
                    if not valid(nextPoint[0], nextPoint[1]) or nextPoint in dist.keys(): #Node within boundaries, and not of type obstacle and not visited
                        continue
                    dist[nextPoint] = curDist + 1
                    
                    Q.append(nextPoint) #Add the next unvisited node
                    prev[nextPoint[0]][nextPoint[1]] = curPoint #Keep track of the parent node of the next node
                    path.append(curPoint)

                    # path.append((curPoint[0], curPoint[1])
                    # prev[nextPoint[0]][nextPoint[1]] = curPoint
            
                
        # print("Self pos: ", self.pos)
        # print("Shortest Distance: ", shortestDistance)
        def reconstructPath(s, e, prev):
            #Rebuild the path and invert it
            path = []
            at = e
            # print("Prev", prev) Print preview of the rebuilded path
            print(prev[0][at[0]][at[1]]) 
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
        #print("Solved: ", reconstructPath(self.pos, shortestDistance, solve(self.pos, shortestDistance)))
        #print("Solved: ", solve(self.pos, shortestDistance))  
        
        pathArray = reconstructPath(self.pos, shortestDistance, solve(self.pos, shortestDistance))

        
        
        if self.pos != shortestDistance:
            print("Moving to: ",pathArray[stepsBFS], " Steps: ", stepsBFS)
            stepsBFS += 1
            self.model.grid.move_agent(self, pathArray[stepsBFS])

        """ BFS BEARBONES """

        road = self.model.grid.get_cell_list_contents(self.pos)
        trafLight = self.model.grid.get_cell_list_contents(self.front)
    
        for agentL in trafLight:
            if isinstance(agentL, Traffic_Light):
                if not agentL.state:
                    return
            elif isinstance(agentL, Car):
                return
                    
        
        for i in listOfNeighboursPoints:
            if isinstance(i, Destination):
                print("Position: ", possible_end_points[possible_end_points.index(i.pos)])
                print("-----------------")
                print("I AM GOING TO THE POINT")
                print("-----------------")
                self.model.grid.move_agent(self, possible_end_points[possible_end_points.index(i.pos)])
                self.model.grid.move_agent(self, (22, 0))
                
               
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
