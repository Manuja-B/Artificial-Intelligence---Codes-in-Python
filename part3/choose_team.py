#!/usr/local/bin/python3
#
# choose_team.py : Choose a team of maximum skill under a fixed budget
#
# Code by: [Divyanshu Jhawar- djhawar, Manuja Bandal- msbandal, Sathyan- satvenk]
#
# Based on skeleton code by D. Crandall, September 2019
#
import sys
import queue as Q

def load_people(filename):
    people={}
    with open(filename, "r") as file:
        for line in file:
            l = line.split()
            people[l[0]] = [ float(i) for i in l[1:] ] 
    return people

class State:
    def __init__(self, depth, rate, bound, cost):
         self.depth = depth
         self.rate = rate
         self.bound = bound
         self.cost = cost


# This function implements a greedy solution to the problem:
#  It adds people in decreasing order of "skill per dollar,"
#  until the budget is exhausted. It exactly exhausts the budget
#  by adding a fraction of the last person.
#
def approx_solve(people, budget):

    solution=()
    for (person, (skill, cost)) in sorted(people.items(), key=lambda x: x[1][0]/x[1][1]):
        if budget - cost > 0:
            solution += ( ( person, 1), )
            budget -= cost

    return solution

# Referenced from: https://www.geeksforgeeks.org/0-1-knapsack-using-branch-and-bound/
# Using branch and bound algorithm
def solve(people,budget):

    max_profit = 0

    q = Q.Queue()


    skills = []
    rates = []
    names = []
    people_sorted = sorted(people.items(), key=lambda x: x[1][0]/x[1][1], reverse = True)

    print(people_sorted)

    for key in range(len(people_sorted)):
        skills.append(people_sorted[key][1][0])
        rates.append(people_sorted[key][1][1])
        names.append(key)

    value = 0

    root = State(-1,0.0,0,0)

    temp = State(0,0.0,0,0)

    q.put(root)

    while not q.empty():
        print("Max_profit",max_profit)

        succ = q.get()
        
        if succ.depth == -1:
            temp.depth = 0

        if succ.depth == len(rates)-1:
            continue

        temp.depth = succ.depth + 1
        #print(temp.depth)


        temp.rate = succ.rate + rates[temp.depth]
        print(rates[temp.depth])
        print("temp.rate : ",temp.rate)

        temp.cost = succ.cost + skills[temp.depth]
        print("temp.cost : ",temp.cost)

        if temp.rate <= budget and temp.cost > max_profit:
            max_profit = temp.cost


        temp.bound = find_bound(temp,budget,rates,skills)

        #print("temp.bound",temp.bound)

        if temp.bound > max_profit:
            print("True")
            q.put(temp)

        temp.rate = succ.rate
        temp.cost = succ.cost
        temp.bound = find_bound(temp,budget,rates,skills)
        if temp.bound > max_profit:
            print("Truuue")
            q.put(temp)

    return max_profit

    '''
        if succ[3] > value:
            current_level = succ[0]+1

            left = [current_level,succ[1]+skills[current_level-1],succ[2]+rates[current_level-1],0.0,succ[4]]
            left[3] = find_bound(left,budget,len(people),skills,rates)
            left[4].append(current_level)

            if left[2] <= budget:
                if left[1] > value:
                    value = left[1]
                    best = set(left[4])
                if left[3] > value:
                    q.put(left)

            right = [current_level,succ[1],succ[2],0.0,succ[4]]
            right[3] = find_bound(right,budget,len(people),skills,rates)
            if right[2] <= budget:
                if right[1] > value:
                    value = right[1]
                    best = set(left[4])
                if right[3] > value:
                    q.put(right)
    for b in best:
        taken[b-1] = 1
    value = sum([i*j for (i,j) in zip(skills,taken)])

    '''


def find_bound(temp,budget,rates,skills):

    if temp.rate >= budget:
        return 0

    current_bound = temp.cost
    current_level = temp.depth + 1
    current_rate = temp.rate
    while ((current_level<len(rates)) and (current_rate+rates[current_level] <= budget)):

        current_rate += rates[current_level]
        current_bound += skills[current_level]
        current_level += 1

    if current_level < len(rates):
        current_bound += (budget-current_rate)*skills[current_level]/rates[current_level]

    return int(current_bound)

    '''
    if root[2] > budget:
        return 0

    current_bound = root[1]
    current_weight = root[2]
    current_level = root[0]

    print(current_weight)

    while (current_level < length) and (current_weight+rates[int(current_weight)] <= budget):
        current_bound += skills[current_level]
        current_weight += rates[current_level]
        current_level += 1

    if current_level < length:
        current_bound += (budget-current_weight)*float(skills[current_level])/rates[current_level]

    return current_bound
    '''
    
if __name__ == "__main__":

    if(len(sys.argv) != 3):
        raise Exception('Error: expected 2 command line arguments')

    budget = float(sys.argv[2])
    people = load_people(sys.argv[1])
    solution = solve(people, budget)

    print("Solution is: ", solution)
    '''
    print("Found a group with %d people costing %f with total skill %f" % \
               ( len(solution), sum(people[p][1]*f for p,f in solution), sum(people[p][0]*f for p,f in solution)))

    for s in solution:
        print("%s %f" % s)
    '''
