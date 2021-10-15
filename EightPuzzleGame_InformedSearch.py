import numpy as np
from EightPuzzleGame_State import State
'''
This class implement the Best-First-Search (BFS) algorithm along with the Heuristic search strategies

In this algorithm, an Open list is used to store the unexplored states and 
a Closed list is used to store the visited state. Open list is a priority queue (First-In-First-Out). 
The priority is insured through sorting the Open list each time after new states are generated 
and added into the list. The heuristics are used to decide which node should be visited next.

In this informed search, reducing the state space search complexity is the main criterion. 
We define heuristic evaluations to reduce the states that need to be checked every iteration. 
Evaluation function is used to express the quality of informedness of a heuristic algorithm. 

'''

class InformedSearchSolver:
    current = State()
    goal = State()
    openlist = []
    closed = []
    depth = 0

    def __init__(self, current, goal):
        self.current = current
        self.goal = goal
        self.openlist.append(current)

    def sortFun(self, e):
        return e.weight

    def check_inclusive(self, s):
        """
         * The check_inclusive function is designed to check if the expanded state is in open list or closed list
         * This is done to prevent looping. (You can use a similar code from uninformedsearch program)
         * @param s
         * @return
        """
        in_open = False
        in_closed = False
        ret = [-1, -1]

        #TODO your code start here
        for i in self.openlist:
            if i.equals(s):
                in_open = True
                break
        for i in self.closed:
            if i.equals(s):
                in_closed = True
                break

        return {"open": in_open, "closed": in_closed}

        # TODO your code end here


    def state_walk(self):
        """
        * The following state_walk function is designed to move the blank tile --> perform actions
        * There are four types of possible actions/walks of for the blank tile, i.e.,
        *  ↑ ↓ ← → (move up, move down, move left, move right)
        * Note that in this framework the blank tile is represent by '0'
        """
        self.closed.append(self.current)
        self.openlist.remove(self.current)

        # move to the next heuristic state
        walk_state = self.current.tile_seq
        row = 0
        col = 0

        for i in range(len(walk_state)):
            for j in range(len(walk_state[i])):
                if walk_state[i, j] == 0:
                    row = i
                    col = j
                    break

        self.depth += 1

        children = []

        ''' The following program is used to do the state space actions
         The 4 conditions for moving the tiles all use similar logic, they only differ in the location of the 
         tile that needs to be swapped. That being the case, I will only comment the first subroutine'''
        # TODO your code start here
        ### ↑(move up) action ###
        #(row - 1) is checked to prevent out of bounds errors, the tile is swapped with the one above it
        if (row - 1) >= 0:
            """
             *get the 2d array of current 
             *define a temp 2d array and loop over current.tile_seq
             *pass the value from current.tile_seq to temp array
             *↑ is correspond to (row, col) and (row-1, col)
             *exchange these two tiles of temp
             *define a new temp state via temp array
             *call check_inclusive(temp state)
             *do the next steps according to flag
             *if flag = 1 //not in open and closed
             *begin
             *assign the child a heuristic value via heuristic_test(temp state);
             *add the child to open
             *end;
             *if flag = 2 //in the open list
             *if the child was reached by a shorter path
             *then give the state on open the shorter path
             *if flag = 3 //in the closed list
             *if the child was reached by a shorter path then
             *begin
             *remove the state from closed;
             *add the child to open
             *end;
            """
            temp = self.current.tile_seq.copy()
            #Swap the blank space with the tile above it
            temp[row][col] = temp[row-1][col]
            temp[row-1][col] = 0
            tempState = State(temp, self.depth)
            children.append(tempState)

        ### ↓(move down) action ###
        #row + 1 is checked to make sure it will stay in bounds
        if (row + 1 < len(walk_state)):
            temp = self.current.tile_seq.copy()
            #Swap the blank space with the tile above it
            temp[row][col] = temp[row+1][col]
            temp[row+1][col] = 0
            tempState = State(temp, self.depth)
            children.append(tempState)

        ### ←(move left) action ###
        if (col - 1 >= 0):
            temp = self.current.tile_seq.copy()
            #Swap the blank space with the tile above it
            temp[row][col] = temp[row][col-1]
            temp[row][col-1] = 0
            tempState = State(temp, self.depth)
            children.append(tempState)


        ### →(move right) action ###
        if (col + 1 < len(walk_state)):
            temp = self.current.tile_seq.copy()
            #Swap the blank space with the tile above it
            temp[row][col] = temp[row][col+1]
            temp[row][col+1] = 0
            tempState = State(temp, self.depth)
            children.append(tempState)

        for child in children:
            flags = self.check_inclusive(child)
            child.weight = self.heuristic_test(child)
            if not (flags['open'] or flags['closed']):
                self.openlist.append(child)
            elif flags['open']:
                existingState = None
                existingStateIndex = -1
                for i in self.openlist:
                    if i.equals(child):
                        existingState = i
                        existingStateIndex = self.openlist.index(i)
                        break
                if child.depth < existingState.depth:
                    self.openlist[existingStateIndex] = child
            elif flags['closed']:
                existingState = None
                existingStateIndex = -1
                for i in self.closed:
                    if i.equals(child):
                        existingState = i
                        existingStateIndex = self.closed.index(i)
                        break
                if child.depth < existingState.depth:
                    self.closed.remove(existingState)
                    self.openlist.append(child)



        # sort the open list first by h(n) then g(n)

        newList = []
        for val in self.openlist:
            index = 0
          #  print(index)
            while index < len(newList) and newList[index].weight < val.weight:
                index += 1
            newList.insert(index, val)
        self.openlist = newList

        # Set the next current state

        self.current = self.openlist[0]

        #TODO your code end here




    def heuristic_test(self, current):
        """
        * Solve the game using heuristic search strategies

        * There are three types of heuristic rules:
        * (1) Tiles out of place
        * (2) Sum of distances out of place
        * (3) 2 x the number of direct tile reversals

        * evaluation function
        * f(n) = g(n) + h(n)
        * g(n) = depth of path length to start state
        * h(n) = (1) + (2) + (3)
        """

        curr_seq = current.tile_seq
        goal_seq = self.goal.tile_seq

        # (1) Tiles out of place
        h1 = 0
        #TODO your code start here
        """
         *loop over the curr_seq
         *check the every entry in curr_seq with goal_seq
        """

        dimens = len(curr_seq)

        for row in range(0, dimens):
            for col in range(0, dimens):
                if curr_seq[row][col] != goal_seq[row][col]:
                    h1 += 1
        #TODO your code end here
        

        # (2) Sum of distances out of place
        h2 = 0
        #TODO your code start here
        """
         *loop over the goal_seq and curr_seq in nested way
         *locate the entry which has the same value in 
         *curr_seq and goal_seq then calculate the offset
         *through the absolute value of two differences
         *of curr_row-goal_row and curr_col-goal_col
         *absoulte value can be calculated by abs(...)
        """
        for currRow in range(0, dimens):
            for currCol in range(0, dimens):
                val = curr_seq[currRow][currCol]
                for goalRow in range(0, dimens):
                    for goalCol in range(0, dimens):
                        if goal_seq[goalRow][goalCol] == val:
                            h2 += abs(currRow-goalRow) + abs(currCol-goalCol)
                            break
        #TODO your code end here
        
        
        # (3) 2 x the number of direct tile reversals
        h3 = 0
        #TODO* your code start here
        """
         *loop over the curr_seq
         *use a Γ(gamma)shap slider to walk throught curr_seq and goal_seq
         *rule out the entry with value 0
         *set the boundry restriction
         *don't forget to time 2 at last
         *for example 
         *goal_seq  1 2 3   curr_seq  2 1 3 the Γ shape starts 
         *       4 5 6          4 5 6
         *       7 8 0          7 8 0
         *with 1 2 in goal_seq and 2 1 in curr_seq thus the 
         *    4             4
         *reversal is 1 2 and 2 1
        """



        # update the heuristic value for current state

        return h1 + h2 + h3

        #TODO your code end here




    # You can change the following code to print all the states on the search path
    def run(self):
        # output the goal state
        target = self.goal.tile_seq
        print("\nReached goal state: ")
        target_str = np.array2string(target, precision=2, separator=' ')
        print(target_str[1:-1])

        print("\n The visited states are: ")
        path = 0
        while not self.current.equals(self.goal):
            self.state_walk()
            path += 1
            print('Visited State number', path)
            pathstate_str = np.array2string(self.current.tile_seq, precision=2, separator=' ')
            print(pathstate_str[1:-1])

        print("\nIt took", path, "iterations to reach to the goal state")
        print("The length of the path is:", self.current.depth)

