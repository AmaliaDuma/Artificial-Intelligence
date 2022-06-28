from random import randint

from domain import Map, Colony, Sensor


class Repository:

    def __init__(self):
        self.crt_map = Map()
        self.drone = [0, 0]
        self.colonies = []

    def set_drone(self, x, y):
        self.drone = [x, y]

    def random_drone(self):
        x = randint(0, self.crt_map.n - 1)
        y = randint(0, self.crt_map.m - 1)
        while self.crt_map.surface[x][y] != 0:
            x = randint(0, self.crt_map.n - 1)
            y = randint(0, self.crt_map.m - 1)
        self.drone = [x, y]

    def add_colony(self, nr_ants, energy):
        self.colonies.append(Colony(nr_ants, energy))

    def get_crt_colony(self):
        return self.colonies[-1]

    def get_sensors(self):
        sensors = []
        for i in range(0, self.crt_map.n):
            for j in range(0, self.crt_map.m):
                if self.crt_map.surface[i][j] == 2:
                    s = Sensor(i, j)
                    s.discover_squares(self.crt_map)
                    sensors.append(s)
        return sensors
