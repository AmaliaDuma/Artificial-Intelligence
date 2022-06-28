import pygame, time
from pygame.locals import *
from random import randint

from Domain.drone import Drone
from Domain.map import Map
from Service.service import Service
from Common.Common import GREEN, WHITE, RED, BLACK, BLUE, CYAN, PINK


def displayWithPath(image, path, algo):
    mark = pygame.Surface((20, 20))
    if algo == 1:
        mark.fill(GREEN)
    elif algo == 2:
        mark.fill(CYAN)
    else:
        mark.fill(PINK)
    for move in path:
        image.blit(mark, (move[1] * 20, move[0] * 20))

    return image


def display_st(image, start, end):
    mark_start = pygame.Surface((20, 20))
    mark_start.fill(RED)
    mark_end = pygame.Surface((20, 20))
    mark_end.fill(BLACK)
    image.blit(mark_start, (start[1] * 20, start[0] * 20))
    image.blit(mark_end, (end[1] * 20, end[0] * 20))
    return image


# define a main function
def main():
    # we create the map
    m = Map()
    # m.randomMap()
    # m.saveMap("test2.map")
    m.loadMap("test1.map")

    # initialize the pygame module
    pygame.init()
    # load and set the logo
    logo = pygame.image.load("Images/logo32x32.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Path in simple environment")

    # we position the drone somewhere in the area
    x = randint(0, 19)
    y = randint(0, 19)

    # create drona
    d = Drone(x, y)

    # create a surface on screen that has the size of 400 x 480
    screen = pygame.display.set_mode((400, 400))
    screen.fill(WHITE)

    service = Service(d, m)

    # define a variable to control the main loop
    running = True

    # main loop
    while running:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False

            if event.type == KEYDOWN:
                endX = randint(0, 20 - 1)
                endY = randint(0, 20 - 1)
                while not service.get_map().is_brick_valid([endX, endY]):
                    endX = randint(0, 20 - 1)
                    endY = randint(0, 20 - 1)

                # Print the start and end positions
                screen.blit(display_st(m.image(), (x, y), (endX, endY)), (0,0))
                pygame.display.flip()
                pygame.time.delay(1000)

                # Clear map
                screen.blit(d.mapWithDrone(m.image()), (0, 0))
                pygame.display.flip()

                # Start greedy
                start_time_greedy = time.time()
                path1 = service.greedy_path(x, y, endX, endY)
                if len(path1) == 0:
                    continue
                end_time_greedy = time.time()
                print("Greedy took", end_time_greedy - start_time_greedy, "time.")
                print("The path is: ", path1)
                screen.blit(displayWithPath(m.image(), path1, 1), (0, 0))
                pygame.display.flip()
                pygame.time.delay(5000)

                # Clear map
                screen.blit(d.mapWithDrone(m.image()), (0, 0))
                pygame.display.flip()
                pygame.time.delay(1000)

                # Start A*
                start_time_aStar = time.time()
                path2 = service.aStar_path(x, y, endX, endY)
                if len(path2) == 0:
                    continue
                end_time_aStar = time.time()
                print("A* took", end_time_aStar - start_time_aStar, "time.")
                print("The path is: ", path2)
                screen.blit(displayWithPath(m.image(), path2, 2), (0, 0))
                pygame.display.flip()
                pygame.time.delay(5000)

                # Clear map
                screen.blit(d.mapWithDrone(m.image()), (0, 0))
                pygame.display.flip()
                pygame.time.delay(1000)

                #Start uniform cost
                start_time_uc = time.time()
                path3 = service.uc_path(x, y, endX, endY)
                if len(path3) == 0:
                    continue
                end_time_uc = time.time()
                print("Uniform cost took", end_time_uc - start_time_uc, "time.")
                print("The path is: ", path3)
                screen.blit(displayWithPath(m.image(), path3, 3), (0, 0))
                pygame.display.flip()
                pygame.time.delay(5000)

        screen.blit(d.mapWithDrone(m.image()), (0, 0))
        pygame.display.flip()

    # path = dummysearch()
    # screen.blit(displayWithPath(m.image(), path1),(0,0))

    pygame.display.flip()
    time.sleep(5)
    pygame.quit()


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    main()
