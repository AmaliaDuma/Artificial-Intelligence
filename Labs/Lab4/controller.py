import numpy as np
import pygame

from Utils import alpha, beta, evap_coef


class Controller:

    def __init__(self, repo):
        self._repository = repo
        self._colony_size = 0
        self._visibility_matrix = None
        self._pheromone_matrix = None
        self._list_sensors = []
        self._sensors_paths = []
        self._probability_ranges = []
        self._energy = None
        self._no_iterations = None

    def set_drone(self, x, y):
        self._repository.set_drone(x, y)

    def set_energy(self, energy):
        self._energy = energy

    def set_colony_size(self, size):
        self._colony_size = size

    def set_nr_iterations(self, iter_no):
        self._no_iterations = iter_no

    def map_with_drone(self, map_img):
        drone = pygame.image.load("drona.png")
        map_img.blit(drone, (0, 0))

        return map_img

    def sort(self, nodes, total_dist):
        list_nodes = nodes
        ordered = False
        while not ordered:
            ordered = True
            for i in range(0, len(list_nodes) - 1):
                if total_dist[list_nodes[i][0]][list_nodes[i][1]] > total_dist[list_nodes[i + 1][0]][list_nodes[i + 1][1]]:
                    aux = list_nodes[i]
                    list_nodes[i] = list_nodes[i + 1]
                    list_nodes[i + 1] = aux
                    ordered = False
        return list_nodes

    def search_A(self, crt_map, start_x, start_y, end_x, end_y):
        v = [[-1, 0], [0, 1], [1, 0], [0, -1]]
        queue = []
        visited = []
        parent = {}

        start = [start_x, start_y]
        end = [end_x, end_y]
        parent[str(start)] = None
        parent[str(end)] = None
        total_dist = np.zeros((crt_map.n, crt_map.m))
        start_dist = np.zeros((crt_map.n, crt_map.m))
        goal_dist = np.zeros((crt_map.n, crt_map.m))
        queue.append(start)

        while len(queue) > 0:
            queue = self.sort(queue, total_dist)
            crt_node = queue.pop(0)
            visited.append(crt_node)

            if crt_node == end:
                path = []
                while crt_node != start:
                    path.append([crt_node[0], crt_node[1]])
                    crt_node = parent[str(crt_node)]
                path.append([crt_node[0], crt_node[1]])
                return path[::-1]

            for i in range(0, 4):
                new_node = [crt_node[0] + v[i][0], crt_node[1] + v[i][1]]
                if new_node not in visited and new_node[0] >= 0 and new_node[1] >= 0 and new_node[0] < crt_map.n and \
                        new_node[1] < crt_map.m:
                    if crt_map.surface[new_node[0]][new_node[1]] == 0 or crt_map.surface[new_node[0]][new_node[1]] == 2:
                        parent[str(new_node)] = crt_node
                        start_dist[new_node[0]][new_node[1]] = start_dist[crt_node[0]][crt_node[1]]
                        goal_dist[new_node[0]][new_node[1]] = 1
                        total_dist[new_node[0]][new_node[1]] = start_dist[new_node[0]][new_node[1]] + \
                                                               goal_dist[new_node[0]][new_node[1]]

                        if self.add_queue(queue, new_node, total_dist):
                            queue.append(new_node)
        return None

    def add_queue(self, queue, new_node, total_dist):
        for node in queue:
            if node == new_node and total_dist[node[0]][node[1]] <= total_dist[new_node[0]][new_node[1]]:
                return False
        return True

    def get_sensor_byProb(self, ant, prob):
        prob += 1
        crt_next_sensor = 0

        for i in range(1, len(self._list_sensors)):
            if i not in ant.visited_sensors:
                crt_next_sensor += 1
                if crt_next_sensor == prob:
                    return i

    def sensors_paths(self):
        self._sensors_paths = [[] for _ in range(len(self._list_sensors))]

        for i in range(len(self._list_sensors)):
            for j in range(len(self._list_sensors)):
                self._sensors_paths[i].append(
                    self.search_A(self._repository.crt_map, self._list_sensors[i].x, self._list_sensors[i].y,
                                  self._list_sensors[j].x, self._list_sensors[j].y))

    def pheromone_matrix(self):
        self._pheromone_matrix = np.ones((len(self._list_sensors), len(self._list_sensors)))

    def visibility_matrix(self):
        self._visibility_matrix = np.zeros((len(self._list_sensors), len(self._list_sensors)))

        for i in range(len(self._list_sensors)):
            for j in range(len(self._list_sensors)):
                if i != j:
                    self._visibility_matrix[i][j] = 1 / len(self._sensors_paths[i][j])

        for i in range(len(self._sensors_paths)):
            self._visibility_matrix[i][0] = 0

    def update_probs(self, ant):
        crt_sensor = ant.crt_sensor
        num = []
        for j in range(1, len(self._list_sensors)):
            if j not in ant.visited_sensors:
                num.append(self._pheromone_matrix[crt_sensor][j] ** alpha * self._visibility_matrix[crt_sensor][
                    j] ** beta)

        den = sum(num)
        prob = []

        for i in num:
            prob.append(i / den)

        self._probability_ranges = []
        for i in range(len(prob)):
            self._probability_ranges.append(sum(prob[i:]))

    def update_pheromone(self, colony):
        for i in range(len(self._list_sensors)):
            for j in range(len(self._list_sensors)):
                self._pheromone_matrix[i][j] = (1 - evap_coef) * self._pheromone_matrix[i][j]

        for ant in colony.ants:
            visited = ant.visited_sensors
            for i in range(len(visited) - 1):
                self._pheromone_matrix[visited[i]][visited[i + 1]] += (1 / len(ant.path))

    def get_best_ant(self):
        best_quality = -1
        best_ant = None
        for ant in self._repository.get_crt_colony().ants:
            if ant.quality() < best_quality or best_quality == -1:
                best_quality = ant.quality()
                best_ant = ant

        return best_ant

    def aco_iteration(self):
        colony = self._repository.get_crt_colony()

        for ant in colony.ants:
            visibility_matrix = self._visibility_matrix.copy()
            while ant.energy > 0 and len(ant.visited_sensors) < len(self._list_sensors):
                for i in range(len(self._list_sensors)):
                    visibility_matrix[i][ant.crt_sensor] = 0

                self.update_probs(ant)
                next_sensor_prob = ant.pick_sensor(self._probability_ranges)
                next_sensor = self.get_sensor_byProb(ant, next_sensor_prob)

                if next_sensor is None:
                    continue

                path = self._sensors_paths[ant.crt_sensor][next_sensor]
                ant.add_path(path)
                ant.energy -= len(path)

                if ant.energy < 0:
                    ant.path = ant.path[0:len(ant.path) - abs(ant.energy)]
                    ant.energy = 0
                elif ant.energy > 0:
                    optimal_energy = self._list_sensors[next_sensor].get_optimal_energy()
                    ant.energy -= optimal_energy

                    if ant.energy < 0:
                        initial_energy = ant.energy + optimal_energy
                        ant.squares_visited_bySensors[next_sensor] = self._list_sensors[next_sensor].squares_discovered[initial_energy]
                        ant.energy = 0
                    else:
                        ant.squares_visited_bySensors[next_sensor] = self._list_sensors[next_sensor].squares_discovered[optimal_energy]

                    ant.crt_sensor = next_sensor
                    ant.visited_sensors.append(next_sensor)

        self.update_pheromone(colony)
        best_ant = self.get_best_ant()

        colony.reinitialize_ants(self._energy)
        return best_ant

    def run_aco(self):
        self._list_sensors = self._repository.get_sensors()
        self.sensors_paths()
        self.visibility_matrix()
        self.pheromone_matrix()

        self._repository.add_colony(self._colony_size, self._energy)

        best_ant = None
        for i in range(self._no_iterations):
            if i == 0:
                best_ant = self.aco_iteration()
            else:
                ant = self.aco_iteration()
                if len(best_ant.path) >= len(ant.path):
                    best_ant = ant

        return best_ant, self._list_sensors
