import sys,math
import random

import priorityqueue

 
##~ class Node:
##~ 
##~     def __init__(self, h, gval, hval, parent=None):
##~ 
##~         self.h = h   #map coordenates
##~         self.gval = gval
##~         self.hval = hval
##~         self.parent = parent
##~ 
##~     def f(self):
##~         return self.gval + self.hval
##~ 
##~     
##~     def __lt__(self,y):
##~         return (self.gval+self.hval) < (y.gval+y.hval)
##~ 
##~     def __eq__(self,y):
##~         return (self.h == y.h) and (self.gval == y.gval) and (self.hval == y.hval)
##~ 
##~     def __str__(self):
##~         return str(self.h)+","+str(self.gval)+","+str(self.hval)


def max(x,y):
    if x>y:
        return x
    else:
        return y



def dist(map, start, a, b, goal):

    x0,y0 = a
    x1,y1 = b
    x2, y2 = start

    dist = max(math.fabs(x0-x1),math.fabs(y0-y1))

    dx1 = x0 - goal[0]
    dy1 = y0 - goal[1]
    dx2 = start[0] - goal[0]
    dy2 = start[1] - goal[1]
    
    cross = dx1*dy2-dx2*dy1
    
    if cross < 0:
        cross = -cross;

    return float(dist + cross*0.001)
    





def kost(map, obj, a, b):

    # like the cost os my map is actualy alwais 1, or a big number whem it's impossible to
    # cross the way
    if map.isPositionDirty(b,obj):
        return 1000000

    return 1
    

def Neighbor(h, d,speed):
    x0, y0 = h

    directions = {
        0 : ( x0+speed , y0  ), #N
        1 : ( x0+speed , y0+speed), #NE
        2 : ( x0       , y0+speed), #E
        3 : ( x0-speed , y0+speed), #SE
        4 : ( x0-speed , y0  ), #S
        5 : ( x0-speed , y0-speed), #SW
        6 : ( x0       , y0-speed), #W
        7 : ( x0+speed , y0-speed), #NW
    }
    
    return directions[d]



   

def Astar(map, obj, start, goal, speed=1):


    pqueue = priorityqueue.priorityQueue()  # a very cool PQ baseated in a Heap

    seen = {}

    g_costs = {start : 1.0}

    parents = {start : start}

    heur = lambda x,y: kost(map, obj, x,y)
    d_calc = lambda x,y: dist(map,start, x,y, goal)

    

    start_cost = heur(start, goal)

    pqueue[start] = start_cost

    seen[start] = start_cost

    for next_node in pqueue:

        next_cost = pqueue[next_node]

        g_costs[next_node] = g_costs[parents[next_node]] + d_calc(next_node, parents[next_node])

        if next_node == goal:

            solution = getPathToGoal(start, goal, parents)

            return solution

        children = possible_positions(map, next_node, speed)
        
        for child in children.values():

            if g_costs.has_key(child): continue

            f = g_costs[next_node] + d_calc(next_node, child) + heur(child, goal)

            if (not seen.has_key(child) or seen[child] > f):

                seen[child] = f

                pqueue[child] = f

                parents[child] = next_node


    solution = getPathToGoal(start, goal, parents)

    return  solution  
    
    
def getPathToGoal(start, goal, parents):

    """Given the hash of parental links, follow back and return the

    chain of ancestors."""

    try:

        results = []

        while (goal != start):

            results.append(goal)

            goal = parents[goal]

        # end while (goal != start)

        results.append(start)

        results.reverse()

        return results

    except KeyError: return []    

def possible_positions(map, pos, speed):

    x0, y0 = pos
    xo = float(x0)
    yo = float(y0)


    directions = {
        0 : ( x0+speed , y0  ), #N
        1 : ( x0+speed , y0+speed), #NE
        2 : ( x0       , y0+speed), #E
        3 : ( x0-speed , y0+speed), #SE
        4 : ( x0-speed , y0  ), #S
        5 : ( x0-speed , y0-speed), #SW
        6 : ( x0       , y0-speed), #W
        7 : ( x0+speed , y0-speed), #NW
    }    
    

    prev_points = {}

    sx, sy = map.getSize()
    for k in directions:
        x, y = directions[k]
        if  x<sx and y<sy and x>=0 and y>=0:
            prev_points[k] = directions[k]

                    
    return prev_points
