import pygame

from Common import WHITE
from Service import Service


class Ui:
    def main(self):
        # initialize the pygame module
        pygame.init()

        # load and set the logo
        logo = pygame.image.load("logo.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("drone exploration")

        # initialize the service
        service = Service(20, 20)

        # create a surface on screen that has the size of 800 x 480
        screen = pygame.display.set_mode((800, 400))
        screen.fill(WHITE)
        screen.blit(service.get_environment_image(), (0, 0))

        pygame.mixer.init()
        pygame.mixer.music.load("intro.mp3")
        # pygame.mixer.music.play(-1)

        # variable to control the loop
        running = True

        while running:
            # event handling, gets all event from the event queue
            for event in pygame.event.get():
                # only do something if the event is of type QUIT
                if event.type == pygame.QUIT:
                    # change the value to False, to exit the main loop
                    running = False
            if not running:
                break
            if service.can_drone_move():
                if service.drone_explored_all():
                    break
                service.mark_detected_walls()
                screen.blit(service.get_drone_map_image(), (400, 0))
            running = service.move()
            pygame.display.flip()
            pygame.time.delay(1000)

        pygame.time.delay(1500)
        pygame.quit()

