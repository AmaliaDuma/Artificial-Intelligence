# -*- coding: utf-8 -*-
import copy
import pickle
from random import *

import pygame

from utils import *
import numpy as np


# the glass gene can be replaced with int or float, or other types
# depending on your problem's representation

# class gene:
#    def __init__(self):
#         random initialise the gene according to the representation
#        pass


class Individual:
    """
    An Individual is a possible solution.
    A gene it corresponds to a direction: up-0; down-2; left-1; right-3.
    We know that our drone can make a maximum number of m steps before the battery depletes
         => so the size will be given by the size of the battery, m.
    """

    def __init__(self, size=0):
        self.__size = size
        self.__x = [randint(0, 3) for i in range(self.__size)]
        self.__f = None

    def compute_path(self, drone, crt_map):
        """
        We have the directions for our individual, now we want to build the path based on these directions.
        :param drone: [x,y] list
        :param crt_map: the map we use to verify our path is valid
        :return:
        """
        path = [[drone[0], drone[1]]]
        for direction in self.__x:
            if direction == 0:  # 0 - up
                # we take the last elem added with path[-1]; to move up we decrease with one the x component
                path.append([path[-1][0] - 1, path[-1][1]])
            elif direction == 1:  # 1 - left
                path.append([path[-1][0], path[-1][1] - 1])
            elif direction == 2:  # 2 - down
                path.append([path[-1][0] + 1, path[-1][1]])
            elif direction == 3:  # 3 - right
                path.append([path[-1][0], path[-1][1] + 1])

        # We need to check if our path is valid with the map.
        valid_path = []
        for position in path:
            if position[0] < 0 or position[1] < 0 or position[0] > crt_map.n or position[1] > crt_map.m:
                break
            if crt_map.surface[position[0]][position[1]] == 1:
                break
            valid_path.append(position)

        return valid_path

    def get_fitness(self):
        return self.__f

    def fitness(self, drone, crt_map):
        self.__f = 0
        path = self.compute_path(drone, crt_map)
        visited = []

        for i in range(len(path)):
            x = path[i][0]
            y = path[i][1]
            if [x, y] not in visited:
                visited.append([x, y])
                self.__f += 1

                for direction in v:
                    while ((0 <= x + direction[0] < crt_map.n and 0 <= y + direction[1] < crt_map.m) and
                           crt_map.surface[x + direction[0]][y + direction[1]] != 1):
                        if [x + direction[0], y + direction[1]] not in visited:
                            visited.append([x + direction[0], y + direction[1]])
                            self.__f += 1
                        x = x + direction[0]
                        y = y + direction[1]

    def mutate(self, mutateProbability=0.04):
        """
        We do a Random resetting mutation where the value of a gene is changed into another value
        :param mutateProbability: probability that dictates if a gene is changed or not
        :return:-
        """
        if random() < mutateProbability:
            # We take a random gene and change it
            self.__x[randint(0, self.__size-1)] = randint(0, 3)

    def crossover(self, otherParent, crossoverProbability=0.8):
        """
        We do a N-cutting point crossover. We cut the parents in half so N=1.
        :param otherParent: the other parent that gives genes.
        :param crossoverProbability: probability that dictates the crossover
        :return: the offsprings
        """
        offspring1, offspring2 = Individual(self.__size), Individual(self.__size)
        if random() < crossoverProbability:
            n = randint(0, self.__size-1)
            offspring1.__x = otherParent.__x[:n] + self.__x[n:]
            offspring2.__x = self.__x[:n] + otherParent.__x[n:]

        return offspring1, offspring2


class Population():
    def __init__(self, populationSize=0, individualSize=0):
        self.__populationSize = populationSize
        self.__v = [Individual(individualSize) for x in range(populationSize)]

    def add_individual(self, individual, crt_map, drone):
        individual.fitness(drone, crt_map)
        self.__v.append(individual)

    def set_individuals(self, individuals):
        self.__v = individuals

    def evaluate(self, crt_map, drone):
        # evaluates the population
        for x in self.__v:
            x.fitness(drone, crt_map)

    def sort_individuals(self, individuals):
        # Sort them based on the fitness
        done = False
        while not done:
            done = True
            for i in range(0, len(individuals) - 1):
                if individuals[i].get_fitness() < individuals[i + 1].get_fitness():
                    aux = individuals[i]
                    individuals[i] = individuals[i + 1]
                    individuals[i + 1] = aux
                    done = False
        return individuals

    def selection(self, k=0):
        """
        We make a Proportional selection so we sort the individuals based on fitness.
        :param k: how many individuals we have selected
        :return: the selected individuals
        """
        selected = []
        individuals_copy = copy.deepcopy(self.__v)
        individuals_copy = self.sort_individuals(individuals_copy)

        # Get only the first k
        for i in range(0, k):
            selected.append(individuals_copy[i])

        return selected

    def avg_fitness_and_deviation(self, crt_map, drone):
        fitness = []
        for individual in self.__v:
            individual.fitness(drone, crt_map)
            fitness.append(individual.get_fitness())
        return [np.average(fitness), np.std(fitness)]

    def get_first_path(self, crt_map, drone):
        self.evaluate(crt_map, drone)
        individuals_copy = copy.deepcopy(self.__v)
        individuals_copy = self.sort_individuals(individuals_copy)
        return individuals_copy[0].compute_path(drone, crt_map)

    def get_best_fitness(self, crt_map, drone):
        self.evaluate(crt_map, drone)
        individuals_copy = copy.deepcopy(self.__v)
        individuals_copy = self.sort_individuals(individuals_copy)
        return individuals_copy[0].get_fitness()

    def size(self):
        return len(self.__v)


class Map:
    def __init__(self, n=20, m=20):
        self.n = n
        self.m = m
        self.surface = np.zeros((self.n, self.m))

    def randomMap(self, fill=0.2):
        for i in range(self.n):
            for j in range(self.m):
                if random() <= fill:
                    self.surface[i][j] = 1

    def saveMap(self, numFile="test.map"):
        with open(numFile, 'wb') as f:
            pickle.dump(self, f)
            f.close()

    def loadMap(self, numfile):
        with open(numfile, "rb") as f:
            dummy = pickle.load(f)
            self.n = dummy.n
            self.m = dummy.m
            self.surface = dummy.surface
            f.close()

    def image(self, colour=BLUE, background=WHITE):
        imagine = pygame.Surface((400, 400))
        brick = pygame.Surface((20, 20))
        brick.fill(BLUE)
        imagine.fill(WHITE)
        for i in range(self.n):
            for j in range(self.m):
                if (self.surface[i][j] == 1):
                    imagine.blit(brick, (j * 20, i * 20))

        return imagine

    def __str__(self):
        string = ""
        for i in range(self.n):
            for j in range(self.m):
                string = string + str(int(self.surface[i][j]))
            string = string + "\n"
        return string
