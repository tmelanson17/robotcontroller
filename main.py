# import the pygame module, so you can use it
import pygame
import sys
from math import sin, cos

class Robot:
    def __init__(self, link_params):
        self._links = list()
        for link in link_params:
            self._links.append(RobotLink(*link))
    
    def draw(self, screen, basex, basey):
        x, y = basex, basey
        for link in self._links:
            pygame.draw.polygon(screen, (0, 0, 0), link.draw(x, y), 1)
            x, y = link.get_ee(x, y)

    def set_rotation(self, rotations):
        if len(rotations) != len(self._links):
            print("Error: Rotation lengths do not match robot length")
            sys.exit(1)
        for link, rotation in zip(self._links, rotations):
            link.rotate(rotation)


class RobotLink:
    def __init__(self, length, width):
        self.angle = 0.
        self.length = length
        self.width = width
    
    def draw(self, x, y):
        point1 = (x + self.width/2.*sin(self.angle), y + self.width/2.*cos(self.angle))
        point2 = (x - self.width/2.*sin(self.angle), y - self.width/2.*cos(self.angle))
        point3 = (point1[0] + self.length*cos(self.angle), point1[1] - self.length*sin(self.angle))
        point4 = (point2[0] + self.length*cos(self.angle), point2[1] - self.length*sin(self.angle))
        return point2, point1, point3, point4, point2

    def rotate(self, angle):
        self.angle = angle
 
    def get_ee(self, basex, basey):
        return basex + self.length*cos(self.angle), basey - self.length*sin(self.angle)
   
# define a main function
def main():
     
    # initialize the pygame module
    pygame.init()
    # load and set the logo
    pygame.display.set_caption("minimal program")
     
    # create a surface on screen that has the size of 240 x 180
    screen = pygame.display.set_mode((1080,920))

    # define a variable to control the main loop
    running = True
     
    i = 0
    robot = Robot([
                (150, 30),
                (100, 30),
                (70, 30),
            ])
    # main loop
    while running:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                sys.exit()
        screen.fill((255, 255, 255))

        # draw a rectangle
        robot.set_rotation([
            i / 100.,
            i / 50.,
            i / 90.,
        ])
        robot.draw(screen, 540, 460)

        i+=1
        pygame.display.flip()
     

# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()
