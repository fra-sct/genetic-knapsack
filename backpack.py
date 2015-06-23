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
	if len(sys.argv) > 1:
		infile = open(sys.argv[1], "r")
	backpack_size, nuggets = parse_input(infile.read())
	genome_width = len(nuggets)
	backpack = ga.GeneticAlgorithm(
		population = 100,
		generate_function = generate(genome_width),
		fitness_function = fitness(backpack_size, nuggets),
		mutate_function = mutate(genome_width),
		crossover_function = crossover(genome_width)
	)
	solution = backpack.evolve_until(
		fitness=0.99999, 
		generation=10000, 
		update_each=100
	)