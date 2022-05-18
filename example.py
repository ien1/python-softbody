
from math import sqrt
import pygame
import pymunk
import pymunk.pygame_util as pygu
from softbody import SoftBody


def create_ball(space, radius:float, mass:float, position:int):
    """Creating a ball in pymunk.Space.

    Args:
        space: pymunk space
        radius (float): Radius of the ball.
        mass (float): Mass of the ball.
        position (int): Where the ball should be placed to.

    Returns:
        pymunk.Circle
    """
    body = pymunk.Body()
    body.position = position
    shape = pymunk.Circle(body, radius)
    shape.mass = mass
    # shape.color = (255, 0, 0, 100)
    space.add(body, shape)
    shape.elasticity = 0.9
    shape.friction = 1
    return shape


def create_boundaries(space, width, height):
    """Create boundaries (walls at the top, left, bottom and right).

    Args:
        space (pymunk.Space): pymunk space
        width (int): screen width
        height (int): screen height
    """
    rects = [
        [(width / 2, height - 10), (width, 20)],
        [(width / 2, 10), (width, 20)],
        [(10, height / 2), (20, height)],
        [(width - 10, height / 2), (20, height)]
    ]
    for pos, size in rects:
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = pos
        shape = pymunk.Poly.create_box(body, size)
        shape.elasticity = 0.4
        shape.friction = 0.5
        space.add(body, shape)


def draw(space:pymunk.Space, window, draw_options):
    """Drawing the pymunk objects on pygame screen.

    Args:
        space: pymunk space
        window: pygame screen
        draw_options: pymunk settings to draw on pygame (pymunk.pygame_util)
    """

    window.fill("white")
    space.debug_draw(draw_options)
    pygame.display.update()


if __name__ == "__main__":
    pygame.init()

    # window settings
    WIDTH, HEIGHT = 800, 800
    fps = 144

    # Softbody Properties
    # springs:
    STIFFNESS = 1000
    DAMPING = 1
    REST_LENGTH = 25

    # additional ball properties
    ADD_BALL_MASS = 3
    ADD_BALL_RAD = 35


    # pygame screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    # variable to control window behaviour
    run = True
    
    # pygame clock
    clock = pygame.time.Clock()
    dt = 1 / fps
    
    # create pymunk space and set its gravity
    space = pymunk.Space()
    space.gravity = (0, 981)

    # create boundaries (walls at the top, left, bottom and right)
    create_boundaries(space, WIDTH, HEIGHT)
    
    # initialize module to draw on pygame screen
    draw_options = pygu.DrawOptions(screen)
    
    # saving additional balls
    additional_balls = []

    # creating softbody
    softbody = SoftBody(space, (100, 100), 5, 5, REST_LENGTH, STIFFNESS, DAMPING)

    # pygame main loop
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                # adding ball to the position of the cursor when clicking on window
                pos = pygame.mouse.get_pos()
                additional_balls.append(create_ball(space, ADD_BALL_RAD, ADD_BALL_MASS, pos))
                if len(additional_balls) == 10:
                    del additional_balls[0]
        
        # drawing onto screen
        draw(space, screen, draw_options)

        # go to next step of animation
        space.step(dt)
        clock.tick(fps)
    
    pygame.quit()
