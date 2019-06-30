# import the pygame module, so you can use it
import pygame
import sys
import time
from math import sin, cos
from jacobian import get_dq

# TODO: Move the draw function to a separate graphics section
# TODO: Move the Robot class functionality into its own section
class Robot:
    def __init__(self, link_params, base):
        self._links = list()
        for link in link_params:
            self._links.append(RobotLink(*link))
        self._n_joints = len(link_params)
        self._base = base

    def n_joints(self):
        return self._n_joints

    def get_links(self, reverse=False):
        if reverse:
            return self._links[::-1]
        else:
            return self._links

    def get_angles(self):
        return [link.angle for link in self._links]

    def draw(self, screen):
        x, y = self._base
        for link in self._links:
            pygame.draw.polygon(screen, (0, 0, 0), link.draw(x, y), 1)
            x, y, _ = link.get_ee(x, y)

    def get_ee(self):
        x, y = self._base
        for link in self._links:
            x, y, _ = link.get_ee(x, y)
        return x, y

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
        # TODO: support curved link (low pri)
        self._link = [1, 0]
    
    def draw(self, x, y):
        point1 = (x + self.width/2.*sin(self.angle), y + self.width/2.*cos(self.angle))
        point2 = (x - self.width/2.*sin(self.angle), y - self.width/2.*cos(self.angle))
        point3 = (point1[0] + self.length*cos(self.angle), point1[1] - self.length*sin(self.angle))
        point4 = (point2[0] + self.length*cos(self.angle), point2[1] - self.length*sin(self.angle))
        return point2, point1, point3, point4, point2

    def rotate(self, angle):
        self.angle = angle

    # TODO: Change this function to just return the offset
    def get_ee(self, basex, basey):
        return basex + self.length*cos(self.angle), basey - self.length*sin(self.angle), 0

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
    robot = Robot(
        [
            (150, 30),
            (100, 30),
            (70, 30),
        ],
        [540, 460])

    goal_pos = (400, 500)
    q = [0.1, 0.2, -0.3]
    dt = 1 / 100.
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
        current_pos = robot.get_ee()
        # Here, the y value is the reverse of expected
        dx = [goal_pos[0] - current_pos[0], -(goal_pos[1] - current_pos[1])]
        dq = get_dq(robot, dx)
        for i in range(len(q)):
            q[i] += dq[i] * dt
        robot.set_rotation([
            q[0],
            q[1],
            q[2],
        ])
        robot.draw(screen)
        i+=1
        pygame.display.flip()
        time.sleep(dt/ 10.)

     

# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()
