import pygame
from pygame import K_UP, K_DOWN, K_LEFT, K_RIGHT

class Drone:
    def __init__(self, x, y, defS_x, defS_y):
        self.x = x
        self.y = y
        self.__default_sizeX = defS_x
        self.__default_sizeY = defS_y
        self.__visited = {}
        self.__visited_stack = [(x, y)]
        for i in range(0, 20):
            for j in range(0, 20):
                self.__visited[(i, j)] = 0

    def move(self, detected_map):
        pressed_keys = pygame.key.get_pressed()
        if self.x > 0:
            if pressed_keys[K_UP] and detected_map.surface[self.x - 1][self.y] == 0:
                self.x = self.x - 1
        if self.x < 19:
            if pressed_keys[K_DOWN] and detected_map.surface[self.x + 1][self.y] == 0:
                self.x = self.x + 1

        if self.y > 0:
            if pressed_keys[K_LEFT] and detected_map.surface[self.x][self.y - 1] == 0:
                self.y = self.y - 1
        if self.y < 19:
            if pressed_keys[K_RIGHT] and detected_map.surface[self.x][self.y + 1] == 0:
                self.y = self.y + 1

    def get_neighbours(self, detected_map):
        neighbours = []
        if self.x > 0 and detected_map.surface[self.x-1][self.y] == 0:
            neighbours.append((self.x-1, self.y))
        if self.x < self.__default_sizeX - 1 and detected_map.surface[self.x+1][self.y] == 0:
            neighbours.append((self.x+1, self.y))
        if self.y > 0 and detected_map.surface[self.x][self.y - 1] == 0:
            neighbours.append((self.x, self.y - 1))
        if self.y < self.__default_sizeY - 1 and detected_map.surface[self.x][self.y + 1] == 0:
            neighbours.append((self.x, self.y + 1))
        return neighbours

    def move_dfs(self, detected_map):
        neighbours = self.get_neighbours(detected_map)
        unvisited = [elem for elem in neighbours if self.__visited[elem] == 0]

        if not unvisited:
            if not self.__visited_stack:
                self.x = None
                self.y = None
                return False
            self.x, self.y = self.__visited_stack.pop()
        else:
            self.__visited_stack.append((self.x, self.y))
            self.x, self.y = unvisited.pop()
            self.__visited[(self.x, self.y)] += 1
        return True

    def can_move(self):
        if self.x is None or self.y is None:
            return False
        return True

    def explored_all(self, detected_map):
        for elem in self.__visited:
            if self.__visited[elem] == 0 and detected_map.surface[elem[0]][elem[1]] != 1:
                return False
        return True

