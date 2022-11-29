from mesa import Agent
from collections import deque

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
        endPointDictionary = self.model.endPointDict
        stepsBFS = 0
        #Get the object of an endpoint using its value and get limit
        getEndPointKey = {i for i in endPointDictionary if endPointDictionary[i] == endPointsM[0]}
        print("Endpoint dicitonary: ", next(iter(getEndPointKey)).limit)

        #If there are any boxes around the robot, add them to the list
        boxes = [box_agent for box_agent in self.model.grid.get_neighbors(
            self.pos, moore=True
        ) if isinstance(box_agent, BoxAgent)]

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

                self.model.grid.move_agent(self, next_move)
                self.steps_taken += 1

        elif self.hasBox == True:
            
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
                self.hasBox = False

            elif (len(isNear) > 0 and self.pos == isNear[0].pos):
                #Stop Moving (later drop the box)
                print("Has Box State: ", self.hasBox)

                #Get the endPoint object
                getEndPointKey = {i for i in endPointDictionary if endPointDictionary[i] == isNear[0].pos}

                if((next(iter(getEndPointKey)).limit) > 0):
                    next(iter(getEndPointKey)).limit = next(iter(getEndPointKey)).limit - 1

                #If the endpoint reaches the limit remove it from the possible endpoints
                if(next(iter(getEndPointKey)).limit <= 0):
                    endPointsM.pop(endPointsM.index(isNear[0].pos))
                    for key, value in dict(endPointDictionary).items():
                        if value == isNear[0].pos:
                            del endPointDictionary[key]


            #If the robot is not inside the point nor near
            else:
                typeArray = []
                prev = []
                path = []
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
                    return (not isinstance(typeArray[x][y], BoxAgent))

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
                    print("Prev", prev)
                    print(prev[0][at[0]][at[1]]) 
                    for i in range(len(prev[0])):
                        while at != 0:
                            print("i", at)
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
                    
                # R, C = self.model.grid.width, self.model.grid.height
                # m = self.model.grid
                # sr, sc = self.pos[0], self.pos[1] #Starting row and column values
                # rq, cq = [], [] #Empty Row queue and Column queue

                # #RxC matrix of false values for each of the "casillas"
                # visited = []

                # #Track previous movements
                # prev = []

                # for i in range(C):
                #     rowList = []
                #     prevList = []
                #     for j in range(R):
                #         rowList.append(False)
                #         prevList.append(None)
                #     prev.append(prevList)
                #     visited.append(rowList)

                # dr = [self.directions[0], self.directions[2], 0, 0]
                # dc = [0, 0, self.directions[1], self.directions[3]]

                # def findPath():
                #     #Track numbers of steps taken
                #     moveCount = 0
                #     nodesLeftInLayer = 1
                #     nodesInNextLayer = 0
                #     endPointPos = 0

                #     #Track if we have reached the endpoint during the search
                #     reachedEnd = False

                #     rq.append(sr)
                #     cq.append(sc)

                #     visited[sr][sc] = True

                #     while len(rq) > 0:
                #         r = rq.pop(0)
                #         c = cq.pop(0)
                #         print("Rows: ",[rq])

                #         if len(self.model.grid[r][c]) > 0 and isinstance(self.model.grid[r][c][0], EndPointAgent):
                #             print("Found end point!")
                #             endPointPos = self.model.grid[r][c][0]
                #             reachedEnd = True
                #             break
                #         nodesInNextLayer = exploreNeighbours(r, c)
                #         nodesLeftInLayer = nodesLeftInLayer- 1
                #         if nodesLeftInLayer == 0:
                #             nodesLeftInLayer = nodesInNextLayer
                #             nodesInNextLayer = 0
                #             moveCount = moveCount + 1   
                #     if reachedEnd:
                #         return moveCount
                #     return -1
                
                # def exploreNeighbours(r, c):
                #     nodesInNextLayer = 0
                #     for i in range(4):
                #         rr = r + dr[i]
                #         cc = c + dc[i]
                    
                #         #Skip out of bound locations
                #         if rr < 0 or cc < 0: continue
                #         if rr >= R or cc >= C: continue
                    
                #         #Skip visited locations or blocked cells
                #         if visited[rr][cc]: continue
                #         if len(m[rr][cc]) > 0 and isinstance(m[rr][cc][0], BoxAgent):print("Box found at:  ", [rr], [cc]); continue
                        
                #         rq.append(rr)
                #         cq.append(cc)

                #         visited[rr][cc] = True
                #         prev[rr][cc] = [r,c]
                #         nodesInNextLayer = nodesInNextLayer + 1
                #     print("Nodes left in layer: ", nodesInNextLayer)
                #     return nodesInNextLayer

                # def reconstructPath(prev):
                #     path = []
                #     for i in prev:
                #         for j in i:
                #             if j != None: 
                #                 path.append(j)
                                
                #     #let i = 0, i != null, at = prev[i]
                #     print(path)
                    
                # print("Find path: ", findPath())
                
                # --------------------------------------------------------------------
                #     #Initialice the move to station state and within we will modify the state of the robot
                # #Move towards the point if it gets farther from the roobot
                # #Update X
                # if (self.pos[0] > shortestDistance[0] and freeSpaces[self.directions[3]]):
                #     self.model.grid.move_agent(self, possible_steps[self.directions[3]])
                #     print(f"Se mueve de {self.pos} a {possible_steps[self.directions[3]]}; direction self.directions[3]")
                # elif (self.pos[0] < shortestDistance[0] and freeSpaces[self.directions[1]]):
                #     self.model.grid.move_agent(self, possible_steps[self.directions[1]])
                #     print(f"Se mueve de {self.pos} a {possible_steps[self.directions[1]]}; direction self.directions[1]")
                # #When X is the same but there is an obstacle to the right move up
                # elif (self.pos[0] == shortestDistance[0] and freeSpaces[self.directions[1]] and not freeSpaces[self.directions[2]]):
                #     self.model.grid.move_agent(self, possible_steps[self.directions[1]])
                #     print("When X is the same but there is an obstacle to the right move up")
                # #When X is the same but there is an obstacle to the left move up
                # elif (self.pos[0] == shortestDistance[0] and freeSpaces[self.directions[1]] and not freeSpaces[self.directions[0]]):
                #     self.model.grid.move_agent(self, possible_steps[self.directions[1]])
                #     print("When X is the same but there is an obstacle to the left move up")
                # #When X is the same but there is an obstacle to the left and to the rigth, move up
                # elif (self.pos[0] == shortestDistance[0] and freeSpaces[self.directions[1]] and not freeSpaces[self.directions[0]] and not freeSpaces[self.directions[2]]):
                #     self.model.grid.move_agent(self, possible_steps[self.directions[1]])
                #     print("When X is the same but there is an obstacle to the left and to the rigth, move up")

                # #Update Y
                # if (self.pos[1] > shortestDistance[1] and freeSpaces[self.directions[2]]):
                #     self.model.grid.move_agent(self, possible_steps[self.directions[2]])
                #     print(f"Se mueve de {self.pos} a {possible_steps[self.directions[2]]}; direction self.directions[3]")
                # elif (self.pos[1] < shortestDistance[1] and freeSpaces[self.directions[0]]):
                #     self.model.grid.move_agent(self, possible_steps[self.directions[0]])
                #     print(f"Se mueve de {self.pos} a {possible_steps[self.directions[0]]}; direction self.directions[1]")
                # #When Y is the same but there is an obstacle to the right, move up
                # elif (self.pos[0] == shortestDistance[1] and freeSpaces[self.directions[0]] and not freeSpaces[self.directions[1]]):
                #     self.model.grid.move_agent(self, possible_steps[self.directions[0]])
                #     print("When Y is the same but there is an obstacle to the right, move up")
                # #When Y is the same but there is an obstacle to the left, move up
                # elif (self.pos[0] == shortestDistance[1] and freeSpaces[self.directions[0]] and not freeSpaces[self.directions[3]]):
                #     self.model.grid.move_agent(self, possible_steps[self.directions[0]])
                #     print("When Y is the same but there is an obstacle to the left, move up")
                # #When Y is the same but there is an obstacle to the right and to the left, move down
                # elif (self.pos[0] == shortestDistance[1] and freeSpaces[self.directions[0]] and not freeSpaces[self.directions[1]] and not freeSpaces[self.directions[3]]):
                #     self.model.grid.move_agent(self, possible_steps[self.directions[0]])
                #     print("#When Y is the same but there is an obstacle to the right and to the left and bottom, move up and to the left")
                # elif (self.pos[0] == shortestDistance[1] and freeSpaces[self.directions[2]] and not freeSpaces[self.directions[1]] and not freeSpaces[self.directions[3]] and not freeSpaces[self.directions[2]]):
                #     self.model.grid.move_agent(self, possible_steps[self.directions[0]])
                #     print("#When Y is the same but there is an obstacle to the right and to the left, move up")


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
    Box agent. Just to add boxes to the grid.
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
        self.limit = 5

    def step(self):
        pass