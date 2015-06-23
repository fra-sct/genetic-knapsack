#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, division
import random

class GeneticAlgorithm(object):
	def __init__(self, retain=0.2, random_select=0.05, mutation_rate=0.01, 
		population=1000, generate_function=None, fitness_function=None, 
		mutate_function=None, crossover_function=None):
		#Initializations
		self.generation = 0
		self.retain = retain
		self.random_select = random_select
		self.mutation_rate = mutation_rate
		if generate_function is not None:
			self.generate = generate_function
		if fitness_function is not None:
			self.fitness = fitness_function
		if mutate_function is not None:
			self.mutate = mutate_function
		if crossover_function is not None:
			self.crossover = crossover_function
		#Generate the initial population
		self.size = population
		self.population = []
		for ii in range(self.size):
			self.population.append(self.generate())
	def evolve(self):
		graded = self.grade(self.population)
		parents_number = int(self.retain * self.size)
		#Select the parents
		parents = graded[:parents_number]
		#Select other individuals at random
		parents_size = parents_number + int(self.random_select * self.size)
		while len(parents) < parents_size:
			index = random.randint(parents_number, self.size-1)
			if self.population[index] not in parents:
				parents.append(self.population[index])
		#Mutate
		parents_size = len(parents)
		mutations_number = int(self.mutation_rate * parents_size)
		for i in range(mutations_number):
			index = random.randint(0, parents_size-1)
			self.mutate(parents[index])
		#Crossover
		self.population = [x for x in parents]
		while len(self.population) < self.size:
			parent_a = random.choice(parents)
			parent_b = random.choice(parents)
			if parent_a != parent_b:
				child = self.crossover(parent_a, parent_b)
				self.population.append(child)
		self.generation += 1
	def evolve_until(self, fitness=None, generation=None, update_each=1000, silent=False):
		if not silent: self.print_banner(fitness, generation)
		try:
			while True:
				self.evolve()
				if generation and (generation <= self.generation):
					break
				graded = self.grade(self.population)
				if fitness and (self.fitness(graded[0]) >= fitness):
					break
				if update_each and (self.generation % update_each == 0):
					average_fitness = sum(map(self.fitness, graded)) / self.size
					print("Generation %6s - Average fitness: %f%%" % (self.generation, average_fitness * 100))
		except KeyboardInterrupt:
			pass
		solution = self.grade(self.population)[0]
		if not silent:
			print("\nEvolution stopped at generation %s." % self.generation)
			print("Best solution found has fitness %f%%" % (self.fitness(solution)*100))
		return solution
	def print_banner(self, fitness, generation):
		print(" Starting evolution ".center(79, "="))
		print(" Simulation parameters ".center(79, "-"))
		print("Population:           %s" % self.size)
		print("Individuals retained: %s%%" % (self.retain * 100))
		print("                      %s%% (to preserve diversity)" % (self.random_select * 100))
		print("Mutation rate:        %s%%" % (self.mutation_rate * 100))
		print("-"*79)
		if fitness: print("Target fitness:       %s" % fitness)
		if generation: print("Maximum generations:  %s" % generation)
		print("\nYou can stop the evolution by pressing CTRL+C.")
		print("-"*79)
	def grade(self, population):
		graded = [(self.fitness(genome), genome) for genome in population]
		graded = [item[1] for item in sorted(graded, key=lambda i: i[0], reverse=True)]
		return graded
	def generate(self):
		pass
	def fitness(self, genome):
		pass
	def mutate(self, genome):
		pass
	def crossover(self, parent_a, parent_b):
		pass