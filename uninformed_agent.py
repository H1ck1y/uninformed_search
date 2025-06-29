

# Include your imports here, if any are used.
import  itertools
import  random
import copy
from collections import deque
import math

############################################################
# Section 1: N-Queens
############################################################

def num_placements_all(n):
    if n <= 0:
        return None
    result = math.factorial(n * n)/ (math.factorial(n) * math.factorial(n * n - n))
    return result

def num_placements_one_per_row(n):
    #option for each line
    if n <= 0:
        return None
    result = n ** n
    return result




def n_queens_valid(board):
        n = len(board)
        for i in range(n):
            for j in range(i + 1, n):
                if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                    return False
        return True

def n_queens_solutions(n):
    if n < 1:
        return  None
    stack = [[]]  # initial state
    while stack:
        current_board = stack.pop()
        if  n_queens_valid(current_board):
            if len(current_board) == n:
                yield current_board
            # generate newstates based on current state,push them to the stack
            for i in range(n -1, -1, -1):
                    new_board = current_board + [i]
                    if n_queens_valid(new_board):
                        stack.append(new_board)
    return None



############################################################
# Section 2: Lights Out
############################################################



class LightsOutPuzzle(object):

    def __init__(self, board):
        self.board = board
        self.rows = len(board)
        self.cols = len(board[0])


    def get_board(self):
        return  self.board

    def get_tupleboard(self):
        tuple_board = []
        for row in self.board:
            tuple_row = []
            for val in row:
                tuple_row.append(val)
            tuple_board.append(tuple(tuple_row))
        return tuple(tuple_board)

    def perform_move(self, row, col):
        self.board[row][col] = not self.board[row][col]
        if (row - 1) >= 0:
            self.board[row-1][col] = not self.board[row-1][col]
        if (col -1) >=  0:
            self.board[row][col - 1] = not self.board[row][col - 1]
        if  (row + 1) < self.rows:
            self.board[row+1][col] = not self.board[row + 1][col]
        if  (col + 1) < self.cols:
            self.board[row][col + 1] = not self.board[row][col + 1]


    def scramble(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if random.random() < 0.5:
                    self.perform_move(i, j)


    def is_solved(self):
        for row in self.board:
            for ele in row:
                if ele:
                    return False
        return True

    def copy(self):
        new_board = copy.deepcopy(self.board)
        return LightsOutPuzzle(new_board)

    def successors(self):
        for i in range(self.rows):
            for j in range(self.cols):
                new_puzzle = self.copy()
                new_puzzle.perform_move(i, j)
                move = (i, j)
                yield (move, new_puzzle)


    def find_solution(self):
        # initialize a queue to store frotier
        visited = set()
        frotiers = deque()
        oprations = [] #store moves in tuples
        object = self.copy() # store objects
        first_state_board = object.get_tupleboard()
        visited.add(first_state_board)
        frotiers.append((object,oprations)) #starter
        while frotiers:
            current_state = frotiers.popleft()
            if current_state[0].is_solved():
                return current_state[1]
            for item in current_state[0].successors(): #expand node and add to the queue
                move = item[0]
                new_object = item[1]
                if new_object.get_tupleboard() in visited:
                    continue
                else:
                    newoperation = current_state[1] + [move]
                    if new_object.is_solved():
                        return newoperation
                    frotiers.append((new_object,newoperation))
                    visited.add(new_object.get_tupleboard())
        return None


def create_puzzle(rows, cols):
    board = [[False for i in range(cols)] for j in range(rows)]
    object = LightsOutPuzzle(board)
    return object


############################################################
# Section 3: Linear Disk Movement
############################################################

def createdisk(len, n):
    disk =  [True] * n + [False] * (len -n)
    return  disk

def three_performmove(disk, start, end):
    new_disk = disk.copy()
    new_disk[start] = False
    new_disk[end] = True
    return new_disk

def three_a_succcessors(disk):
    list_store_True = []
    length = len(disk)
    for j in range(len(disk)):
        if disk[j] == True:
            list_store_True.append(j)
    for i in list_store_True:
        #move right case
        if i+1 < length:
            if disk[i+1] == False:
                newdisk = three_performmove(disk,i,i+1)
                yield  (newdisk, (i,i + 1))
        if (i+1 < length) and (i+2 <length):
            if (disk[i+1] == True) and (disk[i + 2] ==  False):
                newdisk2 = three_performmove(disk,i,i+2)
                yield  (newdisk2,(i, i + 2))
        #move left case
        if i-1 >= 0:
            if disk[i-1] == False:
                newdisk = three_performmove(disk,i,i-1)
                yield  (newdisk, (i,i - 1))
        if (i - 1 >= 0) and (i - 2 >= 0):
            if (disk[i - 1] == True) and (disk[i - 2] == False):
                newdisk2 = three_performmove(disk, i, i - 2)
                yield (newdisk2, (i, i - 2))


def check_for_goal_state(lengh , n, currentdisk):
    targetdisk = [False] * (lengh -n) +  [True] * n
    if currentdisk == targetdisk:
        return True
    else:
        return False


def solve_identical_disks(length, n):
    visited = set()
    frontier = deque()
    operations = []
    initial_disk = createdisk(length,n)
    visited.add(tuple(initial_disk))
    frontier.append((initial_disk,operations))
    while frontier:
        currentstate = frontier.popleft()
        currentdisk = currentstate[0]
        currentmove = currentstate[1]
        if check_for_goal_state(length,n,currentdisk):
            return currentmove

        for item in three_a_succcessors(currentdisk):
            newdisk = item[0]
            newmove = item[1]
            if tuple(newdisk) in visited:
                continue
            else:
                newoperation = currentmove + [newmove]
                if check_for_goal_state(length,n,newdisk):
                    return newoperation
                frontier.append((newdisk,newoperation))
                visited.add(tuple(newdisk))
    return  None



############################################################

def createdisk2(len, n):
    disk = []
    for i in range(1,n+1):
     disk.append(i)
    return (disk + (len  -n)* [0])


def threeb_performmove(disk, start, end):
    new_disk = disk.copy()
    new_disk[end] = new_disk[start]
    new_disk[start] = 0
    return new_disk


def three_b_succcessors(disk):
    list_store_not0 = []
    length = len(disk)
    for j in range(len(disk)):
        if disk[j] != 0:
            list_store_not0.append(j)
    for i in list_store_not0:
        if i+1 < length:
            if disk[i+1] == 0:
                newdisk = threeb_performmove(disk,i,i+1)
                yield  (newdisk, (i,i + 1))
        if (i+1 < length) and (i+2 <length):
            if (disk[i+1] != 0) and (disk[i + 2] == 0):
                newdisk2 = threeb_performmove(disk,i,i+2)
                yield  (newdisk2,(i, i + 2))
        if i-1 >= 0:
            if disk[i-1] == 0:
                newdisk = threeb_performmove(disk,i,i-1)
                yield  (newdisk, (i,i - 1))
        if (i - 1 >= 0) and (i - 2 >= 0):
            if (disk[i - 1] != 0) and (disk[i - 2] == 0):
                newdisk2 = threeb_performmove(disk, i, i - 2)
                yield (newdisk2, (i, i - 2))

def check_for_goal_stateb(lengh , n, currentdisk):
    targetdisk = [0]* (lengh -n)
    for i in range(n,0,-1):
        targetdisk.append(i)
    if currentdisk == targetdisk:
        return True
    else:
        return False


def solve_distinct_disks(length, n):
    visited = set()
    frontier = deque()
    operations = []
    initial_disk = createdisk2(length, n)
    visited.add(tuple(initial_disk))
    frontier.append((initial_disk, operations))

    while frontier:
        currentstate = frontier.popleft()
        currentdisk = currentstate[0]
        currentmove = currentstate[1]
        if check_for_goal_stateb(length, n, currentdisk):
            return currentmove

        for item in three_b_succcessors(currentdisk):
            newdisk = item[0]
            newmove = item[1]
            if tuple(newdisk) in visited:
                continue
            else:
                newoperation = currentmove + [newmove]
                if check_for_goal_stateb(length,n,newdisk):
                    return newoperation
                frontier.append((newdisk, newoperation))
                visited.add(tuple(newdisk))
    return None


