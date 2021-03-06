# -*- coding: utf-8 -*-


# imports
from gui import *
from controller import *
from repository import *
from domain import *


# create a menu
#   1. map options:
#         a. create random map
#         b. load a map
#         c. save a map
#         d visualise map
#   2. EA options:
#         a. parameters setup
#         b. run the solver
#         c. visualise the statistics
#         d. view the drone moving on a path
#              function gui.movingDrone(currentMap, path, speed, markseen)
#              ATENTION! the function doesn't check if the path passes trough walls
import matplotlib.pyplot as plt
from controller import *
from repository import *
from domain import *
import pygame
import matplotlib


class UI:
    def __init__(self, controller, repository):
        self._controller = controller
        self._repository = repository
        self._path = []
        self._stats = []
        self.__iterations = []
        self._last_stats = []

    def print_menu1(self):
        print("1. create random map")
        print("2. load a map")
        print("3. save a map")
        print("4. visualise map")
        print("5. EA options.")

    def print_menu2(self):
        print("1. parameters setup")
        print("2. run the solver")
        print("3. visualise the statistics for the last run")
        print("4. view the drone moving on a path")
        print("5. visualise the statistics for the seeds")
        print("6. exit")

    def param_setup(self):
        x = int(input("Enter drone posX: "))
        y = int(input("Enter drone posY: "))
        self._controller.set_drone(x, y)

        steps = int(input("Enter steps: "))
        self._controller.set_steps(steps)

        nr_iter = int(input("Enter nr iterations: "))
        self._controller.set_nr_iterations(nr_iter)

        size = int(input("Enter population size: "))
        self._controller.set_population_size(size)

        mP = float(input("Enter mutation prob: "))
        cP = float(input("Enter crossover prob: "))
        self._controller.set_mutation_prob(mP)
        self._controller.set_crossover_prob(cP)

        seeds = int(input("Set seed nr: "))
        self._controller.set_nr_seeds(seeds)

    def run_solver(self):
        self._path, self._stats, self._last_stats = self._controller.solver()
        # print(self._stats)
        #self.view_drone_moving()

    def view_statistics(self):
        x = []
        average = []
        deviations = []
        for i in range(len(self._last_stats)):
            x.append(i)
            average.append(self._last_stats[i][0])
            deviations.append(self._last_stats[i][1])
        print(average)
        plt.plot(x, average)
        plt.show()

    def view_final_statistics(self):
        print("Fitness: " + str(np.average(self._stats)))
        print("Deviation: " + str(np.std(self._stats)))

    def random_map(self):
        self._repository.cmap.randomMap()
        self._repository.random_drone()

    def load_map(self):
        print("Map title:")
        numfile = input()
        self._repository.cmap.loadMap(numfile)
        self._repository.random_drone()

    def save_map(self):
        print("Map title:")
        numfile = input()
        self._repository.cmap.saveMap(numfile)

    def visualize_map(self):
        pygame.init()
        run = True
        while run:
            screen = pygame.display.set_mode((400, 400))
            screen.fill(WHITE)

            screen.blit(self._controller.mapWithDrone(self._repository.cmap.image()), (0, 0))
            pygame.display.flip()
            # time.sleep(10)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

            pygame.display.update()
        time.sleep(2)
        pygame.quit()

    def view_drone_moving(self):
        movingDrone(self._repository.cmap, self._path, 0.2)

    def initPyGame(self, dimension):
        # init the pygame
        pygame.init()
        logo = pygame.image.load("logo32x32.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("drone exploration with AE")

        # create a surface on screen that has the size of 800 x 480
        screen = pygame.display.set_mode(dimension)
        screen.fill(WHITE)
        return screen

    def closePyGame(self):
        # closes the pygame
        running = True
        # loop for events
        while running:
            # event handling, gets all event from the event queue
            for event in pygame.event.get():
                # only do something if the event is of type QUIT
                if event.type == pygame.QUIT:
                    # change the value to False, to exit the main loop
                    running = False
        pygame.quit()

    def movingDrone(self, currentMap, path, speed=1, markSeen=True):
        # animation of a drone on a path
        time.sleep(2)
        screen = initPyGame((currentMap.n * 20, currentMap.m * 20))

        drona = pygame.image.load("drona.png")

        for i in range(len(path)):
            screen.blit(image(currentMap), (0, 0))

            if markSeen:
                brick = pygame.Surface((20, 20))
                brick.fill(GREEN)
                for j in range(i + 1):
                    for var in v:
                        x = path[j][0]
                        y = path[j][1]
                        while ((0 <= x + var[0] < currentMap.n and
                                0 <= y + var[1] < currentMap.m) and
                               currentMap.surface[x + var[0]][y + var[1]] != 1):
                            x = x + var[0]
                            y = y + var[1]
                            screen.blit(brick, (y * 20, x * 20))

            screen.blit(drona, (path[i][0] * 20, path[i][1] * 20))
            pygame.display.flip()
            time.sleep(0.5 * speed)
        self.closePyGame()

    def image(self, currentMap, colour=BLUE, background=WHITE):
        # creates the image of a map

        imagine = pygame.Surface((currentMap.n * 20, currentMap.m * 20))
        brick = pygame.Surface((20, 20))
        brick.fill(colour)
        imagine.fill(background)
        for i in range(currentMap.n):
            for j in range(currentMap.m):
                if (currentMap.surface[i][j] == 1):
                    imagine.blit(brick, (j * 20, i * 20))

        return imagine

    def run_menu(self):
        option = -1
        while option != 5:
            self.print_menu1()
            option = int(input())
            if option == 1:
                self.random_map()
            elif option == 2:
                self.load_map()
            elif option == 3:
                self.save_map()
            elif option == 4:
                self.visualize_map()
            elif option != 5:
                print("Invalid option.")

        while True:
            self.print_menu2()
            option = int(input())
            if option == 1:
                self.param_setup()
            elif option == 2:
                self.run_solver()
            elif option == 3:
                self.view_statistics()
            elif option == 4:
                self.view_drone_moving()
            elif option == 5:
                self.view_final_statistics()
            elif option == 6:
                return
            else:
                print("Invalid option")