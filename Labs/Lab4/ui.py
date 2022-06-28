import time

import pygame

from Utils import WHITE
from gui import movingDrone


class UI:
    def __init__(self, controller, repository):
        self._controller = controller
        self._repository = repository
        self._path = []

    def print_menu1(self):
        print("1. Random map")
        print("2. Load map")
        print("3. Save map")
        print("4. See map")
        print("5. Parameters setup")
        print("6. Run ACO")
        print("7. Exit")

    def random_map(self):
        self._repository.crt_map.randomMap()
        self._repository.random_drone()

    def load_map(self):
        print("Map title:")
        numfile = input()
        self._repository.crt_map.loadMap(numfile)
        self._repository.random_drone()

    def save_map(self):
        print("Map title:")
        numfile = input()
        self._repository.crt_map.saveMap(numfile)

    def visualize_map(self):
        pygame.init()
        run = True
        while run:
            screen = pygame.display.set_mode((400, 400))
            screen.fill(WHITE)

            screen.blit(self._controller.map_with_drone(self._repository.crt_map.image()), (0, 0))
            pygame.display.flip()
            # time.sleep(10)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

            pygame.display.update()
        time.sleep(2)
        pygame.quit()

    def param_setup(self):
        x = int(input("Enter drone posX: "))
        y = int(input("Enter drone posY: "))
        self._controller.set_drone(x, y)

        energy = int(input("Enter energy: "))
        self._controller.set_energy(energy)

        nr_iter = int(input("Enter nr iterations: "))
        self._controller.set_nr_iterations(nr_iter)

        size = int(input("Enter colony size: "))
        self._controller.set_colony_size(size)

    def run_aco(self):
        best_ant, list_sensors = self._controller.run_aco()
        self._path = best_ant.path
        print(list_sensors[0].get_optimal_energy())
        print(self._path)
        print(len(self._path))
        self.view_drone_moving(list_sensors)

    def run_menu(self):
        while True:
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
            elif option == 5:
                self.param_setup()
            elif option == 6:
                self.run_aco()
            elif option == 7:
                return
            else:
                print("Invalid option")

    def view_drone_moving(self, sensors=None):
        movingDrone(self._repository.crt_map, self._path, 0.2, sensors)
