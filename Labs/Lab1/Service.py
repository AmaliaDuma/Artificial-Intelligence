from random import randint
from Drone import Drone
from DroneMap import DroneMap
from Environment import Environment


class Service:
    def __init__(self, defS_x, defS_y):
        self.__environment = Environment(defS_x, defS_y)
        self.__drone_map = DroneMap(defS_x, defS_y)
        self.__drone = Drone(randint(0, defS_x-1), randint(0, defS_y-1), defS_x, defS_y)
        self.__environment.random_map()

    def get_environment_image(self):
        return self.__environment.image()

    def get_drone_map_image(self):
        return self.__drone_map.image(self.__drone.x, self.__drone.y)

    def mark_detected_walls(self):
        self.__drone_map.mark_detected_walls(self.__environment, self.__drone.x, self.__drone.y)

    def move(self):
        return self.__drone.move_dfs(self.__drone_map)

    def can_drone_move(self):
        return self.__drone.can_move()

    def drone_explored_all(self):
        return self.__drone.explored_all(self.__drone_map)

