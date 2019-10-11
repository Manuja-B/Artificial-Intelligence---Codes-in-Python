#!/usr/local/bin/python3

# put your routing program here!
from __future__ import division
import sys
from math import sin, cos, sqrt, atan2, radians
import time
import math


# Reference
# Code taken from: https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude
# To calculate the distance using lat-lon
def calculate_distance(c1,c2):

    if c1[0] == 0:
        return 0

    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(float(c1[0]))
    lon1 = radians(float(c1[1]))
    lat2 = radians(float(c2[0]))
    lon2 = radians(float(c2[1]))

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance
# *******************************************************************


def calculate_dis(c1,c2):
    return math.sqrt((float(c1[0]) -float(c2[0]))**2 + (float(c1[1]) -float(c2[1]))**2)

# Creating dictionary using city-gps
def complete_list(rSeg,city_gps_updated):
    temp = city_gps_updated

    for key in rSeg:
        lat =0
        lon =0
        #print(rSeg[key])
        if key not in temp:
            #print(key)
            mis_city = rSeg[key]
            count = 0

        
            for j in range(len(mis_city)):
                if mis_city[j][0] in city_gps_updated:
                    lat += float(city_gps_updated[mis_city[j][0]][0])
                    lon += float(city_gps_updated[mis_city[j][0]][1])
                    count += 1
            if count >0:
                lat /= count
                lon /= count
    
            city_gps_updated[key] = ([lat,lon])

    return city_gps_updated

def priority_queue(fringe,c_fun):

    # For priority queue
    min_val = fringe[0][c_fun] + 0.7*fringe[0][6]
    min_idx = 0

    for i in range(len(fringe)):
        temp = fringe[i][c_fun] + 0.7*fringe[i][6]
        if temp < min_val:
            min_val = temp
            min_idx = i
    return min_idx

# Miles per Gallon
def calculate_MPG(velocity):
    temp = int(velocity)/150
    mpg = 400*temp*(pow((1-temp),4))
    return mpg

# check if we've reached the goal
def is_goal(current_city, end_city):

    if current_city == end_city:
        return True
    else:
        return False

def successors(rSeg,current_city):

    succ = []

    if current_city in rSeg:
        for i in range(len(rSeg[current_city])):
            succ.append((rSeg[current_city][i][0],rSeg[current_city][i][1],rSeg[current_city][i][2]))

    return succ

# *************************************************************************************************************
def solve(start_city, end_city, cost_function):

    # Just to resolve the double inverted for Y_city {only case in the data}
    if start_city == 'Y_City,_Arkansas':
        start_city = '"Y"_City,_Arkansas'

    lat = []
    lon = []

    c_fun = 0
    if cost_function == 'segments':
        c_fun = 1
    elif cost_function == 'distance':
        c_fun = 2
    elif cost_function == 'time':
        c_fun = 3
    else:
        c_fun = 4


    city_gps = {}

    with open('city-gps.txt','r') as file:
        for line in file:
            l = line.split()
            city_gps[l[0]] = ([l[1],l[2]])

    # creating dictionary for each city from the input file
    rSeg = {}

    with open('road-segments.txt', 'r') as file:
        for line in file:
            
            temp = line.split()
            if temp[0] in rSeg:
                rSeg[temp[0]].append([temp[1],temp[2],temp[3],temp[4]])
            else:
                rSeg[temp[0]] = ([[temp[1],temp[2],temp[3],temp[4]]])

            if temp[1] in rSeg:
                rSeg[temp[1]].append([temp[0],temp[2],temp[3],temp[4]])
            else:
                rSeg[temp[1]] = ([[temp[0],temp[2],temp[3],temp[4]]])


    # dictionary of all cities
    city_gps = complete_list(rSeg,city_gps)

    #latitude longidude distance
    latlon_total_distance = calculate_distance(city_gps[start_city],city_gps[end_city])


    fringe = [(start_city,0,0,0,0,"",latlon_total_distance)]

    visited = []

    while len(fringe) > 0:
        
        # minimum index according to the priority of the given variant
        min_idx = priority_queue(fringe,c_fun)

        (city,segments,distance,time,gallons,path,latlon_distance) = fringe.pop(min_idx)
        
        visited.append(city)

        if is_goal(city,end_city):
            return segments,distance,time,gallons,path+city

        succ = successors(rSeg,city)

        for i in range(len(succ)):

            if succ[i][0] in visited:
                continue

            # bunch of variables
            temp = []
            c_distance = int(succ[i][1])
            c_velocity = int(succ[i][2])
            c_latlon_distance = calculate_distance(city_gps[succ[i][0]],city_gps[end_city])
            temp.append(segments+1)
            temp.append(distance+c_distance)
            temp.append(time+(c_distance/c_velocity))
            temp.append(gallons+c_distance/calculate_MPG(c_velocity))

            # To check if already shorter path is present in the fringe
            for k in range(len(fringe)):
                if fringe[k][0] == succ[i][0]:
                    if fringe[k][c_fun] > temp[c_fun-1]:
                        fringe.pop(k)
                        break
            lat.append(city_gps[succ[i][0]][0])
            lon.append(city_gps[succ[i][0]][1])


            fringe.insert(0,(succ[i][0],temp[0],temp[1],temp[2],temp[3],path+city+" ",c_latlon_distance))

    return False

# *****************************************************************************************************************

# test cases
if __name__ == "__main__":

    if(len(sys.argv) != 4):
        raise(Exception("Error: expected 3 arguments"))

    start_city = sys.argv[1]
    end_city = sys.argv[2]
    cost_function = sys.argv[3]
    #st = time.time()
    print("Solving...")
    
    segments,distance,time,gas,route = solve(start_city,end_city,cost_function)
    #print(time.time()-st)
    print(segments,distance,round(time,4),round(gas,4),route)

    
