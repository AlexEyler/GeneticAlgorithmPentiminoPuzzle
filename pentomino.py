#############################################################
# Alex Eyler
# Genetic Algorithm for solving pentomino puzzles
# http://en.wikipedia.org/wiki/Pentomino
# Representation: a bit string filled with IDs
# Ex: a 5x2 board needs exactly 2 pentomino polygons to
# completely fill the board. Therefore, there would be 10
# squares that can be represented by the IDs 0 and 1. So
# 1111100000 would be a valid solution (1 line on the left,
# 1 line on the right) 
# Fitness: avg(1 - (5 - connected nodes)/5) + 
#   avg(1 - abs(5 - total counts)/5) * penalty
# 
# Feel free to branch, there are definitely better solutions,
# that would be faster (it takes a fairly long amount of time
# to solve a board with an area of greater than 40). Just
# don't remove this comment!
##############################################################

from math import *
import random
from queue import *

class Node:
    # Node Class: store the coordinates, value, and neighbor list (for connection testing purposes)
    __slots__ = ("r", "c", "value", "neighbors")
    
    def __init__(self, r, c, value):
        self.r = r
        self.c = c
        self.value = value
        self.neighbors = []
        
    def __str__(self):
        return "(" + str(self.r) + ", " + str(self.c) + ", " + self.value + ")"
    
    def is_connected(self, other):
        return self in other.neighbors and other in self.neighbors
    
    def __eq__(self, other):
        if other == None:
            return False
        return self.r == other.r and self.c == other.c and self.value == other.value
        
