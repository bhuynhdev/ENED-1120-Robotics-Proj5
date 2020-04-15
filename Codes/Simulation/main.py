"""
Main program to run ENED simulation
"""

import random
from mysimulation import *
from mysequences import *


def full_box_search_seq(simulation):
    """
    Combine other sequences into a whole box search sequence on entire field
    """
    quad_finished = 0
    while not simulation.finished:
        # Make first search:
        escape_home_seq(simulation)
        pause(0.5)
        quad = simulation.backend.robot.get_quad_num()
        current_quad_direction = QUAD_START_DIRCT[quad]
        if simulation.backend.robot.center[1] in (7, 31, 79, 55):
            x_startscan = simulation.backend.robot.center[0]
            x_stopscan = x_startscan + 38
        else:
            x_startscan = simulation.backend.robot.center[0]
            x_stopscan = x_startscan - 38
        # Scan a shelf line
        print(f"Scanning seq start with {x_startscan}, {x_stopscan}")
        search_shelf_seq(simulation, x_startscan, x_stopscan)
        print("Scanning seq ended")
        simulation.robot_goto_point(add_tuple(tuple((x_stopscan, simulation.backend.robot.center[1])),
                                              mult_tuple(CLOCKWISE[current_quad_direction], 2)))
        print(f"Went into hallway at {simulation.backend.robot.center}")
        # Continuously do subsequence search if necessary
        while simulation.backend.robot.storage_empty and quad_finished < 4:
            next_point, current_quad_direction = generate_next_point_to_go(simulation, current_quad_direction)
            print(next_point, current_quad_direction)
            # Move into next spot
            simulation.robot_goto_point(next_point)
            simulation.robot_become_direction(current_quad_direction)
            if simulation.backend.robot.center[1] in (7, 31, 79, 55):
                x_startscan = next_point[0]
                x_stopscan = x_startscan + 38
            else:
                x_startscan = next_point[0]
                x_stopscan = x_startscan - 38
            # Scan a shelf line
            print(f"Scanning seq start with {x_startscan}, {x_stopscan}")
            search_shelf_seq(simulation, x_startscan, x_stopscan)
            print("Scanning seq ended")
            # Move into hallway area to preapre to navigate to next spot
            simulation.robot_goto_point(add_tuple(tuple((x_stopscan, simulation.backend.robot.center[1])),
                                            mult_tuple(CLOCKWISE[current_quad_direction], 2)))
            print(f"Went into hallway at {simulation.backend.robot.center}")
            if simulation.backend.robot.center in QUAD_END:
                quad_finished = quad_finished + 1
                print(f"Finished quad {simulation.backend.robot.get_quad_num()}")

        # If carrying a box, initiate go_home_seq
        if not simulation.backend.robot.storage_empty:
            go_home_seq(simulation)
        else: # Meaning no box found
            print("Searched 4 quads but no boxes found")

if __name__ == "__main__":
    target_barode = BARCODE[1]
    start_pos = random.choice(HOME)
    game = Simulation(start_pos, target_barode)
    game.set_robot_start()

    game.frontend.render_background(game.backend.box_list)
    game.frontend.render_surface(game.backend.robot)
    
    full_box_search_seq(game)