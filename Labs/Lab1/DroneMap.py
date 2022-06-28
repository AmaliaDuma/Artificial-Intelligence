import numpy as np
import pygame
from Common import UP, DOWN, LEFT, RIGHT, GREEN, DARKGREEN, PINK1, GRAYBLUE, BLUE1, YELLOW


class DroneMap:
    def __init__(self, n, m):
        self.__n = n
        self.__m = m
        self.surface = np.zeros((self.__n, self.__m))
        for i in range(self.__n):
            for j in range(self.__m):
                self.surface[i][j] = -1

    def mark_detected_walls(self, e, x, y):
        if x is None or y is None:
            return None

        walls = e.readUDMSensors(x, y)
        i = x - 1
        if walls[UP] > 0:
            while (i >= 0) and (i >= x - walls[UP]):
                self.surface[i][y] = 0
                i = i - 1
        if i >= 0:
            self.surface[i][y] = 1

        i = x + 1
        if walls[DOWN] > 0:
            while (i < self.__n) and (i <= x + walls[DOWN]):
                self.surface[i][y] = 0
                i = i + 1
        if i < self.__n:
            self.surface[i][y] = 1

        j = y + 1
        if walls[LEFT] > 0:
            while (j < self.__m) and (j <= y + walls[LEFT]):
                self.surface[x][j] = 0
                j = j + 1
        if j < self.__m:
            self.surface[x][j] = 1

        j = y - 1
        if walls[RIGHT] > 0:
            while (j >= 0) and (j >= y - walls[RIGHT]):
                self.surface[x][j] = 0
                j = j - 1
        if j >= 0:
            self.surface[x][j] = 1

        return None

    def image(self, x, y):
        imagine = pygame.Surface((420, 420))
        brick = pygame.Surface((20, 20))
        empty = pygame.Surface((20, 20))
        empty.fill(YELLOW)
        brick.fill(GRAYBLUE)
        brick.blit(pygame.image.load("s1.png"), (0, 0))
        imagine.fill(DARKGREEN)

        for i in range(self.__n):
            for j in range(self.__m):
                if self.surface[i][j] == 1:
                    imagine.blit(brick, (j * 20, i * 20))
                elif self.surface[i][j] == 0:
                    imagine.blit(empty, (j * 20, i * 20))

        drona = pygame.image.load("s2.png")
        imagine.blit(drona, (y * 20, x * 20))
        return imagine

    def __str__(self):
        return str(self.surface)