class Pentomino:
    # Pentomino class: solve a pentomino puzzle (filling an m x n board with 
    # polygons of area = 5 (m x n % 5 = 0)). k = population size
    
    __slots__ = ("reps", "m", "n", "k", "population", "bitstrings")
    
    def __init__(self, m, n, k):
        self.reps = ['~', '*', '$', '^', '#', '@', '>', '<']
        self.m = m
        self.n = n
        self.k = k
        self.population = []
        self.bitstrings = []
        
        # populate
        bsize = self.bitsize()
        for _ in range(0, k):
            bstring = self.init_random_representation(m, n)
            self.bitstrings.append(bstring)
            grid = []
            i = 0  # position of pointer to bitstring 
            for r in range(0, self.n):
                lst = []
                for c in range(0, self.m):
                    idx = bstring[i:i+bsize]
                    lst.append(Node(r, c, idx))
                    i += bsize
                grid.append(lst)
            self.population.append(grid)
            
        # set up neighbors
        for i in range(0, k):
            for r in range(0, self.n):
                for c in range(0, self.m):
                    above = self.get_node(i, r-1, c)
                    below = self.get_node(i, r+1, c)
                    left = self.get_node(i, r, c-1)
                    right = self.get_node(i, r, c+1)
                    if not above == None and above.value == self.get_node(i, r, c).value:
                        self.population[i][r][c].neighbors.append(above)
                    if not below == None and below.value == self.get_node(i, r, c).value:
                        self.population[i][r][c].neighbors.append(below)
                    if not left == None and left.value == self.get_node(i, r, c).value:
                        self.population[i][r][c].neighbors.append(left)
                    if not right == None and right.value == self.get_node(i, r, c).value:
                        self.population[i][r][c].neighbors.append(right)
                    
    # set population for next runthrough, filling neighbors
    def set_population(self, bitstrings):
        self.population = []
        
        # populate
        bsize = self.bitsize()
        for bstring in bitstrings:
            grid = []
            i = 0  # position of pointer to bitstring 
            for r in range(0, self.n):
                lst = []
                for c in range(0, self.m):
                    idx = bstring[i:i+bsize]
                    lst.append(Node(r, c, idx))
                    i += bsize
                grid.append(lst)
            self.population.append(grid)
            
        # set up neighbors
        for i in range(0, len(bitstrings)):
            for r in range(0, self.n):
                for c in range(0, self.m):
                    above = self.get_node(i, r-1, c)
                    below = self.get_node(i, r+1, c)
                    left = self.get_node(i, r, c-1)
                    right = self.get_node(i, r, c+1)
                    if not above == None and above.value == self.get_node(i, r, c).value:
                        self.population[i][r][c].neighbors.append(above)
                    if not below == None and below.value == self.get_node(i, r, c).value:
                        self.population[i][r][c].neighbors.append(below)
                    if not left == None and left.value == self.get_node(i, r, c).value:
                        self.population[i][r][c].neighbors.append(left)
                    if not right == None and right.value == self.get_node(i, r, c).value:
                        self.population[i][r][c].neighbors.append(right)
            
    # get the node at idx, row, col of the population
    def get_node(self, idx, row, col):
        if row >= 0 and col >= 0 and row < self.n and col < self.m:
            return self.population[idx][row][col]
        else:
            return None
        
    # print out the board for easy viewing
    def print_pentomino(self, bitstring, m, n):
        pents = []
        bitsize = int(len(bitstring)/(m*n))
        k = 0 # position in bitstring
        
        while k < len(bitstring):
            idx = bitstring[k:k+bitsize]
            if not idx in pents:
                pents.append(idx)
            k += bitsize
            
        k = 0
        while k < len(bitstring):
            idx = bitstring[k:k+bitsize]
            print (self.reps[pents.index(idx)] + " ", end = "")
            k += bitsize
            if (int(k / bitsize) % m == 0 and not k == 0):
                print()
    
    # create a rnadom representation from a uniform distribution
    def init_random_representation(self, m, n):
        bitstring = ""
        bitsize = ceil(log((m * n) / 5, 2))
        for _ in range(0, (m * n)):
            for _ in range(0, bitsize):
                if random.random() < 0.5:
                    bitstring += "0"
                else:
                    bitstring += "1"
        return bitstring
    
    # apply a score to the current state
    # avg(1 - (5 - connected nodes)/5) + avg(1 - abs(5 - total counts)/5) * penalty
    def fitness(self, penalty):
        scores = []
        for i in range(0, self.k):
            connected_counts = {}
            total_counts = {}
            for r in range(0, self.n):
                for c in range(0, self.m):
                    node = self.population[i][r][c]
                    count = self.bfs(node)
                    if node.value in connected_counts:
                        if abs(count - 5) < abs(connected_counts[node.value] - 5):
                            connected_counts[node.value] = count
                    else:
                        connected_counts[node.value] = count
                    if node.value in total_counts:
                        total_counts[node.value] += 1
                    else:
                        total_counts[node.value] = 1
            smc = 0
            smt = 0
            for x in connected_counts.values():
                smc += 1 - abs(5 - x)/5
                
            for x in total_counts.values():
                smt += 1 - abs(5 - x)/5
                        
            avgc = smc / len(connected_counts)
            avgt = smt / len(total_counts)
            
            scores.append(avgc + penalty * avgt)
        return scores
        
    # select two random parents
    def selection(self, scores, max_score):
        parents = []
        for _ in range(0, 2):
            x = random.random() * max_score
            sc = 0
            score = 0
            while sc < x:
                sc += scores[score]
                if not sc >= x:
                    score += 1
            parents.append(score)
        return parents
        
    # breed parents by selecting a random bit position
    # to switch
    def crossover(self, parents):
        children = []
        mom = self.bitstrings[parents[0]]
        dad = self.bitstrings[parents[1]]
        loc = random.randint(0, len(mom))
        children.append(mom[0:loc] + dad[loc:len(dad)])
        children.append(dad[0:loc] + mom[loc:len(mom)])
        return children
        
    # randomly mutate a bitstring based on a mutation rate
    def mutation(self, mutation_rate):
        for b in self.bitstrings:
            for i in range(0, len(b)):
                if random.random() < mutation_rate:
                    if b[i] == "1":
                        b = b[:i] + "0" + b[i+1:]
                    else:
                        b = b[:i] + "1" + b[i+1:]
        
    # breadth-first-search to count the number of connected neighbors
    def bfs(self, node):
        q = Queue()
        visited = [node]
        q.put(node)
        count = 1
        while not q.empty():
            s = q.get()
            neighbors = s.neighbors
            for n in neighbors:
                if n not in visited:
                    visited.append(n)
                    q.put(n)
                    count += 1
        return count
        
    # convert a bitstring into a matrix
    def bitstring2matrix(self, bitstring, m, n):
        bitsize = self.calc_bitsize(bitstring, m, n)
        k = 0
        r = 0
        c = 0
        rows = []
        col = []
        while k < len(bitstring):
            idx = bitstring[k:k+bitsize]
            n = Node(r, c, idx)
            col.append(idx)
            k += bitsize
            if (int(k / bitsize) % m == 0 and not k == 0):
                rows.append(col)
                col = []
        
    # calculate the bitsize (number of bits needed to represent
    # a "type")
    def bitsize(self):
        return ceil(log((self.m * self.n) / 5, 2))
        
def main(m, n, k, g):
    # RUN PENTIMINO
    p = Pentomino(m, n, k)
        
    c = 1
    # generic genetic algorithm
    while (c < g):
        scores = p.fitness(.2)
        sm = 0
        
        for score in scores:
            sm += score
        
        # print out every 10 generations to see how close 
        # the solution is    
        if c % 10 == 0:
            s = max(scores)
            idx = scores.index(s)
            print("c: " + str(c))
            print("Score: " + str(s))
            p.print_pentomino(p.bitstrings[idx], m, n)
            print()
            
        children = []
        for _ in range(0, int(k/2)):
            # parents
            parents = p.selection(scores, sm)
            # crossover
            children.extend(p.crossover(parents))
        p.bitstrings = children
        p.mutation(.05)
        p.set_population(children)
        
        # mutation
        c += 1

main(10, 3, 500, 301) # m, n, population size, number of generations
    
            
        