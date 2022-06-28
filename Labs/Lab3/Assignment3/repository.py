# -*- coding: utf-8 -*-

import pickle
from domain import *


class Repository():
    def __init__(self):
        self.__populations = []
        self.cmap = Map()
        self.drone = [0, 0]

    def add_individual(self, population, individual):
        population.add_individual(individual, self.cmap, self.drone)
        
    def createPopulation(self, args):
        # args = [populationSize, individualSize] -- you can add more args    
        return Population(args[0], args[1])

    def add_population(self, population):
        self.__populations.append(population)

    def current_population(self):
        return self.__populations[-1]

    def evaluate_population(self, population):
        population.evaluate(self.cmap, self.drone)

    def random_drone(self):
        x = randint(0, self.cmap.n - 1)
        y = randint(0, self.cmap.m - 1)
        while self.cmap.surface[x][y] != 0:
            x = randint(0, self.cmap.n - 1)
            y = randint(0, self.cmap.m - 1)
        self.drone = [x, y]
        
    def set_drone(self, x, y):
        self.drone = [x, y]

    def avg_fitness_and_deviation(self):
        return self.__populations[-1].avg_fitness_and_deviation(self.cmap, self.drone)

    def get_first_path(self):
        return self.__populations[-1].get_first_path(self.cmap, self.drone)

    def get_best_fitness(self):
        return self.__populations[-1].get_best_fitness(self.cmap, self.drone)