#!/usr/local/bin/python3
# solve_luddy.py : Sliding tile puzzle solver
#
# Code by: [PLEASE PUT Divyanshu Jhawar, Manuja Mandal & Sathyan djhawar, msbandal, satvenk]
#
# Based on skeleton code by D. Crandall, September 2019
#
from queue import PriorityQueue
import queue as Q
import sys
import time
import os
import heapq
from heapq import heapify, heappush, heappop

MOVES = { "R": (0, -1), "L": (0, 1), "D": (-1, 0), "U": (1,0) }

MOVES_LUDDY = { "A":(2,1),"B": (2,-1),"C":(-2,1),"D": (-2, -1),"E":(1,2),"F":(1,-2),"G": (-1,2),"H": (-1, -2) }
#MOVES_LUDDY = { "A": (-2,-1), "B": (-2,1), "C": (2,-1), "D": (2,1), "E": (-1,-2), "F": (-1,2), "G": (1,-2), "H": (1,2) }

def rowcol2ind(row, col):
    return row*4 + col

# Find the number of misplaced tiles on the board
def misplaced_tiles(state):
    count =0
    #print(state)
    for i in range(15):
        if state[i] != (i+1):
            count+=1
    if state[15] != 0:
        count+= 1
    #print("Count is ", count)
    return count

# Checks the board is solvable or not
def solvability(state):

    inversions = 0

    for i in range(len(state)):
        for j in range(i,len(state)):
            #print((state[i] > state[j]))
            if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
                inversions += 1
    (empty_row, empty_col) = ind2rowcol(state.index(0))

    print("Inv: ",inversions)
    print("\n")

    if empty_row %2 == 0 and inversions %2 == 1:
        return True
    if empty_row %2 == 1 and inversions %2 == 0:
        return True

    return False

def ind2rowcol(ind):
    return (int(ind/4), ind % 4)

def valid_index(row, col):
    return 0 <= row <= 3 and 0 <= col <= 3

def swap_ind(list, ind1, ind2):
    return list[0:ind1] + (list[ind2],) + list[ind1+1:ind2] + (list[ind1],) + list[ind2+1:]

def swap_tiles(state, row1, col1, row2, col2):
    return swap_ind(state, *(sorted((rowcol2ind(row1,col1), rowcol2ind(row2,col2)))))

def printable_board(row):
    return [ '%3d %3d %3d %3d'  % (row[j:(j+4)]) for j in range(0, 16, 4) ]

# return a list of possible successor states
def successors(state):
    # Finding the coordinates of '0'
    (empty_row, empty_col) = ind2rowcol(state.index(0))
    if (sys.argv[2] == 'original'):
        return [ (swap_tiles(state, empty_row, empty_col, empty_row+i, empty_col+j), c) \
             for (c, (i, j)) in MOVES.items() if valid_index(empty_row+i, empty_col+j) ]
    elif (sys.argv[2] == 'luddy'):

        return [(swap_tiles(state, empty_row, empty_col, empty_row + i, empty_col + j), c) \
                for (c, (i, j)) in MOVES_LUDDY.items() if valid_index(empty_row + i, empty_col + j)]
    else:
        return [(swap_tiles(state, empty_row, empty_col, (empty_row + i) % 4, (empty_col + j) % 4), c) for (c, (i, j))
                in MOVES.items()]

    #return [ (swap_tiles(state, empty_row, empty_col, empty_row+i, empty_col+j), c) for (c, (i, j)) in MOVES.items() if valid_index(empty_row+i, empty_col+j) ]

# successor for circular moves
#def successors_circular(state):

    #(empty_row, empty_col) = ind2rowcol(state.index(0))

    #return [ (swap_tiles(state, empty_row, empty_col, (empty_row+i)%4, (empty_col+j)%4), c) for (c, (i, j)) in MOVES.items() ]


#def successors_luddy(state):
    #(empty_row, empty_col) = ind2rowcol(state.index(0))

    #return [ (swap_tiles(state, empty_row, empty_col, empty_row+i, empty_col+j), c) for (c, (i, j)) in MOVES_LUDDY.items() if valid_index(empty_row+i, empty_col+j) ]

# check if we've reached the goal
def is_goal(state):
    return sorted(state[:-1]) == list(state[:-1]) and state[-1]==0
    
# The solver! - using A* Search
def solve(initial_board):
    fringe = [ (initial_board, "") ]
    closed = []
    open= []
    #l=[]
    q = Q.PriorityQueue()
    cost = 0
    q.put(((misplaced_tiles(initial_board) + 0), initial_board, ""))


    while not q.empty():
        (h, state, route_so_far) = q.get()
        cost +=1
        #print("mmm", q.get())
        #closed.append(state)
        closed.append(state)
        if is_goal(state):
            return (route_so_far)

        for (succ, move) in successors(state):
            if succ in closed: continue
            q.put((misplaced_tiles(succ) + len(move), succ, route_so_far + move))

    return "Inf"
                # q.pop(((misplaced_tiles(succ)), succ, route_so_far + move))
                # break
                #if succ in open and (cost) < (fringe[]):
                    #print("im in first condition")
                    #open.remove(succ)
                    #closed.append(succ)
                #if succ in closed and (cost + misplaced_tiles(state)) < (misplaced_tiles(succ) + cost):
                    #print("im in second condition")
                    #closed.remove(succ)
                #if succ not in open and succ not in closed:
                    #heappush(open, ((misplaced_tiles(succ)), succ, route_so_far + move))
            #if is_goal(state):
                #return (route_so_far)
                #if succ in closed:
                    #continue
            #prev_cost = misplaced_tiles(succ) + 1
            #cost += 1



            #closed.append(succ)
            #for k in range(len(fringe)):
                #if succ == fringe[k][0]:
                    #print("I am checking succesors")
                    #if len(move) < len(fringe[k][1]):
                    #if (cost + misplaced_tiles(succ)) > ((misplaced_tiles(succ) + 1)):
                        #print("I am checking the if condition")
                        #q.pop(((misplaced_tiles(succ)), succ, route_so_far + move))
                        #break
            #fringe.insert(0, (succ, route_so_far + move))
            #q.put(((misplaced_tiles(succ) + len(move)) , succ, route_so_far + move))


# test cases
if __name__ == "__main__":
    if(len(sys.argv) != 3):
        raise(Exception("Error: expected 2 arguments"))

    start_state = []
    file_path = "C:/Users/manuj/Desktop/Courses/AI/msbandal-satvenk-djhawar-a1-master/msbandal-satvenk-djhawar-a1-master/part1/"
    os.chdir(file_path)
    with open(sys.argv[1], 'r') as file:
        for line in file:
            start_state += [ int(i) for i in line.split() ]

    '''
    if(sys.argv[2] != "original"):
        raise(Exception("Error: only 'original' puzzle currently supported -- you need to implement the other two!"))
    '''
    if len(start_state) != 16:
        raise(Exception("Error: couldn't parse start state file"))


    start_state = tuple(start_state)

    print("Start state: \n" +"\n".join(printable_board(start_state)))

    if solvability(start_state):

        print("Solving...")
        st = time.time()
        route = solve(tuple(start_state))
        et = time.time()
        print(et-st)
        print("Solution found in " + str(len(route)) + " moves:" + "\n" + route)

    elif ():
        print("Inf")
