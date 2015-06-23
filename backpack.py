#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, division
import genetic_algorithm as ga
import sys, random, argparse
if sys.version_info.major < 3:
	input = raw_input

def parse_input(input):
	nuggets = []
	for i, line in enumerate(input.splitlines()):
		if i == 0:
			backpack_size = float(line)
			continue
		elif i == 1:
			continue
		nuggets.append(float(line))
	return backpack_size, nuggets

def generate(genome_size):
	def _generate_inner():
		genome = []
		for j in range(genome_size):
			genome.append(random.randint(0, 1))
		return genome
	return _generate_inner

def fitness(target, sizes):
	size = len(sizes)
	def _fitness(gene):
		fitness = 0
		for i in range(size):
			fitness += gene[i] * sizes[i]
		fitness /= target
		if fitness > 1:
			fitness = 0
		return fitness
	return _fitness

def mutate(size):
	def _mutate(gene):
		index = random.randint(0, size-1)
		gene[index] = 0 if gene[index] else 1
	return _mutate

def crossover(length):
	half = length // 2
	def _crossover(parent_a, parent_b):
		child = parent_a[:half] + parent_b[half:]
		return child
	return _crossover

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Finds a solution to the knapsack problem using genetic programming.")
	parser.add_argument('infile', type=argparse.FileType('r'), 
		help="The file from which to read the problem to solve.")
	parser.add_argument('-p', '--population', type=int, default=100,
		metavar='P', help="size of the population to evolve (default: %(default)s)")
	parser.add_argument('-r', '--retain', type=float, default=0.2,
		metavar='R', help="percent of individuals to retain (default: %(default)s)")
	parser.add_argument('-d', '--diversity', type=float, default=0.05,
		metavar='D', help="percent of individuals to retain to improve genetic diversity (default: %(default)s)")
	parser.add_argument('-m', '--mutation', type=float, default=0.01,
		metavar='M', help="mutation rate (default: %(default)s)")
	parser.add_argument('-t', '--target', type=float, default=0.99,
		metavar='T', help="target fitness (default: %(default)s)")
	parser.add_argument('-g', '--generation', type=int, default=None,
		metavar='G', help="maximum number of generations (default: %(default)s)")
	parser.add_argument('-v', '--verbose', action='count',
		help="show a more detailed output")
	args = parser.parse_args()

	backpack_size, nuggets = parse_input(args.infile.read())
	genome_width = len(nuggets)
	backpack = ga.GeneticAlgorithm(
		population = args.population,
		retain = args.retain,
		random_select = args.diversity,
		mutation_rate = args.mutation,
		generate_function = generate(genome_width),
		fitness_function = fitness(backpack_size, nuggets),
		mutate_function = mutate(genome_width),
		crossover_function = crossover(genome_width)
	)
	solution = backpack.evolve_until(
		fitness = args.target, 
		generation = args.generation, 
		update_each = args.generation // 20 if args.generation else 100,
		silent = not args.verbose,
	)