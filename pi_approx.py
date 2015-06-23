#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Finding an approximation of pi through a genetic algorithm
from __future__ import print_function, division
import genetic_algorithm as ga
import sys, random, math
if sys.version_info.major < 3:
	input = raw_input

GENOME_RANGE = 6, 12
NUMBER_CHANCE = 0.5 #On average 1 number per operation
NUMBER_RANGE = 1, 10
OPERATIONS = "+", "-", "*", "/"

TARGET = math.pi

def generate():
	genome = []
	genome_size = random.randint(*GENOME_RANGE)
	for i in range(genome_size):
		#Will either append a number 1-10 or an operation
		if random.random() < NUMBER_CHANCE:
			genome.append(random.randint(*NUMBER_RANGE))
		else:
			genome.append(random.choice(OPERATIONS))
	return genome

def evaluate(genome):
	stack = []
	def pop():
		try: result = stack.pop()
		except IndexError: result = 0
		return result
	def safediv(x, y):
		try: result = x / y
		except ZeroDivisionError: result = 0
		return result
	for gene in genome:
		if type(gene) == int:
			stack.append(gene)
		else:
			a = pop()
			b = pop()
			result = {
				"+": lambda x, y: x+y,
				"-": lambda x, y: x-y,
				"*": lambda x, y: x*y,
				"/": safediv
			}[gene](a, b)
			stack.append(result)
	return pop()

def fitness(genome):
	#Evaluates the string and finds the result
	result = evaluate(genome)
	fitness = abs(TARGET - result)
	fitness = 1 - fitness
	return fitness

def mutate(genome):
	index = random.randint(0, len(genome)-1)
	genome[index] = random.randint(*NUMBER_RANGE) \
		if random.random() < NUMBER_CHANCE else \
		random.choice(OPERATIONS)

def crossover(parent_a, parent_b):
	half_a = len(parent_a) // 2
	half_b = len(parent_b) // 2
	child = parent_a[:half_a] + parent_b[half_b:]
	return child

if __name__ == "__main__":
	approximate_pi = ga.GeneticAlgorithm(
		population = 100,
		generate_function = generate,
		fitness_function = fitness,
		mutate_function = mutate,
		crossover_function = crossover
	)
	solution = approximate_pi.evolve_until(
		fitness = 0.99, 
		generation = 10000, 
		update_each = 100,
	)
	#print(evaluate([3, 2, "/"]))
	from pprint import pprint
	pprint(approximate_pi.population)
	print(solution)
	print(evaluate(solution))