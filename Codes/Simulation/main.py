"""
Main program to run ENED simulation
"""

from myconstants import BARCODE, HOME
from mysimulator import Simulator


if __name__ == "__main__":
    target_barode = [1, 1, 1, 1]
    start_pos = HOME[2]

    game = Simulator(start_pos, target_barode)

    game.frontend.render_background(game.backend.box_list)
    game.frontend.render_surface(game.backend.robot)

    game.search_entire_area()
    