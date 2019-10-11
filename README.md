# a1

**Elements of Artificial Intelligence: Assignment1 Report**

**Part 1: Luddy Puzzle-**

The question is to solve the famous 15-tile puzzle with different variants. We have used different algorithms and heuristic combinations and are more explained below.

In the given code, firstly it works only for &quot;Original&quot; variant which we have to modify it to be run for &quot;Circular&quot; and &quot;Luddy&quot; moves too. And, the algorithm is not optimal, as it does not use the &quot;type 3 search algorithm&quot;. So, it misses to find out the already visited states, which might result in moving into an infinite loop. The given code also does not use the priority queue, which is necessary to pop the most probable ones first.

- **The valid states** are, any possible instance of the board which have been derived from the initial\_state using the valid moves.
- **The successor function** provides the neighbouring instance of the board which have not been previously observed. For &quot;original&quot; variant, the neighbours can be, top, left, right, or down. And for &quot;luddy&quot; variant, there are 8 possible moves.
- **Cost function** is, F(s) = h(s) + g(s), where g(s) is the length f the path travelled, and h(s) is the heuristic function. We have used a variety of heuristic functions and their combinations too (details are discussed after this summary).
- **Goal state** of the given problem is fixed, which is when all the numbersn the board becomes sorted ascendingly.
-   **Initial state** is the given state of the board provided as an input.

**Heuristics-** Following are the types of Heuristics we tried:

- Manhattan Distance
- Misplaced Tiles
- Inversions
- Combinations of above three

**Algorithm-** We have used two different algorithms:

- A\* search(using algo 3)
- IDA\* search algo(with depth 4)

1. Insert the starting state of the board into the fringe.
2. Initialize an empty set, &#39;closed&#39;. and initialize cost to zero.
3. Initialize an empty Priority Queue &#39; q &#39;.
4. Insert a set containing the no. of misplaced tiles of the initial board ( which is the cost incurred so far), the state of the initial board, and the steps so far (which is currently an empty path) and 0 into q.
5. Repeat steps 6 to 12 while q is not empty.
6. From q pop out the current cost, the current state and the steps taken so far.
7. Increment the value of cost by 1
7. If the state equals the goal state, return the steps taken so far.
8. For each successor in the list of successors of the current state, repeat steps 10 and 11.
10. If the successor is  not in closed, add the successor to the closed set
11. Insert into q, a set containing the sum of no. of ( misplaced tiles in the successor, the no. of steps taken so far and cost of moves), the state of the successor and the steps taken so far, cost.
12. If q becomes empty, return &quot;Inf.

