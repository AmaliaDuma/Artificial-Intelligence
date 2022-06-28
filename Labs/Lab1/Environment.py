import pickle
from random import random
import numpy as np
import pygame

from Common import UP, DOWN, LEFT, RIGHT, DARKBLUE, PINK, PINK1, GREEN


class Environment:
    def __init__(self, n, m):
        self.__n = n
        self.__m = m
        self.__surface = np.zeros((self.__n, self.__m))

    def get_n(self):
        return self.__n

    def get_m(self):
        return self.__m

    def random_map(self, fill=0.2):
        for i in range(self.__n):
            for j in range(self.__m):
                if random() <= fill:
                    self.__surface[i][j] = 1

    def __str__(self):
        string = ""
        for i in range(self.__n):
            for j in range(self.__m):
                string += str(int(self.__surface[i][j]))
            string += "\n"
        return string

    def readUDMSensors(self, x,y):
        readings = [0, 0, 0, 0]

        # UP
        xf = x - 1
        while (xf >= 0) and (self.__surface[xf][y] == 0):
            xf = xf - 1
            readings[UP] = readings[UP] + 1

        # DOWN
        xf = x + 1
        while (xf < self.__n) and (self.__surface[xf][y] == 0):
            xf = xf + 1
            readings[DOWN] = readings[DOWN] + 1

        # LEFT
        yf = y + 1
        while (yf < self.__m) and (self.__surface[x][yf] == 0):
            yf = yf + 1
            readings[LEFT] = readings[LEFT] + 1

        # RIGHT
        yf = y - 1
        while (yf >= 0) and (self.__surface[x][yf] == 0):
            yf = yf - 1
            readings[RIGHT] = readings[RIGHT] + 1

        return readings

    def save_environment(self, num_file):
        with open(num_file, 'wb') as f:
            pickle.dump(self, f)
            f.close()

    def load_environment(self, num_file):
        with open(num_file, "rb") as f:
            dummy = pickle.load(f)
            self.__n = dummy.__n
            self.__m = dummy.__m
            self.__surface = dummy.__surface
            f.close()

    def image(self, colour=DARKBLUE, background=PINK):
        imagine = pygame.Surface((420, 420))
        brick = pygame.Surface((20, 20))
        brick.fill(PINK1)
        imagine.fill(GREEN)
        for i in range(self.__n):
            for j in range(self.__m):
                if self.__surface[i][j] == 1:
                    imagine.blit(brick, (j * 20, i * 20))
        return imagine