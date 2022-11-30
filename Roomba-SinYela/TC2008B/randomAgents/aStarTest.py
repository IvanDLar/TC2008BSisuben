from collections import deque


graph = [[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 1, 0, 0, 0, 0, 0]]

# To move left, right, up and down
delta_x = [-1, 1, 0, 0]
delta_y = [0, 0, 1, -1]

def valid(x, y):
    if x < 0 or x >= len(graph) or y < 0 or y >= len(graph[x]):
        return False
    return (graph[x][y] != 1)

def solve(start, end):
    Q = deque([start])
    dist = {start: 0}
    while len(Q):
        curPoint = Q.popleft()
        curDist = dist[curPoint]
        if curPoint == end:
            return curDist
        for dx, dy in zip(delta_x, delta_y):
            nextPoint = (curPoint[0] + dx, curPoint[1] + dy)
            if not valid(nextPoint[0], nextPoint[1]) or nextPoint in dist.keys():
                continue
            dist[nextPoint] = curDist + 1
            Q.append(nextPoint)

print(solve((0,0), (6,7)))
 