import numpy as np
from EightPuzzleGame_State import State

'''
This class implement one of the Uninformed Search algorithm
You may choose to implement the Breadth-first or Depth-first or Iterative-Deepening search algorithm

'''


class UninformedSearchSolver:
    current = State()
    goal = State()
    openlist = []
    closed = []
    depth = 0

    def __init__(self, current, goal):
        self.current = current
        self.goal = goal
        self.openlist.append(current)


    def check_inclusive(self, s):
        """
        * The check_inclusive function is designed to check if the expanded state is or is not in open list or closed list
        * This is done to prevent looping
        * @param s
        * @return
        """
        in_open = 0
        in_closed = 0
        ret = [-1, -1]

        #TODO your code start here




        #TODO your code end here



    def state_walk(self):
        """
        * The following state_walk function is designed to move the blank tile --> perform actions
         * There are four types of possible actions/walks of for the blank tile, i.e.,
         *  ↑ ↓ ← → (move up, move down, move left, move right)
         * Note that in this framework the blank tile is represent by '0'
        """

        # First you need to remove the current node from the open array and move it to the closed array
        self.closed.append(self.current)
        self.openlist.remove(self.current)
        walk_state = self.current.tile_seq
        row = 0
        col = 0

        # Loop to find the location of the blank space
        for i in range(len(walk_state)):
            for j in range(len(walk_state[i])):
                if walk_state[i, j] == 0:
                    row = i
                    col = j
                    break

        self.depth += 1


        ''' The following program is used to do the state space actions
            The 4 conditions for moving the tiles all use similar logic, they only differ in the location of the 
            tile that needs to be swapped. That being the case, I will only comment the first subroutine
        '''
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


        ### ↓(move down) action ###




        ### ←(move left) action ###



        ### →(move right) action ###


        # Set the next current state

        #TODO your code end here


    # # You can change the following code to print all the states on the search path
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
            print('Visited State number ', path+1)
            pathstate_str = np.array2string(self.current.tile_seq, precision=2, separator=' ')
            print(pathstate_str[1:-1])
            path += 1
        print("\n It took ", path, " iterations to reach to the goal state")
        print("The length of the path is: ", self.current.depth)