Both the algorithms were implemented using PriorityQueue, but there seems to be some logic error in the thinking as they were not converging for &quot;Luddy&quot; move fast. In A\* algo, to find the solution using Luddy variant it was taking over 1000secs, which is true because even when the A\* is fast, it alone cannot find the solution as the 15- tile puzzle has a huge state-space. So, we read over the internet and came across with this famous paper: [https://www.aaai.org/Papers/JAIR/Vol22/JAIR-2209.pdf](https://www.aaai.org/Papers/JAIR/Vol22/JAIR-2209.pdf)which explains and compares best techniques to solve the 15-tile puzzle. After searching more on the net, we find out that the best and fastest way to solve the problem is through using the IDA\* algo with pattern-database heuristic. We implemented the IDA\* algorithm, but the problem with that was it gets emptied very fast, and the result is Inf for Luddy move.

And for the pattern-database part, we were not able to implement it, due to its complex implementation and very less resources.

We performed various implementation changes in IDA\*like if two nodes within the &#39;d&#39; depth have the same heuristic value, then we choose both of them. And from them, we pop out the one who has a smaller number of misplaced tiles.

Apart, from these experiments we tried various combinations on heuristics as well, like combining &quot;manhattan distance&quot;, &quot;misplaced tiles&quot; and &quot;permutation inversions&quot;. But no significant result was observed.

Also, we read somewhere over the internet, providing more weights to the tiles which are at their place, might solve the problem fast.

We are getting results for &quot;luddy&quot;.

**Part 2: Road trip!-**

The problem was similar to the famous **&quot;travelling salesman problem&quot;,** where salesman have to travel to different cities in different minimum constraints. Here we were provided with two data-sets: road-segments and city-gps. The first one, road-segments describes the origin-city connected-city and distance, velocity, highway number associated between them. And city-gps data has the latitude and longitude of various cities.

Our task is to find a path from origin to goal city with minimum constraint. The obvious thinking was to use A\*, but the problem arises that what heuristic we should choose because without heuristic it is just Djikstra&#39;s Algo which won&#39;t converge easily. So, we took advantage of the city-gps data. We used it to find the distance between two cities using latitude &amp; longitude. We created a dictionary which stored the connected cities and their latitude-longitude distance and for obvious reasons searching in the dictionary is very fast.

Another problem arose was what to do for the cities that are not present in the city-gps data. So, we averaged the values of latitudes-longitudes from its neighbours. And for the case where the neighbour is also not present in the city-gps, we assigned zero.

The structure of program:

- **The valid states** are any possible move is correct according to the road-segments data, then the resulting path is valid state.
- **The successor function** provides all the neighbours according to the road-segments data, which was actually read from dictionary which we created for ease.
- **Cost function** is, F(s) = h(s) + g(s), where g(s) is the length f the path travelled, and h(s) is the lat-lon distance. Now, this has some abnormalities, which are discussed below.
- **Goal state** when we reach the destination city, the path is our goal state with given constraints.
-   **Initial state** is the empty path, where we are in a city and we have to travel towards the goal city.

Yeah, so problem with using cost function here is:

F(s) = min. constraint{distance, segment, time or mpg} + lat-lon distance

Problem with this is lat-lon part dominates over constraint part and it converges but the cost becomes higher than the optimal one.

So, we thought of penalizing the lat-lon distance, so as to get the optimal result. But penalizing will increase the computation time of the algorithm, so after experimenting we get to a final value which might not be true in all cases but it was working optimally and in within a few seconds.

**F(s) = min. constraint + 0.7\*lat-lon distance**

Here, 0.7 term is just experimental, it could be any number. We were just getting good results with this term. If the result is not correct using this term, then we can reduce it but the running time of algorithm will increase, so there is a trade-off between them.

Algorithm:

1. Create rSeg dictionary, that has information cities connected to other.
2. Use the rSeg dict, to create city\_gps data, to compute the missing latitude-longitude values.
3. Create a fringe and initialize it with lat-lon distance b/w start\_city and goal\_city
4. Pop the element from the fringe that has most priority.
5. Check if it is in goal state. If yes, then return.
6. Look for successors of the popped state.
7. For each successor, check if they are present in visited, if yes then ignore
8. Check if the successor is already present in fringe.
9. If yes, update with the minimum path.
10. If no, insert in the fringe
11. Continue 4-10 till either we got the solution of fringe becomes empty



**Part 3: Choosing a team-**

This problem is the 0/1 Knapsack problem, where we have a bag of given weight and where we have to fill the items with maximum value and the total weight should be under the weight of the bag.

In the given code, we get an answer but it is incorrect in the way that firstly it assigns partial robots for the work, second, even if we can get the correct answer by just removing the &#39;else loop&#39; in the function, but the result is not the optimal one.

The structure of program:

- **The valid states** are any possible count of robots such that their total rate is less than the budget.
- **The successor function** provides the next robot which should be chosen in the list, to get the maximum skill.
- **Cost function** we try to choose that robot whose skills to cost ratio is maximum.
- **Goal state** is the set of robots whose total cost is less than the budget with maximum skill from the data.
- **Initial state** is the empty set, which has to be filled with the robots.

 After exploring over internet, we found on Geeksforgeeks, that this problem can be solved by Branch and Bound algorithm. So, we have used the same in our implementation.

There are other algorithms, like brute-force, greedy search, dynamic programming or backtracking can also be used, but they are not as optimal as Branch and Bound.

The concept of branch and bound algorithm is that, it looks for its subtree and if the cost of subtree is more than the current-best-cost than we omit going doing the tree.  It as a Breadth First Search kind of technique.

Algo:

1. Sort the given array according to skill to rate ratio.
2. Create an empty queue
3. Create root node, that will be used to traverse the tree.
4. Now, for each successor of the given node, check if their bound is greater than the current profit.
5. To check the bound use the function find\_bound, which calculates the left and right bounds.
6. If, no just ignore them
7. If yes, add them to the queue
8. Repeat (4) to (7) until converge
