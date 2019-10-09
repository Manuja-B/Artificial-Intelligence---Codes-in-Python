#!/usr/local/bin/python3
#
# choose_team.py : Choose a team of maximum skill under a fixed budget
#
# Code by: [PLEASE PUT YOUR NAMES AND USER IDS HERE]
#
# Based on skeleton code by D. Crandall, September 2019
#
import sys

def load_people(filename):
    people={}
    with open(filename, "r") as file:
        for line in file:
            l = line.split()
            people[l[0]] = [ float(i) for i in l[1:] ]
    return people


# This function implements a greedy solution to the problem:
#  It adds people in decreasing order of "skill per dollar,"
#  until the budget is exhausted. It exactly exhausts the budget
#  by adding a fraction of the last person.
#
def approx_solve(people, budget):
    '''for i in range(1,n+1):
        for c in range(1,budget):
            maxValWithoutCurr = mat[i-1][c]
            maxValWithCurr = 0
            weightOfCurr = wt[i-1]

            if c >= weightOfCurr:
                maxValWithCurr = val[i-1]
                remainingCapacity = c - weightOfCurr
                maxValWithCurr += mat[i-1][remainingCapacity]
            mat[i][c] = max(maxValWithoutCurr,maxValWithCurr)
    return mat[n][len(mat[0])]

  '''
    solution=()
    #its sorting in ascending order, therefore used reverse = true
    for (person, (skill, cost)) in sorted(people.items(), key=lambda x: x[1][0], reverse = True):
        if budget - cost > 0:
            solution += ( ( person, 1), )
            budget -= cost

    return solution


if __name__ == "__main__":

    if(len(sys.argv) != 3):
        raise Exception('Error: expected 2 command line arguments')

    budget = float(sys.argv[2])
    people = load_people(sys.argv[1])
    n = len(people)
    solution = approx_solve(people, budget)

    print("Found a group with %d people costing %f with total skill %f" % \
               ( len(solution), sum(people[p][1]*f for p,f in solution), sum(people[p][0]*f for p,f in solution)))

    for s in solution:
        print("%s %f" % s)

