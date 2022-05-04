import sys
import pygame as pg

from perceptron import Perceptron
from controller import KeyboardController
from graphics import GFX
from game import AbstractDinoGame

"""
 - main:
 main loop
    - (main function):
    Holds the menu and all general functions
        - Controller:
        Keyboard inputs to update the control scheme
            - Keyboard input controls
            - Runs first in each controller loop
        - Game:
            - Dino
            - Obstacles
            - Physics
            - Output game state
        - ANN:
            - Neural network
            - Inputs, Updates, and Outputs
        - Graphics:
        Takes a list of elements to display
            - Front End Display
            - Shows game frames
            - Loads, stores, and draws pictures
            - Display for the ANN status
            
    Every time the dino sees a cactus (there is a cactus in front of it)
    the dino should become triggered (counts as a data point).
    When triggered, the dino will treat each frame (a potential action frame)
    as a feature and collect its inputs and outputs (where the dino jumps) into a list.
    Then, it will un-trigger once it either passes the cactus or dies
    if the cactus is successfully passed, then there is no need to update the weigths
    if the dino dies, then update the weights by inspecting every action frame,
    considering the action frames where the dino jumped as wrong, and the others as dont care
    (maybe this doesn't work an I should treat all action frames as wrong)
"""

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # initialize pygame
    pg.init()

    # initialize new controller
    key_ctrl = [('play', pg.K_RETURN),
                ('skip', pg.K_LSHIFT),
                ('freeze', pg.K_SPACE),
                ('hitboxes', pg.K_1),
                ('jump', pg.K_UP)]
    keyboard = KeyboardController(key_ctrl)

    # initialize perceptron
    percep_ctrl = [('play', -1),
                ('jump', 0)]
    percep = Perceptron(percep_ctrl)

    # initialize graphics and get image sizes
    fps = 60
    frame_delay = int((1 / fps) * 1000)
    window_size = (1400, 300)
    scale_factor = window_size[1] / 400
    graphics = GFX(window_size, scale_factor, frame_delay)
    image_sizes = graphics.getSizes()

    # initialize the game with sizes of imported sprite images
    game = AbstractDinoGame(keyboard, (0, 0, 1400, 300), image_sizes, frame_delay, scale_factor)
    game_state = game.getGameState()

    graphics.setGround(game.gnd)

    while True:
        # Exit condition:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()

        # Main loop:
        keyboard.tick()
        # percep.tick(game_state)
        game.tick()
        graphics.draw(game_state, game.dino, game.obstacles_in_play)

        # extra inputs
        if keyboard['freeze']:
            if game_state['freeze'] is False:
                print('freezing learning...')
                game_state['freeze'] = True
            else:
                print('live')
                game_state['freeze'] = False

        if keyboard['hitboxes']:
            if game_state['showhb'] is False:
                game_state['showhb'] = True
            else:
                game_state['showhb'] = False

        if not keyboard['skip']:
            pg.time.wait(frame_delay)
            if not game_state['playing']:
                print(percep.deaths)
