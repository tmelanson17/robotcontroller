# import the pygame module, so you can use it
import pygame
from math import sin, cos

class RobotJoint:
    def __init__(self, length, width):
        self.angle = 0.
        self.length = length
        self.width = width
    
    def draw(self, x, y):
        fulcrum = (x, y)
        point1 = (x + self.width/2.*sin(self.angle), y + self.width/2.*cos(self.angle))
        point2 = (x - self.width/2.*sin(self.angle), y - self.width/2.*cos(self.angle))
        point3 = (point1[0] + self.length*cos(self.angle), point1[1] - self.length*sin(self.angle))
        point4 = (point2[0] + self.length*cos(self.angle), point2[1] - self.length*sin(self.angle))
        return point2, point1, point3, point4, point2

    def rotate(self, angle):
        self.angle = angle
 

# define a main function
def main():
     
    # initialize the pygame module
    pygame.init()
    # load and set the logo
    pygame.display.set_caption("minimal program")
     
    # create a surface on screen that has the size of 240 x 180
    screen = pygame.display.set_mode((240,180))

    # define a variable to control the main loop
    running = True
     
    i = 0
    robot = RobotJoint(100, 50)
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
        robot.rotate(i / 100.)
        pygame.draw.polygon(screen, (255, 0, 0), robot.draw(120, 90))

        i+=1
        pygame.display.flip()
     
     
     
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()
