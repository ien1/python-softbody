from math import sqrt
import pygame
import pymunk

class SoftBody():
    def __init__(self, space, position, x, y, rest_length, stiffness, damping, ball_mass=0.1, ball_radius=0.1):
        """SoftBody Class - soft body simulation using mass points and damped springs.

        Args:
            space (_type_): pymunk space
            position (_type_): Position of the soft body (anchor: north west)
            x (int): number of mass points in a row
            y (int): number of mass points in a column
            rest_length (float): default distance between to points (horizontally and vertically)
            stiffness (float): stiffness of the springs
            damping (float): damping factor
            ball_mass (float, optional): mass of mass points. Defaults to 0.1.
            ball_radius (float, optional): radius of mass points. Defaults to 0.1.
        """
        self.rest_length = rest_length
        self.stiffness = stiffness
        self.damping = damping
        self.ball_mass = ball_mass
        self.ball_radius = ball_radius
        self.__space = space
        self.__balls = []
        self.__springs = []
        self.position = position
        self.create(x, y)
    
    def create_ball(self, position):
        """Creating a ball and adding it to the pymunk space.

        Args:
            position (list): position of the ball

        Returns:
            pymunk.Circle
        """
        body = pymunk.Body()
        body.position = position
        shape = pymunk.Circle(body, self.ball_radius)
        shape.mass = self.ball_mass
        # shape.color = (255, 0, 0, 100)
        self.__space.add(body, shape)
        shape.elasticity = 0.9
        shape.friction = 1
        return shape
    
    def create_spring(self, a, b, rest_length=None):
        """Creating a damped spring that connects two mass points (a and b)

        Args:
            a (pymunk.Body): mass point a
            b (pymunk.Body): mass point b
            rest_length (float, optional): distance between the two points (since it can vary for diagonal springs). Defaults to None.

        Returns:
            pymunk.constraints.DampedSpring
        """
        if not rest_length:
            rest_length = self.rest_length
        shape = pymunk.constraints.DampedSpring(a, b, (0, 0), (0, 0), rest_length, self.stiffness, self.damping)
        self.__space.add(shape)
        return shape
    
    def create(self, x, y):
        """Create all balls and connect them with damped springs.

        Args:
            x (int): number of mass points in a row
            y (int): number of mass points in a column
        """

        # Create balls
        for i in range(x):
            self.__balls.append([])
            for j in range(y):
                self.__balls[i].append(self.create_ball((i * self.rest_length + self.position[0], j * self.rest_length + self.position[1])))

        # horizontal + vertical springs
        for i in range(x):
            for j in range(y):
                if i + 1 < x:
                    self.__springs.append(self.create_spring(self.__balls[i][j].body, self.__balls[i + 1][j].body))
                if j + 1 < y:
                    self.__springs.append(self.create_spring(self.__balls[i][j].body, self.__balls[i][j + 1].body))
        
        # diagonal springs
        for i in range(x):
            for j in range(y):
                if i + 1 < x and j + 1 < y:
                    self.__springs.append(self.create_spring(self.__balls[i][j].body, self.__balls[i + 1][j + 1].body, sqrt(2 * self.rest_length ** 2)))
                if i - 1 > -1 and j + 1 < y:
                    self.__springs.append(self.create_spring(self.__balls[i][j].body, self.__balls[i - 1][j + 1].body, sqrt(2 * self.rest_length ** 2)))
