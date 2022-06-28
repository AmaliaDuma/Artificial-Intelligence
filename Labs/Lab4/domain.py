import pickle
from random import random

import numpy as np
import pygame

from Utils import BLUE, WHITE, RED


class Map:
    def __init__(self, n=20, m=20):
        self.n = n
        self.m = m
        self.surface = np.zeros((self.n, self.m))

    def randomMap(self, fill=0.2, total=5):
        counter = 0
        for i in range(self.n):
            for j in range(self.m):
                if random() <= fill:
                    self.surface[i][j] = 1
                elif random() <= fill / 10 and counter < total:
                    self.surface[i][j] = 2
                    counter += 1

    def __str__(self):
        string = ""
        for i in range(self.n):
            for j in range(self.m):
                string = string + str(int(self.surface[i][j]))
            string = string + "\n"
        return string

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
        sensor = pygame.Surface((20, 20))

        brick.fill(BLUE)
        imagine.fill(WHITE)
        sensor.fill(RED)

        for i in range(self.n):
            for j in range(self.m):
                if self.surface[i][j] == 1:
                    imagine.blit(brick, (j * 20, i * 20))
                if self.surface[i][j] == 2:
                    imagine.blit(sensor, (j * 20, i * 20))

        return imagine


class Sensor:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.squares_discovered = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        self.optimal_energy = 0

    def discover_squares(self, crt_map):
        """
          For every value of energy (1-5, 0 will have 0 squares) we compute how many squares our sensor can discover
        until he has no more energy or its position is not a valid one.

        :param crt_map: the environment
        :return: none
        """
        v = [[-1, 0], [0, 1], [1, 0], [0, -1]]
        for energy in range(1, 6):
            for d in v:
                aux = energy
                x = self.x + d[0]
                y = self.y + d[1]
                while True:
                    if aux == 0 or x < 0 or y < 0 or x > crt_map.n or y > crt_map.m or crt_map.surface[x][y] == 1:
                        break
                    aux -= 1
                    self.squares_discovered[energy] += 1
                    x = x + d[0]
                    y = y + d[1]

    def get_optimal_energy(self):
        """
        Find the maximum value from the dict and return its key as optimal energy

        :return: int which holds the value of the optimal energy for current sensor
        """
        max_val = -1
        for k, v in self.squares_discovered.items():
            if v > max_val:
                self.optimal_energy = k
                max_val = v

        return self.optimal_energy


class Ant:

    def __init__(self, energy):
        self.energy = energy
        self.path = []
        self.visited_sensors = [0]
        self.crt_sensor = 0
        self.squares_visited_bySensors = {}

    def pick_sensor(self, prob_ranges):
        rand = random()
        for i in range(len(prob_ranges)-1):
            if prob_ranges[i] > rand >= prob_ranges[i + 1]:
                return i

        return len(prob_ranges) - 1

    def add_path(self, path):
        for pos in path:
            self.path.append(pos)

    def quality(self):
        return sum(self.squares_visited_bySensors.values())


class Colony:

    def __init__(self, nr_ants, energy):
        self.nr_ants = nr_ants
        self.ants = [Ant(energy) for _ in range(nr_ants)]

    def reinitialize_ants(self, energy):
        self.ants = [Ant(energy) for _ in range(self.nr_ants)]
