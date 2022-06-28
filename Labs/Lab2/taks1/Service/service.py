import queue


class Service():
    def __init__(self, drone, droneMap):
        self.__drone = drone
        self.__droneMap = droneMap

    def get_map(self):
        return self.__droneMap

    @staticmethod
    def addCoordinates(x, y):
        return x[0] + y[0], x[1] + y[1]

    def __getNeighbours(self, node):
        pos = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        arr = [self.addCoordinates(node, pos[pos.index(x)]) for x in pos]
        neigh = [x for x in arr if self.__droneMap.is_brick_valid(x)]
        return neigh

    def __get_sorted_neigh(self, node, end, visited):
        neigh = self.__getNeighbours(node)
        neigh.sort(key=lambda coord: self.manhattan_distance(coord, end))
        aux = []
        for e in neigh:
            if e not in visited:
                aux.append(e)
        return aux

    def searchAStar(self, initialX, initialY, finalX, finalY):
        start = (initialX, initialY)
        end = (finalX, finalY)
        predecessor = {start: -1}
        cost = {start: 0}

        found = False
        visited = []
        toVisit = queue.PriorityQueue()
        toVisit.put((self.manhattan_distance(start, end) + cost[start], start))
        while not toVisit.empty() and not found:
            if toVisit.empty():
                return []
            node = toVisit.get(block=False)[1]
            if node not in visited:
                visited.append(node)
            else:
                continue
            if node == end:
                found = True
            else:
                for child in self.__getNeighbours(node):
                    if child not in visited:
                        cost[child] = cost[node] + 1
                        toVisit.put((self.manhattan_distance(child, end) + cost[child], child))
                        predecessor[child] = node

        return found, predecessor

    def searchGreedy(self, initialX, initialY, finalX, finalY):
        start = (initialX, initialY)
        end = (finalX, finalY)
        predecessor = {start: -1}


        found = False
        visited =[]
        toVisit = queue.PriorityQueue()
        toVisit.put((self.manhattan_distance(start, end), start))
        while not toVisit.empty() and not found:
            if toVisit.empty():
                return []
            node = toVisit.get(block=False)[1]
            if node not in visited:
                visited.append(node)
            else:
                continue
            if node == end:
                found = True
            else:
                try:
                    child = self.__get_sorted_neigh(node, end, visited)[0]
                except:
                    return False, predecessor
                toVisit.put((self.manhattan_distance(child, end), child))
                predecessor[child] = node

        return found, predecessor

    def search_uc(self, initialX, initialY, finalX, finalY):
        start = (initialX, initialY)
        end = (finalX, finalY)
        predecessor = {start: -1}
        cost = {start : 0}

        found = False
        visited = []
        toVisit = queue.PriorityQueue()
        toVisit.put((cost[start], start))
        while not toVisit.empty() and not found:
            if toVisit.empty():
                return []
            node = toVisit.get(block=False)[1]
            if node not in visited:
                visited.append(node)
            else:
                continue
            if node == end:
                found = True
            else:
                for child in self.__getNeighbours(node):
                    if child not in visited:
                        cost[child] = cost[node] + 1
                        toVisit.put((cost[child], child))
                        predecessor[child] = node

        return found, predecessor

    def greedy_path(self, initialX, initialY, finalX, finalY):
        path = self.searchGreedy(initialX, initialY, finalX, finalY)
        if not path[0]:
            return []
        else:
            return self.computePath(path[1], (finalX, finalY))

    def aStar_path(self, initialX, initialY, finalX, finalY):
        path = self.searchAStar(initialX, initialY, finalX, finalY)
        if not path[0]:
            return []
        else:
            return self.computePath(path[1], (finalX, finalY))

    def uc_path(self, initialX, initialY, finalX, finalY):
        path = self.search_uc(initialX, initialY, finalX, finalY)
        if not path[0]:
            return []
        else:
            return self.computePath(path[1], (finalX, finalY))

    def dummysearch(self):
        # example of some path in test1.map from [5,7] to [7,11]
        return [[5, 7], [5, 8], [5, 9], [5, 10], [5, 11], [6, 11], [7, 11]]

    @staticmethod
    def computePath(dict, end):
        path = []
        while end != -1:
            path.append(end)
            end = dict[end]
        path.reverse()
        return path

    @staticmethod
    def manhattan_distance(current, end):
        return abs(current[0]-end[0])+abs(current[1]-end[1])
