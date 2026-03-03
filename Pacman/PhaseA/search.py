# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.
    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.
    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    """
    The exploration sequence looks very "deep":
    Pacman goes as far as he can on a path before turning back.
    The visual representation (dark->light red) shows that the depths are explored first.
    Pacman does not visit all explored squares. In the visualization, "explored" expanded nodes, not nodes along the final path.
    DFS explores many dead ends that it ultimately does not use.
    
    The length with 130 nodes is not the least cost solution:
    DFS:
    -ignores cost
    -blindly moves to the first deep path it finds
    -doesn't compare paths with each other
    =>that's why it finds a much larger solution than the minimum (the optimal solution is around 70 moves in mediumMaze).
    
    """
  
 #DFS goes as deep as it can into a path before trying other directions using Stack (LIFO)
    from util import Stack
    stack = Stack() #create stack with LIFO
    start = problem.getStartState() #first state
    print( "Start:", start)
    
    # every element(state, actions)
    stack.push((start, [])) #add first state to stack with null actions
    visited = set() #save the visited states

    while not stack.isEmpty(): #while stack has something
        state, actionlist = stack.pop() #pop the last insert
        if problem.isGoalState(state): #if goal is found return list of actions
            return actionlist
        if state not in visited: 
            #continue # if state is visited ignore
            visited.add(state) # mark as visited
            for successor, action, _cost in problem.getSuccessors(state): 
                if successor not in visited:
                    stack.push((successor, actionlist + [action]))
    print( "Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print( "Start's successors:", problem.getSuccessors(problem.getStartState()))

    return []  # if no solution

    

    #util.raiseNotDefined()
    
def breadthFirstSearch(problem):

    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    """
    The BFS can find the least cost solution for this problem.
    In Pacman, all moves have a cost of 1->BFS finds the shortest path in number of steps, hence the minimum possible cost.
    
    (if BFS doesn't give the optimal solution, then there's something wrong with marking visited nodes or it uses the wrong structure.
    """
 #BFS goes "layer by layer"-first it examines all the neighbors of start, then their neighbors, and so on, using Queue (FIFO)

    from util import Queue
    queue = Queue() #create Queue
    start = problem.getStartState() #first state
    queue.push((start, [])) #add first state to queue with null actions
    visited = set([start])  # instant mark as visited (to never go there again)
    print( "Start:", start)

    while not queue.isEmpty(): #as long as Queue has something
        state, actionlist = queue.pop() #pop the first insert
       # print(state)
        #print( "Start's successors:", problem.getSuccessors(state))

        if problem.isGoalState(state): #if goal is found return list of actions
            return actionlist
        for successor, action, _cost in problem.getSuccessors(state):
            if successor not in visited:
                visited.add(successor) # mark as visited
                queue.push((successor, actionlist + [action]))
    return []
   # util.raiseNotDefined()

def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"
 #UCS always chooses the path with the least total cost until now, ustin PriorityQueue
    from util import PriorityQueue
    pqueue = PriorityQueue() #create the PriorityQueue
    start = problem.getStartState() #first state
    pqueue.push( (start, [], 0), 0 ) #add first state into PriorityQueue with null actions and cost, priority=cost
    mincost = 0 #dict()  # state -> best_cost_seen until now, (min cost)

    while not pqueue.isEmpty(): # as long as PriorityQueue has something
        state, actionlist, cost = pqueue.pop() #pop the first insert
        if problem.isGoalState(state): #if goal is found return list of actions
            return actionlist
        if state in mincost and mincost[state] <= cost: # if cost!=min ignore
            continue
        mincost[state] = cost #mark as visited
        for successor, action, stepCost in problem.getSuccessors(state):
            newCost = cost + stepCost
            # push στον pqueue ανεξάρτητα — το visited_cost θα φιλτράρει τα παλαιότερα
            pqueue.push((successor, actionlist + [action], newCost), newCost) #push into PriorityQueue without dependence-visited_cost will filter the old ones
    return []
    # util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    """
    
    UCS:                                           A*:
    -null heuristic                                -Manhattan heuristic
    -the priority is only g(n), (aggregate cost)   -the priority is f(n)=g(n)+h(n)
    -finds the optimal solution slightly slower    -finds the optimal solution slightly faster
    -expands more nodes                            -expands less nodes
    A consistent and acceptable heuristic directs the search towards the goal ->less pointless exploration.
    (That's why UCS expands more nodes than the A*).
    
    So A* is a little faster, but not by much-because the maze is relatively narrow and the heuristic(Manhattan) is not perfect.
    (The only difference between A*'s and UCS's code is the heuristic they use). 
    
    openMaze is a very large open space:
    DFS:                                        BFS:                                                 UCS:                                                      A*:                                                                                           
    -collapses                                  -guaranteed to find shortest path, but               -like BFS, but slower                                     -the Manhattan heuristic gives good guidance
    -explores huge depth without direction      -explodes in memory cost, because in an open space   (because priority queue operations > queue operations).   -goes almost straight to the goal
    -very large exploration tree->inefficient   each BFS level has a huge number of nodes.                                                                     -finds the solution much faster than BFS/UCS
    
    """
    
 #A* uses UCS+heuristic, chooses state with the least f(n)=g(n)+h(n), g(n):cost until now, h(n): estimate of how far away it is from the end, usint PriorityQueue
    from util import PriorityQueue
    pqueue = PriorityQueue() #create PriorityQueue
    start = problem.getStartState() #first state
    start_h = heuristic(start, problem) #heuristic state
    pqueue.push((start, [], 0), start_h) #push into PriorityQueue
    mincost = dict()  # state -> best g cost

    while not pqueue.isEmpty(): # as long as PriorityQueue has something
        state, actionlist, g = pqueue.pop() #pop the first insert
        if problem.isGoalState(state): #if goal is found return list of actions
            return actionlist
        if state in mincost and mincost[state] <= g: # if cost!=min ignore
            continue
        mincost[state] = g #mark as visited
        for successor, action, stepCost in problem.getSuccessors(state):
            new_g = g + stepCost
            f = new_g + heuristic(successor, problem)
            pqueue.push((successor, actionlist + [action], new_g), f)
    return []

    #util.raiseNotDefined()

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
