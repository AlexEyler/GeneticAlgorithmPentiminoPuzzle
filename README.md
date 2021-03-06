Pentomino Puzzle Solver
================================
A genetic algorithm created in Python to solve pentomino puzzles. 

Pentimino Puzzles
-----------------

A pentimino puzzle consists of a board with m rows by n columns (where m x n must be divisible by 5) and all possible polygons that can be created with 5 squares. To solve the puzzle, one must completely fill a board with polygon pieces of size 5 (without breaking the pieces apart, of course). For instance, a solution for a 3 x 5 board would be:

	a a b b b
	a a b b c
	a c c c c


The Solver
----------

The algorithm is a basic genetic algorithm written in Python. Here's the basic pseudocode:

	while (not done):
		compute fitness of individuals in population
		select parents
		crossover (breeding)
		mutation

I have it implemented so that it will stop after "g" generations, although this could be easily changed (such as only stopping when a solution is found). 

The Representation
------------------

A board can be easily represented by counting the number of squares for a particular piece. For instance, if we define a as 00, b as 01, and c as 10, we can easily represent the board above as a bit string, going from left to right, then top to bottom:

	00 00 01 01 01 00 00 01 01 10 00 10 10 10 10

Fitness
-------

Now that there is a representation in a bit string, a fairly easy fitness function can be defined:

	f(x ; penalty) = Σ((1 - abs(5 - connected nodes)) / 5) / n + penalty * (Σ(1 - abs(5 - total squares)/5) / n)

Σ is defined as the summation over from i = 1 to the number of pieces (not squares but pieces). Originally, the function was only the first part of the term that function is currently, but the program would just throw away a piece and disconnect pieces to give it a fitness of 1. With the current implementation, the maximum fitness an individual can have is 1 + penalty. I have been using .2 as a penalty and it's been able to solve most puzzles given time.

The function works well, but it takes a while to find the connected nodes (breadth first search from each node) so the efficiency isn't where I'd want it to be. This can definitely be improved upon.


Selection
---------

The easiest way to think of the selection is a pie graph, where each piece is filled with the fitnesses of every individual of the current population (therefore the total area of the pie graph is the sum of the fitnesses). The selection function then selects two random pieces from that population to act as parents. Since the individuals with larger fitnesses have a larger area, they have a higher chance of being selected, but dead ends can be prevented by randomly selecting a seemingly bad parent.

Crossover
---------

The current crossover function takes two parents and selects a random index over the bitstrings. It swaps the left side of the first parent with the left side of the second parent, and vice versa with the right side (swapping the right side of the second parent with the first parent's right side) to create two children. 

Mutation
--------

For every individual in the population, randomly decide to mutate it based on a mutation rate by flipping a random bit in the bitstring. This means that mutation_rate * n individuals will be mutated in every population, on average.


How to Run
----------

	Usage: [python3] pentomino.py m n populationSize numberOfGenerations
